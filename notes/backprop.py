# backprop.py - Backpropogation, or gradient descent for neural networks.

import numpy as np


def foward(X, W, V, b, c):
    # Feedfoward for gradient descent.
    # Z = np.tanh(X.dot(W) + b)
    Z = 1 / (1 + np.exp(-X.dot(W) - b))
    A = Z.dot(V) + c
    Y = np.exp(A) / np.exp(A).sum(axis=1, keepdims=True)
    # P = np.argmax(P, axis=1) # Use argmax to make a prediction. 
    # Not needed for gradient.
    return (Y, Z) # Hidden layer is required to calculate gradient.


def class_rate(voutputs, vpred):
    vcorrect = 0
    vtotal = 0
    for i in range(len(voutputs)):
        vtotal += 1
        if voutputs[i] == vpred[i]: vcorrect += 1
    return float(vcorrect / vtotal)



##  Derivatives ################################################################

def derivative_w2(Z, T, Y):
    N, K = T.shape
    M = Z.shape[1]
    #print("[*] Derivitave of W1: N:%s K:%s M:%s" % (N, K, M))
    '''
    ret1 = np.zeros((M, K))
    for n in range(N):
        for k in range(K):
            for m in range(M):
                ret1[m, k] += (T[n,k] - Y[n,k]) * Z[n,m] 
    return ret1
    '''
    return Z.T.dot(T - Y) # Result is M X K


def derivative_b2(vtargs, voutputs):
    "Calc the derivative of T and Y, WRT biases 2."
    return (vtargs - voutputs).sum(axis=0) # Sum of differences. 


def derivative_w1(X, vhidden, vtargs, voutputs, W2):
    "Calc derivative of inputs, WRT 1st weights."
    N, D = X.shape
    M, K = W2.shape # Loop through all weights for all training.

    '''
    ret1 = np.zeros((X.shape[1], M))
    for n in range(N):
        for k in range(K):
            for m in range(M):
                for d in range(D):
                     ret1[d, m] += ((vtargs[n,k] - voutputs[n,k]) * W2[m,k] 
                        * vhidden[n,m] * (1-vhidden[n,m])*X[n,d]) 
                     # Difference times bias.
    return ret1
    '''
    dz = (vtargs - voutputs).dot(W2.T) * vhidden * (1 - vhidden)
    return X.T.dot(dz)


def derivative_b1(vtargs, voutputs, W2, vhidden):
    # Devise how to do this slow way...
    return ((vtargs - voutputs).dot(W2.T) * vhidden * (1 - vhidden)).sum(axis=0)


## Backprop ####################################################################

def cost(vtargs, voutputs):
    "Calculate the error between predictions and target values."
    vtotal = vtargs * np.log(voutputs)
    return vtotal.sum()


def bp(X,        # Training data
       M,        # Size of hidden layer.
       K,        # Number of output categories.
       Y):       # Predictions

    "Backpropagation for multi-classification."

    X1 = X
    N = len(X1)       # Number of samples
    D = len(X1[0])    # Input layer size
    W1 = np.random.randn(D, M) 
    b1 = np.random.randn(M)
    W2 = np.random.randn(M, K)
    b2 = np.random.randn(K)

    print("[*] Training data (%s Samples, %s Features): %s\n" % (len(X1), D, X1))

    # 1-hot encoding for multiple categories.
    Ny = len(Y)
    vtargs = np.zeros((Ny, K))
    for i in range(Ny): vtargs[i, Y[i]] = 1
    print("[*] Targets (%s Samples, %s Categories): %s" % (len(vtargs), K, vtargs))

    # Start backprop.
    vlearn_rate = 1e-3
    vcosts = []

    for epoch in range(1000):

        voutputs, vhidden = foward(X1, W1, W2, b1, b2)
        #print("\n[*] NN Outputs (%s Categories): %s" % (K, voutputs))
        #print("[*] Hidden (Neurons: %s): %s" % (M, vhidden))
        
        if epoch % 100 == 0: # Calculate and print cost every 100 epochs. (DEBUG)
            vcost = cost(vtargs, voutputs)
            vpreds = np.argmax(voutputs, axis=1)

            #print("\n[*] Predictions (%s): %s" % (len(vpreds), vpreds))
            #print("\n[*] Outputs (%s): %s" % (len(voutputs), voutputs))

            vclass_rate = class_rate(Y, vpreds)
            print("[*] Cost: [%s], Class Rate: [%s]" % (vcost, vclass_rate))

            vcosts.append(vcost)

        # Calculate gradients, adjust parameters.
        W2 += vlearn_rate * derivative_w2(vhidden, vtargs, voutputs)

        b2 += vlearn_rate * derivative_b2(vtargs, voutputs)
        W1 += vlearn_rate * derivative_w1(X1, vhidden, vtargs, voutputs, W2)
        b1 += vlearn_rate * derivative_b1(vtargs, voutputs, W2, vhidden)
    
    #import matplotlib.pyplot as plt
    #plt.plot(vcosts)
    #plt.show()


if __name__ == "__main__":
    "Run backprop test."
    
    print("== Backpropagation Example "+"="*64)
    print("[*] Generate training data...")

    N = 500
    D = 2
    X1 = np.random.randn(N, D) + np.array([0, -2])
    X2 = np.random.randn(N, D) + np.array([2, 2])
    X3 = np.random.randn(N, D) + np.array([-2, 2])
    X1 = np.vstack([X1, X2, X3])
    #X1 = np.random.randn(N*3, D) + np.array([-2, 2])
    
    # Create targets to backprop to.
    print("[*] Generate prediction targets...")
    Y = np.array([0]*N + [1]*N + [2]* N)

    # Get the weights from training the mod
    print("[*] Start backprop...")
    vweights = bp(X1, 300, 3, Y)
