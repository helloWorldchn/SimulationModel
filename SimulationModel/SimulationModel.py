from Compensation import Compensation
from FreeFall import FreeFall
from FrequencyDomain import FrequencyDomain
from DCMotor import DCMotor
from MassSpringDamper import MassSpringDamper
from OneInvertedPendulum import OneInvertedPendulum
from RootLocus import RootLocus
from TimeDomainAnalysis import TimeDomainAnalysis

if __name__ == '__main__':
    flag = 4
    if flag == 0:
        FreeFall(g=9.81, t_max=10, dt=0.1).freeFall()
    elif flag == 1:
        rise_time, peak_time, overshoot, settling_time, dampingRatio, naturalFrequency = TimeDomainAnalysis("25", "1 6 25").timeDomainAnalysis()
    elif flag == 2:
        RootLocus("1", "1 3 2 0", 10).rootLocus()
    elif flag == 3:
        gm, pm, wcg, wcp = FrequencyDomain("10", "1 6 5 0").frequencyDomain()
    elif flag == 4:
        flag2 = 1
        if flag2 == 1:
            Compensation("100", "0.001 0.11 1 0", "20").leadCompensation()
        else:
            Compensation("300", "0.2 1 0", "40").lagCompensation()
    elif flag == 5:
        MassSpringDamper("1.0", "2.0", "1").massSpringDamper()
    elif flag == 6:
        DCMotor("1.0" "0.1" "0.5" "0.5" "0.01" "0.01"  "1" "0.8" "0.01" "10" "0.01" "2000").dcMotor()
    elif flag == 7:
        OneInvertedPendulum("1.5" "0.25" "0.24" "0.1" "9.81" "100" "10" "10" "60" "0.01").oneInvertedPendulum()
