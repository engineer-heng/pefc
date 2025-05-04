# Python Engineering Foundation Class Library (pefc)
# qctools Library
# Copyright(C) 2021-2025 Heng Swee Ngee
#
# Released under the MIT License - https://opensource.org/licenses/MIT
#
""" qctools

    A set of qc tools to support the Basic 7 QC Tools.

    Basic Seven QC Tools
    --------------------
    Seven tools typically used for Quality Circle teams are:

        Check sheet. Not implemented.

        Control chart and Process capability

        Stratification

        Pareto chart

        Histogram

        Cause-and-effect diagram ("fishbone diagram" or Ishikawa diagram)
        Not implemented.

        Scatter diagram and correlation analysis
"""

import math
import statistics

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats
import seaborn as sns
from matplotlib.ticker import FuncFormatter


def mround(x, base=5):
    """ Similar to Excel mround function

        x: numpy.darray of values to be rounded

        base: int or float specifying multiples of the base value.
        Default is 5.

        return: numpy.darray rounded to the required base value

        Example
        -------
        >>> mround(3332)
        >>> 3330
        >>> mround(3335)
        >>> 3335
        >>> (mround(3338)
        >>> 3340
        >>> (mround(2.332, .005)
        >>> 2.33
        >>> (mround(2.335, .005)
        >>> 2.335
        >>> (mround(2.338, .005)
        >>> 2.34
        >>> arr = np.array([1006, 987, 1024, 1023, 978])
        >>> mround(arr)
        >>> array([1005.,  985., 1025., 1025.,  980.])
    """
    ret = None
    if isinstance(x, np.ndarray):
        ret = base * np.around(x/base)
    elif isinstance(x, list) or isinstance(x, tuple):
        raise ValueError("x should be a 1D numpy array")
    else:
        try:
            ret = base * round(x/base)
        except Exception as ex:
            print(ex)
    return ret


def normality_test_report(ary, aryname='X'):
    """ Normality test on an array.
        Both Anderson-Darling and Shapiro-Wilk are tested.

        ary: nparray

        return: bool, True if both Anderson-Darling and Shapiro-Wilk passed.
    """
    print("NORMALITY TEST REPORT")
    print(f"Descriptive Statistics on {aryname}:")
    print("  count      =", ary.size)
    print("  mean       =", np.nanmean(ary))
    mo = statistics.multimode(ary)
    if len(mo) == ary.size:
        mo = None
    elif len(mo) == 1:
        mo = mo[0]
    print("  mode       =", mo)
    ary_max = np.nanmax(ary)
    ary_min = np.nanmin(ary)
    std = np.nanstd(ary, ddof=1)  # sample std. dev.
    print(f"  sem        = {std/math.sqrt(ary.size)} (std. error of mean)")
    print(f"  std. dev.  = {std} (sample std. deviation)")
    print(f"  variance   = {np.nanvar(ary, ddof=1)} (sample variance)")
    print("  range      =", ary_max - ary_min)
    percentiles = np.nanpercentile(ary, [0., 25., 50., 75., 100.])
    print("  min        =", ary_min)
    print("  25%        =", percentiles[1])
    print(f"  50%        = {np.nanmedian(ary)} (median)")
    print("  75%        =", percentiles[3])
    print("  max        =", ary_max)
    print("  data type  =", ary.dtype)
    # hist
    # arguments are passed to np.histogram
    plt.hist(ary, bins='auto', color='b')
    plt.title(f"Histogram of {aryname}")
    plt.show()

    print(f"\nNormality tests on {aryname}:")
    stats.probplot(ary, dist="norm", fit=True,
                   rvalue=True, plot=plt)
    plt.title(
        "Probability Plot Comparision with Perfectly Normal Distribution")
    plt.show()
    ad_result = sw_result = False
    print("1. Anderson-Darling(AD) Test(Preferred)")
    ad = stats.anderson(ary)
    print("  AD statistic          =", ad.statistic)
    print("  AD critical_value     =", ad.critical_values)
    print("  AD significance_level =", ad.significance_level)
    if all(ad.critical_values >= ad.statistic) is True:
        ad_result = True
        print("  AD: This is a normal distribution")
    else:
        print("  AD: This is NOT a normal distribution")
    print("2. Shapiro-Wilk(SW) Test")
    sw_stat, sw_pvalue = stats.shapiro(ary)
    print("  SW statistic =", sw_stat)
    print("  SW p-value   =", sw_pvalue)
    if sw_pvalue > 0.05:
        sw_result = True
        print("  SW: This is a normal distribution")
    else:
        print("  SW: This is NOT a normal distribution")
    if all((ad_result, sw_result)):
        ret = True
        result = "Passed."
    else:
        ret = False
        result = "Failed!"
    print(f"Normality Test {result}")

    return ret

# NOTE: Keep the implementation simple and avoid overloading arguments
# to support many charts from one function like R's qcc library


def plot_uchart(c, n, time):
    u = c/n
    cl = sum(c)/sum(n)
    ucl = cl + 3 * np.sqrt(cl/n)
    cl_s = np.ones(len(time))*cl

    # out of control points
    ofc = u[u >= ucl]
    ofc_ind = list(ofc.index)
    ofc_time = time[ofc_ind]
    print("Out of Control:")
    if len(ofc) == 0:
        print("All under control.")
    else:
        for i, j in zip(ofc_ind, range(len(ofc))):
            print(str(j+1) + " - " + str(ofc_time[i]) + ", " + str(ofc[i]))

    plt.style.use('ggplot')
    plt.figure(figsize=(12, 6))  # 15, 6
    # plot u chart
    plt.plot(time, u, 'k', marker='o', markersize=8, lw=3, label='u=c/n')
    plt.plot(time, cl_s, 'g', label='CL')
    plt.plot(time, ucl, 'b--', label='UCL')
    # plot out of control points
    for i in ofc_ind:
        plt.scatter(ofc_time[i], ofc[i], c='r', s=200)
    plt.legend()
    plt.ylim((0, max(u)+0.001))
    plt.title('U chart')
    plt.show()


