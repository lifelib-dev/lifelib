<h1 align="center" style="border-botom: none">
  <b>
  🐍 Bayesian validation of the Economic Scenario Generator using Black-Sholes-Merton model 🐍
 </b>
</h1>

</br>

Economic Scenario Generators simulate potential future paths of financial indicators such as interest rates, indices and spreads. Most of them do this by assuming that the economy behaves according to a certain stochastic process and present multiple sample paths of this process.

To simulate this, the code bellow generates 1000 scenarios from the Black-Sholes-Merton model. Each scenario simulates 50 years in annual increments.

To calculate the most likely parameters used to generate the scenarios, the Maximum Likelihood method is normaly used.
This method could be used in this case since the normal distribution has a well known solution. However there are cases where the maximum likelihood estimator does not have a closed solution. 

What is required is to know a function that is able to tell, how much more likely is that the observed data came from one set of parameters as opposed to another set.

A possible solution to this is to use the [Metropolis Hastings](https://en.wikipedia.org/wiki/Metropolis%E2%80%93Hastings_algorithm) algorithm. To directly quote Wikipedia:

In statistics and statistical physics, the Metropolis–Hastings algorithm is a Markov chain Monte Carlo (MCMC) method for obtaining a sequence of random samples from a probability distribution from which direct sampling is difficult. This sequence can be used to approximate the distribution.

<b> The distribution of interest is the distribution of most likely parameter combinations.</b>  

If the likelihood function is corectly implemented, the distribution should peak at the parameter set, that was set up in the ESG run.
