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

# Custom authentication
사용자 정의 인증 스킴을 구현하려면 `BaseAuthentication`의 서브클래스를 작성하고 `.authenticate(self, request)` 메서드를 override한다. 메서드는 인증에 성공하면 `(user, auth)` 튜플 쌍을, 아니면 `None`을 반환해야 한다.

`None`을 반환하는 대신 `.authenticate()` 메서드가 `AuthenticationFailed` 예외를 발생시키게 할 수도 있다.

일반적으로 취해야 할 접근 방식은 다음과 같다.

- 인증이 시도되지 않는다면 `None`을 반환한다. 사용 중인 다른 인증 스킴 또한 계속 체크한다.
- 인증을 시도했으나 실패한다면 ` AuthenticationFailed` 예외를 발생시킨다. 예외 응답은 권한 체크에 관계 없이, 그리고 다른 인증 스킴 체크 없이 즉시 반환된다.

`.authenticate_header(self, request)` 메서드 또한 override할 수 있다. 구현된다면 `HTTP 401 Unauthorized` 응답 내 `WWW-Authenticate` 헤더의 값으로 사용될 문자열을 반환해야 한다.

만약 `.authenticate_header()` 메서드가 override되지 않았다면 인증 스킴은 인증되지 않은 요청의 접근이 거부되었을 때 `HTTP 403 Forbidden` 응답을 반환한다.

- **Note**:<br>
  요청 객체의 `.user` 또는 `.auth` 속성에 의해 사용자 정의 authenticator가 호출되면 `AttributeError`가 `WrappedAttributeError`로 재발생한다. 이는 속성 외부 접근에 의해 원 예외가 억제되는 것을 방지하기 위해 필요하다. 파이썬은 `AttributeError`가 사용자 정의 authenticator로부터 기인한다는 것을 인지하지 못하며, 그 대신 요청 객체가 `.user` 또는 `.auth` 속성을 가지고 있지 않다고 추정할 것이다. 이러한 오류는 authenticator에 의해 수정되거나 다른 방식으로 다루어져야 한다.

## Example

다음은 'X-USERNAME'이라는 사용자 정의 요청 헤더 안의 사용자명에 의해 주어진 사용자로 들어오는 요청을 인증하는 예시이다.

```python
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions

class ExampleAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        username = request.META.get('HTTP_X_USERNAME')
        if not username:
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)
```

# Third party packages
다음의 서드파티 패키지를 사용할 수 있다.

