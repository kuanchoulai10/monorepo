# Stat

!!! question "What is Variational Inference?"

    ??? tip "Answer"

        Variational inference is a technique used in machine learning and statistics to approximate complex probability distributions. Instead of trying to directly compute the distribution, which can be intractable, variational inference turns the problem into an optimization task. It involves selecting a simpler, known distribution and adjusting its parameters so that it closely approximates the complex distribution. This makes it easier and faster to perform inference in models that would otherwise be too complex to handle.


!!! question "What's the relationship between variational inference and Bayesian statistics?"

    ??? tip "Answer"

        Variational inference is actually closely related to Bayesian statistics because it provides a way to **approximate the posterior distribution of a model's parameters**. In Bayesian statistics, we start with **a prior distribution that represents our initial beliefs about the parameters**, and then **we update that with observed data to get the posterior distribution**. Often, the **exact posterior is difficult or impossible to calculate**, so variational inference steps in as an efficient way to approximate that posterior. So it's basically a practical tool within the Bayesian framework.


!!! question "What is Markov Chain?"

    ??? tip "Answer"

    A Markov Chain is a mathematical system that undergoes transitions from one state to another within a finite or countably infinite set of states. The key property of a Markov Chain is that **it follows the Markov property, which means that the probability of transitioning to the next state depends only on the current state and not on the sequence of states that came before it**. Essentially, it's a **memoryless process**, which makes it simpler to analyze and model.


!!! question "What are some common MCMC methods?"

    ??? tip "Answer"

    Some of the most common MCMC methods include the **Metropolis-Hastings algorithm**, which is a very general and flexible approach where you propose a new sample and then decide whether to accept it based on a certain acceptance probability.
    
    Another popular method is the **Gibbs sampler**, which **is particularly useful when you can easily sample from the conditional distributions of each variable one at a time**.


!!! question "what is p-value?"

    ??? tip "Answer"

    The p-value is a concept used in statistical hypothesis testing. It's basically a measure that helps you understand the strength of your evidence against a null hypothesis. So when you perform a test, the p-value tells you how likely it is to get your observed results, or something more extreme, if the null hypothesis is actually true. A smaller p-value means that your observed data is less likely under the null hypothesis, which often leads researchers to reject the null hypothesis.

    in hypothesis testing, the null hypothesis is kind of like the "innocent until proven guilty" principle. We start by assuming that the null hypothesis is true, just like we presume innocence. The evidence, or our data, has to be strong enough to reject that null hypothesis. If the p-value is small, it’s like having strong evidence in a trial, which means we might reject the null hypothesis. If the p-value is large, then the evidence isn't strong enough, and we continue to assume the null hypothesis is true, just like we would maintain someone's innocence in a legal context.

    if we think of hypothesis testing like a courtroom, the presumption of innocence means we start by assuming the defendant (or the null hypothesis) is innocent, or true. A Type I error would be like wrongly convicting an innocent person, which is rejecting the null hypothesis when it’s actually true. This is considered a serious error because it means we’re concluding there’s an effect or a difference when there really isn’t one. A Type II error would be like letting a guilty person go free, which means failing to reject the null hypothesis when it’s actually false. This is still an error, but often considered less severe than a Type I error, depending on the context. The presumption of innocence helps ensure that we only reject the null hypothesis when we have strong enough evidence, reducing the likelihood of those more costly Type I errors.


!!! question "What are the differences and similarities between Frequentist and Bayesian statistics?"

    ??? tip "Answer"

    the main difference lies in **how they interpret probability**.

    Frequentist statistics **views probability as the long-run frequency of events**. Essentially, it's about **how often something happens if you repeat an experiment over and over again**. Bayesian statistics, on the other hand, **interprets probability as a measure of belief or certainty about an event**. **It incorporates prior knowledge or prior beliefs, and then updates that belief as more evidence or data becomes available**.

    As for similarities, both approaches **use data to make inferences and predictions**, and they both **rely on likelihood functions** to connect models with data. Ultimately, they just have different philosophies on what probability means and how to use it!


!!! question "what's the differences between sequential testing and Bayesian-based statistical method when talking about A-B testing?"

    ??? tip "Answer"

    both sequential testing and Bayesian methods can be used for A/B testing, but they have different approaches. Sequential testing usually follows a frequentist framework, where you analyze the data as it comes in and you can stop the test early if you reach a certain level of statistical significance. The main advantage here is efficiency, because you don't need to fix a sample size in advance.

    Bayesian A/B testing, on the other hand, involves updating your beliefs about which variation is better as new data comes in. Instead of focusing on p-values and significance thresholds, you look at the probability that one variant is better than the other. This approach is more flexible and intuitive for many people, because it provides a direct probability statement about your results. So, in summary, sequential testing is about efficiency in a frequentist framework, while Bayesian A/B testing focuses on continuously updating probabilities and beliefs.