def spc_rules(data, obs, cl, ucl, ucl_b, ucl_c, lcl, lcl_b, lcl_c):
    n = len(data)
    ind = np.array(range(n))

    # rule 1
    ofc1 = data[(data > ucl) | (data < lcl)]
    ofc1_obs = obs[(data > ucl) | (data < lcl)]

    # rule 2
    ofc2_ind = []
    for i in range(n-2):
        d = data[i:i+3]
        index = ind[i:i+3]
        if ((d > ucl_b).sum() == 2) | ((d < lcl_b).sum() == 2):
            ofc2_ind.extend(index[(d > ucl_b) | (d < lcl_b)])
    ofc2_ind = list(sorted(set(ofc2_ind)))
    ofc2 = data[ofc2_ind]
    ofc2_obs = obs[ofc2_ind]

    # rule 3
    ofc3_ind = []
    for i in range(n-4):
        d = data[i:i+5]
        index = ind[i:i+5]
        if ((d > ucl_c).sum() == 4) | ((d < lcl_c).sum() == 4):
            ofc3_ind.extend(index[(d > ucl_c) | (d < lcl_c)])
    ofc3_ind = list(sorted(set(ofc3_ind)))
    ofc3 = data[ofc3_ind]
    ofc3_obs = obs[ofc3_ind]

    # rule 4
    ofc4_ind = []
    for i in range(n-8):
        d = data[i:i+9]
        index = ind[i:i+9]
        if ((d > cl).sum() == 9) | ((d < cl).sum() == 9):
            ofc4_ind.extend(index)
    ofc4_ind = list(sorted(set(ofc4_ind)))
    ofc4 = data[ofc4_ind]
    ofc4_obs = obs[ofc4_ind]

    # rule 5
    ofc5_ind = []
    for i in range(n-6):
        d = data[i:i+7]
        index = ind[i:i+7]
        if (all(u <= v for u, v in zip(d, d[1:])) |
                all(u >= v for u, v in zip(d, d[1:]))):
            ofc5_ind.extend(index)
    ofc5_ind = list(sorted(set(ofc5_ind)))
    ofc5 = data[ofc5_ind]
    ofc5_obs = obs[ofc5_ind]

    # rule 6
    ofc6_ind = []
    for i in range(n-7):
        d = data[i:i+8]
        index = ind[i:i+8]
        if (all(d > ucl_c) | all(d < lcl_c)):
            ofc6_ind.extend(index)
    ofc6_ind = list(sorted(set(ofc6_ind)))
    ofc6 = data[ofc6_ind]
    ofc6_obs = obs[ofc6_ind]

    # rule 7
    ofc7_ind = []
    for i in range(n-14):
        d = data[i:i+15]
        index = ind[i:i+15]
        if all(lcl_c < d) and all(d < ucl_c):
            ofc7_ind.extend(index)
    ofc7_ind = list(sorted(set(ofc7_ind)))
    ofc7 = data[ofc7_ind]
    ofc7_obs = obs[ofc7_ind]

    # rule 8
    ofc8_ind = []
    for i in range(n-13):
        d = data[i:i+14]
        index = ind[i:i+14]
        diff = list(v - u for u, v in zip(d, d[1:]))
        if all(u*v < 0 for u, v in zip(diff, diff[1:])):
            ofc8_ind.extend(index)
    ofc8_ind = list(sorted(set(ofc8_ind)))
    ofc8 = data[ofc8_ind]
    ofc8_obs = obs[ofc8_ind]

    return (ofc1, ofc1_obs, ofc2, ofc2_obs, ofc3, ofc3_obs, ofc4, ofc4_obs,
            ofc5, ofc5_obs, ofc6, ofc6_obs, ofc7, ofc7_obs, ofc8, ofc8_obs)

# NOTE: Python is a zero-based indexing system therefore it is useful
# to have an observation(obs) or subgroup(subg) starting from 1 to
# act as the x-axis for plotting. If not specified it will automatically
# generated.


