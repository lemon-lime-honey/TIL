# [ViewSets](https://www.django-rest-framework.org/api-guide/viewsets/)
```
라우팅이 요청에 어느 컨트롤러를 사용할지 정하면
컨트롤러는 요청을 이해하고 적절한 출력을 생성해야 한다.
- Ruby on Rails 문서
```

Django REST framework는 `ViewSet`이라는 하나의 클래스에서 관련있는 뷰의 집합을 위해 로직을 조합할 수 있게 해준다. 다른 프레임워크에서도 'Resources' 또는 'Controllers'와 같은 이름의 비슷한 개념을 가진 구현물을 찾을 수 있다.

`ViewSet` 클래스는 단순히 **클래스 기반 뷰의 한 종류**이며, `.get()`이나 `.post()` 같은 **메서드 핸들러를 제공하지 않는다.** 대신 `.list()`와 `.create()` 같은 동작을 제공한다.

`ViewSet`의 메서드 핸들러는 `.as_view()` 메서드를 사용해 뷰를 완료하는 시점에 한해 해당하는 동작에 바인딩된다.

보통 url 설정에서 뷰셋 내의 뷰를 명시적으로 등록하는 대신 자동으로 url 설정를 결정하는 라우터 클래스로 뷰셋을 등록한다.

## Example
시스템의 모든 사용자를 리스트화하거나 찾기 위해 사용할 수 있는 뷰셋을 정의해보자.

```python
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from myapps.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.response import Response


class UserViewSet(viewsets.ViewSet):
    """
    사용자 리스트화 또는 조회를 위한 간단한 뷰셋
    """
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_objects_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
```

필요하다면 이 뷰셋을 다음과 같이 두 개의 분리된 뷰에 바인딩할 수 있다:

```python
user_list = UserViewSet.as_view({'get': 'list'})
user_detail = UserViewSet.as_view({'get': 'retrieve'})
```

보통은 이렇게 하지 않고 라우터로 뷰셋을 등록해 url 설정이 자동으로 생성되게 한다.

```python
from myapp.views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
urlpatterns = router.urls
```

직접 뷰셋을 작성하는 대신 기본 동작 집합을 제공하는 베이스 클래스를 사용할 수도 있다. 예를 들어:

```python
class UserViewSet(viewsets.ModelViewSet):
    """
    사용자 인스턴스를 보거나 수정하기 위한 뷰셋
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
```

`View` 클래스 대신 `ViewSet` 클래스를 사용하는데에는 두 가지 주요한 이점이 있다.

- 반복되는 로직이 하나의 클래스로 조합될 수 있다. 위의 예시에서, `queryset`을 한 번만 명시하고 여러 뷰에서 이를 사용할 수 있다.
- 라우터를 사용하기 때문에 URL을 연결하는데 신경을 덜 써도 된다.

둘 모두 포기해야 하는 부분이 있다. 일반적인 뷰와 URL 설정 사용하는 것은 좀 더 명시적이고 더 많은 제어권을 가지게 한다. `ViewSet`은 빠르게 작성하고 싶거나 큰 API에서 이를 통틀어 일관적인 URL 구성을 가지게 하고 싶을 때 도움이 된다.

## ViewSet actions
REST framework에 포함된 기본 라우터는 아래와 같이 표준적인 create/retrieve/update/destroy 스타일 동작 세트를 위한 경로를 제공한다:

```python
class UserViewSet(viewsets.ViewSet):
    """
    라우터 클래스에 의해 처리되는 표준 동작을 보여주는 비어있는 뷰셋 예시

    포맷 접미사를 사용한다면 각 동작에 `format=None` 키워드 인자를 포함시켜야 한다.
    """


    def list(self, request):
        pass


    def create(self, request):
        pass


    def retireve(self, request, pk=None):
        pass


    def update(self, request, pk=None):
        pass


    def partial_update(self, request, pk=None):
        pass


    def destroy(self, request, pk=None):
        pass
```

## Introspecting ViewSet actions
처리하는 동안 `ViewSet`에서 다음 속성을 사용할 수 있다.

- `basename` - 생성되는 URL 이름에 사용되는 기반
- `action` - 현재 동작의 이름 (`list`, `create` 등)
- `detail` - 현재 동작이 리스트 또는 상세 뷰에 할당되었는지 나타내는 불리언
- `suffix` - 뷰셋의 종류를 보여주는 접미사. `detail` 속성을 반영한다.
- `name` - 뷰셋을 위한 표시용 이름. 이 인자는 `suffix`와 상호 배타관계에 있다.
- `description` - 뷰셋 내의 각각의 뷰를 위한 표시용 설명

