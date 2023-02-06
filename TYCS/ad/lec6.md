# Hash tables
- *A very practical* way to maintain a dictionary.
- The idea i simply that looking an item up on an array is $\Theta{(1)}$ once you have its index.
- A hash function is a mathematical function which maps keys to integers.
<br></br>

## Collisions
- The set of keys mapped to the same bucket.
- If the keys are uniformly distributed, then each bucket should contain very few keys.
- The resulting short lists are easily searched.
<br></br>

## Collision Resolution by Chaining
- Chaining is easy, but devotes a considerable amount of memory to pointers, which could be used to make the table larger.
- Insertion, deletion, and query reduce to the problem in linked lists.
If the $n$ keys are distributed uniformly in a table of size $m/n$, each operation takes $O(m/n)$ time.
<br></br>

## Open Addressing
- We can dispense with all these pointers by using an implicit reference derived from a simple function:

|0|1|2|3|4|5|6|7|8|9|
|---|---|---|---|---|---|---|---|---|---|
|34|5|55|21||2||3|8|13|

- If the space we want is filled, we try the next location:
    - Sequentially $h, h + 1, h + 2, \cdots$
    - Quadratically $h, h + 1^2, h + 2^2, h + 3^2, \cdots$
    - Linearly $h, h + k, h + 2k, h + 3k, \cdots$
- Deletion in an open addressing scheme is ugly, since removing one element can break a chain of insertions, making some elements inaccessible.
<br></br>

## Hash Functions
- It is the job of the hash function to map keys to integers.
- A good hash function:
    1. Is cheap to evaluate
    2. Tends to use all positions from $0\cdots M$ with uniform frequency.
- The first step is usually to map the key to a big integer, for example
$$h = \sum_{i = 0}^{keylength}{128^i\times char(key[i])}$$
<br></br>

## Modular Arithmetic
- This large number must be reduced to an integer whose size is between 1 and the size of hash table.
- One way is by $h(k) = k \mod M$, where $M$ is best a large prime not too close to $2^i - 1$, which would just mask off the high bits.
<br></br>

# Birthday Paradox
- No matter how good a hash function is, we had batter be prepared for collisions, because of the birthday paradox.
- The probability of there being *no* collisions after *n* insertions into an *m*-element table is
$$(m / m)\times ((m - 1)/m)\times \cdots \times ((m - n + 1)/m) = \prod_{i = 0}^{n - 1}{(m - i)/m}$$
<br></br>

# Applications of Hashing
## Performance on Set Operations
- With either chaining or open addressing:
    - Search - $O(1)$ expected, $O(n)$ worst case
    - Insert - $O(1)$ expected, $O(n)$ worst case
    - Delete - $O(1)$ expected, $O(n)$ worst case
    - Min, Max and Predecessor, Successor $\Theta (n + m)$ expected and worst case
- Pragmatically, a hash table is often the best data structure to maintain a dictionary.
- However, the worst-case time is unpredictable.
- The best worst-case bounds come from balanced binary trees.
<br></br>

## Hashing, Hashing, and Hashing
- Udi Manber says that the three most important algorithms at Google are hashing, hashing, and hashing.
- Hashing has a variety of clever applications beyond just speeding up search, by giving you a short but distinctive representation of a larger document.
    - *Is this new document different from the rest in a large corpus?* - Hash the new document, and compare it to the hash codes of corpus.
    - *Is part of this document plagerized from part of a document in a large corpus?* - Hash overlapping windows of length $w$ in the document and the corpus. If there is a match of hash codes, there is possibly a text match.
    - *How can I convince you that a file isn't changed?* - Check if the cryptographic hash code of the file you give me today is the same as that of the original. Any changes to the file will change the hash code.
<br></br>

## Hashing as a Representation
- Custom-designed hashcodes can be used to bucket items by a cannonical representation.
    - Which five letters of the alphabet can make the most different words?
    - Hash each word by the letters it contains: $lemon\to molen$ Observe that $dog$ and $god$ collide.
- Proximity-preserving hashing techniques put similar items in the same bucket.
- Use hashing for everything, except worst-case analysis.
<br></br>

# The Rabin-Karp Algorithm
## Substring Pattern Matching
- Input: A text string $\texttt{t}$ and a pattern string $\texttt{p}$.
- Problem: Does $\texttt{t}$ contain the pattern $\texttt{p}$ as a substring, and if so where?
<br></br>

## Brute Force Search
- The simplest algorithm to search for the presence of pattern string $\texttt{p}$ in text $\texttt{t}$ overlays the pattern string at every position in the text, and checks whether every pattern character matches the corresponding text character.
- This runs in $O(nm)$ time, where $n = |t|$ and $m = |p|$.
<br></br>

## String Matching via Hashing
- Suppose we compute a given hash function on both the pattern string $\texttt{p}$ and the $m$-character substring starting from the $\texttt{i}$th position of $\texttt{t}$.
- If these two strings are identical, clearly the resulting hash values will be the same.
- If the two strings are different, the hash values will *almost certainly* be different.
- These false positives should be so rare that we can easily spend the $O(m)$ time it take to explicitly check the identity of two strings whenever the hash values agree.
<br></br>

## The Catch
- This reduces string matching to $n - m + 2$ hash value computations (the $n - m + 1$ windows of $\texttt{t}$, plus one hash of $\texttt{p}$), plus what *should be* a very small number of $O(m)$ time verification steps.
- The catch is that it takes $O(m)$ time to compute a hash function on an $m$-character string, and $O(n)$ such computations seems to leave us with an $O(mn)$ algorithm again.
<br></br>

## The Trick
- Look closely at our string hash function, applied to the $m$ characters starting from the $\texttt{j}$th position of string $\texttt{S}$:
$$H(S, j) = \sum_{i = 0}^{m - 1}{\alpha ^{m - (i + 1)}\times char(s_{i + j})}$$
- A little algebra reveals that
$$H(S, j + 1) = (H(S, j) - \alpha^{m - 1} char(s_j))\alpha + s_{j + m}$$
- Thus once we know the hash value from the $\texttt{j}$ position, we can find the hash value from the $\texttt{(j + 1)}$st position for the cost of two multiplications, one addition, and one subtraction.
- This can be done in constant time.