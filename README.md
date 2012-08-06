# Radio Array Model

A playground to explore the probabilistic and inference properties of
radio interferometry arrays.  The hope is to evolve into a system for
computing likelihoods or posterior probabilities over scenes that
explain a set of radio interferometry data.

### Authors: ###

* [**David W. Hogg**](http://cosmo.nyu.edu/hogg/), New York University

### License: ###

Copyright 2010 2011 2012 the author.  **All rights reserved.**

If you have interest in using or re-using any of this content, get in
touch with Hogg.

### Contributors: ###

* **Frank Bigiel**, Universität Heidelberg
* **Brendon Brewer**, UC Santa Barbara
* **Hans-Walter Rix**, Max-Planck-Institut für Astronomie

### Things to think about: ###

* You have a faint blob in your cleaned image.  Is it significant?
  Surely this is a question that should or could be answered in the
  space of visibilities.

* There are N radio telescopes and ~N^2 baselines; does this mean that
  noise in the baselines must be correlated?  Or does the long
  integration time (relative to the coherence time) erase these
  correlations?  How can we see these correlations empirically; that
  is, can we test this idea directly with the raw data?

* There are N radio telescopes and ~N^2 baselines; does this mean that
  you can infer the phase delays you get from your phase calibrator
  from the science data themselves?  That is, can you self-calibrate
  always when N is large?

* Bandwidth-smearing is something that needs to be a part of any real
  generative model.  That is, we might be able to account for this in
  a proper model.

* Can we go "fully probilistic"?  Is it possible to return a posterior
  PDF over scenes that could have created the data?

### Related projects and bibliography: ###

* **Peter Williams** (Berkeley) is developing Python code to do
    analysis of interferometry data, with an emphasis on transient
    science; see [arXiv:1203.0330](http://arxiv.org/abs/1203.0330)
* **John Monnier** (Michigan) is working on sensible regularizers
    (which are like priors, of course) for optical interferometry
    problems.
* **Sutton** and **Wandelt** (2006)
    [Optimal image reconstruction in radio interferometry](http://arxiv.org/abs/astro-ph/0604331)
    is close to the whole enchilada; includes likelihood function and sophisticated priors.
    *This is the project to outperform or out-code.*
* **Kemball** *et al* (2010)
    [Further evaluation of bootstrap resampling as a tool for radio-interferometric imaging fidelity assessment](http://arxiv.org/abs/0911.2007)
    looks at bootstrap methods to put uncertainties on radio maps generated from interferometry.
