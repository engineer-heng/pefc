import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pefc.qctools import (ProcessCapability, XBarRChart,
                          normality_test_report, plot_uchart,
                          XmrChart, Spec)

# Reference implementations
# https://luca-scr.github.io/qcc/reference/qcc.html


def display_uchart(defect_test):
    time = defect_test['Month']
    u = defect_test['c']/defect_test['n']
    cl = sum(defect_test['c'])/sum(defect_test['n'])
    ucl = cl + 3*np.sqrt(cl/defect_test['n'])

    cl_s = np.ones(12)*cl
    plt.style.use('ggplot')
    plt.figure(figsize=(12, 6))  # 15, 6
    plt.plot(time, u, 'k', marker='o', markersize=10, lw=3, label='u=c/n')
    plt.plot(time, cl_s, 'r', label='CL')
    plt.plot(time, ucl, 'b--', label='UCL')
    plt.legend()
    plt.title('U chart')
    plt.show()


def test_uchart():
    # U Chart
    xlfile = 'data/spc_data.xlsx'
    defect_test = pd.read_excel(xlfile, 'DefectsData')
    display_uchart(defect_test)
    plot_uchart(defect_test['c'], defect_test['n'], defect_test['Month'])


def test_xmrchart():
    # data preparation
    xlfile = './tests/data/qctools_data.xlsx'
    xmr_data = pd.read_excel(xlfile, 'XmrData', header=None, skiprows=2)
    xs = xmr_data.iloc[:, [1, 3, 5, 7, 9]]
    observation = xmr_data.iloc[:, [0, 2, 4, 6, 8]]
    x = []
    for i in range(xs.shape[1]):
        x.extend(xs.iloc[:, i])
    x = np.array(x)

    obs = []
    for i in range(observation.shape[1]):
        obs.extend(observation.iloc[:, i])
    obs = np.array(obs)
    xmr_chart = XmrChart(obs, x)
    xmr_chart.plot()
    xmr_chart.summary()
    normality_test_report(x)


def test_xmr_qctools_data():
    # data preparation
    xlfile = './tests/data/qctools_data.xlsx'
    xmr_data = pd.read_excel(xlfile, 'XMR', header=None, skiprows=8)
    obs = xmr_data.iloc[:, 0]
    obs = obs.to_numpy()
    x = xmr_data.iloc[:, 1]
    x = x.to_numpy()
    xmr_chart = XmrChart(obs, x)
    xmr_chart.plot()
    xmr_chart.summary()


def test_xmrspcxl():
    # data preparation
    xlfile = './tests/data/qctools_data.xlsx'
    xmr_data = pd.read_excel(xlfile, 'XmrSpcXL', header=None, skiprows=7)

    # Table 1: Example Data for a Stable Process
    xs = xmr_data.iloc[:, [1, 4]]
    observation = xmr_data.iloc[:, [0, 3]]

    x = []
    for i in range(xs.shape[1]):
        x.extend(xs.iloc[:, i])
    x = np.array(x)

    obs = []
    for i in range(observation.shape[1]):
        obs.extend(observation.iloc[:, i])
    obs = np.array(obs)
    xmr_chart1 = XmrChart(obs, x)
    xmr_chart1.plot()
    xmr_chart1.summary()
    pc1 = ProcessCapability(xmr_chart1, Spec((75, 125)))
    pc1.summary()
    normality_test_report(x)

    # Table 2: Unstable Process Data
    xs = xmr_data.iloc[:, [7, 10]]
    observation = xmr_data.iloc[:, [6, 9]]

    x = []
    for i in range(xs.shape[1]):
        x.extend(xs.iloc[:, i])
    x = np.array(x)

    obs = []
    for i in range(observation.shape[1]):
        obs.extend(observation.iloc[:, i])
    obs = np.array(obs)
    xmr_chart2 = XmrChart(obs, x)
    xmr_chart2.plot()
    xmr_chart2.summary()
    pc2 = ProcessCapability(xmr_chart2, Spec((90, 110)))
    pc2.summary()
    normality_test_report(x)
    print("first 25 mean  =", np.mean(x[:25]))
    print("first 25 sd    =", np.std(x[:25], ddof=1))
    print("second 25 mean =", np.mean(x[25:]))
    print("second 25 sd   =", np.std(x[25:], ddof=1))


