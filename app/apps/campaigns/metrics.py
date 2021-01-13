from apps.failuremodes.models import FailureMode
from apps.components.models import Component
from apps.subsystems.models import Subsystem
from apps.bops.models import *
from apps.cuts.models import *
from .models import *
from django.db.models import Max
import datetime
from datetime import timedelta
import string
import math
import json
import copy

def run(schema, **kwargs):

    bop = schema.campaign.bop
    m = bop.matrix
    sf_pfds = calculate_SF_PFDS(schema, m)
    return sf_pfds


def gerar_matriz(n_linhas, n_colunas):
    return [[0] * n_colunas for _ in range(n_linhas)]


def getTotalFailMode(bop):
    return FailureMode.objects.filter(component__subsystem__bop__exact=bop).count()

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


def log(*args, **kwargs):
    print('[LOGGER]', args)


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

    t_op = get_t_op(steps, schema, dt, m)
    contagem_pressao = get_pressure_cont(schema, m, steps)
    v_integrate = calculate_failure_modes(m, failure_modes, contagem_pressao, dt, False, steps, t_op)

    schema.cuts_contribution = v_integrate
    schema.save()

    sf = SafetyFunction.objects.filter(bop=schema.campaign.bop)
    safety_function_numbers = SafetyFunction.objects.filter(bop=schema.campaign.bop).count()
    result_each_sf_integrate = gerar_matriz(
        steps + 1, safety_function_numbers + 1)
    result_each_sf_integrate_falho = gerar_matriz(
        steps + 1, safety_function_numbers + 1)
    result_each_sf_integrate_falho = gerar_matriz(steps + 1, safety_function_numbers + 1)
    fl = 0

    events = Event.objects.filter(campaign=schema.campaign).count()
    fail_events = Event.objects.filter(campaign=schema.campaign)
    print("eventos encontrados", events, fail_events)

    for safety_function in sf:
        fl += 1
        print(datetime.datetime.today(),
              "Inicio do calculo da Sf: ", safety_function)
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

        if events > 0:
            print(datetime.datetime.today(), "inicio da redução: ", fail_events)


            vetor_falha = list_fail(v_integrate, fail_events, t_end_camp)

            print(" vetor falha", vetor_falha)
            v_falho = calculate_failure_modes_falho(vetor_falha, v_integrate, t_start_camp, t_end_camp, steps)

            time_fail = fail_op_day(vetor_falha, t_start_camp, t_end_camp)

            matriz_reduzida = reduction_matrix(time_fail, vetor_falha, matriz_index, t_start_camp, safety_function)


            code_final = []
            for item in matriz_reduzida:
                code_reduction = gerar_matriz(len(item), 4)
                for i in range(0, len(item)):
                    for j in range(0, 4):
                        if item[i][j] != ' ':
                            code_reduction[i][j] = v_integrate[int(item[i][j])][0]

                code_final.append(code_reduction)


            cont = 0
            reduzida = matriz_index
            print(datetime.datetime.today(), "fim da redução: ")
            for i in range(1, steps):

                if i == time_fail[cont]:

                    if cont < len(matriz_reduzida):
                        reduzida = matriz_reduzida[cont]
                        cont = cont + 1

                    if cont == len(matriz_reduzida):
                        reduzida = matriz_index

                result_each_sf_integrate_falho[i][0] = i * dt
                result_each_sf_integrate_falho[i][fl] = calc_PFD_this_timestep(i, v_falho,
                                                                                            reduzida)
                result_each_sf_integrate[i][0] = i * dt
                result_each_sf_integrate[i][fl] = calc_PFD_this_timestep(i, v_integrate,
                                                                                      matriz_index)


        else:
            for i in range(1, steps):
                result_each_sf_integrate[i][0] = i * dt
                result_each_sf_integrate[i][fl] = calc_PFD_this_timestep(i, v_integrate, matriz_index)


        print(datetime.datetime.today(), "Fim do calculo da Sf: ", safety_function)

    return result_each_sf_integrate, result_each_sf_integrate_falho


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


