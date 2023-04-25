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
<br><br>

# N:1 Relation
```python
# Comment 모델 작성
# articles/models.py

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## Get - List
```python
# articles/serializers.py

from .models import Article, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


# articles/urls.py

urlpatterns = [
    ...,
    path('comments/', views.comment_list),
]


# articles/views.py

from .models import Article, Comment
from .serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer


@api_view(['GET'])
def comment_list(request):
    comments = Comment.objects.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)
```

## GET - Detail
```python
# articles/urls.py

urlpatterns = [
    ...,
    path('comments/<int:comment_pk>/', views.comment_detail),
]


# articles/views.py

@api_view(['GET'])
def comment_detail(request, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    serializer = CommentSerializer(comment)
    return Response(serializer.data)
```

## POST
```python
# articles/urls.py

urlpatterns = [
    ...,
    path('articles/<int:article_pk>/comments/', views.comment_create),
]

# articles/views.py

@api_view(['POST'])
def comment_create(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(article=article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
```
- `save()` 메서드는 특성 Serializer 인스턴스를 저장하는 과정에서 추가적인 데이터를 받을 수 있다.
- `CommentSerializer`를 통해 Serialize 되는 과정에서 Parameter로 넘어온 `article_pk`에 해당하는 article 객체를 추가적인 데이터로 넘겨 저장한다.

### 읽기 전용 필드 설정
```python
# articles/serializers.py

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = `__all__'
        read_only_fields = ('article',)
```
- `read_only_fields`를 사용해 외래키 필드를 *읽기 전용 필드*로 설정한다.
- 읽기 전용 필드는 데이터를 전송하는 시점에 *해당 필드를 유효성 검사에서 제외시키고 데이터 조회 시에는 출력*하도록 한다.

## DELETE & PUT
```python
# articles/views.py

@api_view(['GET', 'DELETE', 'PUT'])
def comment_detail(request, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
```
<br><br>

# N:1 - 역참조 데이터 조회
## 특정 게시글에 작성된 댓글 목록 출력하기
1. `PrimaryKeyRelatedField()`
  - 게시글 조회 시 해당 게시글의 댓글 목록까지 함께 출력하기
  - Serializer는 기존 필드를 override하거나 추가적인 필드를 구성할 수 있다.
  - `models.py`에서 `related_name`을 통해 역참조 매니저명을 변경할 수 있다.
    ```python
    # articles/serializers.py

    class ArticleSerializer(serializers.ModelSerializer):
        comment_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

        class Meta:
            model = Article
            fields = '__all__'
    

    # articles/models.py

    class Comment(models.Model):
        article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
        content = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
    ```
2. Nested relationships
- 모델 관계상 참조된 대상은 참조하는 대상의 표현에 포함되거나 중첩(nested)될 수 있다.
- 중첩된 관계는 serializers를 필드로 사용하여 표현할 수 있다.
```python
# articles/serializers.py

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('article',)


class ArticleSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
```
## 특정 게시글에 작성된 댓글의 개수 출력하기
1. 새로운 필드 추가: `Article Detail`
  - 게시글 조회 시 해당 게시글의 댓글 개수까지 함께 출력하기
  ```python
  # articles/serializers.py

  class ArticleSerializer(serializers.ModelSerializer):
      comment_set = CommentSerializer(many=True, read_only=True)
      comment_count = serializers.IntegerField(source='comment_set.count', read_only=True)

      class Meta:
          model = Article
          fields = '__all__'
  ```
2. source
  - 필드를 채우는데 사용할 속성의 이름
  - 점 표기법(dotted notation)을 사용하여 속성을 탐색할 수 있다.
  ```python
  # articles/serializers.py

  class ArticleSerializer(serializers.ModelSerializer):
      comment_set = CommentSerializer(many=True, read_only=True)
      comment_count = serializers.IntegerField(source='comment_set.count', read_only=True)

      class Meta:
          model = Article
          fields = '__all__'
```

## [주의] 읽기 전용 필드 지정 이슈
- 특정 필드를 override 혹은 추가한 경우 `read_only_fields`가 동작하지 않는다.
```python
# 사용 불가

class ArticleSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True)
    comment_count = serializers.IntegerField(source='comment_set.count')

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('comment_set', 'comment_count',)
```

## 댓글 조회시 게시글 출력 변경해보기
- 필요한 Serializer는 내부에서 추가로 선언할 수 있다.
```python
# articles/serializers.py

class CommentSerializer(serializers.ModelSerializer):
    class ArticleTitleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Article
            fields = ('title',)
    
    article = ArticleTitleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
```
<br><br>

# Django Shortcuts Functions
## `get_object_or_404()`
- 모델 manager objects에서 `get()`을 호출하지만 해당 객체가 없을 때에는 기존의 `DoesNotExist` 예외 대신 `HTTP404`를 raise한다.
```python
# articles/views.py

from django.shorcuts import get_object_or_404


# article = Article.objects.get(pk=article.pk)
article = get_object_or_404(Article, pk=article.pk)
# comment = Comment.objects.get(pk=comment.pk)
comment = get_object_or_404(Comment, pk=comment.pk)
```

## `get_list_or_404()`
- 모델 manager objects에서 `filter()`의 결과를 반환하고 해당 객체 목록이 없을 때에는 `HTTP404`를 raise한다.
```python
# articles/views.py

from django.shortcuts import get_list_or_404


# articles = Article.objects.all()
articles = get_list_or_404(Article)
# comments = Comment.objects.all()
comments = get_list_or_404(Article)
```
<br><br>

# API 문서화
## Swagger
- REST 웹서비스 설계, 빌드, 문서화 등을 도와주는 오픈소스 소프트웨어 프레임워크

## Swagger Library 사용
- [공식문서](https://drf-yasg.readthedocs.io/en/stable/)
- 설치 및 등록
```bash
$ pip install drf-yasg
```
```python
# settings.py

INSTALLED_APPS = [
    ...,
    'drf_yasg',
    ...
]


# PROJECT_NAME/urls.py

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title='Snippets API',
        defualt_version='v1',
        description='Test description',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='contact@snippets.local'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    ...,
    path('swagger/', schema_view.with_ui('swagger')),
]
```
- 확인: `http://127.0.0.1:8000/swagger/`