def test_xbar_r_qctools_data():
    # data preparation
    xlfile = './tests/data/qctools_data.xlsx'
    tbl = pd.read_excel(xlfile, 'XBarR', header=None,
                        skiprows=8, usecols='A:E')
    sub = tbl.iloc[:, 0]
    sub = sub.to_numpy()
    data = tbl.iloc[:, 1:5]
    data = data.to_numpy()
    print(data)
    xbar_r_chart = XBarRChart(sub, data)
    xbar_r_chart.summary()


def data_generator():
    ch = input("Enter choice no. (1, 2 or 3): ")
    ch = int(ch)
    if ch == 1:
        # generate a normal distribution with the required std. dev.
        # for analysis
        # Generate data for qctools_data.xlxs XmrData sheet
        rng = np.random.default_rng(121)  # 121 is the seed
        vals = rng.normal(1.5, 11.5, 125)
        vals = np.around(vals, 0)  # round to an integer
        print(vals)
        normality_test_report(vals)
        obs = np.arange(1, 126)
        xmr_chart = XmrChart(obs, vals)
        xmr_chart.plot(use_rules=False)
        xmr_chart.summary()
        # vals.reshape(25, 5) will cause a zig-zag out of sequence array
        x = vals.reshape(5, 25).transpose()
        df = pd.DataFrame(x)
        print(df)
    elif ch == 2:
        # generate a stable process
        rng = np.random.default_rng(10)
        vals = rng.normal(100, 8, 50)
        vals = np.around(vals, 2)
        print(vals)
        normality_test_report(vals)
        obs = np.arange(1, 51)
        xmr_chart = XmrChart(obs, vals)
        xmr_chart.plot()
        xmr_chart.summary()
        pc = ProcessCapability(xmr_chart, Spec((75, 125)))
        pc.summary()
        # vals.reshape(25, 2) will cause a zig-zag out of sequence array
        x = vals.reshape(2, 25).transpose()  # stable
        # print(x)
        df = pd.DataFrame(x)
        print(df)
    elif ch == 3:
        # generate an unstable process
        # part 1, first 25
        rng = np.random.default_rng(112)
        x1 = rng.normal(91, 2.5, 25)
        x1 = np.around(x1, 2)
        print(x1)
        normality_test_report(x1, aryname="x1")
        # part 2, second 25, simulating process change over time
        rng = np.random.default_rng(113)
        x2 = rng.normal(98, 3.5, 25)
        x2 = np.around(x2, 2)
        print(x2)
        normality_test_report(x2, aryname="x2")
        # combine into one sequentially, x
        x = np.hstack((x1, x2))
        print(x)
        normality_test_report(x, aryname="x")
        obs = np.arange(1, 51)
        xmr_chart = XmrChart(obs, x)
        xmr_chart.plot()
        xmr_chart.summary()
        pc = ProcessCapability(xmr_chart, Spec((90, 110)))
        pc.summary()
        # reshape() is a zig-zag pattern that will disrupt the order.
        # column_stack() will stack the columns correctly
        df = pd.DataFrame(np.column_stack((x1, x2)))
        print(df)
    # Saved as Excel. Same data points may be  altered for
    # illustration purposes
    with pd.ExcelWriter("erase.xlsx") as writer:
        df.to_excel(writer, 'Data', index=False)


if __name__ == '__main__':
    # Demos of qctools
    # data_generator()
    # test_uchart()
    test_xmrchart()
    # test_xmrspcxl()
    # test_xbar_r_qctools_data()
    # test_xmr_qctools_data()
