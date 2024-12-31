from FreeFall import FreeFall
from TimeDomainAnalysis import TimeDomainAnalysis

if __name__ == '__main__':
    FreeFall(g=9.81,t_max = 10,dt = 0.1).freeFall()
    TimeDomainAnalysis(1, 6, 25).timeDomainAnalysis()