class XmrChart():
    """ Class for managing and plotting XMR charts
    """

    def __init__(self, obs, x) -> None:
        """ Constructor for XmrChart.
            The data x will be used for calculations to 'calibrate'
            the chart and is also suitable for trials.

            obs: np.array of int, observation sequential numbers.
            Default is None. If obs=None it will be automatically
            generated.

            x: np.array of float or int, individual values in a series
        """
        subgroup = 2  # only subgroup is supported
        # depend on subgroup value, n starts from 2 to 10
        e2_ = [2.660, 1.772, 1.457, 1.290, 1.184, 1.109,
               1.054, 1.010, 0.975]
        d4_ = [3.268, 2.574, 2.282, 2.114, 2.004, 1.924,
               1.864, 1.816, 1.777]
        e2 = e2_[subgroup-2]  # Chart constant E2
        d4 = d4_[subgroup-2]  # Chart constant D4

        # for process std deviation calculation
        d2_ = [1.128, 1.693, 2.059, 2.326, 2.534, 2.704, 2.847, 2.970, 3.078]
        d2 = d2_[subgroup-2]  # Chart constant d2

        # data
        self.x = x
        self.obs = obs
        self.n = len(x)

        self.x_bar = x.mean()
        # moving range calculations
        self.mr = np.array(list(abs(v - u) for u, v in zip(x, x[1:])))
        self.mr_bar = self.mr.mean()

        # I chart
        self.x_ucl = self.x_bar + e2 * self.mr_bar  # a
        self.x_ucl_c = self.x_bar + e2 * self.mr_bar * (1/3)
        self.x_ucl_b = self.x_bar + e2 * self.mr_bar * (2/3)
        self.x_lcl = self.x_bar - e2 * self.mr_bar  # a
        self.x_lcl_c = self.x_bar - e2 * self.mr_bar * (1/3)
        self.x_lcl_b = self.x_bar - e2 * self.mr_bar * (2/3)

        # MR chart
        self.mr_ucl = d4 * self.mr_bar  # a
        self.mr_ucl_c = self.mr_bar + (self.mr_ucl - self.mr_bar) * (1/3)
        self.mr_ucl_b = self.mr_bar + (self.mr_ucl - self.mr_bar) * (2/3)
        self.mr_lcl = 0  # a
        self.mr_lcl_c = self.mr_bar - (self.mr_ucl - self.mr_bar) * (1/3)
        self.mr_lcl_b = self.mr_bar - (self.mr_ucl - self.mr_bar) * (2/3)
        if self.mr_lcl_c < 0:
            self.mr_lcl_c = 0
        if self.mr_lcl_b < 0:
            self.mr_lcl_b = 0

        self.proc_mean = self.x_bar
        self.proc_std_dev = self.mr_bar/d2  # ASQ's pooled std. dev.
        self.total_std_dev = np.std(self.x, ddof=1)  # ASQ's total std. dev.

    def plot(self, new_obs=None, new_x=None, use_rules=True):
        """ Plots the XMR Chart
            Assumes new data below is from a different data set than
            those used for calibration. These new data will not be used for
            calculations on the control limits.

            new_obs: np.array of int, observation sequential numbers.
            If None the data for calibration will be plotted.

            new_x: np.array of float or int, individual values in a series
            If None the data for calibration will be plotted.

        """
        if new_obs is None and new_x is None:
            # calibration data when chart is first created
            obs = self.obs
            x = self.x
            n = self.n
            mr = self.mr
        else:
            # new data for process monitoring.
            # assume different data set from calibration.
            x = new_x
            n = len(x)
            obs = new_obs
            # moving range calculations
            mr = np.array(list(abs(v - u) for u, v in zip(x, x[1:])))

        if use_rules:
            # 8 rules
            x_ofc = spc_rules(
                x, obs, self.x_bar, self.x_ucl, self.x_ucl_b,
                self.x_ucl_c, self.x_lcl, self.x_lcl_b, self.x_lcl_c)
            print("========== I chart test ==========")
            for r in range(8):
                print(f"Against Rule: {(r+1):d}")
                if len(x_ofc[r*2]) == 0:
                    print("None.")
                else:
                    for num, i, j in zip(
                        range(len(x_ofc[r*2])), x_ofc[r*2+1], x_ofc[r*2]
                    ):
                        print(f"\t{num+1:d} -> {str(i):s}, {j:f}")

            mr_ofc = spc_rules(
                mr, obs[1:], self.mr_bar, self.mr_ucl, self.mr_ucl_b,
                self.mr_ucl_c, self.mr_lcl, self.mr_lcl_b, self.mr_lcl_c)
            print("========== MR chart test ==========")
            for r in range(8):
                print(f"Against Rule: {(r+1):d}")
                if len(mr_ofc[r*2]) == 0:
                    print("None.")
                else:
                    for num, i, j in zip(
                        range(len(mr_ofc[r*2])), mr_ofc[r*2+1], mr_ofc[r*2]
                    ):
                        print(f"\t{num+1:d} -> {str(i):s}, {j:f}")

        # plot
        plt.style.use('ggplot')
        plt.figure(figsize=(12, 8))  # 15, 8

        plt.subplot(2, 1, 1)
        plt.plot(obs, x, 'k', marker='o', markersize=5, lw=2, label='X')
        plt.plot(obs, np.ones(n)*self.x_bar, 'r', label='CL')
        plt.plot(obs, np.ones(n)*self.x_ucl, 'b', lw=1)
        plt.plot(obs, np.ones(n)*self.x_ucl_c, 'b-.', lw=1)
        plt.plot(obs, np.ones(n)*self.x_ucl_b, 'b-.', lw=1)
        plt.plot(obs, np.ones(n)*self.x_lcl, 'b', lw=1)
        plt.plot(obs, np.ones(n)*self.x_lcl_c, 'b-.', lw=1)
        plt.plot(obs, np.ones(n)*self.x_lcl_b, 'b-.', lw=1)
        if use_rules:
            for r in range(8):
                for i in range(len(x_ofc[r*2])):
                    plt.scatter(x_ofc[r*2+1][i], x_ofc[r*2][i], c='r', s=70)
        plt.ylabel('Individual X')
        # plt.xlabel('Observation')
        plt.legend()
        plt.title('Individual X chart', fontweight='bold')

        plt.subplot(2, 1, 2)
        plt.plot(obs[1:], mr, 'k', marker='o', markersize=5,
                 lw=2, label='MR')
        plt.plot(obs[1:], np.ones(n-1)*self.mr_bar, 'r', label='CL')
        plt.plot(obs[1:], np.ones(n-1)*self.mr_ucl, 'b', lw=1)
        plt.plot(obs[1:], np.ones(n-1)*self.mr_ucl_c, 'b-.', lw=1)
        plt.plot(obs[1:], np.ones(n-1)*self.mr_ucl_b, 'b-.', lw=1)
        plt.plot(obs[1:], np.ones(n-1)*self.mr_lcl, 'b', lw=1)
        plt.plot(obs[1:], np.ones(n-1)*self.mr_lcl_c, 'b-.', lw=1)
        if use_rules:
            for r in range(8):
                for i in range(len(mr_ofc[r*2])):
                    plt.scatter(mr_ofc[r*2+1][i], mr_ofc[r*2][i], c='r', s=70)
        plt.ylabel('Moving Range')
        plt.xlabel('Observation')
        plt.legend()
        plt.title('MR chart', fontweight='bold')
        plt.show()

    @property
    def process_mean(self):
        """ Returns the process mean for the trial or
            calibration data. New data is not used for calculations but
            for monitoring the process.

            process_mean = x_bar, based on Shewhart's formula
        """
        return self.proc_mean

    @property
    def process_std_dev(self):
        """ Returns the process standard deviation for the trial or
            calibration data. New data is not used for calculations but
            for monitoring the process.

            process_std_dev = mr_bar/d2, based on Shewhart's formula
        """
        return self.proc_std_dev

    @property
    def within_std_dev(self):
        """ Returns the process standard deviation for the trial or
            calibration data. New data is not used for calculations but
            for monitoring the process.

            process_std_dev = mr_bar/d2, based on Shewhart's formula
        """
        return self.proc_std_dev

    @property
    def overall_std_dev(self):
        """ Returns the sample standard deviation using the
            mathematical formula for standard deviation instead of using
            Shewhart's formula for charts.
        """
        return self.total_std_dev

    def summary(self):
        print("Individual X Chart:")
        print(f"  Number of obs    = {self.x.size}")
        print(f"  Center           = {self.x_bar}")
        # Use Overall and Within same as minitab and SPC for Excel
        print(f"  StdDev (Overall) = {self.overall_std_dev}")
        print(f"  StdDev (Within)  = {self.within_std_dev}")
        print(f"  UCL              = {self.x_ucl}")
        print(f"  LCL              = {self.x_lcl}")
        print("Moving Range (MR) Chart:")
        print(f"  Number of obs    = {self.mr.size}")
        print(f"  Center           = {self.mr_bar}")
        # repeat the sample std. dev. in case it is plotted separately
        print(f"  StdDev (Overall) = {self.overall_std_dev}")
        print(f"  StdDev (Within)  = {self.within_std_dev}")
        print(f"  UCL              = {self.mr_ucl}")
        print(f"  LCL              = {self.mr_lcl}")


