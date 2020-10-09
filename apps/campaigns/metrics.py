from apps.failuremodes.models import FailureMode
from apps.components.models import Component
from apps.bops.models import *
from apps.cuts.models import *
from .models import *
import copy
import csv
from django.db.models import Max, Q
import datetime
import string
import math
import numpy as np


def run(campaign, **kwargs):
    datetime.today()
    print(datetime.datetime.today(), "incio do calculo")
    bop = campaign.bop

    m = get_m_matrix(bop)

    sf_pfds = calculate_SF_PFDS(campaign, m)

    # campaign.schemas.all() # 2
    # if phase.has_test:
    #       phase.test_groups.all()


    return sf_pfds


def gerar_matriz(n_linhas, n_colunas):
    return [[0] * n_colunas for _ in range(n_linhas)]


def getTotalFailMode(bop):
    return FailureMode.objects.filter(component__subsystem__bop__exact=bop).count()


def get_m_matrix(bop):
    failure_modes = getTotalFailMode(bop)

    m = gerar_matriz(failure_modes, 32)
    fmodes = FailureMode.objects.filter(component__subsystem__bop__exact=bop).all()

    index = 0
    for f in fmodes:
        m[index][0] = index

        if f.component is not None:
            cp = f.component
            m[index][4] = cp.name
            m[index][5] = cp.code
            # m[index][22] = f.Last_Replacement_Date
            m[index][22] = 0
            bs = cp.subsystem
            m[index][2] = bs.name
            m[index][3] = bs.code
        else:
            m[index][2] = "CCF"
            m[index][3] = "CCF"
            m[index][4] = "CCF"
            m[index][5] = "CCF"

            # ccfs = ""
            # for m in f.ccf_impacted.all():
            #    fm = BopFailureMode.objects.get(pk=m.id)
            #    if len(ccfs) != 0:
            #        ccfs += ","
            #    ccfs += fm.code

        # m[index][9] = f.ccf_impacted
        # print("f", f.ccf_impacted)

        # if m[index][9]:
        #    m[index][9] = modefail(m[index][9])

        m[index][6] = f.name
        m[index][7] = f.code
        m[index][8] = f.code
        m[index][10] = 168

        #     if f.test_interval_1 == None:
        #         m[index][10] = 0
        #    else:
        #       m[index][10] = f.test_interval_1 / 24

        #   if f.test_interval_2 == None:
        ###      m[index][11] = 0
        #    else:
        #      m[index][11] = f.test_interval_2 / 24

        #   if f.test_interval_3 == None:
        #       m[index][12] = 0
        #   else:
        #       m[index][12] = f.test_interval_3 / 24

        #   if f.test_interval_4 == None:
        #       m[index][13] = 0
        #   else:
        #       m[index][13] = f.test_interval_4 / 24

        m[index][14] = f.diagnostic_coverage
        m[index][15] = 1
        # m[index][15] = f.test_coverage_1
        # m[index][16] = f.test_coverage_2
        # m[index][17] = f.test_coverage_3
        # m[index][18] = f.test_coverage_4

        if m[index][19] == None:
            m[index][19] = 0
        else:
            # m[index][19] = f.staggering_Test_Time_t0
            m[index][19] = 0
        # if f.repairable_with_BOP_Installed:
        #   m[index][20] = "x"
        # else:
        m[index][20] = ""

        # if f.mean_time_to_restoration == None:
        m[index][21] = 0
        # else:
        #   m[index][21] = f.mean_time_to_restoration / 24
        dist = f.distribution

        m[index][23] = dist['type']
        if m[index][23] == 'Exponential':
            m[index][24] = dist['exponential_failure_rate']

        elif m[index][23] == 'Probability':
            m[index][31] = dist['probability']

        elif m[index][23] == 'Weibull':
            m[index][25] = dist['scale']
            m[index][26] = dist['form']

        elif m[index][23] == 'Step':
            dist['cycle'] = {}
            m[index][27] = dist['initial_failure_rate']
            m[index][28] = 0
            m[index][29] = 0
            m[index][30] = 0

        index += 1

    return m


