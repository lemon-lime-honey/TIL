# [Permissions](https://www.django-rest-framework.org/api-guide/permissions/)
```
인증 또는 식별은 보통 정보나 코드에 접근하기에는 충분하지 못하다.
이를 위해서, 접근을 요청하는 엔터티는 권한(authorization)을 가져야 한다.

- 애플 개발자 문서
```

[인증](https://github.com/lemon-lime-honey/TIL/blob/main/django/drf/authentication.md), [스로틀링](https://github.com/lemon-lime-honey/TIL/blob/main/django/drf/throttling.md)과 함께, 권한은 요청의 접근을 허용할지 거부할지를 결정한다.

권한 확인은 언제나 다른 코드가 진행되도록 허용되기 전, 뷰의 가장 시작점에서 실행된다. 권한 확인은 보통 들어오는 요청의 허가 여부를 결정하기 위해 `request.user`와 `request.auth` 속성 내의 인증 정보를 사용한다.

권한은 API의 다른 부분의 다른 클래스의 사용자들의 접근을 허용할지 거부할지를 결정하기 위해 사용된다.

권한의 가장 단순한 방식은 모든 인증된 사용자의 접근을 허용하고 인증되지 않은 사용자의 접근을 거부한다. 이는 REST framework의 `IsAuthenticated` 클래스에 대응된다.

약간 덜 엄격한 형식의 권한은 인증된 사용자에게 완전한 접근을 허용하지만 인증되지 않은 사용자에게는 읽기 전용 접근을 허용한다. 이는 REST framework의 `IsAuthenticatedOrReadOnly` 클래스에 대응된다.

## How permissions are determined
REST framework의 권한은 언제나 권한 클래스의 리스트로 정의된다.

뷰의 메인 바디를 실행하기 전에 리스트 내의 각 권한이 체크된다. 만약 권한 체크에 실패한다면 `exceptions.PermissionDenied` 또는 `exceptions.NotAuthenticated` 예외가 발생하며 뷰의 메인 바디는 실행되지 않을 것이다.

권한 체크에 실패한다면, 다음 규칙에 의해 "403 Forbidden" 또는 "401 Unauthorized" 응답이 반환된다.

- 요청이 성공적으로 인증되었으나 권한이 거절되었을 때<br>
  ***HTTP 403 Forbidden 응답이 반환된다.***
- 요청이 성공적으로 인증되지 못했고, 가장 우선순위가 높은 인증 클래스가 `WWW-Authenticate` 헤더를 *사용하지 않을 때*<br>
  ***HTTP 403 Forbidden 응답이 반환된다.***
- 요청이 성공적으로 인증되지 못했고, 가장 우선순위가 높은 인증 클래스가 `WWW-Authenticate` 헤더를 *사용할 때*<br>
  ***적절한 `WWW-Authenticate` 헤더를 가진 HTTP 401 Unauthorized 응답이 반환된다.***

## Object level permissions
REST framework 권한은 객체 수준 권한 부여 또한 지원한다. 객체 수준 권한은 사용자가 보통 모델 인스턴스인 특정 객체에 어떤 행위를 할 수 있게 허용할 것인지를 결정하는데 사용된다.

객체 수준 권한은 `.get_object()`가 호출되었을 때 REST framework의 제네릭 뷰에 의해 동작한다. 뷰 수준 권한처럼 사용자가 주어진 객체에 무언가 하는 것을 허용하지 않을 때 `exceptions.PermissionDenied` 예외가 발생한다.

뷰를 직접 작성하고 객체 수준 권한을 강제하고 싶거나 제네릭 뷰의 `get_object` 메서드를 override한다면, 객체를 불러온 시점에서 뷰의 `.check_object_permissions(request, obj)` 메서드를 명시적으로 호출할 필요가 있다.

이는 `PermissionDenied` 혹은 `NotAuthenticated` 예외를 발생시키거나 단순히 뷰가 적절한 권한을 가지고 있는지를 반환한다.

예를 들어:

```python
def get_object(self):
    obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
    self.check_object_permissions(self.request, obj)
    return obj
```

- **Note**: <br>
  `DjangoOjbectPermissions`의 예외와 함께, `rest_framework.permissions` 에서 제공된 권한 클래스는 객체 권한을 체크하기 위해 필요한 메서드를 **구현하지 않는다**.

  객체 권한을 체크하기 위해 제공된 권한 클래스를 사용한다면 **반드시** 서브클래스를 생성하고 아래의 [Custom permissions](https://github.com/lemon-lime-honey/TIL/blob/main/django/drf/permissions.md#custom-permissions) 섹션에서 설명된 `has_object_permission()` 메서드를 구현해야 한다.

### Limitations of object level permissions
성능 상의 이유로 제네릭 뷰는 객체 리스트를 반환할 때 queryset의 각 인스턴스에 객체 수준 권한을 자동으로 적용하지 않는다.

때로 객체 수준 권한을 사용할 때 사용자가 볼 수 있도록 허용된 인스턴스만 볼 수 있도록 하기 위해 [queryset을 적절히 필터링](https://www.django-rest-framework.org/api-guide/filtering/)할 수 있다.

`get_object()` 메서드가 호출되지 않기 때문에, `has_object_permission()` 메서드에서 기인하는 객체 수준 권한은 객체를 생성할 때에는 **적용되지 않는다**. 객체 생성을 제한하기 위해서, 시리얼라이저 클래스에 권한 체크를 구현하거나 ViewSet 클래스의 `perform_create()` 메서드를 override해야 한다.

## Setting the permission policy
기본 권한 정책은 `DEFAULT_PERMISSION_CLASSES` 설정을 사용해 전역적으로 설정될 수 있다. 예를 들면:
```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
```

명시되지 않았다면 이 설정은 기본적으로 제한되지 않은 접근을 허용한다.

```python
'DEFAULT_PERMISSION_CLASSES': [
    'REST_framework.permissions.AllowAny',
]
```

또한 `APIView` 클래스 기반 뷰를 사용하여 뷰당, viewset당 기반으로 인증 정책을 설정할 수 있다.

```python
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class ExampleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)
```

함수 기반 뷰와 함께 `@api_view` 데코레이터를 사용한다면:

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def example_view(request, format=None):
    content = {
        'status': 'request was permitted'
    }
    return Response(content)
```

- **Note**: <br>
  클래스 속성이나 데코레이터를 통해 새로운 권한 클래스를 설정할 때, 뷰가 **settings.py** 파일에서 설정된 기본 리스트를 무시하도록 해야 한다.

`rest_framework.permissions.BasePermission`을 상속해 제공되기 때문에, 권한은 표준 파이썬 비트 연산자를 사용해 구성될 수 있다. 예를 들어 `IsAuthenticatedOrReadOnly`는 다음과 같이 작성될 수 있다.

```python
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
    

class ExampleView(APIView):
    permission_classes = [IsAuthenticated|ReadOnly]


    def get(self, request, format=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)
```

**Note**: `&`(and), `|`(or), `~`(not)을 지원한다.