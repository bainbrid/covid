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

N_p = float(12597) # population
N_t = float(919)   # tested
N_i = float(138)   # infections
N_f = float(7)     # fatal

trials = 1000000

########################################
# Throw Binomial toys based on 138 infected cases in the test sample of 919

n = N_t
p = N_i/N_t
binomial = np.random.binomial(n,p,trials)
print("Infections:")
print(" binomial.shape",binomial.shape)
print(" mean:",np.mean(binomial))
print(" sigma:",np.std(binomial))

bins=np.linspace(100,180,81)
plt.hist(binomial, bins, normed=True)
plt.xlabel('Number of infections in test sample')
plt.ylabel('a.u.')
plt.savefig("infected.pdf")
plt.clf()

########################################
# Throw Binomial toys to estimate number infections in the full population of 12597 
# ASSUMPTION: the test sample is a representative sample of the full population!

n = N_p
p = N_i/N_t
binomial = np.random.binomial(n,p,trials)
print("Estimated infections:")
print(" binomial.shape",binomial.shape)
print(" mean:",np.mean(binomial))
print(" sigma:",np.std(binomial))

bins=np.linspace(1700,2100,81)
count, bins, ignored = plt.hist(binomial, bins, normed=True)
plt.xlabel('Estimated number of infections in full population')
plt.ylabel('a.u.')
plt.savefig("estimated.pdf")
plt.clf()

########################################
# Throw toys on number of fatalities using Poisson(mu=N_f)

poisson = np.random.poisson(N_f, trials)
print("Fatalities:")
print(" poisson.shape",poisson.shape)
print(" mean:",np.mean(poisson))
print(" sigma:",np.std(poisson))

bins=np.linspace(0,30,31)
count, bins, ignored = plt.hist(poisson, bins, normed=True)
plt.xlabel('Number of fatalities in full population')
plt.ylabel('a.u.')
plt.savefig("fatal.pdf")
plt.clf()

########################################
# Determine Infection Mortality Rate (IFR)
# IFR = (N_f/N_i) / (N_t/N_p)
# ASSUMPTION: 

ifr = (poisson*1.) / (binomial*1.) * 100. # expressed as %
print("Infection fatality rate:")
print(" ifr.shape",ifr.shape)
print(" mean:",np.mean(ifr))
print(" sigma:",np.std(ifr))

# Display the histogram of the samples
bins=np.linspace(0,1.,101)
count, bins, ignored = plt.hist(ifr, bins, weights=np.full_like(ifr,1./ifr.sum()))
plt.xlabel('Infection Fatality Rate (%)')
plt.ylabel('a.u.')
plt.savefig("ifr.pdf")
plt.clf()

########################################
# Intervals

ifr = sorted(ifr)
mean = np.mean(ifr)
l68 = (0.+((1.-0.683)/2.))*100. # %
u68 = (1.-((1.-0.683)/2.))*100. # %
l95 = (0.+((1.-0.950)/2.))*100. # %
u95 = (1.-((1.-0.950)/2.))*100. # %
print("<IFR> = {:5.3f} % | CL68: [{:5.3f} {:5.3f}] % CL95: [{:5.3f} {:5.3f}] %".format(
        np.mean(ifr), 
        np.percentile(ifr,l68),
        np.percentile(ifr,u68),
        np.percentile(ifr,l95),
        np.percentile(ifr,u95),
        )
      )
