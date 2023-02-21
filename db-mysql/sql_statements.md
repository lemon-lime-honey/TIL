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
<br></br>

#  Joining tables
## JOIN
- 둘 이상의 테이블에서 데이터를 검색할 수 있다.

### INNER JOIN
```SQL
SELECT
    select_list
FROM
    table1
INNER JOIN table 2
    ON table1.fk = table2.pk;
```
- `FROM`절 이후 메인 테이블을 지정한다.
- `INNER JOIN`절 이후 메인 테이블과 `JOIN`할 테이블을 지정한다.
- `ON` 키워드 이후 `JOIN` 조건을 작성한다.
    - `JOIN` 조건은 table1, table2 간의 레코드를 일치시키는 규칙으로 지정한다.

### LEFT JOIN
```SQL
SELECT
    select_list
FROM
    table1
LEFT [OUTER] JOIN table2
    ON table1.fk = table2.pk;
```
- 오른쪽 테이블과 일치하는 레코드와 함께 왼쪽 테이블의 모든 레코드를 반환한다.
- `FROM`절 이후 왼쪽 테이블을 지정한다.
- `LEFT JOIN`절 이후 오른쪽 테이블을 지정한다.
- `ON` 키워드 이후 `JOIN` 조건을 작성한다.
    - 왼쪽 테이블의 각 레코드를 오른쪽 테이블의 모든 레코드와 일치시킨다.
- 왼쪽은 무조건 표시하고, 매치되는 레코드가 없으면 `NULL`을 표시한다.
- 왼쪽 테이블 한 개의 레코드에 여러 개의 오른쪽 테이블 레코드가 일치할 경우, 해당 왼쪽 레코드를 여러 번 표시한다.

### RIGHT JOIN
```SQL
SELECT select_list
FROM
    table1
RIGHT [OUTER] JOIN table2
    ON table1.fk = table2.pk;
```
- `FROM`절 이후 왼쪽 테이블을 지정한다.
- `RIGHT JOIN`절 이후 오른쪽 테이블을 지정한다.
- `ON` 키워드 이후 조인 조건을 작성한다.
    - 오른쪽 테이블의 각 레코드를 왼쪽 테이블의 모든 레코드와 일치시킨다.
- 오른쪽은 무조건 표시하고, 매치되는 레코드가 없으면 `NULL`을 표시한다.
- 오른족 테이블 한 개의 레코드에 여러 개의 왼쪽 테이블 레코드가 일치할 경우, 해당 오른쪽 레코드를 여러 번 표시한다.

### JOIN 정리
#### INNER JOIN
```SQL
SELECT
    *
FROM
    tableA
INNER JOIN
    ON tableA.fk = tableB.id;
```

#### LEFT JOIN
```SQL
SELECT
    *
FROM
    tableA
LEFT JOIN tableB
    ON tableA.fk = tableB.id;
```

#### RIGHT JOIN
```SQL
SELECT
    *
FROM
    talbeA
RIGHT JOIN tableB
    ON tableA.fk = tableB.id;
```

#### $A - B$
```SQL
SELECT
    *
FROM
    tableA
LEFT JOIN tableB
    ON tableA.fk = tableB.id
WHERE tableB.id IS NULL;
```

#### $B - A$
```SQL
SELECT
    *
FROM
    tableA
RIGHT JOIN tableB
    ON tableA.fk = tableB.id
WHERE tableA.fk IS NULL;
```

#### $A\cup B$
```SQL
SELECT * FROM tableA
LEFT JOIN tableB ON tableA.fk = tableB.id
UNION
SELECT * FROM tableA
RIGHT JOIN tableB ON tableA.fk = tableB.id;
```
<br></br>

# Subquery
- 단일 쿼리문에 여러 테이블의 데이터를 결합하는 방법
- 조건에 따라 하나 이상의 테이블에서 데이터를 검색하는데 사용한다.
- `SELECT`, `FROM`, `WHERE`, `HAVING`절 등에서 다양한 맥락으로 사용한다.
<br></br>

## EXISTS
```SQL
SELECT
    select_list
FROM
    table
WHERE
    [NOT] EXISTS (subquery);
```
- 쿼리 문에서 반환된 레코드의 존재 여부를 확인한다.
- subquery가 하나 이상의 행을 반환하면 `EXISTS` 연산자는 `true`를 반환하고 그렇지 않으면 `false`를 반환한다.
- 주로 `WHERE`절에서 subquery의 반환 값 존재 여부를 확인하는데 사용한다.
<br></br>

# CASE
```SQL
CASE case_value
    WHEN when_value1 THEN statements
    WHEN when_value2 THEN statements
    ...
    [ELSE else-statements]
END CASE;
```
- SQL문에서 조건문을 구성한다.
- `case_value`가 `when_value`와 동일한 것을 찾을 때까지 순차적으로 비교한다.
- `when_value`와 동일한 `case_value`를 찾으면 해당 `THEN`절의 코드를 실행한다.
- 동일한 값을 찾지 못하면 `ELSE`절의 코드를 실행한다.
    - `ELSE`절이 없을 때 동일한 값을 찾지 못하면 오류가 발생한다.
<br></br>

# Transaction
```SQL
START TRANSACTION;
statements;
...
[ROLLBACK||COMMIT];
```
- 무조건 전부 성공하거나 혹은 전부 실패해야 하는 여러 쿼리문을 묶어 하나의 작업처럼 처리하는 방법
- 쪼개질 수 없는 업무처리의 단위
- `START TRANSACTION`: 트랜잭션 구문의 시작
- `COMMIT`: 모든 작업이 정상적으로 완료되면 한꺼번에 DB에 반영한다.
- `ROLLBACK`: 부분적으로 작업이 실패하면 트랜잭션에서 진행한 모든 연산을 취소하고 트랜잭션 이전으로 되돌린다.
<br></br>

# Triggers
```SQL
CREATE TRIGGER trigger_name
    {BEFORE | AFTER} {INSERT | UPDATE | DELETE}
    ON table_name FOR EACH ROW
    trigger_body;
```
- 특정 이벤트에 대한 응답으로 자동으로 실행되는 것
- DML의 영향을 받는 필드 값에만 적용할 수 있다.
- `CREATE TRIGGER` 키워드 다음에 생성하려는 트리거의 이름을 지정한다.
- 각 레코드의 어느 시점에 트리거가 실행될지 지정한다.
- `ON` 키워드 뒤에 트리거가 속한 테이블의 이름을 지정한다.
- 트리거가 활성화될 때 실행할 코드를 `trigger_body`에 지정한다.
    - 여러 명령문을 실행하려면 `BEGIN END` 키워드로 묶어서 사용한다.