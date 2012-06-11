"""
This file is part of the Radio Array Model project.

Copyright 2012 David W. Hogg (NYU).

It contains a playground for building intuitions about radio
interferometers.

### issues:
* should work in log frequency and nu I_nu, rather than frequency and
  I_nu
* Not sure the black_body units make sense.  Auditing necessary.
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

def make_signal(nu0, deltaNu, T, Omega, K):
    """
    Obtain a set of `K` frequencies and corresponding complex
    amplitudes, given a temperature `T`.  The frequencies are chosen
    from a uniform distribution of of width `deltaNu` centered at
    frequency `nu0`.  They are drawn from a uniform distribution in
    *frequency*.  The amplitudes are chosen deterministically from the
    Planck Law for a patch of (presumed tiny) solid angle Omega
    emitting at temperature `T`.  The phases are randomized to make
    the signal properly stochastic.
    """
    dnu = deltaNu / float(K)
    minNu = nu0 - 0.5 * deltaNu
    maxNu = nu0 + 0.5 * deltaNu
    nubreaks = np.sort(minNu + deltaNu * np.random.uniform(size=(K - 1)))
    nubreaks = np.append(np.append([minNu, ], nubreaks), [maxNu])
    nus = 0.5 * (nubreaks[1:] + nubreaks[:-1])
    dnus = (nubreaks[1:] - nubreaks[:-1])
    intensities = black_body(nus, T) * Omega * dnus
    phaseFactors = np.exp(-1.j * 2. * np.pi * np.random.uniform(size=K))
    return nus, np.sqrt(intensities) * phaseFactors

def get_amplitudes_at_times(times, nus, amps):
    """
    Run the clock forward to a set of times and return the complex
    amplitudes at those times.
    """
    phaseFactors = np.exp(-1.j * 2. * np.pi * nus[None, :] * times[:, None])
    print "phase factors", phaseFactors.shape, np.min(np.abs(phaseFactors)), np.max(np.abs(phaseFactors))
    return np.sum(amps[None, :] * phaseFactors, axis=1)

def delay_amplitudes(delay, nus, amps):
    """
    Delay a set of complex amplitudes `amps` at a set of frequencies
    `nus` by a fixed time delay `delay`.
    """
    phaseFactors = np.exp(-1.j * 2. * np.pi * nus * delay)
    print "delay phase factors", phaseFactors.shape, np.min(np.abs(phaseFactors)), np.max(np.abs(phaseFactors))
    return amps * phaseFactors

def get_correlations_at_times(times, nus, amps1, amps2):
    """
    Correlate two signals (represented by a set of complex amplitudes
    `amps1` and `amps2` at a common set of frequencies `nus`.  Give
    the output on a grid of times `times`.
    """
    return get_amplitudes_at_times(times, nus, amps1) * np.conj(get_amplitudes_at_times(times, nus, amps2))

def get_array_correlations(times, delays, nus, amps):
    """
    Compute and return all cross-correlations and auto-correlations
    for an array of telescopes.
    """
    ampss = [delay_amplitudes(delay, nus, amps) for delay in delays]
    corrs = np.zeros((delays.size, delays.size, times.size)).astype("complex")
    for i in range(delays.size):
        for j in range(delays.size):
            corrs[i, j, :] = get_correlations_at_times(times, nus, ampss[i], ampss[j])
    return corrs

def plot_corrs(times, corrs):
    """
    Plot a correlation between two antennae.
    """
    assert times.shape == corrs.shape
    rcorrs = np.real(corrs)
    mrcorrs = np.mean(rcorrs)
    icorrs = np.imag(corrs)
    micorrs = np.mean(icorrs)
    acorrs = np.abs(corrs)
    macorrs = np.sqrt(mrcorrs ** 2 + micorrs ** 2)
    pcorrs = np.arctan2(icorrs, rcorrs)
    mpcorrs = np.arctan2(micorrs, mrcorrs)
    y0 = 4. * macorrs # out to 2-sigma
    xlim = (np.min(times), np.max(times))
    for s, ys, meany, ylim, label, in [
        (1, rcorrs, mrcorrs, (-y0, y0), "real part"),
        (2, icorrs, micorrs, (-y0, y0), "imaginary part"),
        (4, acorrs, macorrs, (0., y0), "amplitude"),
        (5, pcorrs, mpcorrs, (-np.pi, np.pi), "phase (argument)"),
        ]:
        plt.subplot(2, 3, s)
        plt.plot(times, ys, "k.", alpha=0.5)
        plt.axhline(meany, color="r")
        plt.xlabel("time")
        plt.title(label)
        plt.xlim(xlim)
        plt.ylim(ylim)
    plt.subplot(2, 3, 3)
    plt.plot(rcorrs, icorrs, "k.", alpha=0.5)
    plt.plot(macorrs * np.cos(2. * np.pi * np.arange(1001) / 1000.),
             macorrs * np.sin(2. * np.pi * np.arange(1001) / 1000.), "r-")
    plt.plot([0., 10. * macorrs * np.cos(mpcorrs)],
             [0., 10. * macorrs * np.sin(mpcorrs)], "r-")
    plt.title("complex plane")
    plt.xlim(-y0, y0)
    plt.ylim(-y0, y0)
    return None

def plot_all_corrs(times, corrs, prefix):
    """
    Make full set of plots of all cross- and auto-correlations.
    """
    N, N2, M = corrs.shape
    assert N == N2
    assert M == times.size
    for i in range(N):
        for j in range(N):
            plt.figure(figsize = (9., 6.)) # inches?
            plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9,
                                wspace=0.3, hspace=0.3)
            plt.clf()
            plot_corrs(times, corrs[i, j])
            fn = "%s_%02d_%02d.png" % (prefix, i, j)
            print "writing %s" % fn
            plt.savefig(fn)
    return None

def main(prefix):
    nu0 = 8.e9 # Hz; typical VLA frequency?
    dnu = 1.e7 # Hz; typical VLA bandwidth?
    # dnu = 1. # made up to be visibly smooth
    deltaT = 600. # s; integration interval; typical for VLA?
    T = 3.e12 # K; source temperature; totally made up for no reason
    Omega = 1.e-12 # ster; source solid angle; totally made up for no reason
    K = 32 # number of frequencies to simulate
    nus, amps = make_signal(nu0, dnu, T, Omega, K)
    print "nus", nus.shape
    print "amps", amps.shape
    M = 4096 # number of time samples to average per integration interval
    t0 = 0.
    t2 = t0 + deltaT
    dt = (t2 - t0) / float(M)
    times = np.sort(t0 + (t2 - t0) * np.random.uniform(size=M))
    print "times", times.shape, times.min(), times.max()
    N = 4 # number of telescopes
    delays = np.array([(100. / nu0) * np.random.uniform() for n in range(N)])
    corrs = get_array_correlations(times, delays, nus, amps)
    print "correlations", corrs.shape
    plot_all_corrs(times, corrs, prefix)
    return None

if __name__ == "__main__":
    main("sandbox")