이러한 특성들을 확인하여 현재 작업에 기반해 동작을 조정할 수 있다. 예를 들어, 다음과 비슷하게 리스트 작업을 제외한 모든 것에 대한 권한을 제한할 수 있다:

```python
def get_permission(self):
    """
    이 뷰가 요구하는 권한 리스트를 인스턴스화하고 반환한다.
    """
    if self.action == 'list':
        permission_classes = [IsAuthenticated]
    else:
        permission_classes = [IsAdminUser]
    return [permission() for permission in permission_classes]
```

### Marking extra actions for routing
만약 라우팅 가능해야 하는 애드-혹 메서드가 있는 경우 `@action` 데코레이터를 사용하여 표시할 수 있다. 일반적인 동작처럼, 추가 동작은 하나의 객체 또는 전체 콜렉션을 대상으로 할 수 있다. 이를 나타내려면 `detail` 인자의 값을 `True` 또는 `False`로 설정한다. 라우터가 URL 패턴을 이에 따라 구성할 것이다. 예를 들어, `DefaultRouter`는 URL 패턴에 pk를 포함하도록 디테일 동작을 구성한다.

추가 동작에 관한 예시:

```python
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from myapp.serializers import UserSerializer, PasswordSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    표준 동작을 제공하는 뷰셋
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'status': 'password set'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False)
    def recent_users(self, request):
        recent_users = User.objects.all().order_by('-last_login')

        page = self.paginate_queryset(recent_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)
```

`action` 데코레이터는 기본적으로 `GET` 요청을 라우팅하지만 `methods` 인자를 설정하면 다른 HTTP 메서드 또한 수용한다. 예를 들어:

```python
@action(detail=True, methods=['post', 'delete'])
def unset_password(self, request, pk=None):
    ...
```

이 데코레이터는 `permission_classes`, `serializer_class`, `filter_backends`와 같은 뷰셋 수준 구성을 재정의할 수 있게 한다:

```python
@action(detail=True, methods=['post'], permission_classes=[IsAdminOrIsSelf])
def set_password(self, request, pk=None)
```

위의 두 새로운 동작은 url `^users/{pk}/set_password/$`와 `^users/{pk}/unset_password/$`에서 사용할 수 있게 된다. `url_path`와 `url_name` 인자를 사용해 URL 일부와 동작의 reverse URL 이름을 바꿀 수 있다.

모든 추가 동작을 보려면, `.get_extra_actions()` 메서드를 호출한다.

### Routing additional HTTP methods for extra actions
추가 동작은 `ViewSet` 메서드를 분리하기 위해 추가적인 HTTP 메서드를 매핑할 수 있다. 예를 들어, 위의 비밀번호 설정/제거 메서드는 하나의 경로로 통합될 수 있다. 추가적인 매핑이 인자를 허용하지 않는 점에 주의한다.

```python
@action(detail=True, methods=['put'], name='Change Password')
def password(self, request, pk=None):
    """사용자 비밀번호 갱신"""
    ...

@password.mapping.delete
def delete_password(self, request, pk=None):
    """사용자 비밀번호 삭제"""
    ...
```

## Reversing action URLs
만약 동작으로부터 그 URL을 얻어야 한다면 `.reverse_action()` 메서드를 사용한다. 이는 자동으로 뷰의 `request` 객체를 전달하고 `url_name` 앞에 `.basename` 속성값을 추가하는 `reverse()`의 편리한 wrapper이다.

`basename`이 `ViewSet` 등록 중 라우터에 의해 제공된다는 점에 주의한다. 만약 라우터를 사용하지 않는다면 `.as_view()` 메서드에 `basement` 인자를 제공해야 한다.

이전 섹션에서의 예시를 사용한다면:

```python
>>> view.reverse_action('set-password', args=['1'])
'http://localhost:8000/api/users/1/set_password'
```

`@action` 데코레이터에 의해 설정된 `url_name` 속성을 사용할 수도 있다.

```python
>>> view.reverse_action(view.set_password.url_name, args=['1'])
'http://localhost:8000/api/users/1/set_password'
```

`.reverse_action()`을 위한 `url_name` 인자는 `@action` 데코레이터의 동일한 인자와 일치해야 한다. 추가적으로, 이 메서드는 `list`와 `create` 같은 기본 동작의 reverse를 구할 때에도 사용할 수 있다.