def calculate_SF_PFDS(camp, m):
    flag = 1
    dt = 1
    # count_camps = count_Campaings(bop)  # contagem de campanhas
    # number_fails = getUserInputTotalFailures(bop)  # contagem de falhas
    # t_start_recert = getStartCampaignDate(bop.id, flag)
    t_start_recert = 0

    # t_end_camp = getEndCampaignDate(bop.id, count_camps)
    # t_start_camp = getStartCampaignDate(bop.id, 1)
    t_start_camp = camp.start_date
    t_end_camp = camp.end_date
    current_date = datetime.datetime.today()
    # tf_integracao = (t_end_camp - t_start_recert).days
    # ti_integracao = (current_date - t_start_recert).days

    steps = abs((t_end_camp - t_start_camp).days) * 24

    failure_modes = len(m)

    dt = 1
    t_op = get_t_op(t_start_camp, t_end_camp, 0, dt)
    v_integrate = calculate_failure_modes(m, failure_modes, False, dt, False, steps, t_op)
    # print("v integrate",v_integrate)

    safety_function_numbers = SafetyFunction.objects.filter(bop=camp.bop).count()
    sf = SafetyFunction.objects.filter(bop=camp.bop)

    result_each_sf_integrate = gerar_matriz(steps + 1, safety_function_numbers + 1)
    result_each_sf_integrate_falho = gerar_matriz(steps + 1, safety_function_numbers + 1)

    fl = 0
    for safety_function in sf:
        fl += 1
        print(datetime.datetime.today(), "Inicio do calculo da Sf: ", safety_function)

        cuts = Cut.objects.filter(safety_function=safety_function)
        max_cuts = Cut.objects.filter(safety_function=safety_function).count()
        corte = 0

        matriz_index = gerar_matriz(max_cuts, 4)

        print(datetime.datetime.today(), "Inicio da organização da sf ")

        for cut in cuts:

            fails = cut.failure_modes.split(",")
            falha = 0

            for fail in fails:
                fail_line = Fail_line(fail, v_integrate)
                # print("faill", fail, fail_line)
                matriz_index[corte][falha] = fail_line
                falha = falha + 1

            corte = corte + 1

        print(datetime.datetime.today(), "Inicio do calculo PFD, com steps ", steps)
        for i in range(1, steps):
            result_each_sf_integrate[i][0] = i * dt
            result_each_sf_integrate[i][fl] = calc_PFD_this_timestep(i, v_integrate, matriz_index)

        # print("resultado ", result)
        print(datetime.datetime.today(), "Fim do calculo da Sf: ", safety_function)

        # print("total de steps calculados:", i)

    return result_each_sf_integrate


