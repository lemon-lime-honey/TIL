# [Versioning](https://www.django-rest-framework.org/api-guide/versioning/)
```
인터페이스 버전 작성은 배포된 클라이언트를 제거하는 "예의 바른" 방식일 뿐이다.
- Roy Fielding
```

API 버전 작성은 서로 다른 클라이언트 사이의 동작을 변경할 수 있게 한다. REST framework는 여러 다른 버전 작성 스킴을 제공한다.

버전 작성은 들어오는 클라이언트 요청에 의해 결정되고, 요청 URL이나 요청 헤더에 기반한다.

버전 작성에 접근하는 여러 유효한 접근법이 있다. 특히 관리 범위를 벗어난 복수의 클라이언트를 가진 초장기 시스템을 설계하는 경우 [버전 작성을 하지 않는 시스템 또한 적절할 수 있다](https://www.infoq.com/articles/roy-fielding-on-versioning).

## Versioning with REST framework
API 버전 작성이 활성화되면, 들어오는 클라이언트 요청에서 요청된 버전에 대응되는 문자열이 `request.version` 속성에 포함된다.

기본적으로, 버전 작성은 비활성화되어 있으며, `request.versions`은 항상 `None`을 반환한다.

### Varying behavior based on the version
API 동작이 얼마나 달라지는가는 작성자의 의도에 따라 다르지만, 한 가지 예시로 새로운 버전에서 다른 serialization 형식으로 바꾸는 경우가 있다. 예를 들어:

```python
def get_serializer_class(self):
    if self.request.version == 'v1':
        return AccountSerializerVersion1
    return AccountSerializer
```

### Reversing URLs for versioned APIs
REST framework에 포함된 `reverse` 함수는 버전 작성 스킴과 관련 있다. 다음과 같이 현재 `reqeust`를 키워드 인자로 포함해야 한다:

```python
from rest_framework.reverse import reverse

reverse('bookings-list', request=request)
```

위의 함수는 현재 버전에 적합한 URL 변형을 적용할 것이다.

- `NamespaceVersioning`이 사용 중이었고, API 버전이 'v1'이었다면 사용되는 URL 조회는 `http://example.org/bookings/?version=1.0`과 같은 형식의 URL을 반환하는 `'v1:bookings-list'`가 된다.

### Versioned APIs and hyperlinked serializers
URL 기반 버전 작성 스킴과 함께 하이퍼링크된 serialization 형식을 사용할 때에는 요청을 시리얼라이저에 컨텍스트로 포함시켜야 한다.

```python
def get(self, request):
    queryset = Booking.objects.all()
    serializer = BookingsSerializer(queryset, many=True, context={'request': request})
    return Response({'all_bookings': serializer.data})
```

이렇게 하면 모든 반환된 URL에 적절한 버전이 포함된다.

## Configuring the versioning scheme
버전 작성 스킴은 `DEFAULT_VERSIONING_CLASS` 설정 키에 의해 정의된다.

```python
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning'
}
```

명시적으로 설정되지 않았다면 `DEFAULT_VERSIONING_CLASS`의 값은 `None`이다. 이 경우 `request.version` 속성은 언제나 `None`을 반환한다.

각 뷰에서 버전 작성 스킴을 설정할 수도 있다. 보통은 하나의 버전 작성 스킴이 전역적으로 사용되는 것이 더 합리적이기 때문에 그렇게 할 필요가 없다. 그렇게 해야 한다면, `versioning_class` 속성을 사용한다.

```python
class ProfileList(APIView):
    versioning_class = versioning.QueryParameterVersioning
```

### Other versioning settings
다음의 설정 키 또한 버전 작성에 사용된다.

- `DEFAULT_VERSION`<br>
  버전 정보가 없을 때 `request.version`에 사용되는 값. 기본값은 `None`
- `ALLOWED_VERSIONS`<br>
  설정된다면 이 값은 버전 작성 스킴에 의해 반환되는 버전의 집합을 제한하며 주어진 버전이 그 집합에 포함되어 있지 않다면 오류를 발생시킨다. `DEFAULT_VERSION` 설정에 사용되는 값은 (`None`이 아니라면) 언제나 `ALLOWED_VERSIONS` 집합의 일부로 간주된다는 점에 유의한다. 기본값은 `None`
- `VERSION_PARAM`<br>
  미디어 타입이나 URL 쿼리 파라미터와 같은 버전 작성 파라미터에 사용되는 문자열. 기본값은 `'version'`

버전 작성 스킴을 직접 정의하고 `default_version`, `allowed_versions`와 `version_param` 클래스 변수를 사용하여 versioning 클래스와 뷰당 또는 viewset당 기반의 위의 세 값을 직접 설정할 수 있다. 예를 들어, `URLPathVersioning`을 사용하고 싶다면:

```python
from rest_framework.versioning import URLPathVersioning
from rest_framework.views import APIView


class ExampleVersioning(URLPathVersioning):
    default_version = ...
    allowed_versions = ...
    version_param = ...


class ExampleView(APIView):
    versioning_class = ExampleVersioning
```

# API Reference
## AcceptHeaderVersioning
이 스킴은 클라이언트가 버전을 `Accept` 헤더의 미디어 타입의 일부로 명시하는 것을 요구한다. 버전은 주 미디어 타입을 보충하는 미디어 타입 파라미터로 포함된다.

다음은 accept 헤더 버전 작형 형식을 사용하는 HTTP 요청의 예시이다.

```
GET /bookings/ HTTP/1.1
Host: example.com
Accept: application/json; version=1.0
```

위의 요청 예시에서 `request.version` 속성은 문자열 `'1.0'`을 반환한다.

accept 헤더를 기반으로 한 버전 작성은 클라이언트 요구사항에 따라 다른 형식이 더 적합할지라도 [일반적](http://blog.steveklabnik.com/posts/2011-07-03-nobody-understands-rest-or-http#i_want_my_api_to_be_versioned)으로 [가장 좋은 방법](https://github.com/interagent/http-api-design/blob/master/en/foundations/require-versioning-in-the-accepts-header.md)으로 간주된다.

### Using accept headers with vender media types
엄밀히 말해 `json` 미디어 타입은 [추가 파라미터 포함](https://tools.ietf.org/html/rfc4627#section-6)으로 지정되지 않는다.잘 지정된 공용 API를 구축하는 경우 [vendor 미디어 타입](https://en.wikipedia.org/wiki/Internet_media_type#Vendor_tree)을 사용하는 것을 고려할 수 있다. 그렇게 하면 렌더러가 사용자 정의 미디어 타입을 가지는 JSON 기반 렌더러를 사용하도록 설정한다.

```python
class BookingsAPIRenderer(JSONRenderer):
    media_type = 'application/vnd.megacorp.bookings+json'
```

클라이언트 요청은 이제 다음과 같다:

```
GET /bookings/ HTTP/1.1
Host: example.com
Accept: application/vnd.megacorp.bookings+json; version=1.0
```

## URLPathVersioning
이 스킴은 클라이언트가 URL 경로의 일부로 버전을 명시할 것을 요구한다.

```
GET /v1/bookings/ HTTP/1.1
Host: example.com
Accept: application/json
```

URL 설정은 반드시 `'version'` 키워드 인자와 일치하는 버전 패턴을 포함해야 하므로, 이 정보는 버전 작성 스킴에 사용할 수 있다.

```python
urlpatterns = [
    re_path(
        r'^(?P<version>(v1|v2))/bookings/$',
        bookings_list,
        name='bookings-list'
    ),
    re_path(
        r'^(?P<version>(v1|v2))/bookings/(?P<pk>[0-9]+)/$',
        bookings_detail,
        name='bookings-detail'
    )
]
```

## NamespaceVersioning
클라이언트 입장에서 이 스킴은 `URLPathVersioning`과 같다. 유일한 차이는 URL 키워드 인자 대신 URL 네임스페이스를 사용하기 때문에 Django 애플리케이션에서 어떻게 설정되는가이다.

```
GET /v1/something/ HTTP/1.1
Host: example.com
Accept: application/json
```

이 스킴에서 `request.version` 속성은 들어오는 요청 경로와 일치하는 `namespace`에 기반해 결정된다.

다음은 서로 다른 네임스페이스 아래에서 두 개의 가능한 URL 접두사를 뷰 집합에 제공하는 예시이다.

```python
# bookings/urls.py
urlpatterns = [
    re_path(r'^$', bookings_list, name='bookings-list'),
    re_path(r'^(?P<pk>[0-9]+)/$', bookings_detail, name='bookings-detail')
]

# urls.py
urlpatterns = [
    re_path(r'^v1/bookings/', include('bookings.urls', namespace='v1')),
    re_path(r'^v2/bookings/', include('bookings.urls', namespace='v2'))
]
```

그저 단순한 버전 작성 스킴을 필요로 한다면 `URLPathVersioning`과 `NamespaceVersioning` 둘 다 합리적이다. `URLPathVersioning` 접근은 작은 애드혹 프로젝트에 더 적합하고, `NamespaceVersioning`은 더 큰 프로젝트를 관리하기에 쉽다.

## HostNameVersioning
호스트명 버전 작성 스킴은 클라이언트가 URL의 호스트명 일부로 요청된 버전을 명할 것을 요구한다.

예를 들어, 다음은 `http://v1.example.com/bookings/` URL에 대한 HTTP 요청이다:

```
GET /bookings/ HTTP/1.1
Host: v1.example.com
Accept: application/json
```

기본적으로 이 구현은 호스트명이 다음의 간단한 정규 표현식과 일치하는 것을 예상한다.

```
^([a-zA-Z0-9]+)\.[a-zA-Z0-9]+\.[a-zA-Z0-9]+$
```

첫 번째 그룹은 대괄호 안에 있어 호스트명과 일치하는 부분이라는 것을 가리킨다.

`HostNameVersioning` 스킴은 일반적으로 127.0.0.1과 같은 원시 IP 주소에 접근하기 때문에 디버그 모드에서 사용하기 불편할 수 있다. 이런 경우 유용한 [사용자 정의 서브도메인을 가지는 로컬호스트에 접근](https://reinteractive.net/posts/199-developing-and-testing-rails-applications-with-subdomains)하는 방법에 관한 다양한 온라인 튜토리얼이 있다.

버전에 기반한 호스트명은 서로 다른 API 버전에 서로 다른 DNS 레코드를 설정할 수 있으므로 들어오는 요청을 버전에 기반한 서로 다른 서버로 라우팅해야 하는 요구사항이 있을 경우 유용하다. 

## QueryParameterVersioning
이 스킴은 URL의 쿼리 파라미터로 버전을 포함하는 단순한 형식이다. 예를 들어:

```
GET /something/?version=0.1 HTTP/1.1
Host: example.com
Accept: application/json
```

# Custom versioning schemes
사용자 정의 버전 작성 스킴을 구현하려면 `BaseVersioning`의 서브클래스를 작성하고 `.determine_version` 메서드를 override한다.

## Example
다음의 예시는 요청된 버전을 결정하기 위해 사용자 정의 `X-API-Version` 헤더를 사용한다.

```python
class XAPIVersionScheme(versioning.BaseVersioning):
    def determine_version(self, request, *args, **kwargs):
        return request.META.get('HTTP_X_API_VERSION', None)
```

버전 작성 스킴이 요청 URL에 기반한다면 버전이 작성된 URL이 어떻게 결정되는지를 바꿀 수도 있다. 그렇게 하려면 클래스의 `.reverse()` 메서드를 override해야 한다. 소스코드를 참고한다.