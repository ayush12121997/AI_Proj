import numpy as np
import matplotlib.pyplot as plt


def Plotter():
    Y1 = np.loadtxt("WICC_2_yValues_QL_5.txt")
    Y1 = Y1[81:]

    array_y = []
    gap = len(Y1) / 91
    rewardsForEveryHundred = np.split(np.array(Y1), len(Y1) / gap)
    for r in rewardsForEveryHundred:
        array_y.append(sum(r / gap))
    Y1 = np.loadtxt("WICC_0_yValues_QL_1.txt")
    Y3 = np.loadtxt("WICC_1_yValues_QL_1.txt")
    Y5 = np.loadtxt("WICC_2_yValues_QL_1.txt")
    Y7 = np.loadtxt("WOCC_yValues_QL_1.txt")
    X = np.loadtxt("WICC_0_xValues_QL_1.txt")
    ZeroLine = [0] * np.shape(Y1)[0]

    Figure, ax = plt.subplots()
    Y1 = np.array(array_y)
    ax.plot(X, Y1 / 1, color='blue', label='Card counting (2 Arrays)')
    ax.plot(X, Y3 / 1, color='cyan', label='Card counting (3 Arrays)')
    ax.plot(X, Y5 / 1, color='green', label='Card counting (10 Arrays)')
    ax.plot(X, Y7 / 1, color='blue', label='No Card counting')
    ax.plot(X, ZeroLine, color='black', linewidth=0.5)
    ax.set_ylim(-1, 1)

    plt.xlabel("Number of Episodes")
    plt.ylabel("Estimated Rewards per Round")
    plt.title("Q Learning for 1 Round")
    plt.legend(loc=4)
    plt.show()


if __name__ == '__main__':
    Plotter()
