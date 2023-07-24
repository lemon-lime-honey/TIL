# [Authentication](https://www.django-rest-framework.org/api-guide/authentication/)
```
Auth는 착탈식일 필요가 있다.
- Jacob Kaplan-Moss, "REST worst practices"
```

인증은 들어오는 요청을 요청을 보내는 사용자나 서명된 토큰과 같은 식별 자격 세트와 연관짓는 매커니즘이다. 그 다음에 [권한](https://www.django-rest-framework.org/api-guide/permissions/)과 [스로틀링](https://www.django-rest-framework.org/api-guide/throttling/)은 요청이 허가되어야 하는지를 결정하기 위해 그러한 자격을 이용한다.

REST framework는 바로 사용할 수 있는 여러 인증 스킴을 제공하며, 사용자 정의 스킴을 구현할 수 있게 허용한다.

인증은 언제나 권한과 스로틀링 체크를 하기 전과 다른 어떤 코드가 진행되도록 허용되기 전에 뷰의 시작지점에서 실행된다.

`request.user` 속성은 보통 `contrib.auth` 패키지의 `User` 클래스의 인스턴스로 설정된다.

`request.auth` 속성은 요청이 서명된 인증 토큰을 표현하는데 사용되는 등과 같은 추가적인 인증 정보에 사용된다.

- **Note**:<br>
  **인증 그 자체는 들어오는 요청을 허용하거나 불허하지 않는다**는 점에 유의한다. 인증은 단순히 요청이 자격을 가지고 있는지를 식별한다.

  API를 위한 인증 정책을 설정하는 방법은 [인증](https://www.django-rest-framework.org/api-guide/permissions/) 문서에서 확인한다.

## How authentication is determined
인증 스킴은 언제나 클래스 리스트로 정의된다. REST framework는 리스트의 각 클래스를 이용해 인증을 시도할 것이며, 첫번째로 인증에 성공하는 클래스의 반환 값을 사용해 `request.user`와 `request.auth`를 설정할 것이다.

어느 클래스도 인증에 성공하지 못한다면, `request.user`는 `django.contrib.auth.models.AnonymousUser`의 인스턴스로 설정되며, `request.auth`는 `None`으로 설정된다.

인증되지 않은 요청을 위한 `request.user`와 `request.auth`의 값은 `UNAUTHENTICATED_USER`와 `UNAUTHENTICATED_TOKEN` 설정을 이용해 변경할 수 있다.

## Setting the authentication shceme
기본 인증 스킴은 다음과 같이 `DEFAULT_AUTHENTICATION_CLASSES` 설정을 이용해 전역적으로 설정될 수 있다.

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}
```

`APIView` 클래스 기반 뷰를 사용해 뷰 당 혹은 뷰셋 당 기반으로 인증 스킴을 설정할 수 있다.

```python
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user), # `django.contrib.auth.User` instance.
            'auth': str(request.auth), # None
        }
        return Response(content)
```

함수 기반 뷰와 `@api_view` 데코레이터를 사용할 수도 있다.

```python
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def example_view(request, format=None):
    content = {
        'user': str(request.user), # `django.contrib.auth.User` instance.
        'auth': str(request.auth), # None
    }
    return Response(content)
```

## Unauthorized and Forbidden responses
인증되지 않은 요청이 권한을 거부당했을 때 발생하기에 적절한 두 에러 코드가 있다.

- [HTTP 401 Unauthorized](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.2)
- [HTTP 403 Permission Denied](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.4)

HTTP 401 응답은 언제나 클라이언트가 어떻게 인증해야 할지를 지시하는 `WWW-Authenticate` 헤더를 포함해야 한다. HTTP 403 응답은 `WWW-Authenticate` 헤더를 포함하지 않는다.

어떤 종류의 응답이 사용될 것인지는 인증 스킴에 따라 다르다. 복수의 인증 스킴이 사용될지라도, 응답의 타입을 결정하는데에는 하나의 스킴만이 사용된다. **응답의 타입을 결정할 때에는 뷰에 설정된 첫번째 인증 클래스가 사용된다.**

인증 스킴에 관계없이 `403 Permission Denied` 응답이 언제나 사용되는 경우에는 요청이 성공적으로 인증되더라도 요청을 실행하기 위한 권한이 거절된다.

## Apache mod_wsgi specific configuration
[mod_wsgi를 사용한 아파치](https://modwsgi.readthedocs.io/en/develop/configuration-directives/WSGIPassAuthorization.html)에 배포하는 경우, 애플리케이션 수준이 아닌 아파치에 의해 인증이 다루어지는 것으로 간주되기 때문에 인증 헤더는 기본적으로 WSGI 애플리케이션을 통해 전달되지 않는다.

세션 기반이 아닌 인증을 사용해 아파치에 배포한다면 애플리케이션을 통해 요구되는 헤더를 전달하도록 mod_wsgi를 명시적으로 설정해야 한다. 적절한 컨텍스트에서 `WSGIPassAuthorization`을 직접 명시하고 `'On'`으로 설정하면 된다.

```bash
# this can go in either server config, virtual host, directory or .htaccess
WSGIPassAuthorization On
```