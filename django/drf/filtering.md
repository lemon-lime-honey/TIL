# [Filtering](https://www.django-rest-framework.org/api-guide/filtering/)
```
매니저에 의해 제공된 루트 QuerySet은 데이터베이스 테이블에 있는 모든 객체를 설명한다.
그럼에도 불구하고 보통은 객체의 전체 모음의 부분을 선택한다.
- Django 공식문서
```

REST framework의 제네릭 리스트 뷰의 기본 동작은 모델 매니저를 위한 전체 queryset을 반환하는 것이다. 때로 queryset이 반환하는 아이템을 API가 한정하기를 원할 것이다.

`GenericAPIView`의 서브클래스인 뷰의 queryset을 필터링하는 가장 단순한 방법은 `.get_queryset()` 메서드를 override하는 것이다.

이 메서드를 override하면 뷰가 반환하는 queryset을 다양한 방법으로 커스터마이즈 할 수 있다.

## Filtering against the current user
요청을 생성한 현재 인증된 사용자에 관한 결과만 반환하도록 queryset을 필터링할 수 있다.

`request.user` 값에 기반해 필터링하면 된다.

예를 들어:

```python
from myapp.models import Purchase
from myapp.serializers import PurchaseSerializer
from rest_framework import generics


class PurchaseList(generics.ListAPIView):
    serializer_class = PurchaseSerializer


    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Purchase.objects.filter(purchaser=user)
```

## Filtering against the URL
다른 방식의 필터링은 URL의 일부를 기반으로 한 queryset 제한을 포함할 수 있다.

예를 들어, URL 설정이 다음과 같은 엔트리를 포함하고 있다면:

```python
re_path('^purchases/(?P<username>.+)/$', PurchaseList.as_view()),
```

URL의 사용자명 부분으로 필터링된 구매 queryset을 반환하는 뷰를 작성할 수 있다.

```python
class PurchaseList(generics.ListAPIView):
    serializer_class = PurchaseSerializer


    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        username = self.kwargs['username']
        return Purchase.objects.filter(purchaser__username=username)
```

## Filtering against query parameters
초기 queryset 필터링의 최종 예시는 url 내의 쿼리 파라미터에 기반한 초기 queryset을 결정하는 것이다.

`.get_queryset()`을 override해 `http://example.com/api/purchases?username=lime`와 같은 URL을 다루고 URL에 `username` 파라미터가 포함된 경우 queryset을 필터링하게 한다.

```python
class PurchaseList(generics.ListAPIView):
    serializer_class = PurchaseSerializer


    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Purchase.objects.all()
        username = self.request.query_params.get('username')
        if username is not None:
            queryset = queryset.filter(purchaser__username=username)
        return queryset
```

# Generic Filtering
기본 queryset을 override할 수 있게 하는 것 뿐만 아니라, REST framework는 쉽게 복잡한 검색과 필터링을 할 수 있게 해주는 제네릭 필터링 백엔드 지원을 포함한다.

제네릭 필터는 브라우징 가능한 API와 관리자 API에서 HTML 컨트롤로 나타난다.

