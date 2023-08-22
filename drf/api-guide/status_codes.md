# [Status Codes](https://www.django-rest-framework.org/api-guide/status-codes/)
```
418 I'm a teapot - 찻주전자로 커피를 끓이려는 모든 시도는 오류 코드 "418 I'm a teapot"로 끝난다.
결과 엔터티 바디는 짧고 통통할 수 있다.
- RFC 2324, Hyper Textg Coffee Pot Control Protocol
```

응답에서 아무 것도 없이 그저 상태 코드를 사용하는 것은 권장하지 않는 일이다. REST framework는 코드를 더 명백하고 가독성 있게 만들어주는 명명된 상수 모음을 제공한다.

```python
from rest_framework import status
from rest_framework.response import Response


def empty_view(self):
    content = {'please move along': 'nothing to see here'}
    return Response(content, status=status.HTTP_404_NOT_FOUND)
```

아래에 `status` 모듈에 포함된 HTTP 상태 코드의 전체 모음이 있다.

이 모듈은 상태 코드가 주어진 범위 안에 있을 때 테스트하기 위한 헬퍼 함수 모음 또한 포함한다.

```python
from rest_framework import status
from rest_framework.test import APITestCase


class ExampleTestCase(APITestCase):
    def test_url_root(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertTrue(status.is_success(response.status_code))
```

HTTP 상태 코드의 적절한 사용법에 관해서는 [RFC2616](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html)과 [RFC 6585](https://tools.ietf.org/html/rfc6585)를 참조한다.

## Informational - 1xx
이 상태 코드 클래스는 일시적인 응답을 가리킨다. REST framework에서 기본으로 사용되는 1xx 상태 코드는 없다.

```
HTTP_100_CONTINUE
HTTP_101_SWITCHING_PROTOCOLS
```

## Successful - 2xx
이 상태 코드 클래스는 클라이언트의 요청이 성공적으로 수신되었고, 이해되었고, 받아들여짐을 가리킨다.

```
HTTP_200_OK
HTTP_201_CREATED
HTTP_202_ACCEPTED
HTTP_203_NON_AUTHORITATIVE_INFORMATION
HTTP_204_NO_CONTENT
HTTP_205_RESET_CONTENT
HTTP_206_PARTIAL_CONTENT
HTTP_207_MULTI_STATUS
HTTP_208_ALREADY_REPORTED
HTTP_226_IM_USED
```

## Redirection - 3xx
이 상태 코드 클래스는 요청을 만족시키기 위해 사용자 에이전트에 의한 추가 작업이 수행되어야 함을 가리킨다.

```
HTTP_300_MULTIPLE_CHOICES
HTTP_301_MOVED_PERMANENTLY
HTTP_302_FOUND
HTTP_303_SEE_OTHER
HTTP_304_NOT_MODIFIED
HTTP_305_USE_PROXY
HTTP_306_RESERVED
HTTP_307_TEMPORARY_REDIRECT
HTTP_308_PERMANENT_REDIRECT
```

## Clinet Error - 4xx
상태 코드 4xx 클래스는 클라이언트가 오류를 일으킨 것으로 보이는 경우를 위한 것이다. HEAD 요청에 응답하는 경우를 제외하면, 서버는 오류 상황 설명과 일시적이거나 영구적인 조건을 포함하는 엔터티를 포함해야 한다.

```
HTTP_400_BAD_REQUEST
HTTP_401_UNAUTHORIZED
HTTP_402_PAYMENT_REQUIRED
HTTP_403_FORBIDDEN
HTTP_404_NOT_FOUND
HTTP_405_METHOD_NOT_ALLOWED
HTTP_406_NOT_ACCEPTABLE
HTTP_407_PROXY_AUTHENTICATION_REQUIRED
HTTP_408_REQUEST_TIMEOUT
HTTP_409_CONFLICT
HTTP_410_GONE
HTTP_411_LENGTH_REQUIRED
HTTP_412_PRECONDITION_FAILED
HTTP_413_REQUEST_ENTITY_TOO_LARGE
HTTP_414_REQUEST_URI_TOO_LONG
HTTP_415_UNSUPPORTED_MEDIA_TYPE
HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE
HTTP_417_EXPECTATION_FAILED
HTTP_422_UNPROCESSABLE_ENTITY
HTTP_423_LOCKED
HTTP_424_FAILED_DEPENDENCY
HTTP_426_UPGRADE_REQUIRED
HTTP_428_PRECONDITION_REQUIRED
HTTP_429_TOO_MANY_REQUESTS
HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE
HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS
```

## Server Error - 5xx
"5"로 시작하는 상태 코드 응답은 서버가 서버에 오류가 일어났다는 것을 인지했거나 요청을 수행할 수 없는 경우를 가리킨다. HEAD 요청에 응답하는 경우를 제외하면, 서버는 오류 상황 설명과 일시적이거나 영구적인 조건을 포함하는 엔터티를 포함해야 한다.

```
HTTP_500_INTERNAL_SERVER_ERROR
HTTP_501_NOT_IMPLEMENTED
HTTP_502_BAD_GATEWAY
HTTP_503_SERVICE_UNAVAILABLE
HTTP_504_GATEWAY_TIMEOUT
HTTP_505_HTTP_VERSION_NOT_SUPPORTED
HTTP_506_VARIANT_ALSO_NEGOTIATES
HTTP_507_INSUFFICIENT_STORAGE
HTTP_508_LOOP_DETECTED
HTTP_509_BANDWIDTH_LIMIT_EXCEEDED
HTTP_510_NOT_EXTENDED
HTTP_511_NETWORK_AUTHENTICATION_REQUIRED
```

## Helper functions
다음의 헬퍼 함수는 응답 코드의 분류를 식별하기 위해 사용할 수 있다.

```python
is_informational()  # 1xx
is_success()        # 2xx
is_redirect()       # 3xx
is_client_error()   # 4xx
is_server_error()   # 5xx
```