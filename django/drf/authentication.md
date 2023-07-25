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

# API Reference
## BasicAuthentication
이 인증 스킴은 사용자의 사용자명과 비밀번호에 대해 서명된 [HTTP 기본 인증](https://tools.ietf.org/html/rfc2617)을 사용한다. 기본 인증은 보통 테스트에만 적절하다.

성공적으로 인증되었다면, `BasicAuthentication`은 다음의 자격을 제공한다.

- `request.user`는 Django의 `User` 인스턴스가 된다.
- `request.auth`는 `None`이 된다.

권한이 거부된 인증되지 않은 응답은 적절한 WWW-Authenticate 헤더을 가진 `HTTP 401 Unauthorized` 응답이 된다. 예를 들면:

```
WWW-Authenticate: Basic realm="api"
```

- **Note**:<br>
  `BasicAuthentication`을 제품에서 사용한다면 API가 오직 `https`를 통해서만 사용 가능하게 해야 한다. 또한 API 클라이언트가 로그인을 할 때 언제나 사용자명과 비밀번호를 재요청하게 해야하고, 절대 영구 저장소에 그러한 정보를 저장하지 않도록 해야한다.

## ToeknAuthentication
- **Note**:<br>
  Django REST framework가 제공하는 토큰 인증은 꽤 단순한 구현이다.

  유저당 하나 이상의 토큰을 허용하는, 더 엄격한 보안 디테일을 가지며 토큰 만료를 지원하는 구현을 원한다면 서드파티 패키지 [Django REST Knox](https://github.com/James1345/django-rest-knox)를 확인한다.

이 인증 스킴은 단순한 토큰 기반 HTTP 인증 스킴을 사용한다. 토큰 인증은 네이티브 데스크탑과 모바일 클라이언트와 같은 클라이언트-서버 구성에 적합하다.

`TokenAuthentication` 스킴을 사용하려면 `TokenAuthentication`을 포함하게 하고 추가적으로 `INSTALLED_APPS` 설정에 `rest_framework.authtoken`을 포함하게 하기 위해 [인증 클래스를 설정](https://github.com/lemon-lime-honey/TIL/blob/main/django/drf/authentication.md#setting-the-authentication-shceme)할 필요가 있다.

```python
INSTALLED_APPS = [
    ...
    'rest_framework.authtoken'
]
```

설정을 변경한 후 `manage.py migrate`를 반드시 실행한다.

`rest_framework.authtoken` 앱은 Django 데이터베이스 마이그레이션을 제공한다.

또한 사용자를 위한 토큰을 생성해야 한다.

```python
from rest_framework.authtoken.models import Token

token = Token.objects.create(user=...)
print(token.key)
```

클라이언트 인증을 위해서, 토큰 키는 `Authorization` HTTP 헤더에 포함되어야 한다. 키는 문자열 "Token"으로 시작해야 하며, 두 문자열 사이는 공백으로 분리되어야 한다. 예를 들어:

```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

*헤더에 `Bearer`와 같은 다른 키워드를 사용하고 싶다면 그저 `TokenAuthentication`의 서브클래스를 생성하고 `keyword` 클래스 변수를 설정하면 된다.*

성공적으로 인증되었다면 `TokenAuthentication`은 다음 자격을 제공한다.

- `request.user`는 Django의 `User` 인스턴스가 된다.
- `request.auth`는 `rest_framework.authtoken.models.Token`의 인스턴스가 된다.

권한이 거부된 인증되지 않은 응답은 적절한 WWW-Authenticate 헤더을 가진 `HTTP 401 Unauthorized` 응답이 된다. 예를 들면:

```
WWW-Authenticate: Token
```

토큰 인증된 API를 테스트할 때 `curl` 명령줄 도구가 유용하다. 예를 들면:

```bash
curl -X GET http://127.0.0.1:8000/api/example/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'
```

`TokenAuthentication`을 제품에서 사용한다면 API가 오직 `https`를 통해서만 사용 가능하게 해야 한다.

### Generating Tokens
#### By using signals
모든 사용자가 자동으로 생성된 토큰을 가지게 하려면 사용자의 `post_save` 시그널을 감지하면 된다.

```python
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
```

이 코드 조각을 설치된 `models.py` 모듈이나 Django가 시작될 때 불러올 다른 장소에 위치시켜야 한다.

이미 사용자를 생성했다면, 존재하는 사용자를 위한 토큰은 다음과 같이 생성할 수 있다.

```python
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

for user in User.objects.all():
    Token.objects.get_or_create(user=user)
```

#### By exposing an api endpoint
`TokenAuthentication`을 사용할 때 클라이언트가 사용자명과 비밀번호가 주어진 토큰을 얻게 하는 매커니즘을 제공할 수 있다. REST framework는 이 동작을 제공하기 위해 빌트인 뷰를 제공한다. 이를 사용하려면 URLconf에 `obtain_auth_token` 뷰를 추가한다.

```python
from rest_framework.authtoken import views

urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token)
]
```

패턴의 URL 부분은 뭐든지 될 수 있다.

`obtain_auth_token` 뷰는 유효한 `username`과 `password` 필드가 폼 데이터 혹은 JSON을 사용해 뷰에 POST되었을 때 JSON 응답을 반환한다.

```
{ 'token' : '9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b' }
```

기본 `obtain_auth_token` 뷰는 설정의 기본 렌더러와 parser 클래스를 사용하기보다 JSON 요청과 응답을 명시적으로 사용한다.

기본적으로 `obtain_auth_token` 뷰에는 적용된 권한이나 스로틀링이 없다. 스로틀을 적용하려면 뷰 클래스를 override하고 `throttle_classes` 속성을 이용해 포함시킨다.

사용자 정의 버전 `obtain_auth_token` 뷰가 필요하다면 `ObtainAuthToken` 뷰의 서브클래스를 생성하고 url 설정에서 그것을 사용한다.

예를 들어, `token` 값 이외에 추가 사용자 정보를 반환할 수 있다.

```python
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
```

`urls.py`에서는

```python
urlpatterns += [
    path('api-token-auth/', CustomAuthToken.as_view())
]
```

#### With Django admin
관리자 인터페이스를 통해 토큰을 수동으로 생성할 수도 있다. 큰 사용자 베이스를 사용하는 경우 `TokenAdmin` 클래스를 필요에 따라, 더 자세히는 `user` 필드를 `raw_field`로 선언해 커스터마이즈하기 위해 몽키패치하는 걸 추천한다.

`your_app/admin.py`:

```python
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']
```

#### Using Django manage.py command
버전 3.6.4부터 다음 명령어로 사용자 토큰을 생성할 수 있게 되었다.

```bash
./manage.py drf_create_token <username>
```

이 명령은 주어진 사용자를 위한 API 토큰을 반환하는데, 존재하지 않으면 생성한다.

```bash
Generated token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b for user user1
```

토큰을 재생성하고 싶은 경우(가령 손상되었거나 유출되었을 때) 추가 인자를 전달한다.

```bash
./manage.py drf_create_token -r <username>
```

## SessionAuthentication
이 인증 스킴은 Django의 인증을 위한 기본 세션 백엔드를 사용한다. 세션 인증은 웹사이트와 같은 세션 컨텍스트에서 동작하는 AJAX 클라이언트에 적합하다.

성공적으로 인증되었다면 `SessionAuthentication`은 다음 자격을 제공한다.

- `request.user`는 Django `User` 인스턴스가 된다.
- `request.auth`는 `None`이 된다.

권한이 거부된 인증되지 않은 응답은 `HTTP 403 Forbidden` 응답이 된다.

SessionAuthentication과 함께 AJAX 스타일 API를 사용한다면 `PUT`, `PATCH`, `POST`, `DELETE` 요청과 같은 "안전하지 않은" HTTP 메서드 호출을 위한 유효한 CSRF 토큰을 포함시켜야 한다. 자세한 사항은 [Django CSRF 문서](https://docs.djangoproject.com/en/stable/ref/csrf/#ajax)에서 확인할 수 있다.

- **경고**:<br>
  로그인 페이지를 생성할 때에는 언제나 Django의 기본 로그인 뷰를 사용한다. 이는 로그인 뷰가 적절히 보호되는 것을 보장한다.

REST framework의 CSRF 유효성 검사는 같은 뷰에 세션 기반, 세션을 기반으로 하지 않은 인증을 지원해야 할 필요성 때문에 표준 Django와 약간 다르다. 이는 오직 인증된 요청이 CSRF 토큰을 필요로 하며, 익명의 요청은 CSRF 토큰 없이 송신된다는 것을 의미한다. 이 동작은 언제나 CSRF 유효성 검사를 적용해야 하는 로그인 뷰에는 적합하지 않다.

## RemoteUserAuthentication
이 인증 스킴은 인증을 `REMOTE_USER` 환경 변수를 설정하는 웹 서버에 위임하는 것을 허용한다.

이를 사용하려면 `AUTHENTICATION_BACKENDS` 설정에 `django.contrib.auth.backends.RemoteUserBackend` 혹은 그 서브클래스가 있어야 한다. 기본적으로 `RemoteUserBackend`는 이미 존재하지 않는 유저명을 위해 `User` 객체를 생성한다. 이것과 다른 동작을 변경하려면 [Django 문서](https://docs.djangoproject.com/en/stable/howto/auth-remote-user/)를 참조한다.

성공적으로 인증되었다면 `RemoteUserAuthentication`은 다음 자격을 제공한다.

- `requset.user`는 Django `User` 인스턴스가 된다.
- `request.auth`는 `None`이 된다.

인증 방법을 설정하는 것에 관한 정보를 확인하려면 다음과 같은 웹 서버의 문서를 확인한다.

- [Apache Authentication How-To](https://httpd.apache.org/docs/2.4/howto/auth.html)
- [NGINX (Restricting Access)](https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-http-basic-authentication/)