class XBarRChart():
    """ Class for managing and plotting XBar R charts
    """

    def __init__(self, subgn, data) -> None:
        """ Constructor for XBarRChart.
            This data will be used for calculations to 'calibrate'
            the chart and is also suitable for trials.

            subgn: np.array of int, sub-group sequential numbers.
            Typically 20 to 25 sub-groups.

            data: 2D Matrix np.array in float or int values.
            Sample size from 2 to 9 samples per sub-group.
            Typically 2 to 5 samples. 10 or more use the Xbar S Chart.
        """

        # data
        self.m2d = data  # 2D numpy matrix
        self.subs = subgn  # subgroups sequential nos start from 1

        self.k = self.m2d.shape[0]  # total number of sub-groups
        self.n = n = self.m2d.shape[1]  # number of samples in sub-group
        self.obs = self.k * self.n  # total number of observations
        self.x_bar = self.m2d.mean(axis=1)
        self.x_bar_bar = self.x_bar.mean()
        self.r = self.m2d.max(axis=1) - self.m2d.min(axis=1)
        self.r_bar = self.r.mean()

        # XBar R Chart Constants.
        d4_ = [3.267, 2.574, 2.282, 2.114, 2.004, 1.924, 1.864, 1.816,
               1.777, 1.744, 1.717, 1.693, 1.672, 1.653, 1.637, 1.622,
               1.608, 1.597, 1.585, 1.575, 1.566, 1.557, 1.548, 1.541]

        d3_ = [0.0, 0.0, 0.0, 0.0, 0.0, 0.076, 0.136, 0.184,
               0.223, 0.256, 0.283, 0.307, 0.328, 0.347, 0.363,  0.378,
               0.391, 0.403, 0.415, 0.425, 0.434, 0.443, 0.451, 0.459]

        a2_ = [1.880, 1.023, 0.729, 0.577, 0.483, 0.419, 0.373, 0.337,
               0.308, 0.285, 0.266, 0.249, 0.235, 0.223, 0.212, 0.203,
               0.194, 0.187, 0.180, 0.173, 0.167, 0.162, 0.157, 0.153]
        # n-2 to map into the correct value. array starts at n = 2 to 25
        d4 = d4_[n-2]  # Chart constant D4
        d3 = d3_[n-2]  # Chart constant D3
        a2 = a2_[n-2]  # Chart constant A2

        # XBar or Average chart
        self.x_bar_ucl = self.x_bar_bar + a2 * self.r_bar  # a
        self.x_bar_ucl_b = self.x_bar_ucl * (2/3)
        self.x_bar_ucl_c = self.x_bar_ucl * (1/3)
        self.x_bar_lcl = self.x_bar_bar - a2 * self.r_bar  # a
        self.x_bar_lcl_b = self.x_bar_lcl * (2/3)
        self.x_bar_lcl_c = self.x_bar_lcl * (1/3)

        # R or Range chart
        self.r_ucl = d4 * self.r_bar  # a
        self.r_ucl_b = self.r_bar + (self.r_ucl - self.r_bar) * (2/3)
        self.r_ucl_c = self.r_bar + (self.r_ucl - self.r_bar) * (1/3)

        self.r_lcl = d3 * self.r_bar  # a
        self.r_lcl_b = self.r_bar - (self.r_ucl - self.r_bar) * (2/3)
        self.r_lcl_c = self.r_bar - (self.r_ucl - self.r_bar) * (1/3)
        if self.r_lcl_c < 0:
            self.r_lcl_c = 0
        if self.r_lcl_b < 0:
            self.r_lcl_b = 0

        # n starts from 2 which is 0 on this list
        d2_ = [1.128, 1.693, 2.059, 2.326, 2.534, 2.704, 2.847, 2.970,
               3.078, 3.173, 3.258, 3.336, 3.407, 3.472, 3.532, 3.588,
               3.640, 3.689, 3.735, 3.778, 3.819, 3.858, 3.895, 3.931]
        d2 = d2_[n-2]  # Chart d2

        self.proc_std_dev = self.r_bar/d2  # ASQ's pooled std. dev.
        self.proc_mean = self.x_bar_bar
        self.total_std_dev = np.std(self.m2d, ddof=1)  # ASQ's total std. dev.

    @property
    def process_std_dev(self):
        """ Returns the process standard deviation for the trial or
            calibration data. New data is not used for calculations but
            for monitoring the process.

            process_std_dev = r_bar/d2, based on Shewhart's formula
        """
        return self.proc_std_dev

    @property
    def within_std_dev(self):
        """ Returns the process standard deviation for the trial or
            calibration data. New data is not used for calculations but
            for monitoring the process.

            process_std_dev = mr_bar/d2, based on Shewhart's formula
        """
        return self.proc_std_dev

    @property
    def process_mean(self):
        """ Returns the process mean for the trial or
            calibration data. New data is not used for calculations but
            for monitoring the process.

            process_mean = x_bar_bar, based on Shewhart's formula
        """
        return self.proc_mean

    @property
    def overall_std_dev(self):
        """ Returns the sample standard deviation using the
            mathematical formula for standard deviation instead of using
            Shewhart's formula for charts.
        """
        return self.total_std_dev

    def summary(self):
        print("Average X-Bar Chart:")
        print(f"  Number of groups = {self.k}")
        print(f"  Each group size  = {self.n}")
        print(f"  Number of obs.   = {self.obs}")
        print(f"  Center           = {self.x_bar_bar}")
        # Use Overall and Within same as minitab and SPC for Excel
        print(f"  StdDev (Overall) = {self.overall_std_dev}")
        print(f"  StdDev (Within)  = {self.within_std_dev}")
        print(f"  UCL              = {self.x_bar_ucl}")
        print(f"  LCL              = {self.x_bar_lcl}")
        print("Range (R) Chart:")
        print(f"  Number of groups = {self.k}")
        print(f"  Each group size  = {self.n}")
        print(f"  Number of obs.   = {self.obs}")
        print(f"  Center           = {self.r_bar}")
        # repeat the sample std. dev. in case it is plotted separately
        print(f"  StdDev (Overall) = {self.overall_std_dev}")
        print(f"  StdDev (Within)  = {self.within_std_dev}")
        print(f"  UCL              = {self.r_ucl}")
        print(f"  LCL              = {self.r_lcl}")


