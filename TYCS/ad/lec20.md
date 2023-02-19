# Satisfiability
Consider the following logic problem:
- Instance: A set $V$ of variables and a set of clauses $C$ over $V$.
- Question: Does there exist a satisfying truth assignment for $C$?
- Example 1: $V = v_1, v_2$ and $C = \{\{v_1, \bar{v_2}\}, \{\bar{v_1}, v_2\}\}$

A clause is satisfied when at least one literal in it is true. $C$ is satisfied when $v_1=v_2=$ true.
<br></br>

## Not Satisfiable
Example 2: $V = v_1, v_2, \ \ C=\{\{v_1, v_2\}, \{v_1, \bar{v_2}\}, \{\bar{v_1}\}\}$

- Although you try and try, you can get no satisfaction.
- There is no satisfying assignment since $v_1$ must be false (third clause), so $v_2$ must be false (second clause), but then the first clause is unsatisfiable!
<br></br>

## Satisfiability is Hard
- Satisfiability is known/assumed to be a hard problem.
- Every top-notch algorithm expert in the world has tried and failed to come up with a fast algorithm to test whether a given set of clauses is satisfiable.
- Further, many strange and impossible-to-believe things have been shown to be true if someone in fact did find a fast satisfiability algorithm.
<br></br>

# 3-Satisfiability
- Instance: A collection of clause $C$ where each clause contains *exactly* 3 literals, boolean variable $v$.
- Question: Is there a truth assignment to $v$ so that each clause is satisfied?
<br></br>

## 3-SAT is NP-Complete
To prove it is complete, we give a reduction from $Sat\propto 3-Sat$. We will transform each clause independantly based on its *length*.<br></br>
Suppose the clause $C_i$ contains $k$ literals.
- If $k = 1$, meaning $C_i = \{z_1\}$, create two new variables $v_1, \ \ v_2$ and four new 3-literal clauses:
$$\{v_1, v_2, z_1\}, \{v_1, \bar{v_2}, z_1\}, \{\bar{v_1}, v_2, z_1\}, \{\bar{v_1}, \bar{v_2}, z_1\}$$
$\qquad$ Note that the only way all four of these can be satisfied is if $z$ is true.<br>
- If $k = 2$, meaning $\{z_1, z_2\}$, create one new variable $v_1$ and two new clauses: $\{v_1, z_1, z_2\}, \{\bar{v_1}, z_1, z_2\}$
- If $k = 3$, meaning $\{z_1, z_2, z_3\}$, copy into the 3-SAT instance as it is.
- If $k > 3$, meaning $\{z_1, z_2, \cdots , z_n\}$, create $n - 3$ new variables and $n - 2$ new clauses in a chain: $\{v_i, z_i, \bar{v_i}\}, \cdots$
<br></br>

## Why does the Chain Work?
- If none of the original variables in a clause are true, there is no way to satisfy all of them using the additional variable:
$$(F, F, T), (F, F, T), \cdots , (F, F, F)$$
- But if any literal is true, we have $n - 3$ free variables and $n - 3$ remaining 3-clauses, so we can satisfy all clauses.
- $(F, F, T), (F, F, T), \cdots , (\bold{F}, \bold{T}, \bold{F}), \cdots , (T, F, F), (T, F, F)$
- Any SAT solution will also satisfy the 3-SAT instance and any 3-SAT solution sets variables giving a SAT solution, so the problems are equivalent.\
<br></br>

## 4-Sat and 2-Sat
- A slight modification to this construction would prove 4-SAT, or 5-SAT,... also NP-complete.
- However, it breaks down when we try to use it for 2-SAT, since there is no way to stuff anything into the chain of clauses.
<br></br>

# Vertex Cover
## The Power of 3-SAT