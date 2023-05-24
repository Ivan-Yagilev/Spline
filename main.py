import matplotlib.pyplot as plt
from math import pi
import numpy as np
from interpolation import cubic_interpolation, main_task_func,\
    test_task_func, osc_task_func


plt.style.use('seaborn')


def get_info(n, x, lst, diff_lst, diff2_lst):
    print(f"""          СПРАВКА
    Сетка сплайна: n = {n};
    Контрольная сетка: N = {len(x)};

    Погрешность сплайна на контрольной сетке: max(F-S) = {max(lst)}
    При x = {x[lst.index(max(lst))]};

    Погрешность производной на контрольной сетке: max(dF-dS) = {max(diff_lst)},
    При x = {x[diff_lst.index(max(diff_lst))]};

    Погрешность вторых производных на контрольной сетке: max(ddF-ddS) = {max(diff2_lst)},
    При x = {x[diff2_lst.index(max(diff2_lst))]}""")


def get_plot(x_new, F, S, dF, dS, ddF, ddS):
    plt.subplot(1, 3, 1)
    plt.plot(x_new, F, 'g--', label='Точное решение')
    plt.plot(x_new, S, 'b-', label='Интерполяция')
    plt.legend(loc='best')
    plt.title("График точного решения и сплайн")

    plt.subplot(1, 3, 2)
    plt.plot(x_new, dF, 'g--', label='Точное решение, первая производная')
    plt.plot(x_new, dS, 'b-', label='Интерполяция, первая производная')
    plt.legend(loc='best')
    plt.title("Первые производные")

    plt.subplot(1, 3, 3)
    plt.plot(x_new, ddF, 'g--', label='Точное решение, вторая производная')
    plt.plot(x_new, ddS, 'b-', label='Интерполяция, вторая производная')
    plt.legend(loc='best')
    plt.title("Вторые производные")
    plt.show()

    plt.subplot(1, 3, 1)
    plt.plot(x_new, [abs(F[i]-S[i]) for i in range(len(S))], 'g--')
    plt.title("Разность точного решения и интерполяции")

    plt.subplot(1, 3, 2)
    plt.plot(x_new, [abs(dF[i]-dS[i]) for i in range(len(dS))], 'b--')
    plt.title("Разность первых производных")

    plt.subplot(1, 3, 3)
    plt.plot(x_new, [abs(ddF[i]-ddS[i]) for i in range(len(ddS))], 'r--')
    plt.title("Разности вторых производных")
    plt.show()


def main_task(n):
    a, b = 0, pi
    h = (b - a) / n
    border1 = 0
    border2 = 0

    x = [a]
    coord = a
    while coord <= b:
        coord += h
        x.append(coord)

    f = [main_task_func(el) for el in x]
    N = 2*n if n > 750 else 1500
    x_new = np.linspace(a, b, N)

    S, F, dF, dS, ddF, ddS = cubic_interpolation(h, border1, border2, f, x, x_new, '2')

    get_plot(x_new, F, S, dF, dS, ddF, ddS)
    get_info(n, x_new, [abs(F[i]-S[i]) for i in range(len(S))], \
        [abs(dF[i]-dS[i]) for i in range(len(dS))], [abs(ddF[i]-ddS[i]) for i in range(len(dS))])


def test_task(n):
    a, b = -1, 1
    h = (b - a) / n
    border1 = 0
    border2 = 0

    x = [a]
    coord = a
    while coord <= b:
        coord += h
        x.append(coord)

    f = [test_task_func(el) for el in x]
    N = 2*n if n > 750 else 1500
    x_new = np.linspace(a, b, N)

    S, F, dF, dS, ddF, ddS = cubic_interpolation(h, border1, border2, f, x, x_new, '1')
    get_plot(x_new, F, S, dF, dS, ddF, ddS)
    get_info(n, x_new, [abs(F[i]-S[i]) for i in range(len(S))], \
        [abs(dF[i]-dS[i]) for i in range(len(dS))], [abs(ddF[i]-ddS[i]) for i in range(len(dS))])


def osc_task(n):
    a, b = 0, pi
    h = (b - a) / n
    border1 = 0
    border2 = 0

    x = [a]
    coord = a
    while coord <= b:
        coord += h
        x.append(coord)

    f = [osc_task_func(el) for el in x]
    N = 2*n if n > 750 else 1500
    x_new = np.linspace(a, b, N)

    S, F, dF, dS, ddF, ddS = cubic_interpolation(h, border1, border2, f, x, x_new, '3')
    get_plot(x_new, F, S, dF, dS, ddF, ddS)
    get_info(n, x_new, [abs(F[i]-S[i]) for i in range(len(S))], \
        [abs(dF[i]-dS[i]) for i in range(len(dS))], [abs(ddF[i]-ddS[i]) for i in range(len(dS))])


if __name__ == '__main__':
    n = int(input("\nВведите число разбиений n\n"))
    choice = input('\nТип задачи\n1. Тестовая\n2. Основная\n3. Осциллирующая\n')
    if choice == '2':
        main_task(n)
    elif choice == '1':
        test_task(n)
    elif choice == '3':
        osc_task(n)
