"""The main Space in the :mod:`~economic.BasicHullWhite` model.

Mathematical notations are defined consistent with those in Brigo and Mercurio (2001, 2nd Ed. 2006)

.. seealso::

   * Damiano Brigo, Fabio Mercurio (2001, 2nd Ed. 2006). Interest Rate Models — Theory and Practice with Smile, Inflation and Credit


Attributes:

    scen_size: Number of scenarios. 1000 by default.

    np: numpy module.

    step_size: Number of time steps. 360 by default.

    time_len: Simulation length in years. 30 by default.

    a: Parameter :math:`a` in the Hull-White stochastic differential equation. 0.1 by default.

    sigma: Parameter :math:`\sigma` in the Hull-White stochastic differential equation. 0.1 by default.

    seed1: Seed number to generate random numbers. 1234 by default. See :meth:`std_norm_rand`.

    seed2: Seed for the second random numbers used for :meth:`accum_short_rate2`.
"""

from modelx.serialize.jsonvalues import *

_formula = None

_bases = []

_allow_none = None

_spaces = []

# ---------------------------------------------------------------------------
# Cells

def A_t_T(i, j):
    r""":math:`A(t_i, t_j)` in :math:`P(t_i, t_j)`

    See :meth:`P_t_T`.
    """
    t = t_(i)
    P_t = mkt_zcb(i)
    P_T = mkt_zcb(j)
    f_t = mkt_fwd(i)
    B = B_t_T(i, j)

    return P_T / P_t * np.exp(
        B * f_t - sigma**2 / (4*a) * (1 - np.exp(-2*a*t)) * B**2 
    )


def B_t_T(i, j):
    r""":math:`B(t_i, t_j)` in :math:`P(t_i, t_j)`

    See :meth:`P_t_T`.
    """
    t, T = t_(i), t_(j)
    return (1 / a) * (1 - np.exp(-a * (T-t)))


def E_rt():
    """The expected values of :math:`r(t_i)` at time 0 for all :math:`t_i`.

    Returns, in a numpy array, the expected values of
    :math:`r(t_i)` for all :math:`t_i`.
    Calculated as :math:`E\{r(t_i) | \mathcal{F}_{0}\}`.

    .. seealso::

       * :meth:`E_rt_s`

    """
    return np.array([E_rt_s(0, i)[0] for i in range(step_size + 1)])


def E_rt_s(i, j):
    r"""Conditional expected values of :math:`r(t_j)`

    Returns, in a numpy array,
    :math:`E\{r(t_j) | \mathcal{F}_{i}\}`,
    the expected values of :math:`r(t_j)` conditional on :math:`\mathcal{F}_{i}`
    for all scenarios.
    :math:`E\{r(t) | \mathcal{F}_{s}\}` is calculated as:

    .. math::

        r(s)e^{-a(t-s)}  + \alpha(t) - \alpha(s)e^{-a(t-s)}

    where :math:`\alpha(t)` is calculated by :meth:`alpha`.

    .. seealso:
        * :meth:`short_rate`
        * :meth:`alpha`
    """
    s, t = t_(i), t_(j)
    r_s = short_rate(i)
    return r_s * np.exp(-a * (t-s)) + alpha(j) - alpha(i) * np.exp(-a * (t-s))


def P_t_T(i, j):
    r"""The price at :math:`t_i` of a zero-coupon bond paying off 1 at :math:`t_j`

    This formula corresponds to :math:`P(t, T)` in Brigo and Mercurio, which is defined as:

    .. math::

        P(t, T)=A(t, T)e^{-B(t, T)r(t)}

    where :math:`t_i` and :math:`t_j` substitute for :math:`t` and :math:`T`.

    .. seealso::
        * :meth:`A_t_T` for :math:`A(t, T)`
        * :meth:`B_t_T` for :math:`B(t, T)`
        * :meth:`short_rate` for :math:`r(t)`
        * Brigo and Mercurio (2001, 2nd Ed. 2006). Interest Rate Models — Theory and Practice with Smile, Inflation and Credit

    """
    return A_t_T(i, j) * np.exp(-B_t_T(i, j) * short_rate(i))


def V_t_T(i, j):
    r"""The variance of :math:`\int_{t_j}^{t_i} r(u)du|\mathcal{F}_{t_i}`

    This formula corresponds to :math:`V(t, T)` in Brigo and Mercurio, which is defined as:

    .. math::

        V(t, T)=\frac{\sigma^2}{a^2}\left[T-t+\frac{2}{a}e^{-a(T-t)}-\frac{1}{2a}e^{-2a(T-t)}-\frac{3}{2a}\right]

    where :math:`t_i` and :math:`t_j` substitute for :math:`t` and :math:`T`.

    .. seealso::
        * :attr:`sigma` for :math:`\sigma`
        * :attr:`a` for :math:`a`
        * Brigo and Mercurio (2001, 2nd Ed. 2006). Interest Rate Models — Theory and Practice with Smile, Inflation and Credit

    """
    dt = t_(j) - t_(i)
    return sigma**2 / a**2 * (dt + (2/a)*np.exp(-a*dt) - (1/(2*a))*np.exp(-2*a*dt) - (3/(2*a)))


