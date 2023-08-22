# Class-based Views
```
Django의 클래스 기반 뷰는 옛 스타일 뷰로부터의 환영할 만한 출발이다.
- Reinout van Rees
```

REST framework는 Django의 `View` 클래스의 서브클래스인 `APIView` 클래스를 제공한다.

`APIView` 클래스는 다음과 같은 점에서 정규 `View` 클래스와 다르다.

- 핸들러 메서드를 통과하는 요청은 Django의 `HttpRequest` 인스턴스가 아닌 REST framework의 `Request` 인스턴스가 된다.
- 핸들러 메서드는 Django의 `HttpResponse` 대신 REST framework의 `Response`를 반환할 것이다. 뷰가 컨텐츠 협상을 관리하고 응답의 적절한 렌더러를 설정할 것이다.
- 어떠한 `APIException` 예외도 포착되어 적절한 응답으로 중개된다.
- 접근하는 요청은 인증될 것이며, 적절한 권한 그리고/또는 스로틀 체크가 요청을 핸들러 메서드에 부착하기 전에 실행된다.

`APIView` 클래스를 사용하는 것은 일반적인 `View` 클래스를 사용하는 것과 거의 같아 접근하는 요청이 `.get()` 또는 `.post()`와 같은 적절한 핸들러 메서드에 부착된다. 추가로, 여러 속성이 API 정책의 다양한 면을 조정하는 클래스에서 설정될 수 있다.

예를 들어:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        username = [user.username for user in User.objects.all()]
        return Response(usernames)
```

- Note:<br>
  Django REST framework의 `APIView`, `GenericAPIView`, 다양한 `Mixin`, `Viewset`의 모든 메서드, 속성, 관계는 초반에 복잡할 수 있다. 여기 있는 문서 외에도 [Classy Django REST Framework](https://www.cdrf.co/)에서도 Django REST Framework의 클래스 기반 뷰 각각에 관한 모든 메서드와 속성을 포함한 탐색 가능한 참조를 제공한다.

## API policy attributes
다음의 속성은 API 뷰의 플러그 가능한 특성을 컨트롤한다.

- `.renderer_classes`
- `.parser_classes`
- `.authentication_classes`
- `.throttle_classes`
- `.permission_classes`
- `.content_negotiation_class`

## API policy instantiation methods
다음의 메서드는 플러그 가능한 다양한 API 정책을 인스턴스화할 때 REST framework에 의해 사용된다. 보통은 override할 필요가 없다.

- `.get_renderers(self)`
- `.get_parsers(self)`
- `.get_authenticatiors(self)`
- `.get_throttles(self)`
- `.get_permissions(self)`
- `.get_content_negotiator(self)`
- `.get_exception_handler(self)`

## API policy implementation methods
다음의 메서드는 핸들러 메서드에 부착되기 전에 호출된다.

- `.check_permissions(self, request)`
- `.check_throttles(self, request)`
- `.perform_content_negotiation(self, request, forse=False)`

## Dispatch methods
다음의 메서드는 뷰의 `.dispatch()` 메서드에 의해 직접적으로 호출된다. `.get()`, `.post()`, `put()`, `patch()`, `.delete()`와 같은 핸들러 메서드를 호출하기 전 혹은 후에 일어나야 할 동작을 실행한다.

- `.initial(self, request, *args, **kwargs)`<br>
  핸들러 메서드가 호출되기 전에 실행되어야 할 동작을 수행한다. 이 메서드는 권한과 스로틀링, 컨텐츠 협상을 실행하기 위해 사용된다.
- `.handle_exception(self, exc)`<br>
  핸들러 메서드에 의해 발생된 모든 예외는 이 메서드를 통과하며, `Response` 인스턴스를 반환하게 하거나 다시 예외를 재발생시킨다.

  기본 구현은 Django의 `Http404`와 `PermissionDenied` 예외 뿐만이 아니라 `rest_framework.exceptions.APIException`의 모든 서브클래스를 다루며, 적절한 에러 응답을 반환한다.

  만약 API가 반환하는 에러 응답을 커스터마이즈 해야 한다면 이 클래스를 override한다.
- `.initialize_request(self, request, *args, **kwargs)`<br>
  핸들러 메서드를 통과한 요청 객체가 일반적인 Django의 `HttpRequest`가 아니라 `Request` 인스턴스인 것을 확실하게 한다.

  보통은 이 메서드를 override할 필요가 없다.
- `.finalize_response(self, request, response, *args, **kwargs)`
  핸들러 메서드에서 반환된 모든 `Response` 객체가 컨텐츠 협상에서 정해진 올바른 컨텐츠 유형으로 렌더링되게 한다.

  보통은 이 메서드를 override할 필요가 없다.

# Function Based Views
```
클래스 기반 뷰가 언제나 우월한 해결법이라고 말하는 것은 실수다.
- Nick Coghlan
```

REST framework는 일반적인 함수 기반 뷰를 다루는 것 또한 허용한다. 함수 기반 뷰를 감싸 (일반적인 Django의 `HttpRequest`가 아닌) `Request` 인스턴스를 받게 하고 (Django의 `HttpResponse`가 아닌) `Response`를 반환하게 하는 단순한 데코레이터 세트를 제공하며 요청이 가공되는 방법을 정하게 한다.

## @api_view()
**Signature:** `@api_view(http_method_names=['GET'])`

이 기능의 핵심은 뷰가 응답해야 하는 HTTP 메서드의 리스트를 가지는 `api_view` 데코레이터이다. 예를 들어, 아래는 그저 약간의 데이터를 직접 반환하게 하는 매우 간단한 뷰를 작성하는 방법이다.

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view()
def hello_world(request):
    return Response({"message": "Hello, world!"})
```

