# Type I and Type II Errors

When performing a hypothesis test, two kinds of mistakes are possible: concluding that an effect exists when it does not, or missing a real effect. These mistakes — Type I and Type II errors — have direct consequences for scientific conclusions and decision-making. This section defines both error types, quantifies their probabilities, and examines the fundamental trade-off between them.

!!! tip "Mental Model"
    Type I is a false alarm (convicting an innocent person); Type II is a missed detection (letting a guilty person go free). Lowering one error rate raises the other unless you increase the sample size. The significance level $\alpha$ directly controls the Type I rate, while power $1 - \beta$ controls the Type II rate.

## Type I Error (False Positive)

A **Type I error** occurs when the null hypothesis $H_0$ is true, but the test incorrectly rejects it. Informally, this is a "false alarm" — we declare a significant result when there is actually no effect.

The probability of a Type I error is denoted by $\alpha$ and equals the significance level of the test:

$$
\alpha = P(\text{reject } H_0 \mid H_0 \text{ is true})
$$

The value of $\alpha$ is chosen by the analyst before conducting the test. A common choice is $\alpha = 0.05$, meaning we accept a 5% chance of falsely rejecting a true null hypothesis.

!!! example "Type I Error in Practice"
    A pharmaceutical company tests whether a new drug lowers blood pressure more than a placebo. If the drug has no real effect ($H_0$ is true) but the test yields $p < 0.05$, the company would incorrectly conclude the drug works. This false positive could lead to costly clinical trials of an ineffective treatment.

## Type II Error (False Negative)

A **Type II error** occurs when the alternative hypothesis $H_1$ is true, but the test fails to reject $H_0$. This means a real effect goes undetected.

The probability of a Type II error is denoted by $\beta$:

$$
\beta = P(\text{fail to reject } H_0 \mid H_1 \text{ is true})
$$

Unlike $\alpha$, the value of $\beta$ is generally not fixed directly. Instead, it depends on the true effect size, the sample size $n$, the chosen significance level $\alpha$, and the variability in the data.

!!! example "Type II Error in Practice"
    Continuing the drug trial example, suppose the drug truly does lower blood pressure by a small amount. If the sample size is too small to detect this modest effect, the test fails to reject $H_0$, and the effective drug is incorrectly deemed no better than a placebo.

## Power and the Error Trade-off

The **power** of a test is the probability of correctly rejecting $H_0$ when $H_1$ is true:

$$
\text{Power} = 1 - \beta = P(\text{reject } H_0 \mid H_1 \text{ is true})
$$

Higher power means a lower chance of missing a real effect. A conventional target is power $\geq 0.80$, meaning at most a 20% chance of a Type II error.

The key trade-off in hypothesis testing is that, for a fixed sample size, decreasing $\alpha$ (making the test more conservative) increases $\beta$ (making it harder to detect real effects), and vice versa. The only way to reduce both error rates simultaneously is to increase the sample size $n$ or to study a larger effect size.

The following table summarizes the four possible outcomes of a hypothesis test:

|  | $H_0$ is true | $H_1$ is true |
|---|---|---|
| **Reject** $H_0$ | Type I error (prob. $\alpha$) | Correct decision (prob. $1 - \beta$) |
| **Fail to reject** $H_0$ | Correct decision (prob. $1 - \alpha$) | Type II error (prob. $\beta$) |

## Summary

Type I errors (false positives, probability $\alpha$) and Type II errors (false negatives, probability $\beta$) represent the two fundamental mistakes in hypothesis testing. The power of a test, $1 - \beta$, measures its ability to detect a true effect, and the trade-off between $\alpha$ and $\beta$ is governed by sample size and effect size.

---

## Exercises

**Exercise 1.**
Simulate the Type I error rate: run 10,000 one-sample t-tests with data drawn from $N(0, 1)$ (i.e., $H_0$ is true, testing $\mu = 0$). Count how many reject at $\alpha = 0.01, 0.05, 0.10$ and verify the rejection rates match the nominal levels.

??? success "Solution to Exercise 1"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        p_values = []
        for _ in range(10000):
            data = np.random.normal(0, 1, 30)
            _, p = stats.ttest_1samp(data, 0)
            p_values.append(p)
        p_values = np.array(p_values)

        for alpha in [0.01, 0.05, 0.10]:
            rate = np.mean(p_values < alpha)
            print(f"alpha={alpha}: rejection rate={rate:.4f}")

---

**Exercise 2.**
Simulate the Type II error rate: run 10,000 t-tests with data from $N(0.3, 1)$ and $n = 30$ (i.e., $H_0: \mu = 0$ is false). Compute the proportion of times $H_0$ is not rejected at $\alpha = 0.05$ (this is the Type II error rate $\beta$), and the power $1 - \beta$.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        not_rejected = 0
        for _ in range(10000):
            data = np.random.normal(0.3, 1, 30)
            _, p = stats.ttest_1samp(data, 0)
            if p >= 0.05:
                not_rejected += 1
        beta = not_rejected / 10000
        print(f"Type II error rate (beta): {beta:.4f}")
        print(f"Power (1-beta): {1-beta:.4f}")

---

**Exercise 3.**
Show the trade-off between Type I and Type II errors by computing the power of a one-sample t-test ($n = 25$, true $\mu = 0.4$, $\sigma = 1$) at significance levels $\alpha = 0.001, 0.01, 0.05, 0.10$ using `statsmodels.stats.power.tt_solve_power()`.

??? success "Solution to Exercise 3"

        from statsmodels.stats.power import tt_solve_power

        for alpha in [0.001, 0.01, 0.05, 0.10]:
            power = tt_solve_power(effect_size=0.4, nobs=25, alpha=alpha,
                                   alternative='two-sided')
            print(f"alpha={alpha:.3f}: power={power:.4f}")
