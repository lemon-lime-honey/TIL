# 1339. 단어 수학

n = int(input())
letters = dict()
ten = [i for i in range(10)]
words = [input() for i in range(n)]
result = 0

# 단어 리스트를 순회한다
for word in words:
    # 단어의 문자 위치에 따른 값을 딕셔너리 내 문자에 해당하는 값에 더한다
    # 문자별로 일종의 가중치를 부여하는 역할
    for i in range(len(word)):
        if word[i] not in letters:
            letters[word[i]] = 10 ** (len(word) - 1 - i)
        else:
            letters[word[i]] += 10 ** (len(word) - 1 - i)

# 내림차순으로 딕셔너리의 값만 있는 리스트를 정렬한다
numbers = sorted(list(letters.values()), reverse=True)

# 위에서 정렬한 리스트를 순회하며 9부터 곱해 더해준다
for number in numbers:
    result += number * ten.pop()

print(result)