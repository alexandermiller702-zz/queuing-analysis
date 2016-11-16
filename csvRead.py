# find the number of c=servers
import csv, numpy
import matplotlib.pyplot as p

def done(fName = 'rawData.csv'):
    # list of call received times
    Rec = []
    # interarrival times = received 2 - received 1
    IAtimes = []
    # call answered times
    Ans = []
    # service completion times
    Comp = []
    # Service time = Completion time - answer time
    Serve = []

    with open(fName) as data:
        imp = csv.DictReader(data)
        for line in imp:
            # Received time, split and converted into seconds after 5PM
            Rec.append((int)(line['Received time']))
            # Answer times ?less automated message??
            Ans.append((int)(line['Answer seconds']))
            # Completion times
            Comp.append((int)(line['Completion seconds']))
            # Service time
            Serve.append((int)(line['Service time']))
            IAtimes.append((int)(line['Interarrival time']))
    return [Rec, Ans, Comp, Serve, IAtimes]


def dat(fName = "d.csv", oName = "rawData.csv", write = False):
    # list of call received times
    Rec = []
    # interarrival times = received 2 - received 1
    IAtimes = []
    # call answered times
    Ans = []
    # service completion times
    Comp = []
    # Service time = Completion time - answer time
    Serve = []

    with open(fName) as data:
        imp = csv.DictReader(data)
        for line in imp:
            # Received time, split and converted into seconds after 5PM
            Rec.append(timesplit(line['Call Received']))
            # Answer times ?less automated message??
            rawANS = (int) (line['Call Answered'])
            Ans.append(rawANS)
            # Completion times
            rawCOM = (int) (line['Call Completed'])
            Comp.append(rawCOM)
            # Service time
            s = rawCOM - rawANS
            Serve.append(s)
        IAtimes = interarrivaltimes(Rec)

    if write:
        with open(oName, 'w') as out:
            writ = csv.writer(out)
            # add headers
            writ.writerow(['Received time', 'Answer seconds', 'Completion seconds', 'Service time', 'Interarrival time'])
            # make data a matrix
            rows = zip(Rec, Ans, Comp, Serve, IAtimes)
            writ.writerows(rows)
    return [Rec, Ans, Comp, Serve, IAtimes]

def timesplit(time):
    """Converts a list of H:MM:SS PM times to seconds"""
    # split time into components
    split = time.split(':')
    # get the seconds from the last string
    split[2] = split[2][0:2]
    # Convert into seconds after 5 pm
    secspast = (int(split[0]) - 5) * 3600 + int(split[1]) * 60 + int(split[2])
    return secspast

def interarrivaltimes(L):
    """takes the list of arrival times and creates a list of inter arrival times"""
    # need a starting character to equalise lengths for csvWriting
    res = [0,]
    for call in range(1,len(L)):
        res.append(L[call]-L[call-1])
    return res


def IAgraph():
    d = done()
    p.clf()
    p.hold(True)
    x = d[0]
    y = ave(d[4])
    ymean = y[0]
    ystd = y[1]
    p.plot(x, ymean,'b')
    p.plot(x,ystd, 'g')
    p.title('Inter-arrival time rolling average and rolling standard deviation')
    p.xlabel("Time past 5")
    p.ylabel("InterArrival Time")
    p.axis("tight")
    p.savefig("IArollingAVERAGE.png")
    # pl.show()

def Sergraph():
    d = done()
    p.clf()
    p.hold(True)
    x = d[0]
    y = ave(d[3])
    ymean = y[0]
    ystd = y[1]
    p.plot(x, ymean,'b')
    p.plot(x, ystd, 'g')
    p.title('Service time rolling average and rolling standard deviation')
    p.xlabel("Time past 5")
    p.ylabel("Service Time")
    p.axis("tight")
    p.savefig("SERrollingAVERAGE.png")
    # pl.show()

def ave(L):
    """creates a list of len(L) rolling averages"""
    rStd = []
    rAve = []
    temp = []
    for i in range(len(L)):
        if len(temp)<50:
            temp.append(L[i])
        else:
            temp = shuffle(temp, L[i])
        rStd.append(numpy.std(temp))
        rAve.append(numpy.mean(temp))
    return [rAve,rStd]


def shuffle(L, item):
    """takes a list and adds an item to the top of it"""
    new = [item,]
    for i in range(len(L)-2):
        new.append(L[i])
    return new