![filter controls](https://www.django-rest-framework.org/img/filter-controls.png)

## Setting filter backends
기본 필터 백엔드는 `DEFAULT_FILTER_BACKENDS` 설정을 이용해 전역적으로 설정될 수 있다. 예를 들어:

```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}
```

`GenericAPIView` 클래스 기반 뷰를 사용하여 뷰당 또는 viewset당 기반으로 필터 백엔드를 설정할 수 있다.

```python
import django_filters.rest_framework
from django.contrib.auth.models import User
from myapp.serializers import UserSerializer
from rest_framework import generics


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [django_filter.rest_framework.DjangoFilterBackend]
```

## Filtering and object lookups
필터 백엔드가 뷰를 위에 설정된다면, 그것이 리스트 뷰 뿐만 아니라 하나의 객체를 반환하는데 사용되는 queryset을 필터링할 때에도 사용된다는 점에 유의한다.

예를 들어, 이전의 예시와 id가 `4675`인 제품이 주어졌을 때 다음의 URL은 필터링 조건이 주어진 제품 인스턴스에 일치하는지에 따라 대응되는 객체나 404 응답을 반환한다.

```
http://example.com/api/products/4675/?category=clothing&max_price=10.00
```

## Overriding the initial queryset
Override된 `.get_queryset()`과 제네릭 필터링을 함께 사용해 원하는 결과를 얻을 수 있다. 예를 들어, `Product`가 `User`와 `purchase`라는 이름으로 다대다 관계를 가진다면 다음과 같은 뷰를 작성할 수 있다.

```python
class PurchasedProductsList(generics.ListAPIView):
    """
    Return a list of all the products that the authenticated
    user has ever purchased, with optional filtering.
    """
    model = Product
    serializer_class = ProductSerializer
    filterset_class = ProductFilter


    def get_queryset(self):
        user = self.request.user
        return user.purchase_set.all()
```

# API Guide
## DjangoFilterBackend
`django-filter` 라이브러리는 REST framework를 위한 고도의 커스터마이즈를 할 수 있는 필드 필터링을 지원하는 `DjangoFilterBackend`를 포함한다.

`DjangoFilterBackend`를 사용하려면 우선 `django-filter`를 설치한다.

```bash
pip install django-filter
```

Django의 `INSTALLED_APPS`에 `django_filters`를 추가한다.

```python
INSTALLED_APPS = [
    ...
    'django_filters',
    ...
]
```

설정에 필터 백엔드를 추가하거나:

```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}
```

개별 View 또는 ViewSet에 필터 백엔드를 추가한다.

```python
from django_filters.rest_framework import DjangoFilterBackend


class UserListView(generics.ListAPIView):
    ...
    filter_backends = [DjangoFilterBackend]
```

그저 단순한 등식 기반의 필터링만을 필요로 한다면 필터링하고 싶은 필드 모음을 리스트로 만들어 뷰 또는 viewset에 `filterset_fields` 속성을 설정하면 된다.

```python
class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'in_stock']
```

이는 주어진 필드를 위해 `FilterSet` 클래스를 생성하고 다음과 같은 요청을 생성할 수 있게 한다:

```
http://example.com/api/products?category=clothing&in_stock=True
```

더 자세한 필터링 요구 사항은 뷰에서 사용할 `FilterSet` 클래스에서 명시하면 된다. `FilterSet`에 관해서는 [django-filter 문서](https://django-filter.readthedocs.io/en/latest/index.html)를 확인하면 된다. [DRF integration](https://django-filter.readthedocs.io/en/latest/guide/rest_framework.html) 섹션을 보는 것 또한 권장된다.

## SearchFilter
`SearchFilter` 클래스는 [Django 관리자의 검색 기능](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields)에 기반한 단순한 하나의 쿼리 파라미터를 기반으로 한 검색을 지원한다.

사용하면 브라우징 가능한 API는 `SearchFilter` 컨트롤을 가지게 된다:

![search filter](https://www.django-rest-framework.org/img/search-filter.png)

`SearchFilter` 클래스는 뷰가 `search_fields` 속성 설정을 가질 때에만 적용된다. `search_fields` 속성은 `CharField` 또는 `TextField`와 같은 모델의 텍스트 타입 필드의 이름 리스트여야 한다.

```python
from rest_ramework import filters


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']
```

이는 클라이언트가 다음과 같은 쿼리를 생성하여 리스트 안의 요소를 필터링할 수 있게 한다.

```
http://example.com/api/users?search=russell
```

또한 조회 API 이중 언더스코어 표기를 사용해 ForeignKey 또는 ManyToManyField에서 연관된 조회를 할 수 있다:

```python
search_fields = ['username', 'email', 'profile__profession']
```

[JSONField](https://docs.djangoproject.com/en/3.0/ref/contrib/postgres/fields/#jsonfield)와 [HStoreField](https://docs.djangoproject.com/en/3.0/ref/contrib/postgres/fields/#hstorefield)의 경우 동일한 이중 언더스코어 표기를 사용해 자료 구조 내에서 중첩된 값을 기반으로 필터링할 수 있다.

```python
search_fields = ['data__breed', 'data__owner__other_pets__0__name']
```

기본적으로 검색은 대소문자를 가리지 않는 부분일치 검색이다. 검색 파라미터는 공백 그리고/또는 반점으로 분리된 복수의 검색 조건을 포함할 수 있다. 복수의 검색 조건이 사용된다면 객체가 모든 주어진 조건을 만족하는 경우에만 리스트에 들어가 반환된다.

`search_fields`에 여러 문자를 추가해 검색 동작을 제한할 수 있다.

- `^`: ~로 시작하는 검색
- `=`: 완전 일치
- `@`: 풀텍스트 검색(현재 Django의 [PostgreSQL 백엔드](https://docs.djangoproject.com/en/stable/ref/contrib/postgres/search/)에만 지원된다.)
- `$`: 정규식 검색

예를 들어:

```python
search_fields = ['=username', 'email']
```

기본적으로 검색 파라미터는 `'search'`라는 이름을 가지지만, `SEARCH_PARAM` 설정으로 override할 수 있다.

요청 컨텐츠에 기반해 검색 필드를 동적으로 변경하려면 `SearchFilter`의 서브클래스를 생성하고 `get_search_fields()` 함수를 override한다. 예를 들어, 다음의 서브클래스는 요청에 쿼리 파라미터 `title_only`가 있다면 `title`에 관해서만 검색한다.

```python
from rest_framework import filters


class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
      if request.query_params.get('title_only'):
          return ['title']
      return super().get_search_fields(view, request)
```

자세한 사항은 [Django 공식문서](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields)에서 확인할 수 있다.

## OrderingFilter
`OrderingFilter` 클래스는 결과 정렬에 의해 제어되는 단순한 쿼리 파라미터를 지원한다.

![ordering filter](https://www.django-rest-framework.org/img/ordering-filter.png)

기본적으로, 쿼리 파라미터는 `'ordering'`이름을 가지지만 `ORDERING_PARAM` 설정으로 override될 수 있다.

예를 들어, 사용자명으로 사용자를 정렬하려면:

```
http://example.com/api/users?ordering=username
```

클라이언트는 다음과 같이 필드 이름 앞에 `-`를 붙여 반전된 정렬을 명시할 수 있다:

```
http://example.com/api/users?ordering=-username
```

복수 정렬 또한 명시될 수 있다:

```
http://example.com/api/users?ordering=account,username
```

### Specifying which fields may be ordered against
API가 어느 필드를 정렬 필터에서 허용해야할지 명시적으로 지정하는 것을 권장한다. 다음과 같이 뷰에서 `ordering_fields` 속성을 설정하면 된다:

```python
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['username', 'email']
```

이는 사용자를 비밀번호 해시 필드나 다른 민감한 데이터로 정렬하는 것과 같은 예측하지 못한 데이터 유출을 방지할 수 있다.

뷰에 `ordering_fields ` 속성을 명시하지 *않는다면*, 필터 클래스는 `serializer_class` 속성에 의해 명시된 시리얼라이저의 임의의 읽기 가능한 필드를 사용해 필터링할 수 있게 허용한다.

뷰가 사용하는 queryset이 민감한 데이터를 포함하고 있지 않다면 특수값 `'__all__`을 사용하여 뷰가 *임의의* 모델 필드 또는 queryset 집합에 대한 정렬을 허용하도록 명시적으로 지정할 수 있다.

```python
class BookingsListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'
```

### Specifying a default ordering
뷰에 `ordering` 속성이 설정되어 있다면 이것이 기본 정렬로 사용된다.

보통 초기 queryset에 `order_by`를 설정하여 이를 제어하지만, 뷰에서 `ordering` 파라미터를 사용하면 렌더링된 컨텍스트로 자동으로 전달되는 방식으로 순서를 지정할 수 있다. 이는 열 헤더가 결과를 정렬하는데 사용되었을 때 자동으로 열 헤더를 다르게 렌더링할 수 있게 허용한다.

```python
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['username', 'email']
    ordering = ['username']
```

`ordering` 속성은 문자열이나 문자열의 리스트/튜플이다.

# Custom generic filtering
직접 작성한 제네릭 필터링 백엔드를 제공하거나 다른 개발자가 사용할 수 있는 설치 가능한 앱을 작성할 수도 있다.

그렇게 하려면 `BaseFilterBackend`를 override하고 `.filter_queryset(self, request, queryset, view)` 메서드를 override한다. 메서드는 새로운 필터링된 queryset를 반환한다.

제네릭 필터 백엔드는 클라이언트가 검색과 필터링을 수행할 수 있게 할 뿐만 아니라 주어진 요청이나 사용자가 어느 객체를 볼 수 있게 할지 제한할 때에도 유용하다.

## Example
예를 들어, 사용자가 자기가 생성한 객체만 볼 수 있게 할 수 있다.

```python
class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)
```

뷰에서 `get_queryset()`을 override하여 같은 동작을 얻을 수 있지만, 필터 백엔드를 사용하는 것은 더 쉽게 복수의 뷰에 이 제한을 추가하거나 전체 API에 적용할 수 있게 한다.

## Customizing the interface
제네릭 필터는 브라우징 가능한 API에서 인터페이스로 나타날 수 있다. 그렇게 하려면 필터의 렌더링된 HTML 표현을 반환하는 `to_html()` 메서드를 구현해야 한다. 이 메서드는 다음의 시그니처를 가진다:

`to_html(self, request, queryset, view)`

이 메서드는 렌더링된 HTML 문자열을 반환한다.

## Filtering & schemas
`get_schema_fields()` 메서드를 구현해 REST framework가 제공하는 스키마 자동생성에 필터 제어를 사용할 수 있도록 할 수도 있다. 이 메서드는 다음의 시그니처를 가진다:

`get_schema_fields(self, view)`

이 메서드는 `coreapi.Field` 인스턴스의 리스트를 반환해야 한다.

# Third party packages
다음의 서드파티 패키지는 추가적인 필터 구현을 제공한다.

## Django REST framework filters package
[django-rest-framework-filters 패키지](https://github.com/philipn/django-rest-framework-filters)는 `DjangoFilterBackend` 클래스와 함께 동작하며, 관계에 걸쳐 쉽게 필터를 생성하거나 주어진 필드를 위한 복수의 필터 조회 타입을 생성할 수 있게 한다.

## Django REST framework full word search filter
[djangorestframework-word-filter](https://github.com/trollknurr/django-rest-framework-word-search-filter)는 텍스트 또는 완전 일치로 전체 단어를 검색하는 `filters.SearchFilter`의 대체제로 개발되었다.

## Django URL Filter
[django-url-filter](https://github.com/miki725/django-url-filter)는 인간 친화적인 URL을 통해 데이터를 필터링하는 안전한 방법을 제공한다. filterset과 filter로 불리는 것을 제외한다면 중첩될 수 있다는 점에서 DRF 시리얼라이저, 필드와 매우 유사하게 동작한다. 연관된 데이터를 필터링하는 쉬운 방법을 제공한다. 또한 이 라이브러리는 범용이므로 Django의 `QuerySet` 뿐만 아니라 다른 데이터 소스를 필터링할 때에도 사용할 수 있다.

## drf-url-filters
[drf-url-filter](https://github.com/manjitkumar/drf-url-filters)는 drf `ModelViewSet`의 `Queryset`을 깨끗하고 단순하며 설정 가능한 방법으로 필터를 적용할 수 있게 해주는 간단한 Django 앱이다. 들어오는 쿼리 파라미터와 그 값에 대한 유효성 검사 또한 지원한다. 들어오는 쿼리 파라미터에 대한 유효성 검사를 위해서 아름다운 파이썬 패키지인 `Voluptuous`가 사용된다. Voluptuous의 가장 훌륭한 점은 쿼리 파라미터 요구사항에 따라 유효성 검사를 정의할 수 있다는 것이다.