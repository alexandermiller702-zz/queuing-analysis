import numpy as np
import scipy.stats as ss
import matplotlib.pyplot as plt
import csv

""" data analysis with chi-square goodness of fit"""

def obs_cts(n, data):
    """ given: the data and number of bins
        returns: the observed values and the bin edges as lists"""
    events, edges = np.histogram(data, n)
    return events.tolist() , edges.tolist()

def exp_cts(n, data):
    """ given: the data and number of bins
        returns: the expected values and prob over each of the bins with
        the necessary modification of the first and last bins"""
    L=[]
    P_bins =[]
    for x in obs_cts(n,data)[1]:
        L.append(rv.cdf(x))
    P_bins.append(L[1])    
    for i in range(1,len(L)-2):
        P_bins.append(L[i+1]-L[i])    
    P_bins.append(1-L[-2])
    exp_cnt = [x * len(data) for x in P_bins]
    return exp_cnt, P_bins

def ind_bins_to_reduce(f_exp):
    """ given: a list
        returns: the indexes of the elements < 5"""
    NC_to_red =[index for index,value in enumerate(f_exp) if value < 5]
    return NC_to_red

def one_reduce(f_exp, f_obs, f_edge):
    """ given: lists of exp, obs, edges
        returns: new lists with one reduced bin with value < 5 """
    BTR = ind_bins_to_reduce(f_exp)
  
    if (len(BTR)>1 or (len(BTR)==1 and BTR[0]!=0)):
        f_exp[BTR[-1]-1] = f_exp[BTR[-1]-1]+f_exp[BTR[-1]]
        f_obs[BTR[-1]-1] = f_obs[BTR[-1]-1]+f_obs[BTR[-1]]
        del(f_edge[BTR[-1]])
        del(f_obs[BTR[-1]])
        del(f_exp[BTR[-1]])
    else:
        if BTR[0]==0:
            f_exp[1]= f_exp[1]+f_exp[0]
            f_obs[1]= f_obs[1]+f_obs[0]
            del(f_edge[1])
            del(f_obs[0])
            del(f_exp[0])

    f_expN = f_exp
    f_obsN = f_obs
    f_edgeN = f_edge
    BTRN = ind_bins_to_reduce(f_expN)
    return f_expN, f_obsN, f_edgeN, BTRN

def all_reduce(f_expF, f_obsF, f_edgeF, BTRF):
    """ finalizes the bin reduction """
    while BTRF !=[]:
        u = one_reduce(f_expF, f_obsF, f_edgeF)
        f_expF = u[0]
        f_obsF = u[1]
        f_edgeF = u[2]
        BTRF = u[3]
    return f_expF, f_obsF, f_edgeF, BTRF


def model(data, n, dof):
        """ given data, the number of bins (n) and the number of estimated parameters (dof)
        produces the value of the chi-squate test statistics and the p-value"""

        ## final expected count and final observed count after amalgamating bins
        exp, obs = all_reduce(exp_cts(n, data)[0],obs_cts(n, data)[0],
                obs_cts(n, data)[1], ind_bins_to_reduce(exp_cts(n, data)[0]))[0:2] 

        # build in chi-gof test, the last argument is the adjustment to the dof
        result = ss.chisquare( np.asarray(obs), np.asarray(exp), dof) 
        return result 


if __name__ == "__main__":

    ## experiment data --------------------------------------------------------------
    import csvRead
    #generate data or read your raw data - for this example the data are iid gamma
    np.random.seed(seed=1234)
    alpha = 1
    loc = 0
    beta = 3.574
    data = csvRead.done("finalData.csv")[4]#ss.gamma.rvs(alpha, loc=loc, scale=beta, size=100000)

    for i in range(len(data)):
        data[i] = data[i] + 0.00001
    #parameter estimation (in ss.gamma EX=alpha*beta, V(X)= alpha*beta*beta)!!!!
    fit_alpha, fit_loc, fit_beta = ss.gamma.fit(data, floc=0)
    rv = ss.gamma(fit_alpha, fit_loc, fit_beta)
    print "The parameters estimations are: alpha=%9.6f, loc(always)=%2d, beta=%9.6f "%(fit_alpha, fit_loc, fit_beta)
    

    # set the adjustment to dof (degree of freedom) = to the number of parameters estimated
    dof = 1

    # chose the number of bins
    n=30

##  experiment--------------------------------------------------
    
print "The IA chi_sq test value is %10.6f and the p-value is %10.6f" % (model(data, n, dof)[0], model(data,n,dof)[1])




