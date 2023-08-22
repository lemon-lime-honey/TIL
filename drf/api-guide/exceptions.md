# [Exceptions](https://www.django-rest-framework.org/api-guide/exceptions/)
```
예외...는 오류 처리가 프로그램 구조의 중심 혹은 최상위 위치에서 깔끔하게 정리될 수 있도록 해준다.
- Doug Hellmann, Python Exception Handling Techniques
```

## Exception handling in REST framework views
REST framework의 뷰는 다양한 예외를 처리하고 적절한 오류 응답을 반환한다.

처리되는 예외는 다음과 같다:

- REST framework 안에서 발생된 `APIException`의 서브클래스
- Django의 `Http404` 예외
- Django의 `PermissionDenied` 예외

각각의 경우에서 REST framework는 적절한 상태 코드와 컨텐츠 타입을 가지는 응답을 반환한다. 응답의 바디는 오류의 성격에 따른 추가적인 세부 사항을 포함한다.

대부분의 오류 응답은 응답 바디에 키 `detail`를 포함한다.

예를 들어, 다음의 요청은:

```
DELETE http://api.example.com/foo/bar HTTP/1.1
Accept: application/json
```

그 리소스에서는 `DELETE` 메서드가 허용되지 않는다는 것을 알리는 오류 응답을 받을 수 있다:

```
HTTP 1.1 405 Method Not Allowed
Content-Type: application/json
Content-Length: 42

{"detail": "Method 'DELETE' not allowed."}
```

유효성 검사 오류는 조금 다르게 처리되며 응답에 키로 필드명이 포함된다. 유효성 검사 오류가 특정 필드에 특정된 것이 아니라면 "non_field_errors"를 사용하거나 `NON_FIELD_ERRORS_KEY` 설정에서 설정된 문자열 값을 사용한다.

유효성 검사 오류의 예시는 다음과 같다:

```
HTTP/1.1 400 Bad Request
Content-Type: application/json
Content-Length: 94

{"amount": ["A valid integer is required."], "description": ["This field may not be blank."]}
```

## Custom exception handling
API 뷰에서 발생된 예외를 응답 객체로 변환하는 핸들러 함수를 생성하여 사용자 정의 예외 처리를 구현할 수 있다. 이는 API에 의해 사용되는 오류 응답의 형식을 제어할 수 있게 한다.

해당 함수는 한 쌍의 인자를 가져야만 한다. 첫 번째는 처리될 예외, 두 번째는 현재 처리 중인 뷰와 같은 추가적인 컨텍스트를 포함하는 딕셔너리이다. 예외 처리 함수는 `Response` 객체를 반환하거나 예외가 처리될 수 없는 경우 `None`을 반환해야 한다. 핸들러가 `None`을 반환하면 예외가 재발생되며 Django가 표준 HTTP 500 'server error' 응답을 반환한다.

예를 들어, 다음과 같이 모든 오류 응답이 응답 바디에 HTTP 상태 코드를 포함하도록 한다면:

```
HTTP/1.1 405 Method Not Allowed
Content-Type: application/json
Content-Length: 62

{"status_code": 405, "detail": "Method 'DELETE' not allowed."}
```

응답의 형식을 변경하기 위해 다음의 사용자 정의 예외 핸들러를 작성할 수 있다:

```python
from rest_framework.views import exception_handler


def custom_exception_handler(exc, content):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response
```

컨텍스트 인자는 기본 핸들러가 사용하지는 않지만 예외 핸들러가 `context['view']`로 접근 가능한 현재 처리 중인 뷰와 같은 추가적인 정보를 필요로 할 때 유용할 수 있다.

예외 핸들러는 `EXCEPTION_HANDLER` 설정 키를 사용해 설정에서 설정되어야 한다. 예를 들어:

```python
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'my_project.my_app.utils.custom_exception_handler'
}
```

명시되지 않았다면 `'EXCEPTION_HANDLER'` 설정은 기본값으로 REST framework가 제공하는 기본 예외 핸들러를 가진다.

```python
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler'
}
```

예외 핸들러는 발생된 예외에 의해 생성된 응답을 위해서만 호출된다는 점에 유의한다. 시리얼라이저 유효성 검사에 실패했을 때 제네릭 뷰에 반환되는 `HTTP_400_BAD_REQUEST` 응답과 같은 뷰에 직접 반환되는 응답에는 사용되지 않는다.

