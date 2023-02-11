# Multiplication and the Big Oh
## Big Oh Multiplication by Constant
Multiplication by a constant does not change the asymptotics:
$$ O(c\cdot f(n)\rightarrow O(f(n)))$$
$$\Omega (c\cdot f(n))\rightarrow \Omega (f(n))$$
$$\Theta (c\cdot f(n))\rightarrow \Theta (f(n))$$

The "old constant" $C$ from the Big Oh becomes $c\cdot C$.

## Big Oh Multiplication by Function
But when both functions in a product are increasing, both are important.
$$O(f(n))\cdot O(g(n))\rightarrow O(f(n)\cdot g(n))$$
$$\Omega (f(n))\cdot \Omega (g(n))\rightarrow \Omega (f(n)\cdot g(n))$$
$$\Theta (f(n))\cdot \Theta (g(n))\rightarrow \Theta (f(n)\cdot g(n))$$

This is why the running time of two nested loops is $O(n^2)$

# Analyzing Algorithms: Selection and Insertion Sort
## Reasoning About Efficiency
- Grossly reasoning about the running time of an algorithm is usually easy given a precise-enough written description of the algorithm.
- When you *really* understand an algorithm, this analysis can be done in your head. However, recognize there is always implicitly a written algorithm/program we are reasoning about.

## Selection Sort
```c
void selection_sort(item_type s[], int n) {
    int i, j;    /* counters */
    int min;     /* index of minimum */

    for (i = 0; i < n; i++) {
        min = i;
        for (j = i + 1; j < n; j++) {
            if (s[j] < s[min]) {
                min = j;
            }
        }
        swap(&s[i], &s[min]);
    }
}
```

## Worst Case Analysis
- The outer loop goes around $n$ times.
- The inner loop goes around at most $n$ times *for each* iteration of the outer loop.
- Thus selection sort takes at most $n\times n\rightarrow O(n^2)$ time in the worst case.
- In fact, it is $\Theta (n^2)$, because at least $n/2$ times it scans through at least $n/2$ elements, for a total of at least $n^2/4$ steps.

## More Careful Analysis
- An exact count of the number of times the *if* statement is executed is given by:
$$S(n) = \sum_{i = 0}^{n - 1}{\sum_{j = i + 1}^{n - 1}{1}} = \sum_{i = 0}^{n - 1}{(n - i + 1)} = \sum_{i = 0}^{n - 1}{i}$$
$$S(n) = (n - 1) + (n - 2) + (n - 3) + \cdots + 2 + 1 = n(n + 1) / 2$$
- Thus, the worst case running time is $\Theta (n^2)$

## Insertion Sort
```c
    void insertion_sort(item_type s[], int n) {
        int i, j;    /* counters */

        for (i = 1; i < n; i++) {
            j = i;
            while ((j > 0) && (s[j] < s[j - 1])) {
                swap(&s[j], &s[j - 1]);
                j = j - 1;
            }
        }
    }
```
- This involves a while loop, so the analysis is less mechanical.
- But $n$ calls to an inner loop which takes at most $n$ steps on each call is $O(n^2)$.
- The reverse-sorted permutation proves that the worst-case complexity is $\Theta (n^2)$: $(10, 9, 8, 7, 6, 5, 4, 3, 2, 1)$

# Asymptotic Dominance
## Implications of Dominance
- Exponential algorithms get hopeless fast.
- Quadratic algorithms get hopeless at or before 1,000,000.
- $O(n\log{n})$ is possible to about one billion.
- $O(\log{n})$ never sweats.

## Testing Dominance
- $f(n)$ dominates $g(n)$ if $\lim_{n \to \infty}{g(n)/f(n)} = 0$, which is the same as saying $g(n)=o(f(n))$.
- Note the little-oh: it means "grows strictly slower than"

## Properties of Dominance
- $n^a$ dominates $n^b$ if $a > b$ since
$$\lim_{n \to \infty}{n^b/n^a} = n^{b - a} \to 0$$

- $n^a + o(n^a)$ doesn't dominate $n^a$ since
$$\lim_{n \to \infty}{n^a/(n^a + o(n^a))} \to 1$$


## Dominance Rankings
You must come to accept the dominance ranking of the basic function:
$$n! \gg 2^n \gg n^3 \gg n^2 \gg n\log{n} \gg n \gg \log{n} \gg 1$$

## Advanced Dominance Rankings
Additional functions arise in more sophiscated analysis.
$$n! \gg c^n \gg n^3 \gg n^2 \gg n^{1+\epsilon} \gg n\log{n} \gg n \gg \sqrt{n} \gg$$
$$\log^2{n} \gg \log{n} \gg \log{n}/\log{\log{n}} \gg \log{\log{n}} \gg \alpha{(n)} \gg 1$$

# Logarithms
- It is important to understand deep in your bones what logarithms are and where they come from.
- A logarithm is simply an inverse exponential function.
- Saying $b^x = y$ is equivalent to saying that $x = \log_b{y}$.
- Logarithms reflect how many times we can double something until we get to $n$, or halve something until we get to 1.

## Binary Search
- In binary search we throw away half the possible number of keys after each comparison.
- How many time can we halve $n$ before getting to 1? $\to \lg{n}$

## Logarithms and Trees
- How tall a binary tree do we need until we have $n$ leaves?
- The number of potential leaves doubles with each level.
- How many times can we double 1 until we get to $n$? $\to \lg{n}$

## Logarithms and Bits
- How many bits do you need to represent the numbers from $0$ to $2^i - 1$?
- Each bit you add doubles the possible number of bit patterns, so the number of bits equals $\lg{2^i} = i$

## Logarithms and Multiplication
$$\log_a{(xy)} = \log_a{(x)} + \log_a{(y)}$$
- This is how people used to multiply before calculators, and remains useful for analysis.
- What if $x = a$?

## The Base is not Asymptotically Important
- Recall the definition, $c^{\log_c{x}} = x$ and that
$$\log_b{a} = \frac{\log_c{a}}{\log_c{b}}$$
- Thus, $\log_2{n} = (1/\log_{100}{2})\times \log_{100}{n}$. Since $1/\log_{100}{2} = 6.643$ is just a constant, it does not matter in the Big Oh.