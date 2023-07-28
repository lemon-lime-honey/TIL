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

# API Reference
## AllowAny
`AllowAny` 권한 클래스는 **요청이 인증 되었는지 여부와는 관계없이** 제한 없는 접근을 허용한다.

이 권한은 권한 설정에서 빈 리스트나 튜플을 사용하여 같은 결과를 얻을 수 있기 때문에 엄격하게 요구되는 것은 아니지만 의도를 명확하게 해주기 때문에 이 클래스를 명시하는 것이 유용하다.

## IsAuthenticated
`IsAuthenticated` 권한 클래스는 인증되지 않은 사용자에게는 권한을 거부하지만 그렇지 않다면 권한을 허용한다.

이 권한은 등록된 사용자만이 API에 접근할 수 있게 하는 경우 적절하다.

## IsAdminUser
`IsAdminUser` 권한 클래스는 권한이 허용되는 경우인 `user.is_staff`가 `True`인 경우를 제외하면 모든 사용자의 권한을 거부한다.

이 권한은 믿을 수 있는 관리자의 부분집합만이 API에 접근할 수 있게 하는 경우 적절하다.

## IsAuthenticatedOrReadOnly
`IsAuthenticatedOrReadOnly`는 인증된 사용자가 요청을 수행하는 것을 허용한다. 인증되지 않은 사용자를 위한 요청은 요청 메서드가 `GET`, `HEAD`, `OPTION`과 같은 "안전한" 메서드 중 하나일 때에만 허가된다.

이 권한은 API가 익명의 사용자에게 읽기 권한을 허용하지만 쓰기 권한은 인증된 사용자에게만 허용하도록 할 때 유용하다.