# API Reference
## APIException
**Signature**: `APIException()`

`APIView` 클래스 또는 `@api_view` 안에서 발생하는 모든 예외를 위한 **기본 클래스**.

사용자 정의 예외를 제공하려면 `APIException`의 서브클래스를 작성하고 클래스에 `.status_code`, `.default_detail`, `default_code` 속성을 설정한다.

예를 들어, API가 간혹 연결할 수 없는 서드파티 서비스에 의존한다면 "503 Service Unavailable" HTTP 응답 코드를 위한 예외를 구현할 수 있다. 다음과 같이 하면 된다:

```python
from rest_framework.exceptions import APIException


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'
```

### Inspecting API exceptions
API 예외의 상태를 확인하기 위해 사용할 수 있는 여러 속성이 있다. 프로젝트의 사용자 정의 예외 처리를 구축하기 위해 이를 사용할 수 있다.

사용 가능한 속성과 메서드는 다음과 같다:

- `.detail` - 오류에 대한 텍스트 설명을 반환한다.
- `.get_codes()` - 오류의 코드 식별자를 반환한다.
- `.get_full_details()` - 텍스트 설명과 코드 식별자를 함께 반환한다.

대부분의 경우 오류 세부 사항은 단순한 항목이다:

```python
>>> print(exc.detail)
You do not have permission to perform this action.
>>> print(exc.get_codes())
permission_denied
>>> print(exc.get_full_details())
{'message': 'You do not have permission to perform this action.', 'code': 'permission_denied'}
```

유효성 검사 오류의 경우 오류 세부사항은 항목의 리스트 또는 딕셔너리이다:

```python
>>> print(exc.detail)
{"name":"This field is required.","age":"A valid integer is required."}
>>> print(exc.get_codes())
{"name":"required","age":"invalid"}
>>> print(exc.get_full_details())
{"name":{"message":"This field is required.","code":"required"},"age":{"message":"A valid integer is required.","code":"invalid"}}
```

## ParseError
**Signature**: `ParseError(detail=None, code=None)`

`request.data`에 접근할 때 요청이 정상적으로 구성되지 않은 데이터를 포함하면 발생한다.

기본적으로 이 예외는 HTTP 상태 코드 "400 Bad Request"를 가지는 응답을 결과로 가진다.

## AuthenticationFailed
**Signature**: `AuthenticationFailed(detail=None, code=None)`

들어오는 요청이 부정확한 인증을 포함할 때 발생한다.

기본적으로 이 예외는 HTTP 상태 코드 "401 Unauthenticated"를 가지는 응답을 결과로 가지지만, 사용하는 인증 스킴에 따라 "403 Forbidden" 응답이 되기도 한다. 자세한 사항은 [인증 문서](authentication.md)에서 확인할 수 있다.

## NotAuthenticated
**Signature**: `NotAuthenticated(detail=None, code=None)`

인증되지 않은 요청이 권한 확인에 실패했을 때 발생한다.

기본적으로 이 예외는 HTTP 상태 코드 "401 Unauthenticated"를 가지는 응답을 결과로 가지지만, 사용하는 인증 스킴에 따라 "403 Forbidden" 응답이 되기도 한다. 자세한 사항은 [인증 문서](authentication.md)에서 확인할 수 있다.

## PermissionDenied
**Signature**: `PermissionDenied(detail=None, code=None)`

인증되지 않은 요청이 권한 체크에 실패했을 때 발생한다.

기본적으로 이 예외는 HTTP 상태 코드 "403 Forbidden"을 가지는 응답을 결과로 가진다.

## NotFound
**Signature**: `NotFound(detail=None, code=None)`

주어진 URL에 리소스가 존재하지 않을 때 발생한다. 이 예외는 표준 `Http404` Django 예외와 동등하다.

기본적으로 이 예외는 HTTP 상태 코드 "404 Not Found"를 가지는 응답을 결과로 가진다.

## MethodNotAllowed
**Signature**: `MethodNotAllowed(method, detail=None, code=None)`

들어오는 요청이 뷰에 있는 핸들러 메서드에 매핑되지 않을 때 발생한다.

기본적으로 이 예외는 HTTP 상태 코드 "405 Method Not Allowed"를 가지는 응답을 결과로 가진다.

