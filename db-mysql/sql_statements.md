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