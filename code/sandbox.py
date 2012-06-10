"""
This file is part of the Radio Array Model project.

Copyright 2012 David W. Hogg (NYU).

It contains a playground for building intuitions about radio
interferometers.

### issues:
* should work in log frequency and nu I_nu, rather than frequency and
  I_nu
"""

if __name__ == "__main__":
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import rc
    rc("font",**{"family":"serif","serif":"Computer Modern Roman","size":12})
    rc("text", usetex=True)
import numpy as np
import pylab as plt
import cPickle as pickle

# all the following from physics.nist.gov
hh = 6.62606957e-34 # J s
cc = 299792458. # m s^{-1}
kk = 1.3806488e-23 # J K^{-1}

def black_body(nus, T):
    """
    Planck Law.  Return in dimensions of I_nu.
    """
    return (2. * hh * nus ** 3 / cc ** 2 /
            (np.exp(hh * nus / (kk * T)) - 1.))

def sample_frequency(nu, deltaNu, K):
    """
    Obtain a set of `K` frequencies in the waveband of width `deltaNu`
    centered at frequency `nu`.  They are drawn from a uniform
    distribution in *frequency*.
    """
    return nu - 0.5 * deltaNu + deltaNu * np.random.uniform(size=K)

def sample_amplitudes(nus, T):
    """
    Obtain a set of `K` complex amplitudes, one for each frequency in
    `nus` given a temperature.  The amplitudes are chosen from a
    distribution such that the mean squared amplitude is the intensity
    as given by the Planck Law at temperature `T`.
    """
    K = nus.size
    intensities = black_body(nus, T)
    unitAmplitudes = 0.5 * (np.random.normal(size=K) + 1.j * np.random.normal(size=K))
    return np.sqrt(intensities) * unitAmplitudes

def get_amplitudes_at_times(times, nus, amps):
    """
    Run the clock forward to a set of times and return the complex
    amplitudes at those times.
    """
    phases = np.exp(-1.j * 2. * np.pi * nus[None, :] * times[:, None])
    return np.sum(amps[None, :] * phases, axis=1)

def get_intensities_at_times(times, nus, amps):
    return get_amplitudes_at_times(times, nus, amps) ** 2

def main():
    nu0 = 1.e9
    nus = sample_frequency(nu0, 0.05 * nu0, 100)
    print "nus", nus.shape
    amps = sample_amplitudes(nus, 2.7)
    print "amps", amps.shape
    times = np.arange(10000) / nu0 / 10.
    print "times", times.shape
    fields = get_amplitudes_at_times(times, nus, amps)
    print "fields", fields.shape
    Inus = get_intensities_at_times(times, nus, amps)
    print "intensities", fields.shape
    return None

if __name__ == "__main__":
    main()
