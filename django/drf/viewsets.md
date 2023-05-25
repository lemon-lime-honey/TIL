# [ViewSets](https://www.django-rest-framework.org/api-guide/viewsets/)
```
라우팅이 요청에 어느 컨트롤러를 사용할지 정한 후, 컨트롤러는 요청을 이해하고 적절한 출력을 생성해야 한다.
- Ruby on Rails 문서
```

Django REST framework는 `ViewSet`이라는 하나의 클래스에서 관련있는 뷰의 모음을 위해 로직을 조합하는 것을 허용한다. 다른 프레임워크에서도 'Resources' 또는 'Controllers'와 같은 이름의 비슷한 개념의 구현물을 찾을 수 있다.

`ViewSet` 클래스는 단순한 **클래스 기반 뷰의 한 종류**이며, `.get()`이나 `.post()` 같은 **메서드 핸들러를 제공하지 않는다.** 대신 `.list()`와 `.create()` 같은 동작을 제공한다.

`ViewSet`의 메서드 핸들러는 `.as_view()` 메서드를 사용해 뷰를 완료하는 시점에 한해 해당하는 동작에 바인딩된다.

보통 urlconf에서 viewset 안의 뷰를 명시적으로 등록하는 대신 자동으로 urlconf를 결정하는 라우터 클래스로 viewset을 등록한다.

## Example
시스템의 모든 유저의 리스트 혹은 유저 하나를 볼 수 있게 하는 간단한 viewset을 정의해보자.

```python
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from myapps.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.response import Response

class UserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
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

필요하다면 이 viewset을 다음과 같이 두 개의 분리된 뷰에 바인딩할 수 있다.

```python
user_list = UserViewSet.as_view({'get': 'list'})
user_detail = UserViewSet.as_view({'get': 'retrieve'})
```

보통은 이렇게 하지 않고 라우터로 viewset을 등록해 urlconf가 자동으로 생성되게 한다.

```python
from myapp.views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
urlpatterns = router.urls
```

직접 viewset을 작성하는 대신 일반적인 동작 모음을 제공하는 이미 존재하는 베이스 클래스를 사용할 수도 있다. 다음은 예시이다.

```python
class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
```

`View` 클래스 대신 `ViewSet` 클래스를 사용하는데에는 두 가지 주요한 이점이 있다.

- 반복되는 로직이 하나의 클래스로 융합될 수 있다. 위의 예시들에서, `queryset`을 한 번만 명시하고 여러 뷰에서 이를 사용할 수 있다.
- 라우터를 사용하기 때문에 URL conf를 연결하는데 신경을 덜 써도 된다.

둘 모두 포기해야 하는 부분이 있다. 일반적인 뷰와 URL conf를 사용하는 것은 좀 더 명시적이고 더 많은 제어권을 가지게 한다. ViewSet은 빠르게 작성하고 싶거나 큰 API를 가졌는데 이를 통틀어 일관적인 URL 설정을 가지게 하고 싶을 때 도움이 된다.