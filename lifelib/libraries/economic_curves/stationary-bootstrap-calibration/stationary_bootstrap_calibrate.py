import numpy as np


def OptimalLength(data: np.ndarray):
    """
    Function calculates the optimal parameter value when using a stationary bootstraping algorithm.
    The method is based on the 2004 paper by Politis & White:
    Dimitris N. Politis & Halbert White (2004) Automatic Block-Length Selection for the Dependent Bootstrap, Econometric Reviews, 
    23:1, 53-70, DOI: 10.1081/ETC-120028836

    The code was modified compared to Patton's implementation in that it takes as input a one dimensional time-series 
    and returns the optimalblock size only for the stationary bootstrap algorithm.
    
    Warning! The minimal size of the time series is 9 elements.

    Example of use:
    >>> import numpy as np
    >>> data = np.array([0.4,0.2,0.1,0.4,0.3,0.1,0.3,0.4,0.2,0.5,0.1,0.2])
    >>> OptimalLength(data)
      Out[0]:  4.0
    Args:
       data ... ndarray array containing the time-series that we wish to bootstrap. 
           Ex. np.array([-1,0.2,0.3,0.7,0.5,0.1,0.4,0.3,0.5])
    Returns:
       Bstar ... optimal value of the parameter m Ex. 1

    Original Matlab version written by:
    James P. LeSage, Dept of Economics
    University of Toledo
    2801 W. Bancroft St,
    Toledo, OH 43606
    jpl@jpl.econ.utoledo.edu

    This Python implementation is based on Andrew J. Patton's Matlab code avalible at:
    http://public.econ.duke.edu/~ap172/

    Implemented by Gregor Fabjan from Qnity Consultants on 12/11/2021.
    """
    n = data.shape[0]
    kn = max(5,np.sqrt(np.log10(n)))
    mmax = int(np.ceil(np.sqrt(n))+kn)
    bmax = np.ceil(min(3*np.sqrt(n),n/3))
    c = 2

    temp = mlag(data,mmax)
    temp = np.delete(temp,range(mmax),0)
    corcoef= np.zeros(mmax)
    for iCor in range(0,mmax):
       corcoef[iCor] = np.corrcoef(data[mmax:len(data)],temp[:,iCor])[0,1] 

    temp2 =np.transpose(mlag(corcoef,kn))
    temp3 = np.zeros((kn,corcoef.shape[0]+1-kn))

    for iRow in range(kn):
        temp3[iRow,:] = np.append(temp2[iRow,kn:corcoef.shape[0]],corcoef[len(corcoef)-kn+iRow-1])

    treshold = abs(temp3) < (c* np.sqrt(np.log10(n)/n)) #Test if coeff bigger than triger
    treshold = np.sum(treshold,axis = 0 )

    count = 0 
    mhat = None
    for x in treshold:
        if (x==kn):
            mhat = count
            break    
        count +=1

    if (mhat is None):
    # largest lag that is still significant
        seccrit = corcoef >(c* np.sqrt(np.log10(n)/n))
        for iLag in range(seccrit.shape[0]-1,0,-1):
            if (seccrit[iLag]):
                mhat = iLag+1
                break
    if(mhat is None):
        M = 0
    elif (2*mhat > mmax):
        M = mmax
    else:
        M = 2*mhat

    # Computing the inputs to the function for Bstar
    kk = np.arange(-M, M+1, 1)

    if (M>0):
        temp = mlag(data,M)
        temp = np.delete(temp,range(M),0)
        temp2 = np.zeros((temp.shape[0],temp.shape[1]+1))
        for iRow in range(len(data)-M):
            temp2[iRow,:] = np.hstack((data[M+iRow],temp[iRow,:]))

        temp2 = np.transpose(temp2)
        temp3 = np.cov(temp2)
        acv = temp3[:,0]

        acv2 = np.zeros((len(acv)-1,2))
        acv2[:,0] = np.transpose(-np.linspace(1,M,M))
        acv2[:,1] = acv[1:len(acv)]

        if acv2.shape[0]>1:
            acv2 =acv2[::-1] 

        acv3 = np.zeros((acv2.shape[0]+acv.shape[0],1))
        Counter = 0
        for iEl in range(acv2.shape[0]):
            acv3[Counter,0] = acv2[iEl,1]
            Counter +=1
        for iEl in range(acv.shape[0]):
            acv3[Counter,0] = acv[iEl]
            Counter +=1

        Ghat = 0
        DSBhat = 0
        LamTemp =lam(kk/M)

        for iHat in range(acv3.shape[0]):
            Ghat += LamTemp[iHat]* np.absolute(kk[iHat])*acv3[iHat,0]
            DSBhat +=  LamTemp[iHat]*acv3[iHat,0]
        DSBhat = 2* np.square(DSBhat)

        Bstar = np.power(2*np.square(Ghat)/DSBhat,1/3)*np.power(n,1/3)

        if Bstar>bmax:
            Bstar = bmax
    else:
        Bstar = 1
    return Bstar


