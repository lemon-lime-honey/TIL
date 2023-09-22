# 14725. 개미굴

import sys
input = sys.stdin.readline


# 트라이 노드
class TrieNode:
    def __init__(self):
        self.children = dict()
        self.last = False
        self.val = None
        self.depth = -1


# 트라이
class Trie:
    def __init__(self):
        self.root = TrieNode()


# 재귀 호출을 이용해 한 노드에서 시작에 가장 깊은 자식 노드까지 순회하며
# 깊이에 따라 다르게 출력하는 함수
def search(node):
    print('--' * node.depth + node.val)

    if node.last: return

    for child in sorted(node.children.keys()):
        search(node.children[child])


n = int(input())
result = list()
trie = Trie()

for i in range(n):
    # 입구부터 시작하는 경로
    ipt = input().rstrip().split()
    # 입구부터 시작하기 때문에 순회 전에 노드를 트라이의 루트로 지정한다
    node = trie.root

    for j in range(1, len(ipt)):
        # 자식 노드에 입력된 이름이 없으면 노드를 생성하고 등록한다
        if ipt[j] not in node.children:
            node.children[ipt[j]] = TrieNode()
            node.children[ipt[j]].val = ipt[j]
            node.children[ipt[j]].depth = node.depth + 1
        node = node.children[ipt[j]]

    node.last = True

# 같은 층에 여러 개의 방이 있을 때 사전 순서가 앞서는 정보가 먼저 나와야 하므로
# `sorted` 함수를 사용했다
for child in sorted(trie.root.children.keys()):
    search(trie.root.children[child])