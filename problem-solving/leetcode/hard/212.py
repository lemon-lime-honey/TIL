# 212. Word Search II
# 1. Trie를 이용해 `words`에 있는 단어를 저장한다.
# 2. `board`를 순회하며 백트래킹으로 단어를 찾는다.

class TrieNode:
    def __init__(self):
        self.children = dict()
        self.value = None


class Trie:
    def __init__(self):
        self.root = TrieNode()


class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        # 백트래킹으로 단어 찾기
        def search(r, c, node, path):
            nonlocal result, visited

            # `node`에 `last`속성이 있다면 지금까지 생성된 단어를 `result`에 추가한다.
            # `node`에 자식이 없다면 True를 반환한다.
            if hasattr(node, 'last'):
                result.add(path)
                if not node.children: return True

            for nr, nc in ((r - 1, c), (r + 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < len(board) and 0 <= nc < len(board[0]):
                    if board[nr][nc] in node.children and not visited[nr][nc]:
                        # 백트래킹
                        # 해당되는 자식 노드에 `last`가 있고, 재귀호출한 결과가 `True`라면
                        # 자식 노드를 제거한다. (분기 확인 끝)
                        visited[nr][nc] = True
                        if search(nr, nc,
                                  node.children[board[nr][nc]],
                                  path + board[nr][nc]):
                            node.children.pop(board[nr][nc])
                        visited[nr][nc] = False

            return False if node.children else True


        trie = Trie()
        result = set()

        # Trie를 이용해 단어 저장하기
        for word in words:
            node = trie.root
            for letter in word:
                if letter not in node.children:
                    new = TrieNode()
                    new.value = letter
                    node.children[letter] = new
                node = node.children[letter]
            node.last = True

        # `board`를 순회하며 search를 호출해 백트래킹으로 단어 찾기
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] in trie.root.children:
                    visited = [[False for k in range(len(board[0]))]
                               for l in range(len(board))]
                    visited[i][j] = True
                    search(i, j, trie.root.children[board[i][j]], board[i][j])

        return list(result)