## django-rest-knox
[Django-rest-knox](https://github.com/James1345/django-rest-knox) 라이브러리는 싱글 페이지 애플리케이션과 모바일 클라이언트를 염두에 두고 토큰 기반 인증을 빌트인 TokenAuthentication 스킴보다 더 안전하고 확장 가능한 방식으로 다루기 위한 모델과 뷰를 제공한다. 클라이언트당 토큰과 다른 인증(주로 기본 인증)이 제공되었을 때 토큰을 생성하고, 토큰을 삭제(서버에 의한 강제 로그아웃 제공)하고, 모든 토큰을 삭제(사용자가 로그인한 모든 클라이언트에서 로그아웃)하기 위한 뷰를 제공한다.

## Django OAuth Toolkit
[Django OAuth Toolkit](https://github.com/evonove/django-oauth-toolkit) 패키지는 OAuth 2.0 지원을 제공하며 파이썬 3.4 이상에서 사용 가능하다. 이 패키지는 [jazzband](https://github.com/jazzband/)가 관리하며 훌륭한 [OAuthLib](https://github.com/idan/oauthlib)를 사용한다. 문서화가 잘 되어 있고, 잘 지원되며 현재 REST framework에서 **OAuth 2.0 지원을 위한 추천하는 패키지**이다.

### Installation & configuration
`pip`을 사용해 설치한다.

```bash
pip install django-oauth-toolkit
```

`INSTALLED_APPS`에 패키지를 추가하고 REST framework 설정을 수정한다.

```python
INSTALLED_APPS = [
    ...
    'oauth2_provider',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ]
}
```

자세한 사항은 [Django REST framework - 시작하기](https://django-oauth-toolkit.readthedocs.io/en/latest/rest-framework/getting_started.html) 문서에서 확인할 수 있다.

## Django REST framework OAuth
[Django REST framework OAuth](https://jpadilla.github.io/django-rest-framework-oauth/) 패키지는 REST framework를 위한 OAuth1과 OAuth2 지원을 모두 제공한다.

이 패키지는 이전에는 REST framework에 직접 포함되어 있었으나 현재는 서드파티 패키지로 지원되고 유지된다.

### Installation & configuration
`pip`을 사용해 패키지를 설치한다.

```bash
pip install djangorestframework-oauth
```

설정과 사용에 관한 자세한 사항은 [인증](https://jpadilla.github.io/django-rest-framework-oauth/authentication/)과 [권한](https://jpadilla.github.io/django-rest-framework-oauth/permissions/)에 관한 Django REST framework OAuth 문서를 확인한다.

## JSON Web Token Authentication
JSON Web Token은 토큰 기반 인증에 사용될 수 있는 상당히 최근의 표준이다. 빌트인 TokenAuthentication 스킴과는 다르게, JWT 인증은 토큰의 유효성을 검증하기 위해 데이터베이스를 사용할 필요가 없다. JWT 인증을 위한 패키지로는 탈착식 토큰 블랙리스트 앱 같은 몇 가지 기능을 제공하는 [djangorestframework-simplejwt](https://github.com/davesque/django-rest-framework-simplejwt)가 있다.

## Hawk HTTP Authentication
[HawkREST](https://hawkrest.readthedocs.io/en/latest/) 라이브러리는 API에서 [Hawk](https://github.com/hueniverse/hawk)로 서명된 요청과 응답을 다룰 수 있게 하기 위해 [Mohawk](https://mohawk.readthedocs.io/en/latest/) 라이브러리 위에 빌드된다. Hawk는 공유된 키에 의해 서명된 메시지를 사용하여 두 집단이 안전하게 소통할 수 있게 한다. 이는 ([OAuth 1.0](https://oauth.net/core/1.0a/)의 일부에 기반했던)[HTTP MAC access authentication](https://tools.ietf.org/html/draft-hammer-oauth-v2-mac-token-05)에 기반한다.

## HTTP Signature Authentication
HTTP Signature (현재는 [IETF draft](https://datatracker.ietf.org/doc/draft-cavage-http-signatures/))는 HTTP 메시지를 위한 출처 인증과 메시지 무결성을 얻기 위한 방법을 제공한다. 많은 아마존 서비스에서 사용하는 [Amazon's HTTP Signature scheme](https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html)과 유사하게 무상태의, 요청당 인증을 허용한다. [Elvio Toccalino](https://github.com/etoccalino/)가 HTTP Signature 인증 메커니즘을 사용하는 쉬운 방법을 제공하는 [djangorestframework-httpsignature](https://github.com/etoccalino/django-rest-framework-httpsignature) (오래됨) 패키지를 관리한다. [drf-httpsig](https://github.com/ahknight/drf-httpsig)라는 갱신된 포크 버전을 사용할 수도 있다.

## Djoser
[Djoser](https://github.com/sunscrapers/djoser) 라이브러리는 등록, 로그인, 로그아웃, 비밀번호 초기화와 계정 활성화 같은 기본 동작을 다루기 위한 뷰의 모음을 제공한다. 이 패키지는 사용자 정의 사용자 모델과 함께 사용할 수 있으며, 토큰 기반 인증을 사용한다. 이것은 Django 인증 시스템의 REST 구현을 사용할 준비가 되었다.

## django-rest-auth / dj-rest-auth
이 라이브러리는 등록, (소셜 미디어 인증을 포함한) 인증, 비밀번호 초기화, 사용자 정보 검색과 갱신을 위한 REST API 엔드포인트 모음을 제공한다. 이 API 엔드포인트를 가지는 것으로 AngularJS, iOS, Android와 같은 클라이언트 앱이 사용자 관리를 위해 REST API를 경유하여 독립적으로 Django 백엔드 사이트와 통신할 수 있다.

현재 이 프로젝트의 두 개의 포크가 있다.

- [Django-rest-auth](https://github.com/Tivix/django-rest-auth)는 원 프로젝트이지만 [현재 갱신되고 있지 않다](https://github.com/Tivix/django-rest-auth/issues/568).
- [Dj-rest-auth](https://github.com/jazzband/dj-rest-auth)는 프로젝트의 더 새로운 포크이다.

## drf-social-oauth2
[Drf-social-oauth2](https://github.com/wagnerdelima/drf-social-oauth2)는 페이스북, 구글, 트위터, Orcid와 같은 유명 소셜 oauth2 벤더로 인증하는 것을 돕는 프레임워크이다. 설치가 쉽고 JWT 방식으로 토큰을 생성한다.

## drfpasswordless
[drefpasswordless](https://github.com/aaronn/django-rest-framework-passwordless)는 (Medium, Square Cash에서 영감을 얻어) Django REST Framework의 TokenAuthentication 스킴에 비밀번호 없는 지원을 추가한다. 사용자는 이메일 주소나 전화번호 같은 연락 지점에 보내진 토큰으로 로그인을 하거나 가입한다.

## django-rest-authemail
[django-rest-authemail](https://github.com/celiao/django-rest-authemail)는 사용자 가입과 인증을 위한 RESTful API 인터페이스를 제공한다. 사용자명 대신 이메일 주소가 인증에 사용된다. API 엔드포인트는 가입, 가입 이메일 검증, 로그인, 로그아웃, 비밀번호 초기화, 비밀번호 초기화 검증, 이메일 변경, 이메일 변경 검증, 비밀번호 변경 그리고 사용자 정보를 위해 사용 가능하다. 완전히 동작하는 예시 프로젝트와 자세한 설명을 포함한다.

## Django-Rest-Durin
[Django-Rest-Durin](https://github.com/eshaan7/django-rest-durin)는 하나의 라이브러리가 하나의 인터페이스를 통해 복수의 웹/CLI/모바일 API 클라이언트를 위한 토큰 인증을 하지만 API를 사용하는 각 API 클라이언트를 위한 다른 토큰 설정을 허용하는 아이디어에서 구축되었다. Django-Rest-Framework에서 사용가능한 사용자 정의 모델, 뷰, 권한을 통한 유저 당 복수의 토큰을 지원한다. 토큰 민료 시간은 API 클라이언트에 따라 다를 수 있으며 Django 관리자 인터페이스를 통해 변경할 수 있다.

더 많은 정보는 [문서](https://django-rest-durin.readthedocs.io/en/latest/index.html)에서 확인할 수 있다.