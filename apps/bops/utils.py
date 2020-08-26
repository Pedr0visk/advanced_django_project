#!/usr/bin/env python
import os
import sys
import django
from django.db import transaction
import csv
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyBarrier.settings')

django.setup()

from .models import Subsystem, Component, FailureMode, Te


def brazillianDate(date_str):
    tdate = date_str.split("/")
    btime = datetime.date(int(tdate[2]), int(tdate[1]), int(tdate[0]))
    return btime


def objUpdate(obj):
    obj.save()


def importSafetyFunctionCutsFromFile(bop, fileName, safetyFunctionName):
    print(datetime.datetime.today(), "Importing cuts", bop.id, safetyFunctionName)
    sf = BopSafetyFunction.objects.get(code=safetyFunctionName)

    with open(fileName) as csvfile:
        rows = csv.reader(csvfile, delimiter=',')

        for row in rows:
            cut = BopSafetyFunctionCut(bop_id=bop, safety_function_id=sf, code=row[0])
            cut.order = 0
            # objUpdate(cut) #'- this was used when cuts were ManyToMany relationship
            for x in range(1, len(row)):
                # check failure mod e exists
                fm = BopFailureMode.objects.get(code=row[x])
                # cut.cuts.add(fm) - this was used when cuts were ManyToMany relationship
                cut.order += 1
                if len(cut.cuts) != 0:
                    cut.cuts += ","
                cut.cuts += row[x]
        objUpdate(cut)


def importEventsFromFile(bop, fileName):
    print(datetime.datetime.today(), "Importing events", bop.id)
    with open(fileName) as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        count = 1
        for r in rows:
            if count != 1:
                if r[1] != "":
                    evt_time = brazillianDate(r[1])
                    evt = BopEvent(bop_id=bop, event_type='campaign_start', event_time=evt_time)
                    objUpdate(evt)

                if r[2] != "":
                    evt_time = brazillianDate(r[2])
                    evt = BopEvent(bop_id=bop, event_type='campaign_end', event_time=evt_time)
                    objUpdate(evt)

                evt_time = brazillianDate(r[6])

                if r[3] == "Subsystem":
                    ssys = BopSubsystem.objects.get(bop_id=bop, code=r[5])
                    evt = BopEvent(bop_id=bop, event_type='ssys_fail', event_time=evt_time, subsystem_id=ssys)
                elif r[3] == "Component":
                    comp = BopComponent.objects.get(bop_id=bop, code=r[5])
                    evt = BopEvent(bop_id=bop, event_type='comp_fail', event_time=evt_time, component_id=comp)
                elif r[3] == "Failure Mode":
                    fail = BopFailureMode.objects.get(bop_id=bop, code=r[5])
                    evt = BopEvent(bop_id=bop, event_type='fmod_fail', event_time=evt_time, fail_id=fail)

                if r[7] != "":
                    evt.repair_start_with_bop_installed = brazillianDate(r[7])

                if r[8] != "":
                    evt.repair_end_with_bop_installed = brazillianDate(r[8])

                if r[9] != "":
                    evt.failed_bop_withdrawal_date = brazillianDate(r[9])

                if r[10] != "":
                    evt.failed_bop_reinstallaion_date = brazillianDate(r[10])

                objUpdate(evt)
            count = count + 1


def importComponentsFromFile(fileName):
    print(datetime.datetime.today(), "Importing components")
    with open(fileName, 'r') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')

        for r in rows:
            print("salvou componente ", r[1])
            try:

                comp = BopComponent.objects.get(code=r[2])

            except:

                subsystem = BopSubsystem.objects.get(code=r[0])

                comp = BopComponent(subsystem_id=subsystem, description=r[1], code=r[2])
                objUpdate(comp)


def importsafetycutFromFile(bopid, fileName):
    print(datetime.datetime.today(), "Importing safetys ")
    count = 0
    bop = Bop.objects.get(id=bopid)
    with open(fileName, 'r') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')

        for r in rows:

            if count == 0:
                safety = r[0]
                count = 1
                print("safety,", safety)

            else:
                try:

                    cut = BopSafetyFunctionCut.objects.get(safety=safety, code=r[0], bop_id=bop)

                except:

                    cut = BopSafetyFunctionCut(safety=safety, code=r[0], bop_id=bop,
                                               order=(len(r) - 1))
                    cut.save()

                    for i in range(1, len(r)):
                        failmode = BopFailureMode.objects.get(code=r[i], bop_id=bop)

                        cut.failure.add(failmode)

                    cut.save()


def importfailureFromFile(fileName, id):
    with open(fileName, 'r') as csvfile:

        rows = csv.reader(csvfile, delimiter=',')
        for r in rows:

            if id == 0:

                newbop = Bop(name=r[0], code=r[1], description=r[2])
                id = 1

                objUpdate(newbop)


            else:

                try:

                    subsystem = BopSubsystem.objects.get(code=r[2], bop_id=newbop.id)

                except:

                    subsystem = BopSubsystem(bop_id=newbop, description=r[1], code=r[2])
                    objUpdate(subsystem)

                try:

                    comp = BopComponent.objects.get(code=r[4], subsystem_id=subsystem)

                except:

                    comp = BopComponent(subsystem_id=subsystem, description=r[3], code=r[4])
                    objUpdate(comp)

                try:

                    failure = BopFailureMode.objects.get(comp_id=comp, code=r[7])

                except:
                    print("entrou no excetp do fm")
                    fm = BopFailureMode(bop_id=newbop, component_id=comp, code=r[7], description=r[5],
                                        ccf_impacted=r[8])

                    if r[22] == "Exponential":
                        fm.exponential_failure_rate = r[23]

                    elif r[22] == "Weibull":
                        fm.failure_mode_type = "Weibull"
                        fm.exponential_failure_rate = 0
                        fm.weibull_scale_parameter = r[24]
                        fm.weibull_form_parameter = r[25]

                    elif r[22] == "Step":
                        fm.failure_mode_type = "Step"
                        fm.step_initial_Failure_rate = r[26]
                        fm.step_increase_per_cycle = r[27]
                        fm.step_number_of_cycles_to_replace = r[28]
                        fm.step_cycle_size = r[29]

                    elif r[22] == "Probability":
                        fm.failure_mode_type = "Probability"
                        # fm.exponential_failure_rate = r[23]
                        fm.constant_probability = r[30]

                    if r[9] != "":
                        fm.test_interval_1 = r[9]
                    if r[10] != "":
                        fm.test_interval_2 = r[10]
                    if r[11] != "":
                        fm.test_interval_3 = r[11]
                    if r[12] != "":
                        fm.test_interval_4 = r[12]

                    if r[13] != "":
                        fm.diagnostic_coverage = r[13]

                    if r[14] != "":
                        fm.test_coverage_1 = r[14]
                    if r[15] != "":
                        fm.test_coverage_2 = r[15]
                    if r[16] != "":
                        fm.test_coverage_3 = r[16]
                    if r[17] != "":
                        fm.test_coverage_4 = r[17]

                    if r[18] != "":
                        fm.staggering_Test_Time_t0 = r[18]
                    if r[19] != "":
                        fm.repairable_with_BOP_Installed = True
                    if r[20] != "":
                        fm.mean_time_to_restoration = r[20]

                    print("salvar", fm)
                    objUpdate(fm)
                    print("salvou")
