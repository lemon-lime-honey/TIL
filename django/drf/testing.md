# [Testing](https://www.django-rest-framework.org/api-guide/testing/)
```
테스트를 하지 않은 코드는 설계된 대로 고장난다.
- Jacob Kaplan-Moss
```

REST framework는 Django의 테스트 프레임워크를 확장하고 API 요청에 대한 지원을 개선하는 몇 가지 헬퍼 클래스를 포함한다.

# APIRequestFactory
[Django의 `RequestFactory` 클래스](https://docs.djangoproject.com/en/stable/topics/testing/advanced/#django.test.client.RequestFactory)를 확장한다.

## Creating test requests
`APIRequestFactory` 클래스는 Django의 표준 `RequestFactory` 클래스와 거의 동일한 API를 지원한다. 이는 표준 `.get()`, `.post()`, `.put()`, `.patch()`, `.delete()`, `.head()`, `.options()` 메서드를 모두 사용할 수 있다는 것을 의미한다.

```python
from rest_framework.test import APIRequestFactory

# Using the standard RequestFactory API to create a form POST request
factory = APIRequestFactory()
request = factory.post('/notes/', {'title': 'new idea'})
```

### Using the `format` argument
`post`, `put`, `patch`와 같이 요청 바디를 생성하는 매서드는 multipart 폼 데이터 이외의 컨텐츠 타입을 사용하는 요청을 쉽게 생성하기 위해 `format` 인자를 포함한다.

```python
# Create a JSON POST request
factory = APIRequestFactory()
request = factory.post('/notes/', {'title': 'new idea'}, format='json')
```

기본적으로 사용가능한 포맷은 `'multipart'`와 `'json'`이다. Django의 `RequestFactory`와의 호환성을 위해 기본 포맷은 `'multipart'`이다.

더 다양한 요청 포맷 모음을 지원하거나 기본 포맷을 변경하려면 [설정 섹션](#configuration)을 확인한다.

### Explicitly encoding the request body
요청 바디를 명시적으로 인코딩해야 한다면 `content_type` 플래그를 설정한다. 예를 들어:

```python
request.factory.post('/notes/', json.dumps({'title': 'new idea'}), content_type='application/json')
```

### PUT and PATCH with form data
Djangod의 `RequestFactory`와 REST framework의 `APIRequestFactory` 사이에서 주목할 만한 한 가지 차이점은 multipart 폼 데이터가 `.post()` 이외의 다른 메서드에서도 인코딩된다는 점이다.

예를 들어, `APIRequsetFactory`를 사용하면 폼 PUT 요청을 다음과 같이 생성할 수 있다:

```python
factory = APIRequestFactory()
request = factory.put('/notes/547/', {'title': 'remember to email dave'})
```

Django의 `RequestFactory`를 사용하면 데이터를 직접 명시적으로 인코딩해야 한다:

```python
from django.test.client import encode_multipart, RequestFactory

factory = RequestFactory()
data = {'title': 'remember to email dave'}
content = encode_multipart('BoUnDaRyStRiNg', data)
content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
request = factory.put('/notes/547/', content , content_type=content_type)
```

## Forcing authentication
요청 팩토리를 사용해 뷰를 직접적으로 테스트할 때, 올바른 인증 자격 증명을 구축하는 대신 요청을 직접 인증할 수 있게 하는 것이 편리하다.

강제로 요청을 인증하려면 `force_authenticate()` 메서드를 사용한다.

```python
from rest_framework.test import force_authenticate

factory = APIRequestFactory()
user = User.objects.get(username='olivia')
view = AccountDetail.as_view()

# Make an authenticated request to the view...
request = factory.get('/accounts/django-superstars/')
force_authenticate(request, user=user)
response = view(request)
```

이 메서드의 시그니처는 `force_authenticate(request, user=None, token=None)`이다. 호출할 때 사용자나 토큰 중 최소 하나는 설정되어야 한다.

예를 들어, 토큰을 사용해 강제로 인증할 때 다음과 같이 한다:

```python
user = User.objects.get(username='olivia')
request = factory.get('/accounts/django-superstars/')
force_authenticate(request, user=user, token=user.auth_token)
```

- **Note**: `force_authenticate`는 인메모리 `user` 인스턴스에 `request.user`를 직접 설정한다. 저장된 `user` 상태를 갱신하는 복수의 테스트에서 같은 `user`를 재사용한다면 테스트 중간에 `refresh_from_db()`를 호출해야 한다.

- **Note**:<br>
  `APIRequestFactory`를 사용할 때 반환되는 객체는 뷰가 호출되었을 때 오직 단 한 번 생성되는 REST framework의 `Request` 객체가 아니라 Django의 표준 `HttpRequest` 객체이다.

  이는 요청 객체에 속성을 직접 설정하는 것이 언제나 예상한 결과를 불러오지는 않는다는 것을 의미한다. 예를 들어, `.token`을 직접 설정하는 것은 아무런 효과가 없고, `.user`를 직접 설정하는 것은 세션 인증이 사용될 때에만 동작한다.

  ```python
  # Request will only authenticate if `SessionAuthentication` is in use.
  request = factory.get('/accounts/django-superstars/')
  request.user = user
  response = view(request)
  ```

## Forcing CSRF validation
기본적으로 `APIRequestFactory`로 생성되는 요청은 REST framework 뷰로 전달될 때 CSRF 검증이 적용되지 않는다. 명시적으로 CSRF 검증을 설정해야한다면 팩토리를 인스턴스화할 때 `enforce_csrf_checks` 플래그를 설정한다.

```python
factory = APIRequestFactory(enforce_csrf_checks=True)
```

**Note**: Django의 표준 `RequestFactory`는 이 옵션을 포함할 필요가 없다는 점에 주목할 만한데, 이는 일반적인 Django를 사용할 때 CSRF 검증이 뷰를 직접 테스트할 때 실행되지 않는 미들웨어에서 수행되기 때문이다. REST framework를 사용할 때에는 CSRF 검증이 뷰 안에서 수행되기 때문에 요청 팩토리는 뷰 수준 CSRF 검사 비활성을 필요로 한다.

# APIClient
Django의 [`Client` 클래스](https://docs.djangoproject.com/en/stable/topics/testing/tools/#the-test-client)를 확장한다.

## Making requests
`APIClient` 클래스는 Django의 표준 `Client` 클래스와 같은 요청 인터페이스를 제공한다. 이는 표준 `.get()`, `.post()`, `.put()`, `.patch()`, `.delete()`, `.head()`, `.options()` 메서드를 모두 사용할 수 있다는 것을 의미한다. 예를 들어:

```python
from rest_framework.test import APIClient

client = APIClient()
client.post('/notes/', {'title': 'new idea'}, format='json')
```

더 다양한 요청 포맷 모음을 지원하거나 기본 포맷을 변경하려면 [설정 섹션](#configuration)을 확인한다.

## Authenticating
### .login(**kwargs)
`login` 메서드는 Django의 `Client` 클래스에서와 동일하게 동작한다. 이는 `SessionAuthentication`을 포함하는 뷰에 대한 요청을 인증할 수 있게 한다.

```python
# Make all requests in the context of a logged in session.
client = APIClient()
client.login(username='lauren', password='secret')
```

로그아웃하려면 통상적인 방법으로 `logout` 메서드를 호출한다.

```python
# Log out
client.logout()
```

`login` 메서드는 API와의 AJAX 상호작용을 포함하는 웹사이트와 같은 세션 인증을 사용하는 API를 테스트하기에 적합하다.

### .credentials(**kwargs)
`credentials` 메서드는 테스트 클라이언트에 의해 다음 요청에 포함될 헤더를 설정하는데 사용된다.

```python
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

# Include an appropriate `Authorization:` header on all requests.
token = Token.objects.get(user__username='lauren')
client = APIClient()
client.credentials(HTTP_AUTHENTICATION='Token ' + token.key)
```

두 번째로 `credentials`를 호출하면 존재하는 모든 자격 증명을 덮어쓴다는 점에 유의한다. 인자 없이 메서드를 호출해 존재하는 자격 증명을 모두 해제할 수도 있다.

```python
# Stop including any credentials
client.credentials()
```

`credentials` 메서드는 기본 인증, OAuth1a, OAuth2 인증, 단순한 토큰 인증 스킴과 같은 인증 헤더를 필요로 하는 API를 테스트하기에 적합하다.

### .force_authentication(user=None, token=None)
인증 전체를 건너뛰고 모든 테스트 클라이언트에 의한 요청이 자동으로 인증된 것으로 취급되도록 강제해야 할 때가 있다.

API를 테스트하는 중이지만 테스트 요청을 생성하기 위해 유효한 인증 자격 증명을 구축할 필요는 없는 경우, 이는 유용하게 사용할 수 있는 손쉬운 방법이 될 수 있다.

```python
user = User.objects.get(username='lauren')
client = APIClient()
client.force_authenticate(user=user)
```

후속 요청의 인증을 해제하려면 user 그리고/또는 token이 `None`으로 설정된 `force_authenticate`를 호출한다.

```python
client.force_authentication(user=None)
```

## CSRF validation
기본적으로 `APIClient`를 사용할 때 CSRF 검증이 적용되지는 않는다. 명시적으로 CSRF 검증을 사용하려면 클라이언트를 인스턴스화할 때 `enforce_csrf_checks` 플래그를 설정한다.

```python
client = APIClient(enforce_csrf_checks=True)
```

통상적인 경우와 마찬가지로 CSRF 인증은 세션 인증된 뷰에만 적용된다. 이는 클라이언트가 `login()`을 호출하여 로그인한 경우에만 CSRF 인증이 발생한다는 것을 의미한다.