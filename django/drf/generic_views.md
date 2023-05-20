# [Generic views](https://www.django-rest-framework.org/api-guide/generic-views/)

```
Django의 제네릭 뷰는...일반적인 사용 패턴의 지름길로 개발되었다.
...뷰 개발에서 찾을 수 있는 특정 공통 이디엄과 패턴을 가지며 그것을 추상화해 되풀이 할 필요 없이 일반적인 뷰를 빠르게 작성할 수 있게 한다.
- Django Documentation
```

클래스 기반 뷰의 대표적인 이점 중 하나는 재사용 가능한 동작을 구성할 수 있게 하는 방식이다. REST framework는 일반적으로 사용되는 패턴을 위해 제공되는 여러 뷰를 제공하는 것으로 이 이점을 살린다.

REST framework가 제공하는 제네릭 뷰는 데이터베이스 모델에 근접하게 매핑하는 API 뷰를 빠르게 작성할 수 있게 한다.

만약 제네릭 뷰가 API의 요구조건에 맞지 않다면 표준 `APIView` 클래스나 재사용 가능한 제네릭 뷰를 직접 구성하기 위해 제네릭 뷰에 사용되는 mixin과 기본 클래스를 재사용할 수 있다.

## Examples
제네릭 뷰를 사용할 때, 보통 뷰를 override하고 여러 클래스 속성을 설정한다.

```python
from django.contrib.auth.models import User
from myapp.serializers import UserSerializer
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
```

더 복잡한 사례에서는 뷰 클래스의 다양한 메서드를 override 하고 싶을 수도 있다. 다음은 그 예시이다.

```python
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        query set = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
```

매우 단순한 사례에서는 `.as_view()` 메서드를 통해 클래스 속성을 전달할 수도 있다. 예를 들어 URLconf가 다음과 같은 것을 포함할 수 있다.

```python
path('users/', ListCreateAPIView.as_view(queryset=User.objects.all(), serializer_class=UserSerializer), name='user-list')
```

## API Reference
### `GenericAPIView`
이 클래스는 표준 리스트와 디테일 뷰에서 일반적으로 요구되는 동작을 추가해 REST framework의 `APIView` 클래스를 확장한다.

제공되는 각각의 구체적인 제네릭 뷰는 `GenericAPIView`와 한 개 이상의 mixin 클래스를 결합하여 작성되었다.

#### 속성
##### 기본 설정
다음의 속성이 기본 뷰 동작을 제어한다.

- `queryset`<br>
  이 뷰에서 반환되는 객체에 사용되어야 할 queryset. 일반적으로 이 속성을 설정하거나 `get_queryset()` 메서드를 override해야 한다. 만약 뷰 메서드를 override한다면 `queryset`이 도출된 후 그 결과가 이후의 모든 요청을 위해 캐싱되기 때문에 이 속성에 직접 접근하는 대신 `get_queryset()`을 호출하는 것이 중요하다.
- `serializer_class`<br>
  입력의 유효성을 확인하고 직렬화를 해제하고 출력을 직렬화할 때 사용되는 시리얼라이저 클래스. 일반적으로, 이 속성을 설정하거나 `get_serializer_class()` 메서드를 override해야 한다.
- `lookup_field`<br>
  각각의 모델 인스턴스의 객체 조회에 사용되는 모델 필드. 기본값은 `pk`. 하이퍼링크 된 API를 사용할 때 사용자 정의 값을 사용해야하면 API 뷰와 시리얼라이저 클래스 *둘 모두*가 조회 필드를 설정한다는 점에 유의한다.
- `lookup_url_kwarg`<br>
  객체 조회에 사용되는 URL 키워드 인자. URLconf는 이 값에 해당하는 키워드 인자를 포함해야 한다. 기본값은 `lookup_field`와 같은 값이다.

##### 페이지네이션
다음의 속성은 리스트 뷰와 함께 사용할 때 페이지네이션을 제어하는데 사용된다.
- `pagination_class`<br>
  리스트 결과를 페이지네이션할 때 사용하는 페이지네이션 클래스. 기본값은 `rest_framework.pagination.PageNumberPagination`인 `DEFAULT_PAGINATION_CLASS` 설정과 같은 값이다. `pagination_class=None`으로 설정하면 이 뷰에서 페이지네이션을 비활성화하게 된다.

##### 필터링
- `filter_backends`<br>
  Queryset을 필터링할 때 사용하는 필터 백엔드 클래스 리스트. 기본값은 `DEFAULT_FILTER_BACKENDS` 설정과 같은 값을 가진다.