def Var_rt():
    r"""The variance of :math:`r(t_i)` at time 0 for all :math:`t_i`.

    Returns, in a numpy array, the variance of
    :math:`r(t_i)` for all :math:`t_i`.
    Calculated as :math:`Var\{r(t_i) | \mathcal{F}_{0}\}`.

    .. seealso::
        * :meth:`Var_rt_s`
    """
    return np.array([Var_rt_s(0, i) for i in range(step_size + 1)])


def Var_rt_s(i, j):
    r"""The variance of :math:`r(t_j)` conditional on :math:`\mathcal{F}_{t_i}`

    :math:`Var\{r(t_{j}) | \mathcal{F}_{t_i}\}`,
    the variance of :math:`r(t_j)` conditional on :math:`\mathcal{F}_{t_i}`,
    calculated as:

    .. math::

        Var\{ r(t) | \mathcal{F}_s \} = \frac{\sigma^2}{2a} (1 - e^{-2a(t-s)})

    .. seealso::
        * :attr:`a`
        * :attr:`sigma`

    """
    s, t = t_(i), t_(j)
    return sigma**2 / (2*a) * (1 - np.exp(-2 * a * (t-s)))


def accum_short_rate(i):
    r"""Accumulated short rates.

    a descrete approximation to the integral :math:`\int_0^{t_i}r(t)dt`,
    calculated as :math:`\sum_{j=1}^{i}r(t_{j-1})(t_j-t_{j-1})`

    .. seealso::
        * :meth:`disc_factor`
    """
    if i == 0:
        return np.full(scen_size, 0.0)
    else:
        dt = t_(i) - t_(i-1)
        return accum_short_rate(i-1) + short_rate(i-1) * dt


def accum_short_rate2(i):
    r"""Alternative implementation of accumulated short rates.

    An alternative approach to simulate :math:`Y(t_i)=\int_0^{t_i}r(t)dt`
    by using the fact that :math:`Y(t_i)` follows a normal distribution,
    and by simulating the joint distribution of :math:`(r(t_i), Y(t_i))`,
    as suggested in Glasserman (2003).

    .. seealso::
        * :meth:`accum_short_rate`
        * :attr:`seed2`
        * Paul Glasserman (2003). Monte Carlo Methods in Financial Engineering
    """
    if i == 0:
        return np.full(scen_size, 0.0)
    else:
        t, T = t_(i-1), t_(i)
        dt = T - t
        cov = sigma**2/(2*a**2)*(1 + np.exp(-2*a*dt) -2 * np.exp(-a*dt))
        z1 = std_norm_rand(seed1)[:, i-1]
        z2 = std_norm_rand(seed2)[:, i-1]

        rho = cov / (Var_rt_s(i-1, i)**0.5 * V_t_T(i-1, i)**0.5)

        mean = B_t_T(i-1, i) * (short_rate(i-1) - alpha(i-1)) + np.log(mkt_zcb(i-1)/mkt_zcb(i)) + 0.5*(V_t_T(0, i)-V_t_T(0, i-1))
        return accum_short_rate2(i-1) + mean + V_t_T(i-1, i)**0.5 * (rho*z1 + (1-rho**2)**0.5*z2)


def alpha(i):
    r""":math:`\alpha(t_i)`

    Returns, in a numpy array, :math:`\alpha(t_i)` for all scenarios.
    :math:`\alpha` appears in the expression of
    :math:`E\{r(t) | \mathcal{F}_{s}\}` and is defined as:

    .. math::

        \alpha(t) = f^M(0, t) + \frac{\sigma^2} {2a^2}(1-e^{-at})^2

    .. seealso::
        * :meth:`E_rt_s`

    """
    t = t_(i)
    return mkt_fwd(i) + 0.5 * sigma**2 / a**2 * (1 - np.exp(-a*t))**2


def disc_factor(i):
    """Discount factors

    Returns, in a numpy array, the discount factors for
    cashflows at :math:`t_i` for all scenarios.
    Defined as::

        np.exp(-accum_short_rate(i))

    .. seealso::
        * accum_short_rate

    """
    return np.exp(-accum_short_rate(i))


def disc_factor_paths():
    """Discount factor scenarios.

    Returns, as a 2D numpy array, the simulated discount factors
    for all scenarios.

    .. seealso::
        * :meth:`disc_factor`
    """
    return np.array([disc_factor(i) for i in range(step_size + 1)]).transpose()


