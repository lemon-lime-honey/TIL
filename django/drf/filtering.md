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
초기 queryset 필터링의 최종 예시는 url 내의 쿼리 인자에 기반한 초기 queryset을 결정하는 것이다.

`.get_queryset()`을 override해 `http://example.com/api/purchases?username=lime`와 같은 URL을 다루고 URL에 `username` 인자가 포함된 경우 queryset을 필터링하게 한다.

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