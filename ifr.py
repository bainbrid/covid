# Inputs:
# - The study finds that the infection fatality rate (IFR) of SARS-CoV-2 in the random sample was 0.37% [0.29%; 0.45%]. 
# - "The analysis considered 919 individuals chosen out of 12597 people." 
# - "In 919 they found 138 infected and 7 deaths from COVID-19 in all 12597." 

# Assumptions:
# - Sample estimate of "raw infection rate" is 138/919
# - "Raw death rate" for population is 7/12597

# Approach:
# 0) IFR = N_f/N_i' = (N_f/N_p) * (N_i'/N_p) = N_f/N_i'
# - where N_i' is the estimated number of infections in the population N_p
# 1) Throw toys using Gaussian(mu=N_i',sigma=sigma_i')
# - N_i = 138 and sigma_i = sqrt(n*p*(1-p)) = 10.83
#    - where n = N_t = 919 and p = N_i/N_t = 138/919
# - Assume N_i' and sigma_i' is obtained by scaling N_i and sigma_i by factor (N_p/N_t)
#   => N_i' = 1891.6, sigma_i' = 148.4
#   - Question: is there any "sample->population" correction to be applied to N_i' and sigma_i'
# 2) Throw toys using Poisson(mu=N_f)
# - N_f=7
# 3a) Plot N_f/N_i' based on the toys (as N_p cancels out...)

import numpy as np
import matplotlib.pyplot as plt

########################################
# Inputs

N_p = 12597. # population
N_t = 919.   # tested
N_i = 138.   # infected
N_f = 7.     # fatal

trials = 10000000

########################################
# Scaled infection rate and uncertainty (68% CL) using normal approximation

N_I = N_i * (N_p/N_t) # = 1891.6
print("N_I:",N_I)

n = N_t
p = N_i/N_t
sigma_I = np.sqrt(n*p*(1.-p)) * (N_p/N_t) # = 148.4
print("sigma_I:",sigma_I)

########################################
# Gaussian(mu=N_I,sigma=sigma_I) and histogram

toys_I = np.random.normal(N_I, sigma_I, trials)
print("toys_I.shape:",toys_I.shape)
print("N_I:",np.mean(toys_I))
print("sigma_I:",np.std(toys_I))

count, bins, ignored = plt.hist(toys_I, bins=30, normed=True)
plt.plot(bins, 
         1/(sigma_I * np.sqrt(2 * np.pi)) * np.exp( - (bins - N_I)**2 / (2 * sigma_I**2) ),
         linewidth=2, 
         color='r')
plt.savefig("infected.pdf")
plt.clf()

########################################
# Poisson(mu=N_f) and histogram

toys_f = np.random.poisson(N_f, trials)
print("toys_f.shape",toys_f.shape)
print("N_f:",np.mean(toys_f))
print("sigma_f:",np.std(toys_f))

count, bins, ignored = plt.hist(toys_f, bins=np.arange(31), normed=True)
plt.savefig("fatal.pdf")
plt.clf()

########################################
# IFR and histogram

toys_ifr = toys_f / toys_I
print("toys_ifr.shape",toys_ifr.shape)

# Display the histogram of the samples
bins=bins=np.linspace(0,1.,101)
count, bins, ignored = plt.hist(toys_ifr*100., bins, normed=True)
plt.xlabel('IFR (%)')
plt.ylabel('a.u.')
plt.savefig("ifr.pdf")
plt.clf()

########################################
# IFR and histogram

#toys_ifr = np.zeros((0))
#for i,I in enumerate(toys_I) :
#    print("toy:",i)
#    toys_ifr = np.append(toys_ifr,(np.random.poisson(N_f, trials)*1.)/(I*1.))
#print("toys_ifr.shape",toys_ifr.shape)
#
## Display the histogram of the samples
#bins=bins=np.linspace(0,0.01,201)
#count, bins, ignored = plt.hist(toys_ifr, bins, normed=True)
#plt.savefig("ifr.pdf")
#plt.clf()

########################################
# Intervals

ifr = sorted(toys_ifr)
mean = np.mean(ifr)
l68 = (0.+((1.-0.683)/2.))*100.
u68 = (1.-((1.-0.683)/2.))*100.
l95 = (0.+((1.-0.950)/2.))*100.
u95 = (1.-((1.-0.950)/2.))*100.
print("<IFR> = {:5.3f} % | CL68: [{:5.3f} {:5.3f}] % CL95: [{:5.3f} {:5.3f}] %".format(
        np.mean(ifr)*100., 
        np.percentile(ifr,l68)*100.,
        np.percentile(ifr,u68)*100.,
        np.percentile(ifr,l95)*100.,
        np.percentile(ifr,u95)*100.,
        )
      )

########################################
# 3b) Throw toys using Binomial(n=N_f,p=N_f/N_i') and plot
# binomial and histogram
#trials=10000
#binomial = np.zeros((0))
#for i,(f,I) in enumerate(zip(toys_f,toys_I)) :
#    print("toy:",i)
#    binomial = np.append(binomial,(np.random.binomial(I, f*1./I*1., trials)*1.)/(I*1.))
#print("binomial.shape",binomial.shape)
#
## Display the histogram of the samples
#bins=bins=np.linspace(0,0.01,51)
#count, bins, ignored = plt.hist(binomial, bins, normed=True)
#plt.savefig("binomial.pdf")
#plt.clf()
