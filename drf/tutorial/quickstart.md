# [Quickstart](https://www.django-rest-framework.org/tutorial/quickstart/)

관리자가 시스템에 존재하는 사용자와 그룹을 확인하고 수정할 수 있게 하는 간단한 API를 작성한다.

## Project setup
`tutorial`이라는 이름의 새로운 Django 프로젝트를 생성하고 `quickstart`라는 새로운 앱을 시작한다.

```bash
# 프로젝트 디렉토리 생성
mkdir tutorial
cd tutorial

# 패키지 의존성을 로컬로 분리시키기 위해 가상 환경을 생성한다
python3 -m venv env
source env/bin/activate # 윈도우: `env\Scripts\activate`

# 가상환경에 Django와 Django REST framework를 설치한다
pip install django
pip install djangorestframework

# 하나의 애플리케이션으로 새 프로젝트를 설정한다
django-admin startproject tutorial . # '.'이 붙는 것에 유의한다
cd tutorial
django-admin startapp quickstart
cd ..
```

프로젝트 레이아웃은 다음과 같아야 한다.

```bash
$ pwd
<some path>/tutorial
$ find .
.
./manage.py
./tutorial
./tutorial/__init__.py
./tutorial/quickstart
./tutorial/quickstart/__init__.py
./tutorial/quickstart/admin.py
./tutorial/quickstart/apps.py
./tutorial/quickstart/migrations
./tutorial/quickstart/migrations/__init__.py
./tutorial/quickstart/models.py
./tutorial/quickstart/tests.py
./tutorial/quickstart/views.py
./tutorial/asgi.py
./tutorial/settings.py
./tutorial/urls.py
./tutorial/wsgi.py
```

프로젝트 디렉토리 내부에 애플리케이션이 생성된 것이 이상하게 보일 수 있다. 프로젝트의 네임스페이스를 사용하면 외부 모듈과의 이름 충돌을 피할 수 있다(quickstart의 범위를 벗어나는 주제).

이제 처음으로 데이터베이스를 동기화 해본다:

```bash
python manage.py migrate
```

또한 이름은 `admin`, 비밀번호는 `password123`인 초기 사용자를 생성한다. 이후 예시로 이 사용자를 인증할 것이다.

```bash
python manage.py createsuperuser --email admin@example.com --username admin
```

데이터베이스를 설정하고 초기 사용자를 생성해 준비가 되었다면, 앱 디렉토리를 열고 코드를 작성한다...

## Serializers
먼저 시리얼라이저 몇 개를 정의한다. 데이터 표현에 사용할 새로운 모듈 `tutorial/quickstart/serializers.py`를 생성한다.

```python
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
```

여기서는 `HyperlinkedModelSerializer`로 하이퍼링크된 관계를 사용한다는 점에 유의한다. 기본 키와 여러 다른 관계를 사용할 수도 있지만, 하이퍼링크는 좋은 RESTful 설계이다.

## Views
그 다음에는 뷰를 작성한다. `tutorial/quickstart/views.py`를 열고 입력한다.

```python
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from tutorial.quickstart.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    사용자를 보거나 수정할 수 있게 하는 API 엔드포인트
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    그룹을 보거나 수정할 수 있게 하는 API 엔드포인트
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
```

여러 개의 뷰를 작성하는 대신 `ViewSet`이라는 클래스로 공통 동작을 묶는다.

필요하다면 쉽게 개별적인 뷰로 분리할 수 있지만, 뷰셋을 사용하면 뷰 로직을 매우 간결하고 멋지게 구성되도록 유지할 수 있다.

## URLs
API URL을 연결한다. `tutorial/urls.py`를 연다:

```python
from django.urls import include, path
from rest_framework import routers
from tutorial.quickstart import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# 자동 URL 라우팅을 이용해 API를 연결한다
# 추가로 탐색 가능한 API를 위한 로그인 URL을 포함시킨다.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
```

뷰 대신 뷰셋을 사용하므로 라우터 클래스에 뷰셋을 간단히 등록하는 것으로 API를 위한 URL 구성을 자동으로 생성할 수 있다.

API URL에 대한 제어를 더 필요로 한다면 일반적인 클래스 기반 뷰를 사용하고 명시적으로 URL 구성을 작성하면 된다.

마지막으로 탐색 가능한 API에서 사용하기 위한 기본 로그인과 로그아웃 뷰를 포함시킨다. 이것은 선택 사항이지만 만약 API가 인증을 필요로 하고 탐색 가능한 API를 사용한다면 유용하다.

## Pagination
페이지네이션은 페이지 당 얼마나 많은 객체가 반환되는지 제어할 수 있게 한다. 사용하려면 `tutorial/settings.py`에 다음을 추가한다.

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```

## Settings
`INSTALLED_APPS`에 `rest_framework`를 추가한다. 이 설정 모듈은 `tutorial/settings.py`에 있다:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

다했다.

## Testing our API
작성한 API를 테스트할 준비가 끝났다. 명령줄에서 서버를 켠다.

```bash
python manage.py runserver
```

이제 명령줄이나 `curl`과 같은 도구를 사용해 API에 접근할 수 있다:

```bash
bash: curl -H 'Accept: application/json; indent=4' -u admin:password123 http://127.0.0.1:8000/users/
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "email": "admin@example.com",
            "groups": [],
            "url": "http://127.0.0.1:8000/users/1/",
            "username": "admin"
        },
    ]
}
```

또는 명령줄 도구 [httpie](https://httpie.io/docs#installation)를 사용할 수도 있다:

```bash
bash: http -a admin:password123 http://127.0.0.1:8000/users/

HTTP/1.1 200 OK
...
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "email": "admin@example.com",
            "groups": [],
            "url": "http://127.0.0.1:8000/users/1/",
            "username": "admin"
        },
    ]
}
```

또는 브라우저에서 `http://127.0.0.1:8000/users/`로 직접 접속할 수 있다:

![quickstart](https://www.django-rest-framework.org/img/quickstart.png)

브라우저를 사용한다면 우측 상단에 위치한 컨트롤을 사용해 로그인한다.

훌륭하다. 아주 쉬웠다!

REST framework가 어떻게 사용될 수 있는지에 대해 더 깊게 이해하고 싶다면 [튜토리얼](https://www.django-rest-framework.org/tutorial/1-serialization/) 또는 [API 가이드](../api-guide/requests.md)를 확인한다.