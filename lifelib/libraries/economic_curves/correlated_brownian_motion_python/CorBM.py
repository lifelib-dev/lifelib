import numpy as np 

def CorBrownian(mu, E, sampleSize):
    # Algorithm generates samples of increments from a correlated Brownian motion with a given mean and Variance-Covariance matrix (E). 
    # The algorithm uses the fact that if you have n independent brownian motions, the samples given by "mu+ C*Z" are distributed as N(mu,E), where mu is the vector of means and C is the square root of the Variance-Covariance matrix.
    # For calculating the square root of the VarCovar matrix, the Cholesky decomposition is implemented.
    # Arguments:
    #     mu        = Array with n elements containing the mean of each BM  
    #     E         = n x n numpy array with the Variance-Covariance matrix 
    #    sampleSize = integer representing the number of samples
    # 
    # Returns:
    #     sampleSize x n numpy array containing sampled increments for the correlated Brownian motion
    #      
    # Note: 
    #  The algorithm is not optimized for speed and no testing of inputs is implemented. If this would be usefull to you, let us know and we can extend the code.
    #
    # Example of use:
    # import numpy as np 
    # mu = [1,2]
    # VarCovar = np.matrix('1,0.8; 0.8,3')
    # sampleSize = 5
    # out = CorBrownian(mu,VarCovar, sampleSize)
    # > [ 2.83211068  4.50021193]
    #   [ 0.26392619  1.56450446]
    #   [-0.25928109  0.97167124]
    #   [ 1.52038489  1.76274556]]
    #
 
    def Cholesky(X):
        # Cholesky–Banachiewicz algorithm decomposes a Hermitian matrix into a product of a lower triangular matrix and its conjugate transpose.
        # Arguemnts:
        #    X = n x n ndarray representing a Hermitian matrix that the user wants to decompose
        # Returns:
        #    n x n ndarray lower triangular matrix such that the matrix product between it and its conjugate transpose returns X
        # 
        # More info on: https://en.wikipedia.org/wiki/Cholesky_decomposition#The_Cholesky.E2.80.93Banachiewicz_and_Cholesky.E2.80.93Crout_algorithms

        L = np.zeros_like(X)
        n = X.shape[0]

        for i in range(0, n):
            for j in range(0, i+1):
                sum = 0
                for k in range(0, j):
                    sum = sum+ L[i, k]*L[j, k]
                if (i==j):
                    L[i, j] = np.sqrt(X[i, i]-sum)
                else:
                    L[i, j] = 1.0/L[j, j] * (X[i, j]-sum)
        return L

    dim = E.shape[0]                                         # Guess the number of Brownian motions (dimension) from the size of the Var-Covar matrix
    Z = np.random.default_rng().normal(0,1,(sampleSize, dim)) # Generate independent increments of a simpleSize dimensional Brownian motion
    Y = np.zeros((sampleSize, dim))                          # Predefine the final output
    L = Cholesky(E)                                          # Calculate the square root of the Var-Covar matrix

    for iSample in range(sampleSize): # For each sample, calculate mu + L*Z
        Y[iSample] =np.transpose(mu) +  L @ np.transpose(Z[iSample])     
    return Y