class Spec():
    """ Class to define and manage the specifications of a variable
    """

    def __init__(self, lims=None, nominal=None):
        """ Spec Constructor

            Parameters
            ----------
            lims: tuple or list of specification limits
                spec_tuple = (LSL, USL) or spec_list = [LSL, USL]
                If there are no LSL or USL put None in its place.
                LSL is the lower spec limit. USL is the upper spec limit.
                If LSL and USL is in the wrong order it will be corrected here.

            nominal: float, optional
                default is None.
                If not given, it is set to middle of LSL and USL

            Raise ValueError if there are invalid parameters.
            Invalid parameters are more then two limits in lims or
            nominal is outside the bilateral specifications.
            It will fix common spec errors such as incorrect LSL or USL.
        """
        if lims is not None and len(lims) == 2:
            lsl = lims[0]
            usl = lims[1]
        elif lims is None:  # with nominal only or no specs
            lsl = None
            usl = None
        else:  # len(lims) > 2 is illogical
            raise ValueError('invalid limits specifications')

        # init
        if lsl is not None and usl is not None:
            # fix confusion on limits
            self._lsl = lsl if lsl < usl else usl
            self._usl = usl if usl > lsl else lsl
            # bilateral specifications
            if nominal is None:
                self._nominal = (lsl+usl)/2.0
            else:
                self._nominal = nominal
                if nominal > self._usl:  # invalid specs
                    raise ValueError('nominal value not within LSL and USL')
        elif lsl is not None and usl is None:
            # unilateral specifications or single spec
            if nominal is None:
                self._nominal = math.nan
                self._lsl = lsl  # only have LSL
                self._usl = math.nan
            else:
                self._nominal = nominal
                # fix spec confusion
                if nominal > lsl:
                    self._lsl = lsl  # unilateral LSL
                    self._usl = math.nan
                else:
                    self._usl = lsl  # unilateral USL
                    self._lsl = math.nan
        elif lsl is None and usl is not None:
            # unilateral specifications or single spec
            if nominal is None:
                self._nominal = math.nan
                self._lsl = math.nan
                self._usl = usl  # only have USL
            else:
                self._nominal = nominal
                # fix spec confusion
                if nominal < usl:
                    self._lsl = math.nan
                    self._usl = usl  # unilateral USL
                else:
                    self._usl = math.nan
                    self._lsl = usl  # unilateral LSL
        else:  # nominal only without spec or no spec at all
            self._lsl = math.nan
            self._usl = math.nan
            self._nominal = nominal if nominal is not None else math.nan

    # don't allow to set these values to avoid complicated checking in init
    @property
    def lower_limit(self):
        return self._lsl

    @property
    def lsl(self):
        return self._lsl

    @property
    def upper_limit(self):
        return self._usl

    @property
    def usl(self):
        return self._usl

    @property
    def target(self):
        return self._nominal

    @property
    def nominal(self):
        return self._nominal

    def has_spec(self):
        if (math.isnan(self._lsl) and math.isnan(self._usl)
                and math.isnan(self._nominal)):
            return False
        else:
            return True

    def summary(self):
        print('Specifications:')
        print(f'  Lower limit (LSL): {self._lsl:.6f}')
        print(f'  Upper limit (USL): {self._usl:.6f}')
        print(f'  Nominal          : {self._nominal:.6f}')