def mean_disc_factor():
    """Discount factor means

    Returns, as a numpy array, the mean of discount factors of all scenarios
    for each :math:`t_i`.

    .. seealso::
        * :meth:`disc_factor`
    """
    return np.array([np.mean(disc_factor(i)) for i in range(step_size + 1)])


def mean_short_rate():
    """The means of generated short rates

    Returns, as a numpy array, the means of short rates of all scenarios
    for all :math:`t_i`.
    This should converge to the theoretical variances
    calculated by :meth:`E_rt`.

    .. seealso::
        * :meth:`short_rate`
        * :meth:`E_rt`
    """
    return np.array([np.mean(short_rate(i)) for i in range(step_size + 1)])


def mkt_fwd(i):
    """The initial instantaneous forward rate for :attr:`t_(i)<t_>`.

    By default, returns 0.05 for all ``i``.
    """
    return 0.05


def mkt_zcb(i):
    """The initial price of zero coupon bond

    The initial price of the unit zero coupon bond maturing at :attr:`t_(i)<t_>`.

    If ``i=0`` returns 1. Otherwise, defined as::

        mkt_zcb(i-1) * np.exp(-mkt_fwd(i-1)*dt)

    where ``dt = t_(i) - t_(i-1)``.

    .. seealso::
        * :attr:`t_`
        * :attr:`mkt_fwd`
    """
    if i == 0:
        return 1.0
    else:
        dt = t_(i) - t_(i-1)
        return mkt_zcb(i-1) * np.exp(-mkt_fwd(i-1)*dt)


def short_rate(i):
    r"""Stochastic short rates at :attr:`t_(i)<t_>`

    Returns, in a numpy array, simulated stochastic short rates at :attr:`t_(i)<t_>`
    for all scenarios.

    For ``i=0``, defined as :meth:`mkt_fwd(0)<mkt_fwd>`.

    For ``i>0``, defined as
    :math:`r(t_i) = E\{r(t_i) | \mathcal{F}_{i-1}\} + \sqrt{Var\{ r(t_i) | \mathcal{F}_{i-1} \}} * Z`,

    where :math:`E\{r(t_i) | \mathcal{F}_{i-1}\}`, the expected value of
    :math:`r(t_i)` conditional on :math:`\mathcal{F}_{i-1}` is calculated by :meth:`E_rt_s(i-1, i)<E_rt_s>`,
    :math:`Var\{ r(t_i) | \mathcal{F}_{i-1} \}` the variance of :math:`r(t_i)` conditional on :math:`\mathcal{F}_{i-1}`
    is calculated by :meth:`Var_rt_s(i-1, i)<Var_rt_s>`,
    and :math:`Z`, a random number drawn from :math:`\mathcal{N}(0, 1)`
    a standard normal distribution calculated by :meth:`std_norm_rand`.

    .. seealso::
        * :attr:`scen_size`
        * :meth:`mkt_fwd`
        * :meth:`E_rt_s`
        * :meth:`Var_rt_s`
        * :meth:`std_norm_rand`
        * :attr:`seed1`
    """
    if i == 0:
        return np.full(scen_size, mkt_fwd(0))
    else:
        return E_rt_s(i-1, i) + Var_rt_s(i-1, i)**0.5 * std_norm_rand(seed1)[:, i-1]


def short_rate_paths():
    """Short rate paths.

    Returns, as a 2D numpy array, the simulated short rate paths
    for all scenarios.

    .. seealso::
        * :meth:`short_rate`
    """
    return np.array([short_rate(i) for i in range(step_size + 1)]).transpose()


def std_norm_rand(seed=1234):
    """Random numbers from the standard normal distribution.

    Returns a numpy array shaped :attr:`scen_size` x :attr:`step_size`.
    The elements are random numbers drawn from the standard normal distribution.
    """

    size = (scen_size, step_size)

    if hasattr(np.random, 'default_rng'):
        gen = np.random.default_rng(seed)
        return gen.standard_normal(size)
    else:
        np.random.seed(seed)
        return np.random.standard_normal(size)


t_ = lambda i: i * time_len / step_size
"""time index :math:`t_i`"""

def var_short_rate():
    """Variance of generated short rates

    Returns, as a vector in a numpy array, the variances of
    the generated short rates for all :math:`t_i`.
    This should converge to the theoretical variances
    calculated by :meth:`Var_rt`.

    .. seealso::
        * :meth:`short_rate`
        * :meth:`Var_rt`

    """
    return np.array([np.var(short_rate(i)) for i in range(step_size + 1)])


# ---------------------------------------------------------------------------
# References

np = ("Module", "numpy")

step_size = 360

time_len = 30

a = 0.1

sigma = 0.1

seed1 = 1234

seed2 = 5678

scen_size = 1000