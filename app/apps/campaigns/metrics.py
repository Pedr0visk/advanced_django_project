from apps.failuremodes.models import FailureMode
from apps.components.models import Component
from apps.bops.models import *
from apps.cuts.models import *
from .models import *
from django.db.models import Max
import datetime
from datetime import timedelta
import string
import math
import json


def run(schema, **kwargs):

    bop = schema.campaign.bop
    print(datetime.datetime.today(), "Vai chamar Matriz M")
    m = get_m_matrix(bop)
    print(datetime.datetime.today(), "Terminou Matriz M ")
    sf_pfds = calculate_SF_PFDS(schema, m)

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


def get_dates(schema):
    flag = 0
    try:
        first = schema.phases.all().order_by('start_date').first()

        start_date = first.start_date

        last = schema.phases.all().order_by('start_date').last()

        end_date = last.start_date + timedelta(hours=last.duration)


    except:
        start_date = 0
        end_date = 0

    return start_date, end_date


def calculate_SF_PFDS(schema, m):
    print(datetime.datetime.today(), "Entrou no calculo ")
    # number_fails = getUserInputTotalFailures(bop)  # contagem de falhas
    t_start_recert = 0

    t_start_camp = schema.start_date
    t_end_camp = schema.end_date
    camp_period = t_end_camp - t_start_camp

    # tf_integracao = (t_end_camp - t_start_recert).days
    # ti_integracao = (current_date - t_start_recert).days

    steps = int(camp_period.total_seconds() / 60 ** 2)

    failure_modes = len(m)

    dt = 1  # passo horario

    t_op = get_t_op(steps, schema, dt)
    v_integrate = calculate_failure_modes(m, failure_modes, False, dt, False, steps, t_op)
    schema.cuts_contribution = v_integrate
    schema.save()
    print(datetime.datetime.today(), "Terminou o V integrate ")

    safety_function_numbers = SafetyFunction.objects.filter(bop=schema.campaign.bop).count()
    sf = SafetyFunction.objects.filter(bop=schema.campaign.bop)


    result_each_sf_integrate = gerar_matriz(steps + 1, safety_function_numbers + 1)
    result_each_sf_integrate_falho = gerar_matriz(steps + 1, safety_function_numbers + 1)
    fl = 0



    for safety_function in sf:
        fl += 1
        print(datetime.datetime.today(), "Inicio do calculo da Sf: ", safety_function)
        cuts = safety_function.cuts.all()
        max_cuts = len(cuts)
        corte = 0
        # matriz_index = gerar_matriz(max_cuts, 4)
        matriz_index = [[' ' for i in range(4)] for j in range(max_cuts)]
        # print(datetime.datetime.today(), "Inicio da organização da sf ")
        for cut in cuts:
            fails = cut.failure_modes.split(",")
            falha = 0
            for fail in fails:
                if fail:
                    fail_line = Fail_line(fail, v_integrate)
                    matriz_index[corte][falha] = fail_line
                else:
                    matriz_index[corte][falha] = ' '
                falha = falha + 1
            corte = corte + 1


        for i in range(1, steps):
            result_each_sf_integrate[i][0] = i * dt
            result_each_sf_integrate[i][fl] = calc_PFD_this_timestep(i, v_integrate, matriz_index)

        print(datetime.datetime.today(), "Fim do calculo da Sf: ", safety_function)

    return result_each_sf_integrate


def get_t(t_op):
    t = []
    count = 0
    for i in range(0, len(t_op) - 1):
        #        if t_op[i-1][1] == t_op[i][1]:
        #            count = 0
        t.append(t_op[i][1])

    #        else:
    #            count = count + 1
    #            t.append(count)

    return t


def calculate_failure_modes(m, failure_modes, delay, dt, falha, step_max, t_op):
    # coverage = [0.0 for i in range(5)]

    # cc = [0.0 for i in range(5)]
    # print("failure_modes", failure_modes)

    v_integrate = gerar_matriz(failure_modes, step_max)

    # calculates PFD(t) for all listed failure modes
    # t = time_per_op_mode_cert(m, failure_modes, t_op, step_max)
    t = get_t(t_op)

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
                increase = float(m[j][28])

            # get test time for each test

            for i in range(1, step_max - 1):
                tempo = t[i]
                if tempo:
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

                        pol_falha = 1 - math.exp(c_ * ((((-1) * l_) * i_ * t_) + (((-1) * l_) * t_)))

                    v_integrate[j][i] = 1 - (1 - pol_falha)



    return v_integrate


def time_per_op_mode_cert(m, failure_modes, t_op, tmax):
    tx = gerar_matriz(failure_modes, tmax)

    for i in range(0, len(m)):
        stagger = m[i][19]
        cycle_size = 168
        cycle_to_replace = 10
        teste1 = m[i][10]
        teste2 = m[i][11]
        teste3 = m[i][12]
        teste4 = m[i][13]

        tx[i] = calc_op_time_each_test_recert(m, teste1, teste2,
                                              teste3,
                                              teste4, t_op,
                                              stagger, cycle_size,
                                              cycle_to_replace, i, tmax)

    return tx


