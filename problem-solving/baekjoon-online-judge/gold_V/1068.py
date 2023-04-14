# 1068. 트리

# DFS
def dfs(point):
    # 지워졌다는 뜻으로 값을 -2로 지정한다
    nodes[point] = -2
    for i in range(n):
        if point == nodes[i]:
            dfs(i)


n = int(input())
nodes = list(map(int, input().split()))
target = int(input())
result = 0

dfs(target)

for i in range(n):
    # 노드가 지워지지 않았고 누구의 부모 노드도 아닐 때
    if nodes[i] != -2 and i not in nodes:
        result += 1

print(result)