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
    - '%': 0개 이상의 문자열과 일치하는지 확인한다.
    - '_': 단일 문자와 일치하는지 확인한다.
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

# Create/Delete a Table
## CREATE
```SQL
CREATE TABLE table_name (
    column_1 data_type, 
    column_1 data_type, 
    ..., 
    constraints
);
```
- 테이블을 생성한다.
- 각 필드에 적용할 데이터 타입(data type)을 작성한다.
- 테이블 및 필드에 대한 제약조건(constraints)을 작성한다.

### Constraint
- 데이터 무결성을 지키기 위해 데이터를 입력 받을 때 실행하는 검사 규칙
- 대표적인 MySQL Constraints
    - `PRIMARY KEY`: 해당 필드를 기본 키로 지정한다.
    - `NOT NULL`: 해당 필드에 `NULL`값을 저장하지 못하도록 지정한다.

### Auto_INCREMENT Attribute
- 테이블의 기본 키에 대한 번호를 자동으로 생성한다.
- 기본 키 필드에 사용한다.: 고유한 숫자를 부여한다.
- 시작 값은 1이며, 데이터 입력 시 값을 생략하면 자동으로 1씩 증가한다.
- 이미 사용한 값을 재사용하지 않는다.
- 기본적으로 `NOT NULL` 제약 조건을 포함한다.
<br></br>

## DROP
```SQL
DROP TABLE table_name;
```
<br></br>

# Modifying table fields
## ALTER
### ADD
``` SQL
ALTER TABLE
    table_name
ADD
    new_column_name column_definition;
```
- ADD 이후 추가하고자 하는 새 필드 이름과 데이터 타입 및 제약 조건을 작성한다.

### MODIFY
```SQL
ALTER TABLE
    table_name
MODIFY
    column_name column_definiton;
```
- 변경하고자 하는 필드 이름과 데이터 타입, 제약 조건이 필요하다.

### CHANGE COLUMN
``` SQL
ALTER TABLE
    table_name
CHANGE COLUMN
    original_name new_name column_definition;
```
- 기존 필드명, 변경명, 데이터 타입, 제약 조건을 작성해야 한다.

### DROP COLUMN
```SQL
ALTER TABLE
    table_name
DROP COLUMN
    column_name;
```
- `DROP COLUMN`` 이후 삭제하고자 하는 필드의 이름을 작성한다.
<br><br>

# Data Manipulation
## INSERT
```SQL
INSERT INTO table_name (c1, c2, ...)
VALUES (v1, v 2, ...);
```
- `INSERT INTO`절 다음에 테이블 이름과 괄호로 묶은 필드 목록을 작성한다.
- `VALUES` 키워드 다음 괄호 안에 해당 필드에 삽입할 값 목록을 작성한다.

## UPDATE
```SQL
UPDATE table_name
SET column_name = expression,
[WHERE
    condition];
```
- `SET`절 다음에 수정할 필드와 새 값을 지정한다.
- `WHERE`절에서 수정할 레코드를 지정하는 조건을 작성한다.
    - `WHERE`절을 작성하지 않으면 모든 레코드가 수정된다.

### DELETE
```SQL
DELETE FROM table_name
[WHERE
    condition];
```
- `DELETE FROM`절 다음에 테이블 이름을 작성한다.
- `WHERE`절에서 삭제할 레코드를 지정하는 조건 작성
    - `WHERE`절을 작성하지 않으면 모든 레코드가 삭제된다.