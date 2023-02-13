# Querying Data
## SELECT
```SQL
SELECT
    select_list
FROM
    table_name;
```
- `SELECT`: 데이터를 선택하려는 필드를 하나 이상 지정해야 한다.
- `FROM`: 데이터를 선택하려는 테이블의 이름을 지정해야 한다.
- `SELECT *`를 사용하면 테이블의 모든 필드를 선택할 수 있다.
<br></br>

# Sorting Data
## ORDER BY
```SQL
SELECT
    select_list
FROM
    table_name
ORDER BY
    column1 [ASC|DESC], 
    column2 [ASC|DESC], 
    ...;
```
- `FROM`절 뒤에 위치한다.
- 하나 이상의 `column`을 기준으로 결과를 오름차순 또는 내림차순으로 정렬한다.
- `ASC`(기본값), `DESC`
<br></br>

# Filtering Data
## DISTINCT
```SQL
SELECT DISTINCT
    select_list
FROM
    table_name;
```
- 조회 결과에서 중복된 레코드를 제거한다.
- `SELECT` 키워드 바로 뒤에 작성해야 한다.
- `SELECT DISTINCT` 키워드 다음에 고유한 값을 선택하려는 하나 이상의 필드를 지정한다.
<br></br>

## WHERE
```SQL
SELECT
    select_list
FROM
    table_name
WHERE
    search_condition;
```
- 조회 시 특정 검색 조건을 지정한다.
- `FROM` 절 뒤에 위치한다.
- `search_condition`은 비교연산자 및 논리연산자(AND, OR, NOT 등)를 포함한 구문이 사용된다.
<br></br>

## Operators
- Comparison Operator<br>
$\texttt{=, >=, <=, !=, IS, LIKE, IN, BETWEEN...AND}$
- Logical Operator<br>
$\texttt{AND(}$ && $\texttt{), OR(||), NOT(!)}$
- $\texttt{IN}$ operator: 값이 특정 목록 안에 있는지 확인한다.
- $\texttt{LIKE}$ operator: 값이 특정 패턴에 일치하는지 확인한다. 와일드카드와 함께 사용한다.
    - $\texttt{'\%'}$: 0개 이상의 문자열과 일치하는지 확인한다.
    - $\texttt{'\_'}$: 단일 문자와 일치하는지 확인한다.
<br></br>

## LIMIT
```SQL
SELECT
    select_list
FROM
    table_name
LIMIT [offset, ] row_count;
```
- 조회하는 레코드 수를 제한한다.
- 하나 또는 두 개의 인자를 사용한다. (0 또는 양의 정수)
- `row_count`는 조회할 최대 레코드 수를 지정한다.
<br></br>

# Grouping Data
## GROUP BY
```SQL
SELECT
    c1, c2, ..., cn, aggregate_function(ci)
FROM
    table_name
GROUP BY
    c1, c2, ..., cn;
```
- 레코드를 그룹화하여 요약본을 생성한다. *Aggregation Functions*와 함께 사용하기도 한다.
    - Aggregation Functions: $\texttt{SUM, AVG, MAX, MIN, COUNT}$
- `FROM` 및 `WHERE`절 뒤에 배치한다.
- `GROUP BY` 절 뒤에 그룹화할 필드 목록을 작성한다.
- $\texttt{HAVING}$
    - 주로 `GROUP BY`와 함께 사용되며 `GROUP BY`가 없을 경우 `WHERE`처럼 동작한다.
    - 집계 항목에 대한 세부 조건을 지정한다.