def mlag(x: np.ndarray,n)-> np.ndarray:
    """
    Returns a numpy array in which the k-th column is the series x pushed down (lagged) by k places.
    
    Example of use
     >>> import numpy as np
     >>> x = np.array([1,2,3,4])
     >>> n = 2
     >>> mlag(x,n)
      Out[0]:  array([[0, 0],
                      [1, 0],
                      [2, 1],
                      [3, 2]])   
   The function was tested passing a numpy array (ndarray) as input and requires numpy to run.
   Args:
       x ... ndarray array for which the lagged matrix is calculated. np.array([1,2,3,4])
       n ... integer specifying how many lags does the function consider
    Returns:
        xlag... ndarray contining the k-th lagged values in the k-th column of the matrix

    Original Matlab version written by:
    James P. LeSage, Dept of Economics
    University of Toledo
    2801 W. Bancroft St,
    Toledo, OH 43606
    jpl@jpl.econ.utoledo.edu

    This Python implementation is based on Andrew J. Patton's Matlab code avalible at:
    http://public.econ.duke.edu/~ap172/
    
    Implemented by Gregor Fabjan from Qnity Consultants on 12/11/2021
    """
    nobs = x.shape[0]
    out = np.zeros((nobs,n))
    for iLag in range(1,n+1):
        for iCol in range(nobs-iLag):
            out[iCol+iLag,iLag-1] = x[iCol];
    return out


def lam(x: np.ndarray)-> np.ndarray:
    """
    Returns the value at points x of the Trapezoidal function. Trapezoidal funcion maps all numbers bigger than 1 or smaller than -1 to zero.
    Values between -1/2 to 1/2 to 1 and the rest either on the line connecting (-1,0) to (-1/2,1) or (1/2,1) to (1,0).

    Example of use:
    >>> import numpy as np
    >>> x = np.array([0.55])
    >>> lam(x)
      Out[0]:  array([0.9])

    Args:
       x ... ndarray array of points on which we wish to apply the trapezoidal mapping. 
           Ex. np.array([-1,0.2,0.3,0.7])
    Returns:
       out ... ndarray of mapped points Ex. array([0. , 1. , 1. , 0.6])

    Original Matlab version written by:
    James P. LeSage, Dept of Economics
    University of Toledo
    2801 W. Bancroft St,
    Toledo, OH 43606
    jpl@jpl.econ.utoledo.edu

    This Python implementation is based on Andrew J. Patton's Matlab code avalible at:
    http://public.econ.duke.edu/~ap172/
    
    Implemented by Gregor Fabjan from Qnity Consultants on 12/11/2021.
    """
    nrow = x.shape[0]
    out = np.zeros(nrow)
    for row in range(nrow):
        out[row] = (abs(x[row])>=0) * (abs(x[row])<0.5) + 2 * (1-abs(x[row])) * (abs(x[row])>=0.5) * (abs(x[row])<=1)
    return out


