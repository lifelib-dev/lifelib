import numpy as np
from scipy.optimize import minimize

def NelsonSiegelSvansson(T, beta0, beta1, beta2, beta3, lambda0, lambda1):
    # NelsonSiegelSvansson calculates the interpolated/extrapolated curve at points in the array "T" using the Nelson-Siegel-Svannson algorithm,
    # parameterized with parameters beta0, beta1, beta2, beta3, lambda0, lambda1. It returns a numpy ndarray of points.
    # 
    # Arguments:
    #    T =       n x 1 ndarray of maturities for which the user wants to calculate the coresponding rate
    #    beta0 =   1 x 1 floating number, representing the first factor of the NSS parametrisation  
    #    beta1 =   1 x 1 floating number, representing the second factor of the NSS parametrisation 
    #    beta2 =   1 x 1 floating number, representing the third factor of the NSS parametrisation
    #    beta3 =   1 x 1 floating number, representing the fourth factor of the NSS parametrisation
    #    lambda0 = 1 x 1 floating number, representing the first shape parameter lambda of the NSS parametrisation
    #    lambda1 = 1 x 1 floating number, representing the second shape parameter lambda of the NSS parametrisation 
    # 
    # Returns:
    #     n x 1 ndarray of interpolated/extrapolarted points coresponding to maturities inside T. Where n is the length of the vector T.
    # 
    #     LINK TO SOURCE
    alpha1 = (1-np.exp(-T/lambda0)) / (T/lambda0)
    alpha2 = alpha1 - np.exp(-T/lambda0)
    alpha3 = (1-np.exp(-T/lambda1)) / (T/lambda1) - np.exp(-T/lambda1)

    return beta0 + beta1*alpha1 + beta2*alpha2 + beta3*alpha3

def NSSGoodFit(params, TimeVec, YieldVec):
    # NSSGoodFit calculates the residuals between the yield predicted by the NSS algorithm with the specified parameterisation and the market observed ones.
    #
    # Arguments:
    #    params =   6 x 1 tuple containing the 6 parameters of the NSS algorithm. The sequence of parameters needs to be (beta0, ..., beta4, lambda0, lambda1)
    #    TimeVec =  n x 1 ndarray of maturities for which the yields in YieldVec were observed
    #    YieldVec = n x 1 ndarray of observed yields 
    # Returns:
    #     1 x 1 float number Euclidian distance between the calculated points and observed data 
    #
    # LINK TO SOURCE

    return np.sum((NelsonSiegelSvansson(TimeVec, params[0], params[1], params[2], params[3], params[4], params[5])-YieldVec)**2)

def NSSMinimize(beta0, beta1, beta2, beta3, lambda0, lambda1, TimeVec, YieldVec):
    # NSSMinimize uses the built in minimize function from the python's scipy package. The function sets up the parameters and the function NSSGoodFit as to make it
    # compatible with the way minimize requires its arguments. If the optimization does not converge, the output is an empty array.  
    #
    # Arguments:
    #    beta0 =   1 x 1 floating number, representing the first factor of the NSS parametrisation  
    #    beta1 =   1 x 1 floating number, representing the second factor of the NSS parametrisation 
    #    beta2 =   1 x 1 floating number, representing the third factor of the NSS parametrisation
    #    beta3 =   1 x 1 floating number, representing the fourth factor of the NSS parametrisation
    #    lambda0 = 1 x 1 floating number, representing the first shape parameter lambda of the NSS parametrisation
    #    lambda1 = 1 x 1 floating number, representing the second shape parameter lambda of the NSS parametrisation 
    #    TimeVec =  n x 1 ndarray of maturities for which the yields in YieldVec were observed
    #    YieldVec = n x 1 ndarray of observed yields 
    # 
    # Returns:
    #     6 x 1 array of parameters and factors, that best fit the observed yields(Or an empty array if the optimization was not successfull).
    #
    # https://docs.scipy.org/doc/scipy/reference/optimize.minimize-neldermead.html
    # https://en.wikipedia.org/wiki/Nelder%E2%80%93Mead_method


    opt_sol = minimize(NSSGoodFit, x0=np.array([beta0, beta1, beta2, beta3, lambda0, lambda1]), args = (TimeVec, YieldVec), method="Nelder-Mead")
    if (opt_sol.success):
        return opt_sol.x
    else:
        return []
