def calculate_failure_modes(m, failure_modes, pressure_test, dt, falha, step_max, t_op):
    print("m",m[0])
    cont_component_step = 0
    v_integrate = gerar_matriz(failure_modes, step_max)

    # calculates PFD(t) for all listed failure modes
    # t = time_per_op_mode_cert(m, failure_modes, t_op, step_max)



    # else:
    # t = time_per_op_mode(delay)
    step_min = 1

    for i in range(0, len(m)):
        v_integrate[i][0] = m[i][7]


    for j in range(0, failure_modes):
        t = t_op[j]

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

        if m[j][23].upper() == "PROB" or m[j][23].upper() == "PROBABILITY":

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
                pressure = pressure_test[cont_component_step]
                cont_component_step = cont_component_step + 1



            # get test time for each test

            for i in range(1, step_max):
                tempo = t[i][1]
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

                        t_op_atual = tempo
                        p1 = float(xlambda) ** float(eta)

                        p2 = (t_op_atual - t_op_replace) ** eta
                        p3 = (t_op_ltk - t_op_replace) ** eta
                        lambda_effetivo = p1 * (abs(p2 - p3))

                        pol_falha = 1 - math.exp(((-1) * coverage * (lambda_effetivo)))

                    if m[j][23] == "Step":
                        l_ = xlambda
                        c_ = coverage
                        t_ = tempo * (dt)
                        i_ = increase
                        Cin_ = (pressure[i]-1)

                        pol_falha = 1 - math.exp(c_ * ((((-1) * l_) * i_ * Cin_ ) + (((-1) * l_) * t_)))

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


def get_t_op(steps, schema, dt, failmodes_matrix):
    fm = len(failmodes_matrix)
    count = 0
    flag = 0
    tmax = int(steps)
    t_op_total = []
    work = 1

    phases = schema.phases.all().order_by('start_date')

    for failmode in range(0, fm):
        t = [[None for i in range(2)] for j in range(tmax + 1)]
        t[0][0] = 0
        t[0][1] = 0
        t_op_total.append(t)

    count_ext = 0
    for phase in phases:

            if phase.is_drilling:

                for t_op in t_op_total:
                    count_int = count_ext
                    for i in range(0, int(phase.duration)):
                        count_int = count_int + 1
                        t_op[count_int][0] = count_int
                        t_op[count_int][1] = t_op[count_int - 1][1] + dt

            elif phase.has_test:

                tested_failmodes = get_tested_failmodes(phase,failmodes_matrix)

                for failmode in range(0, fm):

                    count_int = count_ext
                    if failmode in tested_failmodes:

                        for i in range(0, int(phase.duration)):
                            count_int = count_int + 1
                            t_op_total[failmode][count_int][0] = count_int
                            t_op_total[failmode][count_int][1] = t_op_total[failmode][count_int - 1][1] + dt

                            if i == int(phase.duration) - 1:
                                t_op_total[failmode][count_int][0] = count_int
                                t_op_total[failmode][count_int][1] = 0


                    else:

                        for i in range(0, int(phase.duration)):
                            count_int = count_int + 1
                            t_op_total[failmode][count_int][0] = count_int
                            t_op_total[failmode][count_int][1] = t_op_total[failmode][count_int - 1][1] + dt




            else:
                for t_op in t_op_total:
                    count_int = count_ext
                    for i in range(0, int(phase.duration)):
                        count_int = count_int + 1
                        t_op[count_int][0] = count_int
                        t_op[count_int][1] = t_op[count_int - 1][1]

            count_ext = count_ext + int(phase.duration)

    return t_op_total

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
           ' flag = flag + 1
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
        for falha in range(0, 4):  # travado em ordem 4, fazer o for em len do corte

            if matriz_index[corte][falha] != ' ':
                try:
                    produtorio = produtorio * \
                        float(v_integrate[matriz_index[corte][falha]][step])
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
                    produtorio = produtorio * \
                        float(v_integrate[matriz_index[corte][falha]][step])

                except:
                    print("errro v_integrate[matriz_index[corte][falha]][step]",
                          matriz_index[corte][falha], corte, falha, step)

        matriz_index[corte][falha+1] = produtorio

    return matriz_index



def list_fail(v_integrate, fails, t_end_camp):

    vector_falha = []

    for fail in fails:
        print("entrou no list fail", fail.type, fail.description)
        if fail.type == 'FIL':

            v_falha = v_failmode(v_integrate, fail, fail.object_code, t_end_camp)

            vector_falha.append(v_falha)

        else:

            if fail.type == 'CIL':

                v_falha = fail_comp(v_integrate, fail,t_end_camp )

            else:

                v_falha = fail_sub(v_integrate, fail)

            for i in range(0, len(v_falha)):
                vector_falha.append(v_falha[i][0])

    return vector_falha


def fail_sub(v_integrate, fail):
    sub = fail.object_code
    components = Component.objects.filter(subsystem_id=sub)
    vector_falha = []
    for comp in components:
        v_falha = fail_comp(v_integrate, fail, comp)
        vector_falha.append(v_falha)
    return vector_falha


def fail_comp(v_integrate, fail, t_end_camp):

    component = fail.object_code
    fails_mode = FailureMode.objects.filter(component_id=component)
    vetor_falha = []

    for failmode in fails_mode:

        v_falha = v_failmode(v_integrate, fail, failmode, t_end_camp)

        vetor_falha.append(v_falha)

    return vetor_falha


