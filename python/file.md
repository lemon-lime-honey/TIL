# file Input/Output
## open, close
```python
infile = open("Data.txt", 'r')
infile.close()
# with 키워드를 사용하면 close를 호출하지 않아도 종료된다.
with open("Data.txt", 'r') as infile:
    # code block
print(infile.closed) # True
```
<br></br>

## Reading Text Files
- `infile.read()`: 파일 내용 전체를 하나의 문자열로 반환한다.
- `infile.readline()`: 파일 내용 한 줄을 문자열로 반환한다.
<br></br>

## Creating Text Files
- `outfile = open(fileName, 'w')`
    - 파일을 쓰기 모드로 연다.
    - 파일이 없으면 생성하는데, `'w'` 뿐만 아니라 `'r'`이나 `'a'`로 열었을 때에도 마찬가지이다.
- `outfile.writelines(list1)`: 리스트에 있는 모든 원소를 파일에 문자열로 입력한다.
- `outfile.write(strVar)`: strVar을 파일에 입력한다.
<br></br>

## Adding Lines to an Existing Text File
- `outfile = open(fileName, 'a')`: a는 append를 의미한다.
<br></br>

## Altering Items in a Text File
```python
import os

os.remove(fileName) # 파일 삭제
os.rename(oldFileName, newFileName)# 파일의 이름을 바꿀 수 있다. 경로 또한 바꿀 수도 있다.
# remove와 rename은 열려있는 파일에는 쓸 수 없다.
# rename의 두 번째 argument는 이미 존재하는 파일의 이름이 될 수 없다.
os.path.isfile(fileName) # 파일 fileName이 존재하면 True, 아니면 False를 반환한다.
```
<br></br>

### mode
| 문자 | 동작 |
| --- | --- |
| 'r' | 읽기 전용(기본값) |
| 'w' | 쓰기 전용. 파일이 먼저 초기화된다. |
| 'x' | 파일 만들기용. 이미 존재하는 경우 실패한다. |
| 'a' | 쓰기 전용. 파일이 이미 존재하는 경우 내용을 추가한다. |
| 'b' | 바이너리 모드 |
| 't' | 텍스트 모드(기본값) |
| '+' | 갱신용(읽기와 쓰기) |
<br></br>

# JSON
- 자바스크립트 객체 표기법
- 개발환경에서 많이 활용되는 데이터 양식이다.
- 웹 어플리케이션에서 데이터를 전송할 때 일반적으로 사용한다.
- 문자 기반(텍스트) 데이터 포맷으로 다수의 프로그래밍 환경에서 쉽게 활용할 수 있다.
    - 텍스트를 언어별 데이터 타입으로 변환할 수 있다.
    - 언어별 데이터 타입을 적절하게 텍스트로 변환할 수 있다.
```python
import json
# 객체를 JSON으로 변환
x = ['Anakin', 'R2-D2', 'C-3PO', 4]
json.dumps(x)
# JSON을 객체로 변환
x = json.load(f)
```
<br></br>