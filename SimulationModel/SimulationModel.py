from FreeFall import FreeFall
from RootLocus import RootLocus
from FrequencyDomain import FrequencyDomain
from TimeDomainAnalysis import TimeDomainAnalysis
from Compensation import Compensation

if __name__ == '__main__':
    flag = 4
    flag2 = 1
    if flag == 0:
        FreeFall(g=9.81, t_max=10, dt=0.1).freeFall()
    elif flag == 1:
        rise_time, peak_time, overshoot, settling_time, dampingRatio, naturalFrequency = TimeDomainAnalysis("25",
                                                                                                            "1 6 25").timeDomainAnalysis()
    elif flag == 2:
        RootLocus("1", "1 3 2 0", 10).rootLocus()
    elif flag == 3:
        gm, pm, wcg, wcp = FrequencyDomain("10", "1 6 5 0").frequencyDomain()
    elif flag == 4:
        if flag2 == 1:
            Compensation("100", "0.001 0.11 1 0", "20").leadCompensation()
        else:
            Compensation("300", "0.2 1 0", "40").lagCompensation()
