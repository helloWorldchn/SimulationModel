from FreeFall import FreeFall
from RootLocus import RootLocus
from FrequencyDomain import FrequencyDomain
from TimeDomainAnalysis import TimeDomainAnalysis

if __name__ == '__main__':
    flag = 3
    if flag == 0:
        FreeFall(g=9.81, t_max=10, dt=0.1).freeFall()
    elif flag == 1:
        TimeDomainAnalysis("25", "1 6 25").timeDomainAnalysis()
    elif flag == 2:
        RootLocus("1", "1 3 2 0", 10).rootLocus()
    elif flag == 3:
        FrequencyDomain("10", "1 6 5 0").frequencyDomain()