class ParetoChart():
    """ Pareto Chart
    """
    # Default DataFrame column names for unlabelled and derived data
    def_defect_col = 'Defect'
    def_freq_col = 'Frequency'
    def_cum_freq_col = 'CumFreq'
    def_percent_col = 'Percentage'
    def_cum_percent_col = 'CumPercent'

    # only data and name of the chart. Other options in plot method
    def __init__(self, x=None, y=None, data=None, title=None):
        """ ParetoChart constructor

                x: list of str, tuple of str or pandas.Series of str
                    If x is defined then y must be too and of same length.
                    x contains the 'Defect' string descriptions
                y: list of int or float or tuple of int or float
                    or pandas.Series of values
                    x must be defined. y must be the same length as x and in
                    the same sequence.
                    y contains the 'Frequency' data. Can be counts or cost.
                data: pandas.DataFrame
                    Use DataFrame to define the data. Must have two columns.
                    First columns is the 'Defect' and the second column is
                    the 'Frequency'. DataFrame header row is optional.
                title: str
                    Pareto Chart Title. Default 'Pareto Chart of Defect'

        """
        # default cum ax scale
        self.cum_ylim = (0.0, 105.0)
        # default figure size
        self.fig_size_inches = (8.0, 6.0)  # w, h

        # default seaborn style
        self.seaborn_style = 'dark'

        if x is not None and y is not None:
            if isinstance(x, pd.Series):
                defect_se = x
            else:
                defect_se = pd.Series(x)
            if isinstance(y, pd.Series):
                frequency_se = y
            else:
                frequency_se = pd.Series(y)
        elif data is not None:
            if isinstance(data, pd.DataFrame):
                defect_se = data.iloc[0:, 0]
                frequency_se = data.iloc[0:, 1]
        else:
            raise Exception('x, y or data parameters are None.')

        # Original Pareto Chart title and column names
        # can be renamed.
        # _pareto_df column names
        if defect_se.name is None:
            self._defect_col = self.def_defect_col
        else:
            self._defect_col = defect_se.name
        if frequency_se.name is None:
            self._freq_col = self.def_freq_col
        else:
            self._freq_col = frequency_se.name
        # derived data columns
        self._cum_freq_col = self.def_cum_freq_col
        self._percent_col = self.def_percent_col
        self._cum_percent_col = self.def_cum_percent_col
        if title is None:
            self._chart_title = 'Pareto Chart of ' + self._defect_col
        else:
            self._chart_title = title

        pareto_dc = {self._defect_col: defect_se,
                     self._freq_col: frequency_se
                     }
        self._pareto_df = pd.DataFrame(pareto_dc)
        self._create_chart_data()

    def _create_chart_data(self):
        self._pareto_df.sort_values(by=self._freq_col, ascending=False,
                                    inplace=True)
        freq_se = self._pareto_df[self._freq_col]
        cum_freq_se = freq_se.cumsum()
        total = freq_se.sum()
        per_se = freq_se / total * 100.0
        cum_per_se = per_se.cumsum()
        # add calc data with their column names
        self._pareto_df = self._pareto_df.assign(
            **{self._cum_freq_col: cum_freq_se,
               self._percent_col: per_se,
               self._cum_percent_col: cum_per_se}
        )
        self._pareto_df.reset_index(drop=True, inplace=True)

    # Properties defined here to avoid renaming error.
    # chart_title is not part of the pandas DataFrame.
    @property
    def chart_title(self):
        """ Returns the Pareto Chart's Title
        """
        return self._chart_title

    @chart_title.setter
    def chart_title(self, new_name):
        """ Renames the Pareto Chart's Title

            new_name: str
                new title name, default name is 'Pareto Chart'
        """
        self._chart_title = new_name

    def rename_columns(self, defnam=None, freqnam=None,
                       cumfreqnam=None, pernam=None, cumpernam=None):
        """ Renames the Pareto Chart's pandas.DataFrame column names.
            The plotted labels of chart is set independently in
            plot the function.

            defnam: str
                new 'defect' column name
            freqnam: str
                new 'frequency' column name
            cumfreqnam: str
                new 'cumulative frequency' column name
            pernam: str
                new 'percentage' column name
            cumpernam: str
                new 'cumulative frequency percentage' column name
        """
        colnam_dc = {}
        if self._pareto_df is not None:
            if defnam is not None:
                colnam_dc[self._defect_col] = defnam
                self._defect_col = defnam
            if freqnam is not None:
                colnam_dc[self._freq_col] = freqnam
                self._freq_col = freqnam
            if cumfreqnam is not None:
                colnam_dc[self._cum_freq_col] = cumfreqnam
                self._cum_freq_col = cumfreqnam
            if pernam is not None:
                colnam_dc[self._percent_col] = pernam
                self._percent_col = pernam
            if cumpernam is not None:
                colnam_dc[self._cum_percent_col] = cumpernam
                self._cum_percent_col = cumpernam
            self._pareto_df.rename(index=int, columns=colnam_dc, inplace=True)

    def reset_col_names(self):
        """ Reset the Pareto Chart's pandas.DataFrame Column names to
            their default values.
        """
        self.rename_columns(self.def_defect_col, self.def_freq_col,
                            self.def_cum_freq_col, self.def_percent_col,
                            self.def_cum_percent_col)

    def chart_data(self):
        """ Returns the Pareto Chart Data as a pandas.DataFrame
        """
        return self._pareto_df

    def summary(self):
        """ Prints the Pareto Chart Data to terminal
        """
        print('\n{}'.format(self._chart_title))
        print(self._pareto_df)

    def plot(self, plot=True, peak=True, xlab=None, ylab=None,
             ylab2='Cumulative Percentage', line80=True):
        """ Plots the Pareto Chart

            return: matplotlib.pyplot.plt
        """
        sns.set_style(self.seaborn_style)
        # Set up the matplotlib figure
        fig1, ax1 = plt.subplots(sharex=True)
        ax2 = ax1.twinx()  # cum % axis
        ax1.yaxis.tick_left()  # freq axis
        # Set the ax1 scale to make the cum % line start
        # at the peak value.
        if peak is True:
            yf1 = self._pareto_df.loc[0, self._freq_col]
            yc1 = self._pareto_df.loc[0, self._cum_percent_col]
            yf2 = yf1 * self.cum_ylim[1] / yc1
            ax1.set(ylim=(0.0, yf2))
        ax2.yaxis.tick_right()
        ax2.set(ylim=self.cum_ylim)
        fig1.set_size_inches(self.fig_size_inches)
        sns.barplot(self._pareto_df[self._defect_col],
                    self._pareto_df[self._freq_col],
                    ax=ax1)
        sns.lineplot(self._pareto_df[self._defect_col],
                     self._pareto_df[self._cum_percent_col],
                     ax=ax2, marker='o', sort=False)
        # title can be set using chart_title
        ax1.set_title(self._chart_title, fontweight='bold')
        if xlab is not None:
            ax1.set_xlabel(xlab, fontweight='bold')
        else:
            ax1.set_xlabel(self._defect_col, fontweight='bold')
        if ylab is not None:
            ax1.set_ylabel(ylab, fontweight='bold')
        else:
            ax1.set_ylabel(self._freq_col, fontweight='bold')
        if line80 is True:  # show 80% line
            ax2.axhline(80.0, color='r', clip_on=False)
        # Allow user to specify a less technical label on chart
        if ylab2 is not None:  # default = 'Cumulative Percentage'
            ax2.set_ylabel(ylab2, fontweight='bold')
        else:  # technical label
            ax2.set_ylabel(self._cum_percent_col, fontweight='bold')
        # Most of the time the defect names are too long so rotate text
        plt.setp(ax1.get_xticklabels(), rotation=30,
                 horizontalalignment='right')
        ax2.yaxis.set_major_formatter(FuncFormatter('{:.0f}%'.format))
        plt.tight_layout()
        if plot is True:
            plt.show()
        return plt


