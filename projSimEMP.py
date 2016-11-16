import csv
import math, random, numpy
from SimPy.Simulation import *

def readDens(fName):
    #read csv file
    dens = []
    val = []
    with open(fName) as data:
        imp = csv.DictReader(data)
        for line in imp:
            val.append(float(line['V']))
            dens.append(int(line['V2']))
    # return array of density
    return [dens,val]

def dist(fname):
    # build dist function
    dis = readDens(fname)
    for i in range(len(dis[0])):
        dis[0][i] = (dis[0][i]*1.0)/dis[0][len(dis[0])-1]
    return dis


ia = dist("IAout.csv")
ser = dist("Sout.csv")

#print ia,ser
# sim using table look up

#conf
def conf(L):
    """generates 95% confidence interval for a list"""
    lower = numpy.mean(L) - 1.96 * numpy.std(L) / math.sqrt(len(L))
    upper = numpy.mean(L) + 1.96 * numpy.std(L) / math.sqrt(len(L))
    return (round(lower,3), round(upper,3))

#table
def time(L):
    v = random.random()
    for i in range(len(L[1])):
        if L[0][i]>v:
            numer = (L[0][i])-v
            denom = L[0][i]-L[0][i-1]
            m = L[1][i]-L[1][i-1]
            c = L[1][i]
            result = m * numer/denom + c
            return result


#Source
class Source(Process):
    def run(self, N):
        for i in range(N):
            a = call(str(i))
            activate(a, a.run())
            t = time(ia)
            yield hold, self, t
#Task
class call(Process):
    """Dictates arrival behaviour to the system"""
    n = 0.0

    def run(self):
        call.n += 1
        atime = now()
        G.nuMon.observe(call.n)

        if (call.n>0):
            G.busMon.observe(1)
        else:
            G.busMon.observe(0)

        yield request, self, G.server
        t = time(ser)
        yield hold, self, t
        yield release, self, G.server
        call.n -= 1
        G.nuMon.observe(call.n)

        if (call.n > 0):
            G.busMon.observe(1)
        else:
            G.busMon.observe(0)

        d = now() - atime
        G.Dmon.observe(d)

#System
def G():
    server = 'Resource'
    Dmon = "delay monitor"
    nuMon = "capacity monitor"
    busMon = 'Monitor'

#model
def model(r,N, seed, runtime):
    initialize()
    random.seed(seed)

    G.server = Resource(r,monitored = True)
    G.Dmon = Monitor()
    G.nuMon = Monitor()
    G.busMon = Monitor()

    s = Source('Source')
    activate(s, s.run(N))
    simulate(runtime)

    # performance
    L = G.nuMon.timeAverage()
    LQ = G.server.waitMon.timeAverage()
    W = G.Dmon.mean()
    leff = L *1.0 / W
    WQ = G.server.waitMon.timeAverage() / leff
    B = G.busMon.timeAverage()


    return [L, LQ, W, WQ, leff,B]

#experiment
L = []
LQ = []
W = []
WQ = []
LE = []
B = []

for i in range(2,6):
    allL = []
    allLQ = []
    allW = []
    allWQ = []
    allLe = []
    allB = []

    for k in range(50):
        s = 123*k
        result = model(i,10000, s, 2000000)
        allL.append(result[0])
        allLQ.append(result[1])
        allW.append(result[2])
        allWQ.append(result[3])
        allLe.append(result[4])
        allB.append(result[5])

    print "Servers = ",i
    print "L: ",round(numpy.mean(allL),3), conf(allL)
    print "Lq: ",round(numpy.mean(allLQ),3), conf(allLQ)
    print "W: ",round(numpy.mean(allW),3),conf(allW)
    print "Wq: ",round(numpy.mean(allWQ),3), conf(allWQ)
    print "LamEf: ",round(numpy.mean(allLe),3), conf(allLe)
    print "B: ",round(numpy.mean(allB),3), conf(allB)

# Servers =  2
# L:  3.503 (3.463, 3.543)
# Lq:  1.218 (1.185, 1.252)
# W:  59.25 (58.667, 59.834)
# Wq:  20.602 (20.059, 21.144)
# LamEf:  0.059 (0.059, 0.059)
# B:  0.936 (0.935, 0.937)

# Servers =  3
# L:  3.503 (3.463, 3.543)
# Lq:  1.218 (1.185, 1.252)
# W:  59.25 (58.667, 59.834)
# Wq:  20.602 (20.059, 21.144)
# LamEf:  0.059 (0.059, 0.059)
# B:  0.936 (0.935, 0.937)

# Servers =  4
# L:  3.503 (3.463, 3.543)
# Lq:  1.218 (1.185, 1.252)
# W:  59.25 (58.667, 59.834)
# Wq:  20.602 (20.059, 21.144)
# LamEf:  0.059 (0.059, 0.059)
# B:  0.936 (0.935, 0.937)

# Servers =  5
# L:  3.503 (3.463, 3.543)
# Lq:  1.218 (1.185, 1.252)
# W:  59.25 (58.667, 59.834)
# Wq:  20.602 (20.059, 21.144)
# LamEf:  0.059 (0.059, 0.059)
# B:  0.936 (0.935, 0.937)
