# What is an Algorithm?
- The idea behind computer programs
- An algorithm has to solve a general, specified problem.
- An algorithm problem is specified by describing the set of instances it must work on, and what desired properties the output must have.
<br></br>

# Correct and Efficient
- A faster algorithm running on a slower computer will *always* win for sufficiently large instances.
- Usually, problems don't have to get that large before the faster algorithm wins.
<br></br>

# Correctness
- Algorithm correctness is not obvious in many optimization problems.
- Algorithm problems must be carefully specified to allow a provably correct algorithm to exist.
<br></br>

# Expressing Algorithms
- Natural languages such as English or Korean, pseudocode, real programming languages
<br></br>

# Proof and Counterexample
## Demonstrating Incorrectness
Searching for counterexamples is the best way to disprove the correctness of a heuristic.
- Think about all small examples.
- Think about examples with ties on your decision criteria (e.g. pick the nearest point)
- Think about examples with extremes of big and small.
<br></br>

## Induction and Recursion
- Failure to find a counterexample to a given algorithm does not mean "it is obvious" that the algorithm is correct.
- Mathematical induction is a very useful method for providing the correctness of recursive algorithms.
- Recursion and induction are the same basic idea:
    1. basis case
    2. general assumption
    3. general case
$$\sum_{i = 1}^{n}{i} = n(n + 1)/2$$