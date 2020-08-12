import numpy as np
from uncertainties import unumpy, ufloat
from math import sqrt

### here are the inputs
### eff1 = \epsilon^\gamma_T
### eff2 = \epsilon^J_T
### Na = N_T: total counts under tight/pass selection
### Nb = N_L: total counts under loose/fail selection
eff1 = ufloat(1.,.01)
eff2 = ufloat(.40,.05)
Na=ufloat(1600,40)
Nb=ufloat(150, 10)

def jet_fake_estimate_uncertainty_by_hand( eff1, eff2, Na, Nb, sigeff1, sigeff2, sigNa, sigNb):
    """
        hand calculated error propagation formula
    """
    det = eff1-eff2
    variance = ( sigeff1*eff2 / det**2 * ((eff2-1)*Na+eff2*Nb) )**2+\
               ( sigeff2*eff1 / det**2 * ((eff1-1)*Na+eff1*Nb) )**2+\
               ( sigNa*eff2*(eff1-1) /det )**2+\
               ( sigNb*eff1* eff2    /det )**2
    return sqrt(variance)

def jet_fake_estimate_by_hand( eff1, eff2, Na, Nb):
    """ hand calculated formula for fake estimate """
    det = eff1-eff2
    estimate = eff2 /det * ( (eff1-1)*Na+eff1*Nb )
    return estimate

def makematrix(eff1, eff2):
    return np.array([[eff1, eff2],[1-eff1, 1-eff2]])

def equivalentN( eff ):
    """
        binomial uncertainty formula: sigma^2 = eff*(1-eff)/N
        we work backwards to get N the sample size, given the efficiency
        i.e. : N = eff*(1-eff)/sigma^2
        For efficiency close to 0 or 1, uncertainty has a minimum that scales with 1/N
        so there is a minimum of N=1/eff
        input: ufloat object of efficiency
    """
    return int( max( 1/eff.s, (eff.n)*(1-eff.n)/eff.s/eff.s ) )


def binomial_monte_carlo( eff1, eff2, N1, N2, Na, Nb, sigNa, sigNb, Ntries=10000 ):
    """
        Monte Carlo method
        eff1:   (float) nominal value of /epsilon^T_/gamma
        eff2:   (float) nominal value of /epsilon^T_J
        N1:     (int)   sample size of eff1
        N2:     (int)   sample size of eff2
        Na:     (float) N_T: total counts under tight/pass selection
        Nb:     (float) N_L: total counts under loose/fail selection
        sigNa, sigNb: uncertainty of Na, Nb
        Ntries: (int) Number of Monte Carlo tries
    """
    ### make efficiency matrix
    p = np.array([eff1,eff2])*np.ones((Ntries,2))
    n = np.array([N1, N2]) ## number of events used to produce efficiencies
    eff = np.random.binomial(n,p)*1./n
    effmat = np.stack([eff,1-eff],axis=1) ## construct matrix
    #print effmat[0] # show a sample of matrix

    ### inverse and matrix multiplication
    invmat = np.linalg.inv(effmat)
    ## when there is degenerate matrix, uncomment the following for a little trick to go around it
    #invmat = manualinvert(effmat)
    Narray = np.random.normal([Na,Nb],np.ones((Ntries,2))*[sigNa,sigNb]) ## initiate N vector with normal distribution
    alphaJ = np.einsum("ikj,ij->ik",invmat,Narray)[:,1] ## matrix multiplcation similar to np.dot or np.matmul, but in einstein notation

    estarray = alphaJ*eff[:,1] # finally, the estimate is alpha_J*epsilon^T_J
    estarray = estarray[np.isfinite(estarray)]

    ### get result
    mean, std = estarray.mean(), estarray.std()
    #print "sample of Monte Carlo estimates: ",estarray[:10]
    print "4. Monte Carlo estimate of %i matrices: %g +/- %g" %(Ntries, mean, std)

    ### standard deviation: how different is it from normal distribution
    est2sigabove = mean+std*2
    est2sigbelow = mean-std*2
    pcabove2sig = np.sum(estarray>est2sigabove)*1./Ntries*100
    pcbelow2sig = np.sum(estarray<est2sigbelow)*1./Ntries*100
    print "   %g percent above 2 sigma (2.5%% normally), that is, estimates larger than %g" %(pcabove2sig, est2sigabove)
    print "   %g percent below 2 sigma (2.5%% normally), that is, estimates smaller than %g" %(pcbelow2sig, est2sigbelow)

def manualinvert(effmat):
    print "encounter degenerate matrix, do manual invert"
    invmat=[]
    errn = 0
    for i in range(effmat.shape[0]):
        try:
            invmat.append(np.linalg.inv(effmat[i]))
        except np.linalg.LinAlgError:
            #if errn<3: print effmat[i]
            errn+=1
            invmat.append(np.zeros((2,2))+np.nan)
    print "number of degenerate matrix: ", errn
    return np.stack(invmat)


def jet_fake_estimate_with_unumpy( eff1, eff2, Na, Nb):
    """ uncertainty+numpy implementation of error propagation """
    arr = unumpy.uarray([[0,0],[0,0]],[[0,0],[0,0]])
    ## fill matrix by hand so that it knows the dependency, essential to error propagation
    arr[0,0] = eff1
    arr[1,0] = 1-eff1
    arr[0,1] = eff2
    arr[1,1] = 1-eff2
    inverse = unumpy.ulinalg.inv(arr)
    alpha = np.dot(inverse,[Na, Nb])
    estimate = alpha[1]*eff2
    return estimate


mat=makematrix(eff1.n,eff2.n)
print "epsilon^T_gamma, epsilon^T_J" ,eff1,eff2
print "N_T, N_L", Na, Nb
print
print "Matrix:"
print mat
print "X alpha = ", np.array([Na.n,Nb.n])
print
print "Inverted matrix:"
print np.linalg.inv(mat)
print
estimate = jet_fake_estimate_by_hand( eff1, eff2, Na, Nb)
estimate2 = jet_fake_estimate_by_hand( eff1.n, eff2.n, Na.n, Nb.n)
variance2 = jet_fake_estimate_uncertainty_by_hand( eff1.n, eff2.n, Na.n, Nb.n, eff1.s, eff2.s, Na.s, Nb.s)
estimate3 =  jet_fake_estimate_with_unumpy( eff1, eff2, Na, Nb)
print "1. solved equation with uncertainty package: ",estimate
print "2. fully by hand error propagation: %g +/- %g" %(estimate2, variance2)
print "3. numpy+uncertainty array implementation: ", estimate3
N1= equivalentN(eff1)
N2= equivalentN(eff2)
print "equivalent sample size: Zgamma %i Z+jets %i" %(N1, N2)
binomial_monte_carlo( eff1.n, eff2.n, N1, N2, Na.n, Nb.n, Na.s, Nb.s, Ntries=10000 )
