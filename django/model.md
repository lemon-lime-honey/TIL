# Django Model
- DB의 테이블을 정의하고 데이터를 조작할 수 있는 기능들을 제공한다.
- 테이블 구조를 설계하는 청사진

## model 클래스 작성
```python
# app/models.py

class ClassName(models.Model):
    # id필드는 자동으로 생성된다
    example1 = models.CharField(max_length=10)
    example2 = models.TextField()
```
- `django.db.models` 모듈의 `Model`이라는 상위 클래스를 상속 받아 작성한다.
- 클래스 변수명: 테이블의 각 필드 이름
- `model Field` 메서드: 테이블 필드의 데이터 타입
- `model Field` 메서드의 키워드 인자: 테이블 필드의 제약조건 관련 설정

## 메서드 예시
- $\texttt{CharField()}$
  - 길이의 제한이 있는 문자열을 넣을 때 사용한다.
  - 필드의 최대 길이를 결정하는 $\texttt{max}$ _ $\texttt{length}$는 필수 인자이다.
- $\texttt{TextField()}$
  - 글자의 수가 많을 때 사용한다.
- $\texttt{DateTimeField()}$
  - 날짜와 시간을 넣을 때 사용한다.
  - 선택 인자
    - $\texttt{auto}$ _ $\texttt{now}$: 데이터가 저장될 때마다 자동으로 현재 날짜와 시각을 저장한다.
    - $\texttt{auto}$ _ $\texttt{now}$ _ $\texttt{add}$: 데이터가 처음 생성될 때에만 자동으로 현재 날짜와 시각을 저장한다.
<br><br>

# Migrations
`model` 클래스의 변경사항(필드 생성, 추가 수정 등)을 DB에 최종 반영하는 방법

## Migration 순서
1. model class
2. $\texttt{makemigrations}$를 통해 migration 파일 생성
3. $\texttt{migrate}$를 통해 DB에 반영

## Migrations 명령어
- $\texttt{python manage.py makemigrations}$
  - model class를 기반으로 migration을 작성한다.
- $\texttt{python manage.py migrate}$
  - migration을 DB에 전달하여 반영한다.
- $\texttt{python manage.py showmigrations}$
  - migrations 파일들이 migrate 되었는지 여부를 확인한다.
  - `[X]` 표시가 있으면 migrate가 완료되었음을 의미한다.
- $\texttt{python manage.py sqlmigrate app}$ _ $\texttt{label migration}$ _ $\texttt{name}$
  - 해당 migrations 파일이 SQL문으로 어떻게 해석되어 DB에 전달되는지 확인한다.

## 이미 생성된 테이블에 필드를 추가하는 경우
1. model class를 수정한다.
2. $\texttt{makemigration}$ 명령어를 사용한다.
  - 이미 기존 테이블이 존재하기 때문에 필드를 추가할 때 필드의 기본 값 설정이 필요하다.
  - 터미널에서 선택지를 두 개 준다.
  - 1번: 직접 기본 값을 입력한다.
  - 2번: `models.py`에 기본 값 관련 설정을 한다.
3. migration이 된 후 migration 파일이 생성된다.
4. $\texttt{migrate}$한다.
<br><br>

# Admin Site
## Automatic admin interface
- Django는 추가 설치 및 설정 없이 자동으로 관리자 인터페이스를 제공한다.
- 데이터 관련 테스트 또는 확인을 하기에 매우 유용하다.

## admin 계정 생성
```bash
$ python manage.py createsuperuser
```
- email은 선택사항이므로 입력하지 않고 진행할 수 있다.
- 비밀번호 생성 시 보안상 터미널에 출력되지 않는다.

## admin에 모델 클래스 등록
```python
# app/admin.py

from django.contrib import admin
from .models import ClassName

admin.site.register(ClassName)
```
- `admin.py`에 등록하지 않으면 admin site에서 확인할 수 없다.