class Histogram():
    """ Histogram synonymous with R's hist() function
    """

    def __init__(self, x=None, bins=None, title=None):
        """ Constructor for Histogram

            x: Pandas Series, tuple, list or numpy array in 1d
               Data to plot

            bins: argument for matplotlib hist(), or None, optional
                  Unlike R's hist() the bin edges are not set
                  to 'pretty' values. Uses numpy's histogram.
                  Default is 'fd' (Freedman Diaconis Estimator)

            title: str, optional
                  Chart title. Default is 'Histogram of x'
        """
        if isinstance(x, pd.Series):
            self._x = x
            if self._x.name is None:
                self._x.name = 'x'
        elif x is None:
            raise Exception('x parameter is None.')
        else:
            self._x = pd.Series(x, name='x')
        # plots cannot have nan values
        self._x.dropna(inplace=True)

        if title is None:
            self._chart_title = 'Histogram of ' + self._x.name
        else:
            self._chart_title = title
        # default figure size
        self.fig_size_inches = (8.0, 6.0)  # w, h
        if bins is None:
            # same as seaborn distplot default
            self._bins = 'fd'  # Freedman Diaconis Estimator
        else:
            self._bins = bins

        # default seaborn style
        self.seaborn_style = 'darkgrid'
        self._spec = None
        self._create_chart_data()

    def _create_chart_data(self):
        """ Generate the chart data similar to R's hist() function
        """
        # matplotlib uses numpy's hist to generate data for plotting
        # set seaborn distplot bins = self._breaks to avoid discrepancies
        # Use numpy's histogram to determine the bin edges same as
        # matplotlib histogram
        self._counts, self._breaks = np.histogram(self._x, bins=self._bins)

        widths = np.empty(len(self._counts))
        self._mids = np.empty(len(self._counts))
        last_edge = self._breaks[0]
        i = 0
        for edge in self._breaks[1:]:
            # Calculates the widths of the bars.
            # It may not be equidistant
            widths[i] = (edge - last_edge)
            # Calculates the mid value of the bar
            self._mids[i] = (edge + last_edge) / 2.0
            last_edge = edge
            i += 1
        # frequency density = f[i] / width[i] is not calculated here but
        # shown here for completeness. Use for widths that are not the same.
        # relative frequency, rf[i] = f[i]/n where n is the sample size
        # f[i] is frequency of ith bar. sum(rf[i]) = 1.0, all i
        # The following is the relative frequency density:
        # density[i] = rf[i] / width[i] where width[i] is ith bar's width
        # area under curve = sum(density[i] * width[i]) = 1.0, all i
        self._densities = (self._counts / self._counts.sum()) / widths

        # equidist
        self._equidist = True
        last_width = widths[0]
        for width in widths[1:]:
            if not math.isclose(last_width, width):
                self._equidist = False
                break

    @property
    def chart_title(self):
        """ Returns the Histogram's Title
        """
        return self._chart_title

    @chart_title.setter
    def chart_title(self, new_name):
        """ Renames the Histogram's Title

            new_name: str
                new title name, default name is 'Histogram'
        """
        self._chart_title = new_name

    @property
    def mean(self):
        """ Returns the mean of x """
        return self._x.mean()

    @property
    def median(self):
        """ Returns the median of x """
        return self._x.median()

    @property
    def stddev(self):
        """ Returns the sample standard deviation of x """
        return self._x.std()

    @property
    def xname(self):
        """ Returns the name of x """
        return self._x.name  # R hist() xname

    @property
    def counts(self):  # R hist() counts
        """ Returns the bin counts

        This is how the bin counts are determined.

        All but the last (righthand-most) bin is half-open for
        example the bins is:

            bins = [e1, e2, e3, e4] where e is the bin's edge value.

        first bin [e1, e2), count x if e1 <= x < e2 and
        the same goes for the second bin except for the last
        bin e3 <= x <= e4 which is same as R's hist(right = FALSE)

        No equivalent for 'right' parameter for numpy's histogram

        return: numpy array of bin counts
        """
        return self._counts

    @property
    def breaks(self):  # R hist() breaks
        """ Returns the histogram's bin breaks

            return: numpy array
        """

        return self._breaks

    @property
    def densities(self):
        """ Returns the histogram's densities

            relative frequency rf = f/n
                where f = frequency and n = sample size.

            density d = rf/w where w is bin width.

            area under curve = sum(d*w) = 1.0, bins widths must be equal

            return: numpy array containing density
        """
        return self._densities

    @property
    def mids(self):
        """ Returns the bar's mid-value

            return: numpy array
        """
        return self._mids

    @property
    def equidist(self):
        """ Returns the whether all the bin widths are equal

            return: bool
                True if all bin widths are equidistant
        """
        return self._equidist

    def summary(self):
        """ Prints the Histogram's Data to terminal
        """
        print('\n{}'.format(self._chart_title))
        print('x variable name   : {}'.format(self.xname))
        print('sample size       : {}'.format(len(self._x)))
        print('mean              : {0:.4f}'.format(self.mean))
        print('sample std. dev.  : {0:.4f}'.format(self.stddev))
        print('median            : {0:.4f}'.format(self.median))
        print('equidistant       : {}'.format(self._equidist))
        print('\nbreaks: ')
        print(self._breaks)
        print('\nmids: ')
        print(self._mids)
        print('\ncounts: ')
        print(self._counts)
        print('\nDensities: ')
        print(self._densities)
        if self._spec is not None:
            self._spec.report()

    def set_spec(self, spec_lims=None, target=None, spec=None):
        """ Sets the specification to be displayed on the Histogram.
            Default is no specification shown on Histogram

        Parameters
        ----------
        lims: tuple specification limits like (LSL, USL) e.g (3.5, 6.5)
            If there are no LSL or USL put None in its place
            e.g. (None, 8.0)
            LSL is the lower spec limit. USL is the upper spec limit.

        target: float, optional
            default is None.
            If not given, it is set to middle of LSL and USL
        spec: emodapi.Spec
            default is None. If present it will overide lims and target.
        """
        if spec is None:
            self._spec = Spec(spec_lims, target)
        else:
            self._spec = spec

    def plot(self, plot=True, kde=False, labels=False, **kwargs):
        """ Plots the Histogram

            Parameters
            ---------
            plot: bool, default is True. Optional.

            kde: bool, default is False. Optional.
                Whether to plot a gaussian kernel density estimate

            labels: bool, default is False. Optional.
                Draw labels on top of bars if True.

            kwargs: keyword arguments to pass to seaborn distplot, optional
                    fit = 'norm' is supported and is same as
                    fit = scipy.stats.norm otherwise supply a random variable
                    object as required by seaborn distplot.

            Return
            ------
            matplotlib.pyplot.plt

            Example
            -------
            >>> hc.plot(fit='norm', kde=True, rug=True)
            plots the histogram with normal distribution, kde and rug plots
        """
        sns.set_style(self.seaborn_style)
        # Set up the matplotlib figure
        fig1, ax1 = plt.subplots()
        fig1.set_size_inches(self.fig_size_inches)

        freq = True  # flag for freq or density plot
        if self._equidist is False:  # to check this
            freq = False
            kwargs['hist'] = False

        fit_value = kwargs.get('fit')
        if fit_value == 'norm':
            # replace fit value with random variable object norm
            kwargs['fit'] = stats.norm  # fit a normal dist curve
            freq = False
        elif fit_value is not None:  # some other fit function
            freq = False

        vert_value = kwargs.get('vertical')
        if freq is True and kde is False:
            if vert_value is True:
                ax1.set_xlabel('Frequency', fontweight='bold')
                ax1.set_ylabel(self._x.name, fontweight='bold')
            else:
                ax1.set_ylabel('Frequency', fontweight='bold')
                ax1.set_xlabel(self._x.name, fontweight='bold')
        else:
            if vert_value is True:  # maybe kde or norm
                ax1.set_xlabel('Density', fontweight='bold')
                ax1.set_ylabel(self._x.name, fontweight='bold')
            else:
                ax1.set_ylabel('Density', fontweight='bold')
                ax1.set_xlabel(self._x.name, fontweight='bold')
        # Use bins=self._breaks to avoid discrepancies between
        # chart data and the actual plot by seaborn
        sns.distplot(self._x, bins=self._breaks, ax=ax1, kde=kde, **kwargs)
        # spec plotting
        if self._spec is not None:
            pad_t = 20  # set higher to make way for spec labels
            _, top_y = plt.ylim()
            if self._spec.has_spec():
                val = self._spec.lower_limit()
                if not math.isnan(val):
                    ax1.axvline(val, color='r', ls='--', clip_on=False)
                    txt = 'LSL({})'.format(val)
                    ax1.text(val, top_y, txt, verticalalignment='bottom',
                             horizontalalignment='center', color='r'
                             )
                val = self._spec.upper_limit()
                if not math.isnan(val):
                    ax1.axvline(val, color='r', ls='--', clip_on=False)
                    txt = 'USL({})'.format(val)
                    ax1.text(val, top_y, txt, verticalalignment='bottom',
                             horizontalalignment='center', color='r'
                             )
                val = self._spec.target()
                if not math.isnan(val):
                    ax1.axvline(val, color='r', ls='--', clip_on=False)
                    txt = 'Target({})'.format(val)
                    ax1.text(val, top_y, txt, verticalalignment='bottom',
                             horizontalalignment='center', color='r'
                             )
        else:
            pad_t = None  # default for no spec

        # draw labels on top of bars
        if labels is True:
            if freq is True and kde is False:
                coords = zip(self._mids, self._counts)
                strf = '{}'
            else:
                coords = zip(self._mids, self._densities)
                strf = '{:1.3f}'
            for lx, ly in coords:
                ax1.annotate(strf.format(ly),
                             xy=(lx, ly),
                             xytext=(0, 2),  # 2 points vertical offset
                             textcoords="offset points",
                             ha='center', va='bottom')
        ax1.set_title(self._chart_title, pad=pad_t, fontweight='bold')
        plt.tight_layout()
        if plot is True:
            plt.show()
        return plt


