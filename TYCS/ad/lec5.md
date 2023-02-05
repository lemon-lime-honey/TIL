# Binary Search Trees
- Binary search trees provide a data structure which efficiently supports all six dictionary operations.
- A binary tree is a rooted tree where each node contains at most two children.
- Each child can be identified as either a left or right child.

```mermaid
%%{init: {'theme':'neutral'}}%%
graph TB
    classDef parent fill:#003153, color:#AEFF6E, stroke-width:1px, stroke:#FFF700
    classDef left_child fill:#003153, color:#EBA937, stroke-width:1px, stroke:#FFF700
    classDef right_child fill:#003153, color:#FFF700, stroke-width:1px, stroke:#FFF700

    A((1)):::parent --left child--> B((2)):::left_child
    A --right child--> C((3)):::right_child
    B --> E((4))
    B --> F((5))
    C --> H((6))
    C --> I((7))
    H --> J((8))
    H --> K((9))
```

- A binary *search* tree labels each node $\texttt{x}$ in a binary tree such that all nodes in the left subtree of $\texttt{x}$ have keys $\texttt{<x}$ and all nodes in the right subtree of $\texttt{x}$ have keys $\texttt{>x}$.

```mermaid
%%{init: {'theme':'neutral'}}%%
graph TB
    A((8))-->B((3))
    A-->C((10))
    B-->D((1))
    B-->E((6))
    C-->F((9))
    C-->G((14))
    E-->H((4))
    E-->I((7))
```
- The search tree labeling enables us to find where any key is.
<br></br>

## Implementing Binary Search Trees
```c
typedef struct tree {
    item_type item;        /* data item */
    struct tree *parent;   /* pointer to parent */
    struct tree *left;     /* pointer to left child */
    struct tree *right;    /* pointer to right child */
} tree;
```
The parent link is optional, since we can usually store the pointer on a stack when we encounter it.
<br></br>

## Searching in a Binary Tree: Implementation
```c
tree *search_tree(tree *l, item_type x) {
    if (l == NULL) {
        return(NULL);
    }
    if (l->item == x) {
        return(l);
    }
    if (x < 1->item) {
        return(search_tree(l->left, x));
    } else {
        return(search_tree(l->right, x));
    }
}
```
<br></br>

## Searching in a Binary Tree: How Much Time?
- The algorithm works because both the left and right subtrees of a binary search tree *are* binary search trees - recursive structure, recursive algorithm.
- This takes time proportional to the height of the tree, $O(h)$.
<br></br>

# Operations on Binary Search Trees
## Maximum and Minimum
```mermaid
%%{init: {'theme':'neutral'}}%%
graph TB
    classDef ref fill:#003153, color:#AEFF6E, stroke-width:1px, stroke:#FFF700
    classDef min fill:#003153, color:#EBA937, stroke-width:1px, stroke:#FFF700
    classDef max fill:#003153, color:#FFF700, stroke-width:1px, stroke:#FFF700

    A((8)):::ref-->B((3))
    A-->C((12))
    B--min-->D((1)):::min
    B-->E((6))
    C-->F((10))
    C--max-->G((14)):::max
    F-->H((9))
    F-->I((11))
```
<br></br>

## Finding the Minimum
```c
tree *find_minimum(tree *t) {
    tree *min;       /* pointer to minimum */

    if (t == NULL) {
        return(NULL);
    }
    min = t;
    while (min->left != NULL) {
        min = min->left;
    }
    return(min);
}
```
Finding the max or min takes time proportional to the height of the tree, $O(h)$.
<br></br>

## Where is the Predecessor?: Internal Node
```mermaid
%%{init: {'theme':'neutral'}}%%
graph TB
    classDef target fill:#003153, color:#AEFF6E, stroke-width:1px, stroke:#FFF700
    classDef pred fill:#003153, color:#EBA937, stroke-width:1px, stroke:#FFF700
    classDef succ fill:#003153, color:#FFF700, stroke-width:1px, stroke:#FFF700

    A((8))-->B((4)):::target
    A-->C((10))
    B-->D((2))
    B-->E((6))
    C-->F((9))
    C-->G((14))
    D-->H((1))
    D--predecessor-->I((3)):::pred
    E--successor-->J((5)):::succ
    E-->K((7))
```
If $\texttt{X}$ has two children, its predecessor is the maximum value in its left subtree and its successor the minimum value in its right subtree.
<br></br>