def calculate_failure_modes(m, failure_modes, delay, dt, falha, step_max, t_op):
    # coverage = [0.0 for i in range(5)]

    # cc = [0.0 for i in range(5)]
    # print("failure_modes", failure_modes)

    v_integrate = gerar_matriz(failure_modes, step_max)

    # calculates PFD(t) for all listed failure modes
    #    t = time_per_op_mode_cert(m, failure_modes, t_op, step_max)

    # else:
    # t = time_per_op_mode(delay)
    step_min = 1

    for i in range(0, len(m)):
        v_integrate[i][0] = m[i][7]

    for j in range(0, failure_modes):

        falha = False
        coverage = 0.0

        cc = 1.0

        dc = 0
        if dc is None:
            dc = 0

        if m[j][20] == "x":

            monit_rep = True
            test_rep = True
        else:
            monit_rep = False
            test_rep = False

        tau = m[j][21]

        if tau == None:
            tau = 0

        if m[j][23].upper() == "CONST" or m[j][23].upper() == "PROBABILITY":
            for i in range(step_min, step_max):
                v_integrate[j][i] = m[j][31]

        else:
            # cc test coverage factor

            if m[j][10] == "" or m[j][10] == None:
                cc = 0

            else:
                cc = m[j][15]

            # reduction_matrix the final coverage factor for each test
            coverage = (1 - dc) * cc

            pol_falha = [0.0 for az in range(5)]
            if m[j][23] == "Exponential":
                xlambda = float(m[j][24])


            elif m[j][23] == "Weibull":

                xlambda = 1 / int(m[j][25])
                eta = float(m[j][26])

            elif m[j][23] == "Step":

                xlambda = float(m[j][27])
                increase = float(m[j][28]) / 100

            # get test time for each test

            for i in range(1, step_max):

                tempo = t_op[i][1]
                # Calculate normal PFD fractions
                if m[j][23] == "Exponential":

                    try:
                        pol_falha = 1 - math.exp((-1) * xlambda * tempo * coverage)
                    except:
                        pol_falha = 0

                if m[j][23] == "Weibull":
                    # treplace = t[j][i][11]
                    # tltk = t[j][i][6 + k]
                    # t_op_replace = t_op[treplace][1]
                    # t_op_ltk = t_op[tltk][1]
                    t_op_replace = 0
                    t_op_ltk = 0

                    t_op_atual = t_op[i][1]
                    p1 = float(xlambda) ** float(eta)
                    p2 = (t_op_atual - t_op_replace) ** eta
                    p3 = (t_op_ltk - t_op_replace) ** eta
                    lambda_effetivo = p1 * (abs(p2 - p3))

                    pol_falha = 1 - math.exp(((-1) * coverage * (lambda_effetivo)))

                if m[j][23] == "Step":
                    # Cintegrated = t[j][i][6 + k]
                    Cintegrated = tempo
                    l_ = xlambda
                    c_ = coverage
                    t_ = tempo * (dt)
                    i_ = increase
                    Cin_ = Cintegrated

                    pol_falha = 1 - math.exp(c_ * ((((-1) * l_) * i_ * Cin_) + (((-1) * l_) * t_)))

                v_integrate[j][i] = 1 - (1 - pol_falha)
        # print(v_integrate[j])
    return v_integrate


0


def get_t_op(start, end, testes, dt):
    count = 0
    flag = 0

    # history = get_campaign_list2(bop)

    # campanhas = len(history)
    # start = history[0][0]
    # end = history[campanhas - 1][1]

    firststart = start
    firstend = end

    tmax = (abs((end - start).days)) * 24
    t_op = [[None for i in range(2)] for j in range(tmax)]
    work = 1
    t_op[0][0] = 0
    t_op[0][1] = 0

    for i in range(1, tmax):

        dataatual = start + datetime.timedelta(days=i)

        if dataatual > firstend:
            flag = flag + 1
            # firststart = history[flag][0]
            # firstend = history[flag][1]
            work = 0

        if dataatual >= firststart and work == 0:
            # firstend = history[flag][1]
            work = 1

        if work == 1:
            t_op[i][0] = i
            t_op[i][1] = t_op[i - 1][1] + dt
            count = count + 1
        else:
            t_op[i][0] = i
            t_op[i][1] = t_op[i - 1][1]

    return t_op


def Fail_line(failmode, v_integrate):
    line = -1

    for i in range(0, len(v_integrate)):

        if failmode == v_integrate[i][0]:
            line = i
            return line

    return line


def calc_PFD_this_timestep(step, v_integrate, matriz_index):
    prod_sf = 1
    print_v = []
    for corte in range(0, len(matriz_index)):
        produtorio = 1
        for falha in range(0, 4):
            if matriz_index[corte][falha] != ' ':
                produtorio = produtorio * float(v_integrate[matriz_index[corte][falha]][step])
        prod_sf = prod_sf * (1.0 - produtorio)

    prod_sf = 1.0 - prod_sf
    print_v.append(prod_sf)

    if prod_sf == 0:
        prod_sf = 10 ** -40

    return prod_sf