이 뷰는 [settings](settings.md)에서 명시된 기본 렌더러, parser, 인증 클래스 등을 사용할 것이다.

기본으로는 오직 `GET` 메서드만이 허용된다. 다른 메서드는 "405 Method Not Allowed"라고 응답할 것이다. 이를 바꾸려면 아래와 같이 뷰가 허용할 메서드를 명시한다.

```python
@api_view(['GET', 'POST'])
def hello_world(request):
    if request.method == 'POST':
        return Response({"message": "Got some data!", "data": request.data})
    return Response({"message": "Hello, world!"})
```

## API policy decorators
기본 설정을 override하기 위해 REST framework는 뷰에 추가할 수 있는 추가적인 데코레이터 세트를 제공한다. 이는 반드시 `@api_view` 데코레이터 *다음*(아래)에 와야 한다. 예를 들어, 특정 사용자에게 오직 하루에 한 번만 호출될 수 있게 [throttle](throttling.md)을 사용하는 뷰를 작성하려면 throttle 클래스 리스트를 전달하는 `@throttle_classes` 데코레이터를 사용한다.

```python
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttiling import UserRateThrottle

class OncePerDayUserThrottle(UserRateThrottle):
    rate = '1/day'


@api_view(['GET'])
@throttle_classes([OncePerDayUserThrottle])
def view(request):
    return Response({"message": "Hello for today! See you tomorrow!"})
```

다음의 데코레이터는 위에서 묘사된 것처럼 `APIView` 서브클래스에서 설정된 속성에 대응된다.

사용할 수 있는 데코레이터로는 다음이 있다.

- `@renderer_classes(...)`
- `@parser_classes(...)`
- `@authentication_classes(...)`
- `@throttle_classes(...)`
- `@permission_classes(...)`

각각의 데코레이터는 클래스 리스트 혹은 튜플인 하나의 인자를 가진다.

## View schema decorator
함수 기반 뷰를 위한 기본 스키마 생성을 override하려면 `@schema` 데코레이터를 사용한다. 이는 반드시 `@api_view` 데코레이터 *다음*(아래)에 위치해야 한다. 아래는 예시이다.

```python
from rest_framework.decorators import api_view, schema
from rest_framework.schemas import AutoSchema

class CustomAutoSchema(AutoSchema):
    def get_link(self, path, method, base_url):
        # override view introspection here...


@api_view(['GET'])
@schema(CustomAutoSchema())
def view(request):
    return Response({"message": "Hello for today! See you tomorrow!"})
```

이 데코레이터는 [Schemas documentation](schema.md)에서 설명하는 대로 `AutoSchema` 서브클래스 인스턴스 혹은 `ManualSchema` 인스턴스인 `AutoSchema` 인스턴스 하나를 가진다. 뷰를 스키마 생성에서 제외하고 싶다면 `None`을 전달한다.

```python
@api_view(['GET'])
@schema(None)
def view(request):
    return Response({"message": "Will not appear in schema!"})
```