#### 메서드
##### 기본 메서드
- `get_queryset(self)`<br>
  리스트 뷰에 사용되며 디테일 뷰에서의 조회의 기반으로 사용되는 queryset을 반환한다. `queryset` 속성에 의해 구체화된 queryset을 반환하는 기본 동작을 가진다.

  `self.queryset`이 단 한번 도출된 후 이후의 모든 요청을 위해 그 결과가 캐싱되기 때문에 `self.queryset`에 직접 접근하는 대신 이 메서드를 사용해야 한다.

  요청을 생성하는 사용자와 관련된 queryset을 반환하는 것과 같은 동적 동작을 제공하기 위해 override되어야 할 수 있다.


  예시

  ```python
  def get_queryset(self):
      user = self.request.user
      return user.accounts.all()
  ```

  - Note<br>
    만약 제네릭 뷰에서 사용된 `serializer_class`가 orm 관계에 걸쳐 n+1 문제를 야기한다면 이 메서드 안에서 `select_related`와 `prefetch_related`를 사용하여 queryset을 최적화할 수 있다. n+1 문제와 언급된 메서드를 사용하는 예시에 관한 더 많은 정보를 보려면 [django documentation](https://docs.djangoproject.com/en/3.2/ref/models/querysets/#django.db.models.query.QuerySet.select_related)의 연관 섹션을 참고한다.

- `get_object(self)`<br>
  디테일 뷰에 사용되는 객체 인스턴스를 반환한다. 기본적으로 기본 queryset을 필터링하기 위해 `lookup_field` 인자를 사용한다.

  하나 이상의 URL 키워드 인자를 기반으로 한 객체 조회와 같은 더 복잡한 동작을 제공하기 위해 override될 수 있다.

  다음은 예시이다.

  ```python
  def get_object(self):
      queryset = self.get_queryset()
      filter = {}
      for field in self.multiple_lookup_fields:
        filter[field] = self.kwargs[field]
      
      obj = get_object_or_404(queryset, **filter)
      self.check_object_permissions(self.request, obj)
      return obj
  ```

  만약 API가 어떠한 객체 레벨 권한도 포함하고 있지 않다면 `self.check_object_permissions`를 제외하고 단순히 `get_object_or_404` 조회 결과 객체를 반환하면 된다.

- `filter_queryset(self, queryset)`<br>
  주어진 queryset을 백엔드에서 사용 중인 필터로 필터링한 후 새로운 queryset으로 반환한다.

  다음은 예시이다.

  ```python
  def filter_queryset(self, queryset):
      filter_backends = [CategoryFilter]

      if 'geo_route' in self.request.query_params:
          filter_backends = [GeoRouteFilter, CategoryFilter]
      elif 'geo_point' in self.request.query_params:
          filter_backends = [GeoPointFilter, CategoryFilter]

      for backend in list(filter_backends):
          queryset = backend().filter_queryset(self.request, queryset, view=self)

      return queryset
  ```

- `get_serializer_class(self)`<br>
  시리얼라이저를 위해 사용되는 클래스를 반환한다. 기본적으로 `serializer_class` 속성을 반환한다.

  읽기와 쓰기 작업에 서로 다른 시리얼라이저를 사용하거나 다른 유형의 사용자에게 다른 시리얼라이저를 제공하는 것과 같은 동적 동작을 제공하려면 override해야 한다.

  다음은 예시이다.

  ```python
  def get_serializer_class(self):
      if self.reqeust.user.is_staff:
          return FullAccountSerializer
      return BasicAccountSerializer
  ```

##### 저장과 삭제 훅
다음의 메서드는 mixin 클래스에 의해 제공되며, 객체 저장이나 삭제 동작의 쉬운 overriding을 제공한다.

- `perform_create(self, serializer)`<br>
  새로운 객체 인스턴스를 저장할 때 `CreateModelMixin`이 호출한다.
- `perform_update(self, serializer)`<br>
  존재하는 객체 인스턴스를 저장할 때 `UpdateModelMixin`이 호출한다.
- `perform_destroy(self, instance)`<br>
  객체 인스턴스를 삭제할 때 `DestroyModelMixin`이 호출한다.

이러한 훅은 요청에서 명시된 속성을 설정하는데 특히 유용하지만 요청 데이터의 일부는 아니다. 예를 들어, 요청 사용자 또는 URL 키워드 인자에 기반하여 객체에 속성을 설정할 때:

  ```python
  def perform_create(self, serializer):
      serializer.save(user=self.request.user)
  ```

이러한 override 지점은 확인 메일을 전송하거나 업데이트 로그를 작성할 때와 같이 객체를 저장하기 전 또는 후에 일어나는 동작을 추가하는데도 특히 유용하다.

```python
def perform_update(self, serializer):
    instance = serializer.save()
    send_email_confirmation(user=self.request.user, modified=instance)
```

또한 `ValidationError()`를 발생시키는 것으로 추가적인 유효성 검사를 제공하는데 이러한 훅을 사용할 수도 있다. 데이터베이스 저장 지점에 유효성 논리를 추가하고 싶을 때 유용할 수 있다. 다음은 예시이다.

```python
def perform_create(self, serializer):
    queryset = SignupRequest.objects.filter(user=self.request.user)
    if queryset.exists():
        raise ValidationError('You have already signed up')
    serializer.save(user=self.request.user)
```

##### 기타 메서드
`GenericAPIView`를 사용해 사용자 정의 뷰를 작성할 때 호출할 필요가 생길지라도 보통은 다음의 메서드를 override할 필요가 없다.

- `get_serializer_context(self)`<br>
  시리얼라이저에 제공되어야 하는 추가 컨텍스트를 포함하는 딕셔너리를 반환한다. 기본적으로 `request`, `view`, `format` 키를 포함하여 동작한다.
- `get_serializer(self, instance=None, data=None, many=False, partial=False)`<br>
  시리얼라이저 인스턴스를 반환한다.
- `get_paginated_response(self, data)`<br>
  페이지네이션된 `Response` 객체를 반환한다.
- `paginate_queryset(self, queryset)`<br>
  페이지 객체, 혹은 이 뷰에서 페이지네이션이 구성되지 않은 경우 `None`을 반환해 필요한 경우 queryset을 페이지네이션한다.
- `filter_queryset(self, queryset)`<br>
  주어진 queryset을 백엔드에서 사용하는 필터로 필터링해서 새로운 queryset으로 반환한다.

## Mixins
Mixin 클래스는 기본 뷰 동작을 제공하기 위해 사용되는 동작을 제공한다. Mixin 클래스는 `.get()`과 `.post()` 같은 핸들러 메서드를 직접 정의하는 대신 동작 메서드를 제공한다. 이는 동작을 더 유연하게 구성할 수 있게 한다.

Mixin 클래스는 `rest_framework.mixins`에서 가져올 수 있다.

### `ListModelMixin`
Queryset 리스트를 구현하는 `.list(request, *args, **kwargs)` 메서드를 제공한다.

Queryset이 채워졌다면 queryset의 직렬화된 표현을 응답 바디로 해 `200 OK` 응답을 반환한다. 응답 데이터는 페이지네이션 될 수 있다.

### `CreateModelMixin`
새로운 모델 인스턴스 생성과 저장을 구현하는 `.create(request, *args, **kwargs)` 메서드를 제공한다.

만약 객체가 생성되면 객체의 직렬화된 표현을 응답의 바디로 해서 `201 Created` 응답을 반환한다. 만약 그 표현이 `url`이라는 이름의 키를 포함한다면 응답의 `Location` 헤더는 그 값으로 채워진다.

만약 객체를 생성하는데 제공된 요청 데이터가 유효하지 않다면 에러 상세 내용을 응답의 바디로 한 `400 Bad Request` 응답이 반환된다.

### `RetrieveModelMixin`
하나의 존재하는 모델 인스턴스를 응답으로 반환하게 하는 `.retrieve(request, *args, **kwargs)`를 제공한다.

만약 객체를 찾을 수 있다면 객체의 직렬화된 표현을 응답의 바디로 해 `200 OK` 응답을 반환한다. 그렇지 않다면 `404 Not Found`를 반환한다.

### `UpdateModelMixin`
존재하는 모델 인스턴스를 갱신하고 저장하게 하는 `.update(request, *args, **kwargs)` 메서드를 제공한다.

또한 갱신 대상인 모든 필드가 선택 입력인 점을 제외하면 `update` 메서드와 유사한 `.partial_update(request, *args, **kwargs)` 메서드를 제공한다. 이는 HTTP `PATCH` 요청을 지원하게 한다.

만약 객체가 갱신되면 객체의 직렬화된 표현을 응답의 바디로 해 `200 OK` 응답을 반환한다.

만약 객체를 갱신하기 위해 제공된 요청 데이터가 유효하지 않다면 에러 상세 사항을 응답의 바디로 한 `400 Bad Request` 응답이 반환된다.

### `DestroyModelMixin`
존재하는 모델 인스턴스 삭제를 구현하는 `.destroy(request, *args, **kwargs)` 메서드를 제공한다. 만약 객체가 삭제된다면 `204 No Content` 응답을 반환하며, 그렇지 않을 경우 `404 Not Found`를 반환한다.

