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

# RequestsClient
REST framework는 인기 있는 파이썬 라이브러리, `requests`를 사용하는 애플리케이션과 상호작용하는 클라이언트 또한 포함한다. 이는 이러한 경우 유용하다:

- 다른 파이썬 서비스의 API와 먼저 소통하고 클라이언트가 보는 것과 같은 수준에서 서비스를 테스트하고 싶은 경우
- 스테이징 또는 실시간 환경에서도 동작할 수 있는 방식으로 테스트를 작성하려는 경우 (아래의 "Live test"를 확인한다.)

이는 요청 세션을 직접 사용하는 것과 정확히 같은 인터페이스를 노출한다.

```python
from rest_framework.test import RequestsClient

client = RequestsClient()
response = client.get('http://testserver/users/')
assert response.status_code == 200
```

요청 클라이언트가 정규화된 URL를 요구한다는 점에 유의한다.

## RequestsClient and working with the database
`RequestsClient` 클래스는 서비스 인터페이스와 단독으로 상호작용하는 테스트를 작성할 때 유용하다. 모든 상호작용이 API를 통해야 하므로 표준 Django 테스트 클라이언트를 사용하는 것보다 좀 더 엄격하다.

`RequestsClient`를 사용한다면 테스트 설정과 결과 판정이 데이터베이스 모델과 직접 상호작용하는 대신 일반적인 API 호출 시 동작하기를 원할 것이다. 예를 들어, `Customer.objects.count() == 3`를 확인하는 것 대신 고객 엔드포인트의 리스트를 만들고 그것이 세 개의 레코드를 가지고 있음을 확인할 것이다.

## Headers & Authentication
사용자 정의 헤더와 인증 자격 증명은 [표준 `requests.Session` 인스턴스를 사용할 때](https://requests.readthedocs.io/en/master/user/advanced/#session-objects)와 같은 방식으로 제공될 수 있다.

```python
from requests.auth import HTTPBasicAuth

client.auth = HTTPBasicAuth('user', 'pass')
client.headers.update({'x-test': 'true'})
```

## CSRF
`SessionAuthentication`을 사용한다면 `POST`, `PUT`, `PATCH`, `DELETE` 요청에 대해 CSRF 토큰을 포함해야 한다.

자바스크립트 기반 클라이언트가 사용하는 것과 같은 플로우를 따라하면 그렇게 할 수 있다. 먼저 CSRF 토큰을 얻기 위해 `GET` 요청을 생성하고, 그 다음 요청에서 그 토큰을 사용한다.

예를 들어...

```python
client = RequestsClient()

# Obtain a CSRF token.
response = client.get('http://testserver/homepage/')
assert response.status_code == 200
csrftoken = response.cookies['csrftoken']

# Interact with the API
response = client.post('http://testserver/organisations/', json={
    'name': 'MegaCorp',
    'status': 'active'
}, headers={'X-CSRFToken': csrftoken})
assert response.status_code == 200
```

## Live tests
주의깊게 사용한다면, `RequestsClient`와 `CoreAPIClient`는 개발 중 또는 스테이징 서버나 운영 환경에서 동작할 수 있는 테스트 케이스를 작성할 수 있는 능력을 제공한다.

약간의 중심 기능을 위한 기본 테스트를 생성하는데 이 스타일을 사용하는 것은 라이브 서비스의 유효성을 검증하기 위한 강력한 방식이다. 이렇게 하는 것은 동작하는 테스트가 고객 데이터에 직접 영향을 주지 않도록 설정 및 해체에 세심한 주의를 필요로 한다.

# API Test cases
REST framework는 [Django의 테스트 케이스 클래스](https://docs.djangoproject.com/en/stable/topics/testing/tools/#provided-test-case-classes)를 따라하지만 Django의 기본 `Client` 대신 `APIClient`를 사용하는 다음의 테스트 케이스 클래스를 포함한다.

- `APISimpleTestCase`
- `APITransactionTestCase`
- `APITestCase`
- `APILiveServerTestCase`

## Example
Django의 표준 테스트 케이스 클래스처럼 REST framework의 테스트 케이스 클래스를 사용할 수 있다. `self.client` 속성은 `APIClient` 인스턴스가 된다.

```python
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from myproject.apps.core.models import Account

class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('account-list')
        data = {'name': 'DabApps'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().name, 'DabApps')
```

# URLPatternsTestCase
REST framework는 클래스당 기반의 `urlpatterns`를 격리하기 위한 테스트 케이스 클래스 또한 제공한다. 이것이 Django의 `SimpleTestCase`를 상속하며 대개 다른 테스트 케이스 클래스와 혼합되어야 한다는 점에 유의한다.

## Example
```python
from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase


class AccountTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('api.urls')),
    ]

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('account-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
```

# Testing responses
## Checking the response data
테스트 응답의 유효성을 확인할 때 완전히 렌더링된 응답을 확인하는 대신 응답을 생성하는데 사용된 데이터를 확인하는 것이 더 편리하다.

예를 들어, `response.data`를 확인하는 것이 더 쉽다:

```python
response = self.client.get('/users/4/')
self.assertEqual(response.data, {'id': 4, 'username': 'lauren'})
```

`response.content`의 파싱된 결과를 확인하는 것보다:
```python
response = self.client.get('/users/4/')
self.assertEqual(json.loads(response.content), {'id': 4, 'username': 'lauren'})
```

## Rendering responses
직접 `APIRequestFactory`를 사용하여 뷰를 테스트한다면, 템플릿 응답 렌더링이 Django의 내부 요청-응답 사이클에 의해 수행되므로 반환될 응답이 아직 렌더링 되지 않는다. `response.content`에 접근하기 위해 먼저 응답을 렌더링할 필요가 있다.

```python
view = UserDetail.as_view()
request = factory.get('/users/4')
response = view(request, pk='4')
response.render()  # Cannot access `response.content` without this.
self.assertEqual(response.content, '{"username": "lauren", "id": 4}')
```

# Configuration
## Setting the default format
테스트 요청을 만드는데 사용되는 기본 포맷은 `TEST_REQUEST_DEFAULT_FORMAT` 설정 키를 사용해 설정할 수 있다. 예를 들어, 표준 multipart 폼 요청 대신 기본으로 항상 테스트 요청에서 JSON을 사용하게 하려면 `settings.py`에서 다음과 같이 설정한다:

```python
REST_FRAMEWORK = {
    ...
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}
```

## Setting the available formats
multipart나 json 요청이 아닌 요청을 테스트해야 한다면 `TEST_REQUEST_RENDERER_CLASSES` 설정을 설정하면 된다.

예를 들어 테스트 요청에서 `format='html'` 사용 지원을 추가하려면 `settings.py`에서 다음과 같이 설정한다:

```python
REST_FRAMEWORK = {
    ...
    'TEST_REQUEST_RENDERER_CLASSES': [
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer'
    ]
}
```