def calc_op_time_each_test_recert(m, T1, T2, T3, T4, t_op, stagger, cycle_size, cycle_to_replace, coluna, tmax):
    a = len(t_op)

    t_tests = gerar_matriz(a, 15)

    prox_teste = [None for i in range(5)]
    #               data_atual =  time_now - time_sv
    syst = m[coluna][3]
    comp = m[coluna][5]
    fm = m[coluna][7]
    tipo = m[coluna][23]

    for ii in range(1, len(t_op)):
        # verify teste change

        t_tests[ii][1] = calc_t_test_recert((t_op[ii][1] / 24), T1, stagger)

        t_tests[ii][2] = calc_t_test_recert((t_op[ii][1] / 24), T2, stagger)

        #    t_tests[ii][3] = calc_t_test_recert((t_op[ii][1]/24), T3, stagger)

        #   t_tests[ii][4] = calc_t_test_recert((t_op[ii][1]/24), T4, stagger)

        if tipo == "Step":

            t_tests[ii][6] = (t_op[ii][1] // cycle_size) % cycle_to_replace + 1
            # Calc t-LTk for Step and Weibull Calculations
            for j in range(1, 5):

                if t_tests[ii][j] < 1:
                    t_tests[ii][6 + j] = ii
                else:
                    if ii == 1:
                        t_tests[ii][6 + j] = 0
                    else:

                        t_tests[ii][6 + j] = t_tests[ii - 1][6 + j]

                t_tests[ii][10 + j] = calc_integral_ciclos(t_tests, j, ii, 24)


        else:
            if tipo == "Weibull":
                for j in range(1, 5):
                    if t_tests[ii][j] < 1:
                        t_tests[ii][6 + j] = ii
                    else:
                        if ii == 1:
                            t_tests[ii][6 + j] = 0
                        else:
                            t_tests[ii][6 + j] = t_tests[ii - 1][6 + j]
                t_tests[ii][11] = calc_last_replacement(t_tests, ii)

    return t_tests


def calc_t_test_recert(tempo, test_interval, stagger):
    # if stagger == None :            #retirando o stagger do calculo, igualando sempre a zero (não altera o seu tempo de teste)
    stagger = 0

    if test_interval == None:
        return 0

    if test_interval > 0:
        if tempo > stagger:
            tempo = tempo - stagger
        t = tempo % test_interval

        return t
    else:
        return 0


def calc_last_replacement(t_tests, tempo):
    if tempo == 1:
        return 0  # na planilha o retorno é 0.
    return t_tests[tempo - 1][11]


def calc_integral_ciclos(t_tests, nivel, tempo, dt):
    if tempo == 1:
        return dt
    if t_tests[tempo][nivel] <= 1:
        return 0

    return t_tests[tempo - 1][10 + nivel] + t_tests[tempo][6] * dt


def get_t_op(steps, schema, dt):
    count = 0
    flag = 0
    tmax = int(steps)
    t_op = [[None for i in range(2)] for j in range(tmax + 1)]
    work = 1
    t_op[0][0] = 0
    t_op[0][1] = 0

    phases = schema.phases.all().order_by('start_date')

    for phase in phases:
        if phase.is_drilling:
            for i in range(0, int(phase.duration)):
                count = count + 1
                t_op[count][0] = count
                t_op[count][1] = t_op[count - 1][1] + dt

        elif phase.has_test:
            for i in range(0, int(phase.duration)):
                count = count + 1
                t_op[count][0] = count
                t_op[count][1] = t_op[count - 1][1] + dt

                if i == int(phase.duration) - 1:
                    t_op[count][0] = count
                    t_op[count][1] = 0

        else:

            for i in range(0, int(phase.duration)):
                count = count + 1
                t_op[count][0] = count
                t_op[count][1] = t_op[count - 1][1]


    return t_op

    """

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

"""


def Fail_line(failmode, v_integrate):
    line = -1


    for i in range(0, len(v_integrate)):

        if failmode == v_integrate[i][0]:
            line = i
            return line

    return line


def calc_PFD_this_timestep(step, v_integrate, matriz_index):
    prod_sf = 1


    for corte in range(0, len(matriz_index)):
        produtorio = 1
        for falha in range(0, 4):                 #travado em ordem 4, fazer o for em len do corte

            if matriz_index[corte][falha] != ' ':
                try:
                    produtorio = produtorio * float(v_integrate[matriz_index[corte][falha]][step])
                except:
                    print("v_integrate[matriz_index[corte][falha]][step]",
                          v_integrate[matriz_index[corte][falha]][step], matriz_index[corte][falha], corte, falha, step)
        try:

            prod_sf = prod_sf * (1.0 - produtorio)
        except:
            print("prod", prod_sf, produtorio)

    prod_sf = 1.0 - prod_sf

    if prod_sf == 0:
        prod_sf = 10 ** -40

    return prod_sf


def calc_cuts_contribuition_this_timestep(step, v_integrate, matriz_index):

    contr = []

    for corte in range(0, len(matriz_index)):
        produtorio = 1
        for falha in range(0, 4):

            if matriz_index[corte][falha] != ' ':
                try:
                    produtorio = produtorio * float(v_integrate[matriz_index[corte][falha]][step])

                except:
                    print("errro v_integrate[matriz_index[corte][falha]][step]",
                          matriz_index[corte][falha], corte, falha, step)

        matriz_index[corte][falha+1] = produtorio


    return matriz_index