# API Reference
## ViewSet
`ViewSet` 클래스는 `APIView` 클래스를 상속한다. 뷰셋의 API 정책을 제어하기 위해 `permission_classes`, `authentication_classes`와 같은 표준 특성들을 사용할 수 있다.

`ViewSet` 클래스는 동작의 구현을 포함하지 않는다. `ViewSet` 클래스를 사용하려면 클래스를 재정의하고 동작 구현을 명시적으로 정의해야 한다.

## GenericViewSet
`GenericViewSet` 클래스는 `GenericAPIView` 클래스를 상속하며 기본적인 `get_object`, `get_queryset` 메서드 세트와 기본적으로는 어떠한 동작도 포함하지 않는 다른 제네릭 뷰 기반 동작을 제공한다.

`GenericViewSet` 클래스를 사용하려면 클래스를 재정의하고 필요한 mixin 클래스를 조합하거나 동작 구현을 명시적으로 정의한다.

## ModelViewSet
`ModelViewSet` 클래스는 `GenericAPIView` 클래스를 상속하며 다양한 mixin 클래스의 동작을 조합해 다양한 동작 구현을 포함한다.

`ModelViewSet` 클래스가 제공하는 동작에는 `.list()`, `.retrieve()`, `.create()`, `.update()`, `.partial_update()`, `.destroy()`가 있다.

### Example
`ModelViewSet`이 `GenericAPIView`를 확장하기 때문에 보통 최소한 `queryset`, `serializer_class` 속성을 제공해야 한다. 예를 들어:

```python
class AccountViewSet(viewsets.ModelViewSet):
    """
    계정을 확인하고 수정하기 위한 간단한 뷰셋
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAccountAdminOrReadOnly]
```

`GenericAPIView`가 제공하는 표준 특성이나 재정의된 메서드를 사용할 수 있다. 예를 들어, 작동해야할 queryset을 동적으로 결정하는 `ViewSet`을 사용하려면 이런 식으로 해야 한다.

```python
class AccountViewSet(viewsets.ModelViewSet):
    """
    사용자와 연결된 계정을 확인하고 수정하기 위한 간단한 뷰셋
    """
    serializer_class = AccountSerializer
    permission_classes = [IsAccountAdminOrReadOnly]

    def get_queryset(self):
        return self.request.user.accounts.all()
```

그러나 `ViewSet`에서 `queryset` 속성을 제거하면 연결된 [라우터](./routers.md)가 자동으로 모델의 basename을 유도할 수 없으므로 [라우터 등록](./routers.md)을 할 때 `basename` 키워드 인자를 명시해야 한다는 점에 유의한다.

또한 이 클래스가 기본으로 create/list/retrieve/update/destroy 동작의 완전한 집합을 제공할지라도, 표준 권한 클래스를 사용하여 사용 가능한 동작을 제한할 수 있다는 점에 유의한다.

## ReadOnlyModelViewSet
`ReadOnlyModelViewSet` 클래스 또한 `GenericAPIView` 클래스를 상속한다. `ModelViewSet`처럼 다양한 동작 구현을 제공하지만 `ModelViewSet`과는 달리 오직 `.list()`와 `.retrieve()`와 같은 '읽기 전용' 동작만 제공한다.

### Example
`ModelViewSet`처럼, 보통 최소한 `queryset`과 `serializer_class` 속성을 제공해야 한다. 예를 들어:

```python
class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    계정 조회를 위한 간단한 뷰셋
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
```

`ModelViewSet`처럼, `GenericAPIView`에 의해 사용 가능한 표준 특성과 재정의된 메서드를 사용할 수 있다.

## Custom ViewSet base classes
전체 `ModelViewSet` 동작 세트를 가지지 않은 사용자 정의 `ViewSet`을 제공하거나 다른 방법으로 동작을 수정해야 할 수도 있다.

### Example
`create`, `list`, `retrieve` 동작을 제공하고 `GenericViewSet`과 필요로 하는 동작을 조합하는 기본 뷰셋 클래스를 작성하려면:

```python
from rest_framework import mixins

class CreateListRetrieveViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                Viewsets.GenericViewSet):
    """
    `retrieve`, `create`, `list` 동작을 제공하는 뷰셋.

    사용하려면 클래스를 재정의하고 `.queryset`과 `.serializer_class` 속성을 설정한다.
    """
    pass
```

기본 `ViewSet` 클래스를 직접 작성하여 API를 통틀어 여러 뷰셋에서 재사용할 수 있는 공통 동작을 제공할 수 있다.