## DjangoModelPermissions
이 권한 클래스는 Django의 표준 `django.contrib.auth` [모델 권한](https://docs.djangoproject.com/en/stable/topics/auth/customizing/#custom-permissions)에 묶인다. 이 권한은 `.queryset` 속성이나 `get_ queryset()` 메서드를 가지는 뷰에만 적용되어야 한다. 권한(Authorization)은 사용자가 *인증되었고* 할당된 *관련된 모델 권한*을 가지고 있을 때에만 승인된다. `get_queryset().model`이나 `queryset.model`을 체크하는 것으로 적절한 모델이 결정된다.

- `POST` 요청을 사용하려면 사용자에게 모델에 대한 `add` 권한이 있어야 한다.
- `PUT`과 `PATCH` 요청을 사용하려면 사용자에게 모델에 대한 `change` 권한이 있어야 한다.
- `DELETE` 요청을 사용하려면 사용자에게 모델에 대한 `delete` 권한이 있어야 한다.

사용자 정의 모델 권한을 지원하기 위해 기본 동작을 override할 수 있다. 예를 들어, `GET` 요청을 위한 `view` 모델 권한을 포함할 수 있다.

사용자 정의 모델 권한을 사용하려면 `DjangoModelPermissions`를 override하고 `.perms_map` 속성을 설정한다. 자세한 사항은 소스코드를 참조한다.

## DjangoModelPermissionsOrAnonReadOnly
`DjangoModelPermissions`와 유사하나 인증되지 않은 사용자의 API에 대한 읽기 전용 접근을 허용한다.

## DjangoObjectPermissions
이 권한 클래스는 모델에서 객체당 권한을 허용하는 Django의 표준 [객체 권한 프레임워크](https://docs.djangoproject.com/en/stable/topics/auth/customizing/#handling-object-permissions)에 묶인다. 이 권한 클래스를 사용하려면 [django-guardian](https://github.com/lukaszb/django-guardian)과 같은 객체 수준 권한을 지원하는 권한 백엔드를 추가해야 한다.

`DjangoModelPermissions`처럼, 이 권한은 `.queryset` 속성 또는 `.get_queryset()` 메서드를 가지는 뷰에만 적용되어야 한다. 권한(Authorization)은 사용자가 *인증되었고* 할당된 *관련된 객체당 권한*과 *관련된 모델 권한*을 가지고 있을 때에만 승인된다.

- `POST` 요청을 사용하려면 사용자에게 모델에 대한 `add` 권한이 있어야 한다.
- `PUT`과 `PATCH` 요청을 사용하려면 사용자에게 모델에 대한 `change` 권한이 있어야 한다.
- `DELETE` 요청을 사용하려면 사용자에게 모델에 대한 `delete` 권한이 있어야 한다.

`DjangoObjectPermissions`는 `django-guardian` 패키지를 필요로 **하지 않으며** 다른 객체 수준 백엔드 또한 잘 지원한다는 점에 유의한다.

`DjangoModelPermissions`처럼, `DjangoObjectPermissions`를 override하고 `.perms_map` 속성을 설정해 사용자 정의 모델 권한을 사용할 수 있다. 자세한 사항은 소스코드를 참조한다.

- **Note**:<br>
`GET`, `HEAD`, `OPTIONS` 요청을 위한 객체 수준 `view` 권한을 필요로 하고, 객체 수준 권한 백엔드로 django-guardian을 사용 중이라면 [`djangorestframework-guardian` 패키지](https://github.com/rpkilby/django-rest-framework-guardian)가 제공하는 `DjangoObjectPermissionsFilter` 클래스를 사용할 수 있다. 이는 리스트 엔드포인트가 오직 사용자가 적절한 뷰 권한을 가지고 있는 객체를 포함한 결과를 반환한다는 것을 보장한다.

# Custom permissions
사용자 정의 권한을 구현하려면 `BasePermissions`을 override하고 다음의 메서드를 둘 다, 혹은 하나만 구현한다.

- `.has_permission(self, request, view)`
- `.has_object_permission(self, request, view, obj)`

이 메서드는 요청의 접근이 허용되면 `True`, 아니면 `False`를 반환해야 한다.

요청이 읽기 연산인지 혹은 쓰기 연산인지를 확인할 필요가 있다면 `'GET'`, `'OPTIONS'`, `'HEAD'`를 포함하는 튜플인 상수 `SAFE_METHODS`에 대해 요청 메서드를 확인해야 한다. 예를 들어:

```python
if request.method in permissions.SAFE_METHODS:
    # Check permissions for read-only request
else:
    # Check permissions for write request
```

- **Note**:<br>
  인스턴스 수준 `has_object_permission` 메서드는 뷰 수준 `has_permission` 체크가 이미 통과되었을 때에만 호출된다. 또한 인스턴스 수준 체크가 진행되려면 뷰 코드는 명시적으로 `.check_object_permissions(request, obj)`를 호출해야 한다. 제네릭 뷰를 사용한다면 기본값으로 이것이 다뤄진다. (함수 기반 뷰는 실패 시 `PermissionDenied`를 발생시키는 식으로 객체 권한을 명시적으로 확인해야 한다.)

사용자 정의 권한은 만약 테스트에 실패하는 경우 `PermissionDenied` 예외를 발생시킨다. 예외에 관련된 오류 메시지를 변경하려면 사용자 정의 권한에 `message` 속성을 직접 구현한다. 그렇게 하지 않으면 `PermissionDenied`의 `defualt_detail` 속성이 사용될 것이다. 비슷하게, 예외에 관련된 코드 식별자를 변경하려면 사용자 정의 권한에 `code` 속성을 직접 구현한다. 그렇게 하지 않으면 `PermissionDenied`의 `default_code` 속성이 사용될 것이다.

```python
from rest_framework import permissions


class CustomerAccessPermission(permissions.BasePermission):
    message = 'Adding customers not allowed.'


    def has_permission(self, request, view):
        ...
```

## Examples
다음은 들어오는 요청의 IP 주소가 차단 리스트에 있는지 확인하고 IP가 차단되었다면 요청을 거부하는 권한 클래스의 예시이다.

```python
from rest_framework import permissions


class BlocklistgPermission(permissions.BasePermission):
    """
    Global permission check for blocked IPs.
    """


    def has_permission(self, request, view):
        ip_addr = request.META['REMOTE_ADDR']
        blocked = Blocklist.objects.filter(ip_addr=ip_addr).exists()
        return not blocked
```

들어오는 요청에 대해 동작하는 전역 권한 뿐만 아니라, 특정 객체 인스턴스에 영향을 주는 권한에 대해서만 동작하는 객체 수준 권한을 생성할 수 있다. 예를 들면:

```python
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
 
        # Instance must have an attribute named `owner`.
        return obj.owner == request.user
```

제네릭 뷰가 적절한 객체 수준 권한을 체크하지만 사용자 정의 뷰를 작성한다면 객체 수준 권한 체크를 직접 확인해야 한다는 점에 유의한다. 객체 인스턴스를 가져오면 뷰에서 `self.check_object_permissions(request, obj)`를 호출하면 이 작업을 수행할 수 있다. 이 호출은 객체 수준 권한 체크에 실패한다면 적절한 `APIException`을 발생시키고, 그렇지 않다면 단순히 반환한다.

제네릭 뷰가 하나의 모델 인스턴스를 가져오는 뷰를 위한 객체 수준 권한만을 체크한다는 점에 유의한다. 객체 수준에서 리스트 뷰를 필터링 해야 한다면 queryset을 별도로 필터링해야 한다. 자세한 사항은 [필터링 문서](https://github.com/lemon-lime-honey/TIL/blob/main/django/drf/authentication.md)에서 확인할 수 있다.

# Overview of access restriction methods
REST framework는 케이스 기반의 접근 제한을 커스터마이즈하기 위한 세 개의 다른 메서드를 제공한다. 메서드는 서로 다른 상황에 적용되고, 다른 효과화 제한을 가진다.

- `queryset`/`get_queryset()`<br>
  데이터베이스에 존재하는 객체의 일반적인 가시성을 제한한다. Queryset은 어느 객체가 list될 것인지와 어느 객체가 수정되거나 삭제될 것인지를 제한한다. `get_queryset()` 메서드는 현재 동작에 기반한 서로 다른 queryset에 적용될 수 있다.
- `permission_classes`/`get_permissions()`<br>
  현재 동작, 요청, 목표 객체에 기반한 일반적인 권한 체크. 객체 수준 권한은 retrieve, 수정 그리고 삭제 동작에만 적용될 수 있다. list와 create를 위한 권한 체크는 모든 객체 타입에 적용된다. (list의 경우: queryset의 제한에 따른다.)
- `serializer_class`/`get_serializer()`<br>
  입출력의 모든 객체에 적용되는 인스턴스 수준 제한. 시리얼라이저가 요청 컨텍스트에 접근할 수 있다. `get_serializer()` 메서드는 현재 동작에 기반한 서로 다른 시리얼라이저에 적용될 수 있다.

다음의 표는 접근 제한 메서드와 메서드가 동작에 따라 제공하는 제어 수준을 열거한다.

| | `queryset` | `permission_classes` | `serializer_class` |
| ---- | --- | --- | --- |
| Action: list | global | global | object-level<sup>*</sup> |
| Action: create | no | global | object-level |
| Action: retrieve | global | object-level | object-level |
| Action: update | global | object-level | object-level |
| Action: partial_update | global | object-level | object-level |
| Action: destroy | global | object-level | no |
| Can reference action in decision | no<sup>**</sup> | yes | no<sup>**</sup> |
| Can reference request in decision | no<sup>**</sup> | yes | yes |

<sup>*</sup> 시리얼라이저 클래스는 모든 list가 반환되지 않는 것을 방지하려면 list 동작에서 PermissionDenied를 발생시키지 않아야 한다.

<sup>**</sup> `get_*()` 메서드는 현재 뷰에 접근해 요청이나 동작에 기반한 서로 다른 Serializer 또는 QuerySet 인스턴스를 반환할 수 있다.

# Third party packages
다음의 서드파티 패키지를 사용할 수도 있다.

## DRF - Access Policy
[Django REST - Access Policy](https://github.com/rsinger86/drf-access-policy) 패키지는 뷰 집합이나 함수 기반 뷰에 첨부된 선언형 정책 클래스에 복잡한 접근 규칙을 정의하는 방법을 제공한다. 정책은 AWS의 식별 및 접근 관리 정책과 유사한 형식의 JSON으로 정의된다.

## Composed Permissions
[Composed Permissions](https://github.com/niwibe/djangorestframework-composed-permissions) 패키지는 작고 재사용 가능한 요소를 사용해 (논리 연산자로) 복잡하고 깊은 권한 객체를 정의하는 단순한 방법을 제공한다.

## REST Condition
[REST Condition](https://github.com/caxap/rest_condition) 패키지는 단순하고 편리한 방식으로 복잡한 권한을 구축하기 위한 또 다른 익스텐션이다. 이 익스텐션은 논리 연산자로 권한을 결합하게 해준다.

## DRY Rest Permissions
[DRY Rest Permissions](https://github.com/FJNR-inc/dry-rest-permissions) 패키지는 개별적인 기본과 사용자 정의 동작을 위한 서로 다른 권한을 정의하기 위한 능력을 제공한다. 이 패키지는 앱의 데이터 모델에서 정의된 관계에서 유도된 권한을 가진 앱을 위해 제작되었다. 또한 API의 시리얼라이저를 통해 클라이언트 앱으로 반환되는 권한 체크를 지원한다. 추가적으로 사용자당 얻는 데이터를 제한하기 위해 기본과 사용자 정의 list 동작에 권한을 추가하는 것을 지원한다.

## Django Rest Framework Roles
[Django Rest Framework Roles](https://github.com/computer-lab/django-rest-framework-roles) 패키지는 여러 타입의 사용자에 대해 API를 더 쉽게 매개변수화해준다.

## Django REST Framework API Key
[Django REST Framework API Key](https://florimondmanca.github.io/djangorestframework-api-key/) 패키지는 API에 API 키 인증을 추가하기 위해 권한 클래스, 모델, 도우미를 제공한다. 사용자 계정을 가지지 않는 내부 혹은 서드파티 백엔드와 서비스 (예: *machines*)에게 권한을 부여하기 위해 사용할 수 있다. API 키는 Django의 비밀번호 해싱 기반을 사용하여 안전하게 저장되며 언제든지 Django 관리자에서 확인, 수정, 삭제할 수 있다.

## Django Rest Framework Role Filters
[Django Rest Framework Role Filters](https://github.com/allisson/django-rest-framework-role-filters) 패키지는 여러 타입의 역할에 대한 단순한 필터링을 제공한다.

## Django Rest Framework PSQ
[Django Rest Framework PSQ](https://github.com/drf-psq/drf-psq)는 권한 기반 규칙에 의존하는 동작 기반 **permission_classes**, **serializer_classes**, **queryset**을 제공한다.