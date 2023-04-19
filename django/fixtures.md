# Django Fixtures
- Django가 데이터베이스로 가져오는 방법을 알고 있는 데이터 모음
- Django가 직접 만들기 때문에 데이터베이스 구조에 맞추어 작성 되어있다.
- Django는 fixtures를 사용해 모델에 초기 데이터를 제공한다.

# 초기 데이터 제공하기
## fixtures 명령어
### dumpdata
```bash
$ python manage.py dumpdata [app_name[.ModelName] [app_name[.ModelName] ...]] > filename.json
```
- 데이터베이스의 모든 데이터를 출력한다.
- 여러 모델을 하나의 json 파일로 만들 수 있다.

#### fixtures 생성
```bash
$ python manage.py dumpdata --indent 4 articles.article > articles.json
$ python manage.py dumpdata --indent 4 accounts.user > users.json
$ python manage.py dumpdata --indent 4 articles.comment > comments.json
```

### loaddata
- fixtures 데이터를 데이터베이스로 불러온다.

#### fixtures 기본 경로
```
app_name/fixtures
```
- Django는 설치된 모든 app의 디렉토리에서 fixtures 폴더 이후의 경로로 fixtures 파일을 찾아 load 한다.

#### fixtures 불러오기
- 기본 경로로 fixtures 파일을 옮긴다.
- `db.sqlite3` 파일을 삭제한 후 migrate를 진행한다.
- load 후 데이터가 잘 입력되었는지 확인한다.
```bash
$ python manage.py loaddata articles.json users.json comments.json
```

#### loaddata 순서 주의사항
- loaddata를 한 번에 실행하지 않고 하나씩 실행한다면 모델 관계에 따라 순서가 중요할 수 있다.
  - comments는 article에 대한 key 및 user에 대한 key가 필요하다.
  - article은 user에 대한 key가 필요하다.
- 현재 모델 관계에서는 `user` $\rightarrow$ `article` $\rightarrow$ `comment` 순으로 데이터를 넣어야 오류가 발생하지 않는다.
  ```bash
  $ python manage.py loaddata users.json
  $ python manage.py loaddata articles.json
  $ python manage.py loaddata comments.json
  ```

#### loaddata 시 encoding codec 관련 에러가 발생하는 경우
- 두 가지 방법 중 택 1
1. dumpdata 시 추가 옵션 작성
  ```bash
  $ python -Xutf8 manage.py dumpdata [...]
  ```
2. 메모장 활용
  1. 메모장으로 json 파일 열기
  2. "다른 이름으로 저장" 선택
  3. 인코딩을 UTF8로 선택 후 저장