## Where is the Successor?: Leaf Node
```mermaid
%%{init: {'theme':'neutral', 'flowchart': {'curve': 'linear'}}}%%
graph TB
    classDef invisible opacity:0.0
    classDef blank color:#EEEEEE
    classDef target fill:#003153, color:#AEFF6E, stroke-width:1px, stroke:#FFF700
    classDef pred fill:#003153, color:#EBA937, stroke-width:1px, stroke:#FFF700

    A((A)):::blank-->B((P)):::pred
    A---Z((Z)):::invisible
    B---Y((Y)):::invisible
    B-->C((C)):::blank
    C-->D((D)):::blank
    C---X((X)):::invisible
    D-->E((E)):::blank
    D---W((W)):::invisible
    E-->F((X)):::target
    E---V((V)):::invisible
    F---U((U)):::invisible
    F-->G((G)):::blank

    linkStyle 1 stroke-width:0px;
    linkStyle 2 stroke-width:0px;
    linkStyle 5 stroke-width:0px;
    linkStyle 7 stroke-width:0px;
    linkStyle 9 stroke-width:0px;
    linkStyle 10 stroke-width:0px;
```
- If it does not have a left child, a node's predecessor is its first left ancestor.
- The proof of correctness comes from looking at the in-order traversal of the tree.
<br></br>

## In-Order Traversal
```mermaid
%%{init: {'theme':'neutral', 'flowchart': {'curve': 'linear'}}}%%
graph TB
    classDef invisible opacity: 0.0

    H((H))-->A((A))
    H((H))---X((X)):::invisible
    A---Y((Y)):::invisible
    A-->F((F))
    F-->B((B))
    F-->G((G))
    B---Z((Z)):::invisible
    B-->D((D))
    D-->C((C))
    D-->E((E))

    linkStyle 1 stroke-width:0px;
    linkStyle 2 stroke-width:0px;
    linkStyle 6 stroke-width:0px;
```

```c
void traverse_tree(tree *l) {
    if (l != NULL) {
        traverse_tree(l->left);
        process_item(l->item);
        traverse_tree(l->right);
    }
}
```
- This traversal visits the nodes in $ABCDEFGH$ order.
- Because it spends $O(1)$ time at each of $n$ nodes in the tree, the total time is $O(n)$.
<br></br>

# Insertion and Deletion
## Tree Insertion
- Do a binary search to find where it should be, then replace the termination $\texttt{NIL}$ pointer with the new item.
```mermaid
%%{init: {'theme':'neutral'}}%%
graph TB
    classDef invisible opacity:0.0
    classDef blank color:#EEEEEE
    classDef accent fill:#003153, color:#FFF700, stroke:#FFF700

    A((A)):::blank-->B((A)):::blank
    A-->C((A)):::blank
    B-->D((A)):::blank
    B-->E((A)):::blank
    E-->X((X)):::accent
    E---Y((Y)):::invisible
    C-->F((A)):::blank
    C-->G((A)):::blank
    F-->H((A)):::blank
    F-->I((A)):::blank
    
    linkStyle 0 stroke:#AEFF6E
    linkStyle 3 stroke:#AEFF6E
    linkStyle 4 stroke:#AEFF6E
    linkStyle 5 stroke-width:0px;
```
- Insertion takes time proportional to tree height, $O(h)$.
<br></br>

## Tree Insertion Code
```c
void insert_tree(tree **l, item_type x, tree *parent) {
    tree *p;    /* temporary pointer */

    if (*l == NULL) {
        p = malloc(sizeof(tree));
        p->item = x;
        p->left = p->right = NULL;
        p->parent = parent;
        *l = p;
        return;
    }
    if (x < (*l)->item) {
        insert_tree(&((*l)->left), x, *l);
    } else {
        insert_tree(&((*l)->right), x, *l);
    }
}
```
<br></br>

## Tree Deletion
- Deletion is trickier than insertion, because the node to die may not be a leaf, and thus effect other nodes.
- There are three cases:
    - Case (a), where the node is a leaf, is simple: just $\texttt{NIL}$ out the parents child pointer.
    - Case (b), where a node has one child, the doomed node can just be cut out.
    - Case (v), relabel the node as its successor (which has at most one child when $x$ has two children!) and delete the successor!
<br></br>

