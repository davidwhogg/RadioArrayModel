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

def make_signal(nu, deltaNu, T, K):
    """
    Obtain a set of `K` frequencies and corresponding complex
    amplitudes, given a temperature `T`.  The frequencies are chosen
    from a uniform distribution of of width `deltaNu` centered at
    frequency `nu`.  They are drawn from a uniform distribution in
    *frequency*.  The amplitudes are chosen from a distribution such
    that the mean squared amplitude is the intensity as given by the
    Planck Law at temperature `T`.
    """
    nus = nu - 0.5 * deltaNu + deltaNu * np.random.uniform(size=K)
    intensities = black_body(nus, T) * deltaNu / K
    unitAmplitudes = 0.5 * (np.random.normal(size=K) + 1.j * np.random.normal(size=K))
    return nus, np.sqrt(intensities) * unitAmplitudes

def get_amplitudes_at_times(times, nus, amps):
    """
    Run the clock forward to a set of times and return the complex
    amplitudes at those times.
    """
    phaseFactors = np.exp(-1.j * 2. * np.pi * nus[None, :] * times[:, None])
    return np.sum(amps[None, :] * phaseFactors, axis=1)

def delay_amplitudes(delay, nus, amps):
    """
    Delay a set of complex amplitudes `amps` at a set of frequencies
    `nus` by a fixed time delay `delay`.
    """
    phaseFactors = np.exp(-1.j * 2. * np.pi * nus * delay)
    return amps * phaseFactors

def get_correlations_at_times(times, nus, amps1, amps2):
    """
    Correlate two signals (represented by a set of complex amplitudes
    `amps1` and `amps2` at a common set of frequencies `nus`.  Give
    the output on a grid of times `times`.
    """
    return get_amplitudes_at_times(times, nus, amps1) * np.conj(get_amplitudes_at_times(times, nus, amps2))

def main(prefix):
    nu0 = 1.e10 # typical VLA frequency?
    dnu = 1.e7 # typical VLA bandwidth?
    # dnu = 1. # made up to be visibly smooth
    nus, amps = make_signal(nu0, dnu, 2.7e10, 100)
    print "nus", nus.shape
    print "amps", amps.shape
    M = 10000
    t0 = 0.
    t1 = 3. / dnu
    t2 = 600.
    times = t0 + (t2 - t0) * np.arange(M) / M # 600 s = 10 min
    print "times", times.shape
    fields = get_amplitudes_at_times(times, nus, amps)
    print "fields", fields.shape
    delay = (100. / nu0) * np.random.uniform()
    amps2 = delay_amplitudes(delay, nus, amps)
    print "amps2", amps2.shape
    Inus = get_correlations_at_times(times, nus, amps, amps2)
    rInus = np.real(Inus)
    mrInus = np.mean(rInus)
    iInus = np.imag(Inus)
    miInus = np.mean(iInus)
    aInus = np.abs(Inus)
    maInus = np.sqrt(mrInus ** 2 + miInus ** 2)
    pInus = np.arctan2(iInus, rInus)
    mpInus = np.arctan2(miInus, mrInus)
    print "intensities", fields.shape
    plt.clf()
    for s, ys, meany, label in [
        (1, rInus, mrInus, "real part of correlation"),
        (2, iInus, miInus, "imaginary part of correlation"),
        (3, aInus, maInus, "amplitude of correlation"),
        (4, pInus, mpInus, "phase (argument) of correlation"),
        ]:
        plt.subplot(2, 2, s)
        plt.plot(times, ys, "k.", alpha=0.5)
        plt.axhline(meany, color="r")
        plt.xlabel("time")
        plt.ylabel(label)
        plt.xlim(t0, t2)
    plt.savefig(prefix + "_Inus.png")
    return None

if __name__ == "__main__":
    main("sandbox")
