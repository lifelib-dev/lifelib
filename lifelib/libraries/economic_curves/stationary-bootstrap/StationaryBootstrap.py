import numpy as np

def StationaryBootstrap(data: np.ndarray, m, sampleLength)-> np.ndarray:
    """
    Returns a bootstraped sample of the time-series "data" of length "sampleLength. 
    The algorithm used is stationary bootstrap from 1994 Politis & Romano.
    
    Args:     
        data ... ndarray array. A single vector of numbers containing the time-series.
        m    ... floating number. Parameter to stationary bootstrap indicating the average length of each block in the sample.
        sampleLength ... integer. Length of the bootstrapped sample returned as output.
     
    Returns:     
        sample ... ndarray array containing the final bootstraped sample.
      
    Example of use:
    >>> import numpy as np
    >>> data = np.array([1,2,3,4,5,6,7,8,9,10])
    >>> m = 4
    >>> sampleLength = 12
    >>> StationaryBootstrap(data, m, sampleLength)
    Out[0]:  array([[9.],
                    [3.],
                    [4.],
                    [5.],
                    [6.],
                    [7.],
                    [8.],
                    [7.],
                    [2.],
                    [3.],
                    [4.],
                    [2.]])

    Original paper about stationary bootstrap:
    Dimitris N. Politis & Joseph P. Romano (1994) The Stationary Bootstrap, Journal of the American Statistical 
        Association, 89:428, 1303-1313, DOI: 10.1080/01621459.1994.10476870    

    Implemented by Gregor Fabjan from Qnity Consultants on 12/11/2021.

    """
    accept = 1/m  
    lenData = data.shape[0]

    sampleIndex = np.random.randint(0,high =lenData,size=1);
    sample = np.zeros((sampleLength,1))
    for iSample in range(sampleLength):
        if np.random.uniform(0,1,1)>=accept:
            sampleIndex += 1
            if sampleIndex >= lenData:
                sampleIndex=0        
        else:
            sampleIndex = np.random.randint(0,high = lenData,size=1)

        sample[iSample,0] = data[sampleIndex]
    return sample