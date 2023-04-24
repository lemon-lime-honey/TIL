# HTTP Request Methods
- 리소스에 대한 행위(수행하고자 하는 동작)를 정의한다.
- HTTP verbs

## 대표적인 HTTP Request Methods
1. `GET`
  - 서버에 리소스의 표현을 요청한다.
  - GET을 사용하는 요청은 데이터만 검색해야 한다.
2. `POST`
  - 데이터를 지정된 리소스에 제출한다.
  - 서버의 상태를 변경한다.
3. `PUT`
  - 요청한 주소의 리소스를 수정한다.
4. `DELETE`
  - 지정된 리소스를 삭제한다.

## HTTP Response Status Codes
- 특정 HTTP 요청이 성공적으로 완료되었는지 여부를 나타낸다.
- 응답은 5개의 그룹으로 나뉜다.
  1. Informational responses(100 - 199)
  2. Successful responses(200 - 299)
  3. Redirection messages(300 - 399)
  4. Client error responses(400 - 499)
  5. Server error responses(500 - 599)
<br><br>

# REST API
## API
- Application Programming Interface
- 애플리케이션과 프로그래밍으로 소통하는 방법
- 복잡한 코드를 추상화하여 대신 사용할 수 있는 몇 가지 더 쉬운 구문을 제공한다.

## Web API
- 웹 서버 또는 웹 브라우저를 위한 API
- 현재 웹 개발은 모든 것을 하나부터 열까지 직접 개발하기보다 여러 Open API를 활용하는 추세
- API는 다양한 타입의 데이터로 응답한다. (HTML, JSON 등)

## REST
- Representational State Transfer
- API Server를 개발하기 위한 일종의 소프트웨어 설계 방법론
- REST 원리를 따르는 시스템을 RESTful하다고 표현한다.
- *자원을 정의*하고 *자원에 대한 주소를 지정*하는 전방적인 방법을 서술한다.

## REST에서 자원을 정의하고 주소를 지정하는 방법
1. 자원의 식별: `URI`
2. 자원의 행위: `HTTP Methods`
3. 자원의 표현
  - 궁극적으로 표현되는 결과물
  - JSON으로 표현된 데이터를 제공한다.

## REST API
- REST라는 API 디자인 아키텍처를 지켜 구현한 API
<br><br>

# Response JSON
## Django REST Framework(DRF)
- Django에서 Restful API 서버를 쉽게 구축할 수 있도록 도와주는 오픈소스 라이브러리
<br><br>

# Serialization
- 여러 시스템에서 활용하기 위해 데이터 구조나 객체 상태를 나중에 재구성할 수 있는 포맷으로 변환하는 과정
- 어떠한 언어나 환경에서도 나중에 다시 쉽게 사용할 수 있는 포맷으로 변환하는 과정
<br><br>

# DRF - Single Model
## ModelSerializer 작성
```python
# articles/serializers.py

from rest_framework import serializers
from .models import Article


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'content',)
```

## ModelSerializer
- 모델 필드에 해당하는 필드가 있는 Serializer 클래스를 자동으로 만든다.
  1. Model 정보에 맞춰 자동으로 필드를 생성한다.
  2. serializer에 대한 유효성 검사기를 자동으로 생성한다.
  3. `.create()` 및 `.update()`의 기본 구현 메서드가 포함된다.

## URL과 HTTP Requests Methods 설계
|  | GET | POST | PUT | DELETE |
| --- | --- | --- | --- | --- |
| articles/ | 전체 글 조회 | 글 작성 |  |  |
| articles/1/ | 1번 글 조회 |  | 1번 글 수정 | 1번 글 삭제 |

## GET - List
- 게시글 데이터 목록 조회하기
```python
# articles/urls.py

urlpatterns = [
    path('articles/', views.article_list),
]


# articles/views.py

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Article
from .serializers import ArticleListSerializer


@api_view(['GET'])
def article_list(request):
    articles = Article.objects.all()
    serializer = ArticleListSerializer(articles, many=True)
    return Response(serializer.data)
```

### `api_view` Decorator
- DRF view 함수가 응답해야 하는 HTTP 메서드 목록을 받는다.
- 기본적으로 GET 메서드만 허용되며 다른 메서드 요청에 대해서는 `405 Method Not Allowed`로 응답한다.
- DRF view 함수에서는 필수로 작성한다.

## GET - Detail
- 단일 게시글 데이터 조회하기
- 각 데이터의 상세 정보를 제공하는 ArticleSerializer 정의
- url 및 view 함수 작성
```python
# articles/serializers.py

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


# articles/urls.py

urlpatterns = [
    ...,
    path('articles/<int:article_pk>/', views.article_detail),
]


# articles/views.py

from .serializers import ArticleListSerializer, ArticleSerializer


@api_view(['GET'])
def article_detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    serializer = ArticleSerializer(article)
    return Response(serializer.data)
```

## POST
- 게시글 데이터 생성하기
- 요청에 대한 데이터 생성이 성공했을 경우 `201 Created` 상태 코드로 응답하고 실패했을 경우 `400 Bad request`로 응답한다.
```python
# articles/views.py

from rest_framework import status


@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Articles.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ArticleSerializer(data.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,   status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### raise_exception
- `is_valid()`는 유효성 검사 오류가 있는 경우 `ValidationError` 예외를 발생시키는 선택적 `raise_exception` 인자를 사용할 수 있다.
- DRF에서 제공하는 기본 예외 처리기에 의해 자동으로 처리되며 기본적으로 `HTTP 400` 응답을 반환한다.
```python
# articles/views.py

@api_view(['GET', 'POST'])
def article_list(request):
    ...
    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
```

## DELETE
- 게시글 데이터 삭제하기
- 요청에 대한 데이터 삭제가 성공했을 경우 `204 No Content` 상태 코드로 응답한다.
```python
# articles/views.py

@api_view(['GET', 'DELETE'])
def article_detail(request, article_pk):
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

## PUT
- 게시글 데이터 수정하기
- 요청에 대한 데이터 수정이 성공했을 경우 `200 OK` 상태 코드로 응답한다.
```python
# articles/views.py

@api_view(['GET', 'DELETE', 'PUT'])
def article_detail(request, article_pk):
    ...
    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
```