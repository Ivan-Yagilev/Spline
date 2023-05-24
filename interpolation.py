import csv
from math import sin, cos


# Численное дифференцирование
def get_diff(lst, x):
    res = [(lst[1] - lst[0])/(x[1] - x[0])]
    for i in range(1, len(x)-1):
        res.append((lst[i+1] - lst[i-1])/(x[i+1] - x[i-1]))
    res.append((lst[-1] - lst[-2])/(x[-1] - x[-2]))
    return res


def main_task_func(x):
    return x * sin(x) / 3


def main_task_func_diff(x):
    return sin(x)/3 + x*cos(x)/3


def main_task_func_diff2(x):
    return (2*cos(x) - x*sin(x))/3


def test_task_func(x):
    if x < 0:
        return x ** 3 + 3*x**2
    return -x ** 3 + 3*x**2


def test_task_func_diff(x):
    if x < 0:
        return 3*x ** 2 + 6*x
    return -3*x ** 2 + 6*x


def test_task_func_diff2(x):
    if x < 0:
        return 6*x + 6
    return -6*x + 6


def osc_task_func(x):
    return main_task_func(x) + cos(10*x)


def osc_task_func_diff(x):
    return main_task_func_diff(x) - 10*sin(10*x)


def osc_task_func_diff2(x):
    return main_task_func_diff2(x) - 100*cos(10*x)


# Кубический сплайн в каноническом виде
def S_x(a, b, c, d, x_new, x0, x):
    def s(y):
        return a + b*(y-x0) + (c/2)*(y-x0)**2 + (d/6)*(y-x0)**3
    res = []
    for el in x_new:
        if x <= el < x0:
            res.append(s(el))
    return res[::-1]


# метод прогонки для коэффициентов Ci
def find_c(h, border1, border2, f_lst):
    N = len(f_lst)
    a = []
    b = [1]
    c = [0]
    d = [border1]
    for i in range(1, N-1):
        a.append(h)
        b.append(4*h)
        c.append(h)
        res = (f_lst[i+1]-2*f_lst[i]+f_lst[i-1])/h
        d.append(6*res)
    a.append(0)
    b.append(1)
    d.append(border2)

    y = [b[0]]
    aplha = [-c[0]/y[0]]
    beta = [d[0]/y[0]]
    for i in range(1, N-1):
        y.append(b[i]+a[i]*aplha[i-1])
        aplha.append(-c[i]/y[i])
        beta.append((d[i]-a[i]*beta[i-1])/y[i])
    y.append(b[-1] + a[-1]*aplha[-1])
    beta.append((d[-1] - a[-1]*beta[-1])/y[-1])

    coeff = [0] * N
    coeff[-1] = beta[-1]
    for i in range(N-2, -1, -1):
        coeff[i] = aplha[i] * coeff[i+1] + beta[i]
    return coeff


# Получение коэффициентов A, B, D
def get_coeff(c, h, f_lst):
    a = f_lst[1:]
    b = []
    d = []
    for i in range(1, len(c)):
        b.append((f_lst[i]-f_lst[i-1])/h + c[i]*h/3 + c[i-1]*h/6)
        d.append((c[i]-c[i-1])/h)
    return a, b, d


# Алгоритм получения кубического сплайна
def cubic_interpolation(h, border1, border2, f_lst, x, x_new, choice):
    ci = find_c(h, border1, border2, f_lst)
    ai, bi, di = get_coeff(ci, h, f_lst)

    res = []
    for i in range(len(bi)):
        res = S_x(ai[i], bi[i], ci[i+1], di[i], x_new, x[i+1], x[i]) + res
    res = res[::-1]

    with open('table_one.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['i', 'Xi-1', 'Xi', 'Ai', 'Bi', 'Ci', 'Di'])
        for i in range(0, len(bi)-1):
            spamwriter.writerow([i+1, x[i], x[i+1], ai[i], bi[i], ci[i+1], di[i]])

    if choice == '2':
        F = [main_task_func(i) for i in x_new]
        dF = [main_task_func_diff(i) for i in x_new]
        ddF = [main_task_func_diff2(i) for i in x_new]
    elif choice == '1':
        F = [test_task_func(i) for i in x_new]
        dF = [test_task_func_diff(i) for i in x_new]
        ddF = [test_task_func_diff2(i) for i in x_new]
    else:
        F = [osc_task_func(i) for i in x_new]
        dF = [osc_task_func_diff(i) for i in x_new]
        ddF = [osc_task_func_diff2(i) for i in x_new]

    dS = get_diff(res, x_new)
    ddS = get_diff(dS, x_new)

    with open('table_two.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar=',', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['j', 'xj', 'F(xj)', 'S(xj)', '|F(xj)-S(xj)|', 'dF(xj)', 'dS(xj)', '|dF(xj)-dS(xj)|', 'ddF(xj)', 'ddS(xj)', '|ddF(xj)-ddS(xj)|'])
        for j in range(0, len(F)):
            spamwriter.writerow([j+1, x_new[j], F[j], res[j], abs(F[j]-res[j]), dF[j], dS[j], abs(dF[j]-dS[j]), ddF[j], ddS[j], abs(ddF[j]-ddS[j])])
    return res, F, dF, dS, ddF, ddS