def v_failmode(v_integrate, fail, failmode, t_end_camp):

    startfail = fail.date

    flag = 0
    for i in range(0, len(v_integrate)):
        if failmode == v_integrate[i][0]:
            position = i
            print("achou a posição", i)

    endfail = t_end_camp

    vetor_falha = [position, startfail, endfail]

    return vetor_falha

def get_tested_failmodes(phase, failmodes_matrix):

    tested_failmodes = []
    groups = phase.test_groups.all()
    for group in groups:
        group_failmode = group.failure_modes.all()
        for fail in group_failmode:

            for failmode in range(0, len(failmodes_matrix)):
                if fail.code == failmodes_matrix[failmode][7]:

                    tested_failmodes.append(failmode)


    return tested_failmodes

def get_pressure_cont(schema, m, tmax):
    print("vai procurar teste de pressao")
    phases = schema.phases.all().order_by('start_date')
    cont = 0
    contagem_total = []

    for failmode in m:
        teste = 1
        if failmode[23] == 'Step':
            print("to no modo de falha", failmode[7], failmode[23])

            contagem = [1 for j in range(tmax + 1)]

            for phase in phases:

                if phase.has_test:
                    groups = phase.test_groups.all()
                    for group in groups:
                        if group.pressure_test:
                            teste = contagem[cont] + 1
                            group_failmode = group.failure_modes.all()

                            for fail in group_failmode:

                                if failmode[7] == fail.code:


                                    for i in range(cont, (cont + int(phase.duration))):
                                        contagem[i] = teste


                else:
                    for i in range(cont, (cont + int(phase.duration))):
                        contagem[i] = teste


                cont = cont + int(phase.duration)

            contagem_total.append(contagem)



    return contagem_total


def reduction_matrix(time_fail, fails, matriz_index, start_camp, safety):
    # verificar a ordenação por ordem do corte antes de realizar a redução

    matrizes_reduzidas = []
    m_reduzida = []
    cod = []

    for i in range(0, len(time_fail) - 1):
        reduction = []
        cont = 0
        new_index = copy.deepcopy(matriz_index)
        cod_cut = []

        for fail in fails:

            fail_step_start = abs((fail[1] - start_camp).days)
            fail_step_end = abs((fail[2] - start_camp).days)
            print("teste", time_fail, i)

            if fail_step_start <= time_fail[i] and fail_step_end > time_fail[i]:
                sub_element = fail[0]

                for j in range(0, len(new_index)):  # com ordenação if i > modo de falha stop o for

                    if sub_element in new_index[j]:
                        reduction.append(new_index[j])
                        reduction[cont][reduction[cont].index(sub_element)] = ' '

                        cont = cont + 1

            cortes_reduzir = []
            print("cont", cont)

            for item in reduction:
                a = 0

                for cuts in new_index:
                    a = a + 1
                    cut = copy.deepcopy(cuts)
                    if ' ' not in cuts:
                        cut.append(' ')

                    if set(item).issubset(cut) and cut != item:
                        cortes_reduzir.append(cuts)

            # reduzida = [item for item in new_index if item not in cortes_reduzir]
            a = 0
            reduzida = []
            for item in new_index:
                a = a + 1
                if item not in cortes_reduzir:
                    reduzida.append(item)
                    cod_cut.append(a)

            new_index = copy.deepcopy(reduzida)

        m_reduzida.append(reduzida)
        saf = str(safety)
        #with open('Codigos da redução - sf-' + saf + '.csv', 'w') as output:
        #    writer = csv.writer(output)
        #    writer.writerow(cod_cut)
        #    writer.writerow(str('next safety'))
        cod.append(cod_cut)

    # print("reduzida", cortes_reduzir)
    # print("redução", reduction)
    # print("matriz original", matriz_index)

    return m_reduzida


def calculate_failure_modes_falho(vetor_falha, v_integrate, t_start_recert, t_end_camp, steps):
    v_integrate_falho = copy.deepcopy(v_integrate)

    for i in range(0, len(vetor_falha)):
        print("vetor_falha[i][1]", vetor_falha[i][1], t_start_recert)

        start = vetor_falha[i][1] - t_start_recert
        start = int(start.total_seconds() / 60 ** 2)

        camp_period = t_end_camp - t_start_recert
        steps = int(camp_period.total_seconds() / 60 ** 2)

        end = steps
        indice = vetor_falha[i][0]

        for j in range(start, end):
            # if j > start and j < end:          #for correndo apenas pelo tempo que a falha está ativa
            v_integrate_falho[indice][j] = 1

    return v_integrate_falho

def fail_op_day(vetor, start_camp, t_end_camp):
    v = []
    for fail in vetor:

        if abs((fail[1] - start_camp).days) not in v:
            v.append(abs((fail[1] - start_camp).days))

        if abs((t_end_camp- start_camp).days) not in v:
            v.append(abs((t_end_camp - start_camp).days))

    v = sorted(v)

    return v