## Cases of Deletion
```mermaid
%%{init: {'theme':'neutral'}}%%
graph TD
    classDef invisible opacity:0.0
    classDef lemon fill:#FFF700, color:#000000
    classDef lime fill:#AEFF6E, color:#000000
    classDef honey fill:#EBA937, color:#000000

    subgraph 1
    A((2))---B((1))
    A---C((7))
    C---D((4)):::lime
    C---E((8))
    D---F((3)):::lemon
    D---G((6)):::honey
    G---H((5))
    G---Z((0)):::invisible
    end

    subgraph 2
    A2((2))---B2((1))
    A2---C2((7))
    C2---D2((4)):::lime
    C2---E2((8))
    D2---F2((3)):::invisible
    D2---G2((6))
    G2---H2((5))
    G2---Z2((0)):::invisible
    end

    subgraph 3
    A3((2))---B3((1))
    A3---C3((7))
    C3---D3((4)):::honey
    C3---E3((8))
    D3---F3((3))
    D3---G3((5)):::honey
    G3---H3((0)):::invisible
    G3---Z3((0)):::invisible
    end

    subgraph 4
    A4((2))---B4((1))
    A4---C4((7))
    C4---D4((5)):::lime
    C4---E4((8))
    D4---F4((3)):::lime
    D4---G4((6)):::lime
    G4---H4((5)):::invisible
    G4---Z4((0)):::invisible
    end

    linkStyle 7 stroke-width:0px
    linkStyle 12 stroke-width:0px
    linkStyle 15 stroke-width:0px
    linkStyle 21 stroke:#EBA937
    linkStyle 22 stroke-width:0px
    linkStyle 23 stroke-width:0px
    linkStyle 28 stroke:#AEFF6E
    linkStyle 29 stroke:#AEFF6E
    linkStyle 30 stroke-width:0px
    linkStyle 31 stroke-width:0px
```
From Left:
1. initial tree
2. delete leaf node (3)
3. delete node with 1 child (6)
4. delete node with 2 children (4)
<br></br>

# Balanced Binary Search Trees
## Binary Search Trees as Dictionaries
- All six of our dictionary operations, when implemented with binary search trees, take $O(h)$, where $h$ is the height of the tree.
- The best height we could hope to get is $\lg{n}$, if the tree was perfectly balanced, since
$$\sum_{i=0}^{|\lg{n}|}{2^i}\approx n$$
- But if we get unlucky with our order of insertion or deletion, we could get linear height!
<br></br>

## Tree Insertion: Worst Case Height
```mermaid
%%{init: {'theme':'neutral'}}%%
graph TB
    classDef invisible opacity:0.0

    A((A))---Z((0)):::invisible
    A---B((B))
    B---Y((0)):::invisible
    B---C((C))
    C---X((0)):::invisible
    C---D((D))

    linkStyle 0 stroke-width:0px;
    linkStyle 2 stroke-width:0px;
    linkStyle 4 stroke-width:0px;
```
If we are unlucky in the order of insertion, and take no steps to rebalance, the tree can have height $\Theta{(n)}$.
<br></br>

## Tree Insertion: Average Case Analysis
- In fact, binary search trees constructed with *random* insertion orders *on average* have $\Theta{(\lg{n})}$ height.
- Why? Because half the time the insertion will be closer to the median key than an end key.
- Our future analysis of Quicksort will explain more precisely why the expected height is $\Theta{(\lg{n})}$.
<br></br>

## Perfectly Balanced Trees
- *Perfectly* balanced trees require a lot of work to maintain.

```mermaid
%%{init: {'theme':'neutral'}}%%
graph TB
    classDef invisible opacity:0.0
    classDef lime fill:#003153, color:#AEFF6E

    A((9))---B((5))
    A---C((13))
    B---D((3))
    B---E((7))
    C---F((11))
    C---G((15))
    D---H((2))
    D---I((4))
    E---J((6))
    E---K((8))
    F---L((10))
    F---M((12))
    G---Z((0)):::invisible
    G---N((14))
    H---O((1)):::lime
    H---Y((0)):::invisible

    linkStyle 12 stroke-width:0px
    linkStyle 15 stroke-width:0px
```

- If we insert the key 1, we must move every single node in the tree to rebalance it, taking $\Theta{(n)}$ time.
<br></br>

## Balanced Search Trees
- Therefore, when we talk about "balanced" trees, we mean trees whose height is $O(\lg{n})$, so all dictionary operations (insert, delete, search, min/max, successor/predecessor) take $O(\lg{n})$ time.
- No data structure can be better than $\Theta(\lg{n})$ in the worst case on all these operations.
- Extra care must be taken on insertion and deletion to guarantee such performance, by rearranging things when they get too lopsided.
- *Red-Black trees*, *AVL trees*, *2-3 trees*, *splay trees*, and *B-trees* are examples of balanced search trees used in practice and discussed in most data structure texts.
<br></br>

## Where Does the Log Come From?
- Often the logarithmic term in an algorithm analysis comes from using a balanced search tree as a dictionary, and performing many (say, $n$) operations on it.
- But often it comes from the idea of a balanced binary tree, partitioning the items into smaller and smaller subsets, and doing little work on each of $\log{(n)}$ levels.