## NotAcceptable
**Signature**: `NotAcceptable(detail=None, code=None)`

들어오는 요청이 사용 가능한 렌더러가 충족할 수 없는 `Accept` 헤더를 가질 때 발생한다.

기본적으로 이 예외는 HTTP 상태 코드 "406 Not Acceptable"을 가지는 응답을 결과로 가진다.

## UnsupportedMediaType
**Signature**: `UnsupportedMediaType(media_type, detail=None, code=None)`

`request.data`에 접근할 때 요청 데이터의 컨텐츠 타입을 처리할 수 있는 parser가 없으면 발생한다.

기본적으로 이 예외는 HTTP 상태 코드 "415 Unsupported Media Type"을 가지는 응답을 결과로 가진다.

## Throttled
**Signature**: `Throttled(wait=None, detail=None, code=None)`

들어오는 요청이 스로틀링 체크에 실패했을 때 발생한다.

기본적으로 이 예외는 HTTP 상태 코드 "429 Too Many Requests"를 가지는 응답을 결과로 가진다.

## ValidationError
**Signature**: `ValidationError(detail=None, code=None)`

`ValidationError` 예외는 다른 `APIException` 클래스와는 약간 다르다.

- `detail` 인자는 옵션이 아니라 필수다.
- `detail` 인자는 오류 세부 사항 리스트 또는 딕셔너리이며 중첩된 자료 구조가 될 수 있다. 딕셔너리를 사용하면 시리얼라이저의 `validate()` 메서드에서 객체 수준 유효성 검사를 수행할 때 필드 수준 오류를 명시할 수 있다. 예: `raise serializers.ValidationError({'name': 'Please enter a valid name.'})`
- 관습적으로, Django의 빌트인 유효성 검사 오류와 차이를 두기 위해 `serializers` 모듈을 가져와 정규화된 `ValidationError` 형식을 사용한다. 예: `raise serializers.ValidationError('This field must be an integer value.')`

`ValidationError` 클래스는 validator 클래스에 의해 시리얼라이저와 필드 유효성 검사에 사용되어야 한다. `raise_exception` 키워드 인자를 가지는 `serializer.is_valid`를 호출할 때 발생할 수 있다:

```python
serializer.is_valid(raise_exception=True)
```

제네릭 뷰는 `raise_exception=True` 플래그를 사용하는데, 이는 API에서 전역적으로 유효성 검사 오류 응답의 형식을 override할 수 있다는 것을 의미한다. 그렇게 하려면 위에서 설명한 것처럼 사용자 정의 예외 핸들러를 사용한다.

기본적으로 이 예외는 HTTP 상태 코드 "400 Bad Request"를 가지는 응답을 결과로 가진다.

# Generic Error Views
Django REST Framework는 제네릭 JSON `500` Server Error와 `400` Bad Request 응답을 제공하는데 적합한 두 오류 뷰를 제공한다. (Django의 기본 오류 뷰는 HTML 응답을 제공하므로 API 전용 애플리케이션에는 적합하지 않다.)

[Django의 에러 뷰 커스터마이즈 문서](https://docs.djangoproject.com/en/dev/topics/http/views/#customizing-error-views)에 따라 사용한다.

### `rest_framework.exceptions.server_error`
상태 코드 `500`과 `application/json` 컨텐츠 타입을 가지는 응답을 반환한다.

`handler500`으로 설정한다:

```python
handler500 = 'rest_framework.exceptions.server_error'
```

### `rest_framework.exceptions.bad_request`
상태 코드 `400`과 `application/json` 컨텐츠 타입을 가지는 응답을 반환한다.

`handler400`으로 설정한다:

```python
handler400 = 'rest_framework.exceptions.bad_request'
```

# Third party packages
다음의 서드파티 패키지를 사용할 수도 있다.

## DRF Standardized Errors
[drf-standardized-errors](https://github.com/ghazi-git/drf-standardized-errors) 패키지는 모든 4xx와 5xx 응답을 위한 동일한 포맷을 생성하는 오류 핸들러를 제공한다. 이는 기본 오류 핸들러의 드롭인 대체이며, 오류 핸들러 전체를 재작성할 필요 없이 오류 응답 포맷을 커스터마이즈할 수 있게 한다. 표준화된 오류 응답 형식은 문서화하기 더 쉽고, API 소비자가 처리하기에도 더 쉽다.