class ProcessCapability():

    def __init__(self, chart, spec) -> None:
        self._chart = chart
        self._spec = spec

        # KISS - avoid getter and setter functions
        # Process Performance (Overall)
        self.pp = ((self._spec.upper_limit - self._spec.lower_limit) /
                   (6 * self._chart.overall_std_dev))

        self.ppu = ((self._spec.upper_limit - self._chart.proc_mean) /
                    (3 * self._chart.overall_std_dev))

        self.ppl = ((self._chart.proc_mean - self._spec.lower_limit) /
                    (3 * self._chart.overall_std_dev))
        self.ppk = min((self.ppu, self.ppl))

        # Process Capability (Within)
        self.cp = ((self._spec.upper_limit - self._spec.lower_limit) /
                   (6 * self._chart.within_std_dev))

        self.cpu = ((self._spec.upper_limit - self._chart.proc_mean) /
                    (3 * self._chart.within_std_dev))

        self.cpl = ((self._chart.proc_mean - self._spec.lower_limit) /
                    (3 * self._chart.within_std_dev))
        self.cpk = min((self.cpu, self.cpl))

    def summary(self):
        print("Specifications:")
        print(f"  Lower Spec Limit(LSL)          = {self._spec.lsl}")
        print(f"  Upper Spec Limit(USL)          = {self._spec.usl}")
        # Similar terms of using overall and within capability to minitab
        print("Process Performance (Overall):")
        print(f"  Process Performance(Pp)        = {self.pp:.2f}")
        print(f"  Process Perf. Index Lower(PPL) = {self.ppl:.2f}")
        print(f"  Process Perf. Index Upper(PPU) = {self.ppu:.2f}")
        print(f"  Process Performance Index(Ppk) = {self.ppk:.2f}")
        print("Process Capability (Within):")
        print(f"  Process Capability(Cp)         = {self.cp:.2f}")
        print(f"  Process Capa. Index Lower(CPL) = {self.cpl:.2f}")
        print(f"  Process Capa. Index Upper(CPU) = {self.cpu:.2f}")
        print(f"  Process Capability Index (Cpk) = {self.cpk:.2f}")
