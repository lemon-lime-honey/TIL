# [Settings](https://www.django-rest-framework.org/api-guide/settings/)
```
네임 스페이스는 멋진 발상 중 하나입니다. 좀 더 해봅시다!
- The Zen of Python
```

REST framework의 구성은 `REST_FRAMEWORK`라는 이름의 하나의 Django 설정 안의 네임 스페이스로 되어있다.

예를 들어, 프로젝트의 `settings.py` 파일은 다음과 같은 것을 포함할 수 있다:

```python
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ]
}
```

## Accessing settings
프로젝트의 REST framework API 설정 값에 접근해야 한다면 `api_settings` 객체를 사용해야 한다. 예를 들어:

```python
from rest_framework.settings import api_settings

print(api_settings.DEFAULT_AUTHENTICATION_CLASSES)
```

`api_settings` 객체는 모든 사용자 정의 설정을 체크하고, 그렇지 않다면 기본 값으로 되돌린다. 클래스를 참조하기 위해 경로를 가져오는 문자열을 사용하는 모든 설정은 문자열 그대로를 반환하는 대신 참조되는 클래스를 자동으로 가져오고 반환한다.

# API Reference
## API policy settings
다음의 설정은 기본 API 정책을 제어하며, 모든 `APIView` 클래스 기반 뷰나 `@api_view` 함수 기반 뷰에 적용된다.

### DEFAULT_RENDERER_CLASSES
`Response` 객체를 반환할 때 사용될 수 있는 렌더러의 기본 집합을 결정하는 렌더러 클래스의 리스트 또는 튜플

#### 기본
```python
[
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
]
```

### DEFAULT_PARSER_CLASSES
`request.data` 속성에 접근할 때 사용되는 parser의 기본 집합을 결정하는 parser 클래스의 리스트 또는 튜플

#### 기본
```python
[
    'rest_framework.parsers.JSONParser',
    'rest_framework.parsers.FormParser',
    'rest_framework.parsers.MultiPartParser',
]
```

### DEFAULT_AUTHENTICATION_CLASSES
`request.user` 또는 `request.auth` 속성에 접근할 때 사용되는 인증자의 기본 집합을 결정하는 인증 클래스의 리스트 또는 튜플

#### 기본
```python
[
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.BasicAuthentication',
]
```

### DEFAULT_PERMISSION_CLASSES
뷰가 시작될 때 체크되는 권한의 기본 집합을 결정하는 권한 클래스의 리스트 또는 튜플. 권한은 리스트 안의 모든 클래스에 의해 승인되어야 한다.

#### 기본
```python
[
    'rest_framework.permissions.AllowAny',
]
```

### DEFAULT_THROTTLE_CLASSES
뷰가 시작될 때 체크되는 스로틀의 기본 집합을 결정하는 스로틀 클래스의 리스트 또는 튜플

#### 기본
`[]`

### DEFAULT_CONTENT_NEGOTIATION_CLASSES
들어오는 요청이 주어졌을 때 응답을 위해 렌더러가 어떻게 선택되어야 할지 결정하는 컨텐츠 협상 클래스

#### 기본
```
'rest_framework.negotiation.DefaultContentNegotiation'
```

### DEFAULT_SCHEMA_CLASSES
스키마 생성에 사용되는 뷰 검사기 클래스

#### 기본
```
'rest_framework.schemas.openapi.AutoSchema'
```

## Generic view settings
다음 설정은 제네릭 클래스 기반 뷰의 동작을 제어한다.

### DEFAULT_FILTER_BACKENDS
제네릭 필터링에 사용되는 필터 백엔드 클래스의 리스트. `None`으로 설정된다면 제네릭 필터링이 비활성화된다.

### DEFAULT_PAGINATION_CLASS
Queryset 페이지 매김에 사용되는 기본 클래스. `None`으로 설정되면 기본으로 페이지 매김이 비활성화된다. 페이지 매김 형식의 [설정](./pagination.md/#setting-the-pagination-style)과 [수정](./pagination.md/#modifying-the-pagination-style)에 관한 자세한 사항은 [페이지 매김 문서](./pagination.md)에서 확인한다.

기본: `None`

### PAGE_SIZE
페이지 매김에 사용되는 기본 페이지 크기. `None`으로 설정되면 페이지 매김은 기본으로 비활성화된다.

기본: `None`

### SEARCH_PARAM
`SearchFilter`가 사용하는 검색 조건을 명시하기 위해 사용되는 쿼리 파라미터의 이름

기본: `search`

### ORDERING_PARAM
`OrderingFilter`가 반환하는 결과의 정렬 조건을 명시하기 위해 사용되는 쿼리 파라미터의 이름

기본: `ordering`

## Versioning settings
### DEFAULT_VERSION
버전 정보가 존재하지 않을 때 `request.version`이 사용하는 값

기본: `None`

### ALLOWED_VERSIONS
설정된다면, 이 값은 버전 작성 스킴에 의해 반환되는 버전 모음을 제한하고 주어진 버전이 그 집합에 없다면 오류를 발생시킨다.

기본: `None`

### VERSION_PARAM
미디어 타입이나 URL 쿼리 파라미터에서와 같이 버전 파라미터에 사용되는 문자열

기본: `'version'`

## Authentication settings
다음 설정은 인증되지 않은 요청의 동작을 제어한다.

### UNAUTHENTICATED_USER
인증되지 않은 요청을 위한 `request.user`를 초기화하는데 사용되는 클래스. (`INSTALLED_APPS`에서 `django.contrib.auth`를 제거하는 것과 같이 인증을 완전히 제거하려면 `UNAUTHENTICATED_USER`를 `None`으로 설정한다.)

기본: `django.contrib.auth.models.AnonymousUser`

### UNAUTHENTICATED_TOKEN
인증되지 않은 요청을 위해 `request.auth`를 초기화하는데 사용되는 클래스.

기본: `None`

## Test settings
다음 설정은 APIRequestFactory와 APIClient의 동작을 제어한다.

### TEST_REQUEST_DEFAULT_FORMAT
테스트 요청을 작성할 때 사용되는 기본 포맷

`TEST_REQUEST_RENDERER_CLASSES` 설정에 있는 렌더러 클래스 중 하나의 포맷과 일치해야 한다.

기본: `'multipart'`

### TEST_REQUEST_RENDERER_CLASSES
테스트 요청을 구축할 때 지원되는 렌더러 클래스

이 렌더러 클래스의 형식은 테스트 요청을 생성할 때 사용될 수 있다. 예를 들어: `client.post('/users', {'username': 'jamie'}, format='json')`

기본:

```python
[
    'rest_framework.renderers.MultiPartRenderer',
    'rest_framework.renderers.JSONRenderer'
]
```

## Schema generation controls
### SCHEMA_COERCE_PATH_PK
설정된다면, 스키마 경로 파라미터를 생성할 때 URL 설정의 `'pk'` 식별자를 실제 필드 이름으로 매핑한다. 보통은 `'id'`이다. "식별자"는 더 일반적인 개념인 반면 "기본 키"가 구현 세부 사항이므로 더 적합한 표현을 제공하게 된다.

기본: `True`

### SCHEMA_COERCE_METHOD_NAMES
설정된다면, 내부 viewset 메서드 이름을 스키마 생성에서 사용되는 외부 동작 이름으로 매핑한다. 이는 코드베이스에서 내부적으로 사용하는 것보다 외부 표현에 더 적합한 이름을 생성하게 해준다.

기본: `{'retrieve': 'read', 'destroy': 'delete'}`

## Content type controls
### URL_FORMAT_OVERRIDE
요청 URL의 `format=...` 쿼리 파라미터를 사용하여 기본 컨텐츠 협상 `Accept` 헤더의 동작을 override하는데 사용되는 URL 파라미터의 이름

예: `http://example.com/organizations/?format=csv`

이 설정의 값이 `None`이라면 URL 포맷 override가 비활성화된다.

기본: `'format'`

### FORMAT_SUFFIX_KWARG
포맷 접미사를 제공하는데 사용되는 URL 설정의 파라미터 이름. 이 설정은 접미사가 붙은 URL 패턴을 포함시키기 위해 `format_suffix_patterns`를 사용할 때 적용된다

예: `http://example.com/organizations.csv`

기본: `'format`

## Date and time formatting
다음의 설정은 날짜와 시간 표현이 어떻게 파싱되고 렌더링되어야 하는지를 제어하는데 사용된다.

### DATETIME_FORMAT
`DateTimeField` 시리얼라이저 필드의 출력을 렌더링할 때 기본으로 사용되는 포맷 문자열. `None`이라면 `DateTimeField` 시리얼라이저 필드는 파이썬 `datetime` 객체를 반환하며, 렌더러에 의해 datetime 인코딩이 결정된다.

`None`, `'iso-8601'` 또는 파이썬 [strftime 포맷](https://docs.python.org/3/library/time.html#time.strftime) 문자열이어야 한다.

기본: `'iso-8601'`

### DATETIME_INPUT_FORMATS
입력을 `DateTimeField` 시리얼라이저 필드로 파싱할 때 기본으로 사용되는 포맷 문자열의 리스트.

문자열 `'iso-8601'`을 포함하는 리스트 또는 파이썬 [strftime 포맷](https://docs.python.org/3/library/time.html#time.strftime) 문자열이어야 한다.

기본: `['iso-8601']`

### DATE_FORMAT
`DateField` 시리얼라이저 필드의 출력을 렌더링할 때 기본으로 사용되는 포맷 문자열. `None`이면 `DateField` 시리얼라이저 필드는 파이썬 `date` 객체를 반환하며, 렌더러에 의해 날짜 인코딩이 결정된다.

`None`, `'iso-8601'` 또는 파이썬 [strftime 포맷](https://docs.python.org/3/library/time.html#time.strftime) 문자열이어야 한다.

기본: `'iso-8601'`

### DATE_INPUT_FORMATS
입력을 `DateField` 시리얼라이저 필드로 파싱할 때 기본으로 사용되는 포맷 문자열의 리스트.

문자열 `'iso-8601'`을 포함하는 리스트 또는 파이썬 [strftime 포맷](https://docs.python.org/3/library/time.html#time.strftime) 문자열이어야 한다.

기본: `['iso-8601']`

### TIME_FORMAT
`TimeField` 시리얼라이저 필드의 출력을 렌더링할 때 기본으로 사용되는 포맷 문자열. `None`이면 `TimeField` 시리얼라이저 필드는 파이썬 `time` 객체를 반환하며, 렌더러에 의해 시간 인코딩이 결정된다.

`None`, `'iso-8601'` 또는 파이썬 [strftime 포맷](https://docs.python.org/3/library/time.html#time.strftime) 문자열이어야 한다.

기본: `'iso-8601'`

### TIME_INPUT_FORMATS
입력을 `TimeField` 시리얼라이저 필드로 파싱할 때 기본으로 사용되는 포맷 문자열의 리스트.

문자열 `'iso-8601'`을 포함하는 리스트 또는 파이썬 [strftime 포맷](https://docs.python.org/3/library/time.html#time.strftime) 문자열이어야 한다.

기본: `['iso-8601']`

## Encodings
### UNICODE_JSON
`True`로 설정되면 JSON 응답이 응답에 유니코드 문자를 허용한다. 예를 들어:

```python
{"unicode black star":"★"}
```

`False`로 설정되면 JSON 응답은 아스키가 아닌 문자를 다음과 같이 이스케이프 문자로 표기한다:

```python
{"unicode black star":"\u2605"}
```

두 형식 모두 [RFC 4627](https://www.ietf.org/rfc/rfc4627.txt)을 따르며, 구문적으로 유효한 JSON이다. 유니코드 형식은 API 응답을 조회할 때 더 사용자 친화적이므로 선호된다.

기본: `True`

### COMPACT_JSON
`True`로 설정되면 JSON 응답이 `':'`와 `','` 문자 다음에 공백이 없는 압축된 표현을 반환한다. 예를 들어:

```python
{"is_admin":false,"email":"jane@example"}
```

`False`로 설정되면 JSON 응답은 다음과 같이 약간 더 긴 표현을 반환한다:

```python
{"is_admin": false, "email": "jane@example"}
```

기본 형식은 [Heroku의 API 디자인 가이드라인](https://github.com/interagent/http-api-design#keep-json-minified-in-all-responses)에 따라 최소화된 응답을 반환하는 것이다.

기본: `True`

### STRICT_JSON
`True`로 설정되었을 때, JSON 렌더링과 파싱은 오직 구문적으로 유효한 JSON만을 확인하며 파이썬의 `json` 모듈에 의해 허용되는 확장된 부동소수점 값(`nan`, `inf`, `-inf`)에 대해서는 예외를 발생시킨다. 이러한 값은 보통은 지원되지 않으므로 권장되는 설정이다. 예를 들어, 자바스크립트의 `JSON.Parse`나 PostgreSQL의 JSON 데이터 파입은 이러한 값을 허용하지 않는다.

`False`로 설정되었을 때 JSON 렌더링과 파싱이 허용된다. 그러나 이런 값들은 여전히 유효하지 않은 값이며, 코드에서 특별히 다루어질 필요가 있다.

기본: `True`

### COERCE_DECIMAL_TO_STRING
네이티브 decimal 타입을 지원하지 않는 API 표현에서 decimal 객체를 반환할 때, 보통은 값을 문자열로 반환하는 것이 최선이다. 그렇게 하면 이진 부동소수점 구현에서 발생하는 정밀성 손실을 피할 수 있다.

`True`로 설정되면, 시리얼라이저 `DecimalField` 클래스는 `Decimal` 객체 대신 문자열을 반환한다. `False`로 설정되면, 시리얼라이저는 기본 JSON 인코더가 float로 반환하는 `Decimal` 객체를 반환한다.

기본: `True`

## View names and descriptions
**다음의 설정은 `OPTIONS` 요청에 대한 응답과 브라우징 가능한 API에서 사용되는 뷰 이름과 설명을 생성하기 위해 사용된다.**

### VIEW_NAME_FUNCTION
뷰 이름을 생성할 때 사용되는 함수를 나타내는 문자열

다음의 시그니처를 가지는 함수여야 한다:

```python
view_name(self)
```

- `self`: 뷰 인스턴스. 보통 name 함수는 설명적 이름을 생성할 때 `self.__class__.__name__`이 접근하는 클래스의 이름을 조회한다.

뷰 인스턴스가 `ViewSet`을 상속한다면 여러 선택 인자를 가지고 초기화될 수 있다:

- `name`: Viewset 안의 뷰에 명시적으로 제공되는 이름. 보통 이 값은 제공된 그대로 사용되어야 한다.
- `suffix`: Viewset 안 각각의 뷰를 구분할 때 사용되는 텍스트. 이 인자는 `name`과 상호 배타적이다.
- `detail`: Viewset 안 각각의 뷰를 'list' 또는 'detail'로 구분하는 불리언.

기본: `'rest_framework.views.get_view_name'`

### VIEW_DESCRIPTION_FUNCTION
뷰 설명을 생성할 때 사용되는 함수를 나타내는 문자열.

이 설정은 기본 마크다운이 아닌 마크업 형식을 지원하기 위해 변경될 수 있다. 예를 들어, 브라우징 가능한 API에서 출력되는 뷰 문서 문자열에 `rst` 마크입을 지원하기 위해 사용할 수 있다.

다음 시그니처를 가지는 함수여야 한다:

```python
view_description(self, html=False)
```

- `self`: 뷰 인스턴스. 보통 description 함수는 설명을 생성할 때 `self.__class__.__doc__`이 접근하는 클래스의 문서 문자열을 조회한다.
- `html`: HTML 출력을 필요로하는지 지시하는 불리언. 브라우징 가능한 API에서 사용될 때에는 `True`, `OPTIONS` 응답을 생성할 때에는 `False`.

뷰 인스턴스가 `ViewSet`을 상속한다면 여러 선택 인자를 가지고 초기화될 수 있다:

- `description`: Viewset 안 뷰에 명시적으로 제공되는 설명. 보통 추가적인 viewset `action` 집합이며, 제공된 대로 사용되어야 한다.

기본: `'rest_framework.views.get_view_description'`

## HTML Select Field cutoffs
브라우징 가능한 API에서 [관계 필드를 렌더링할 때 필드 컷오프를 선택](serializer_relations.md/#select-field-cutoffs)하기 위한 전역 설정.

### HTML_SELECT_CUTOFF
`html_cutoff` 값의 전역 설정. 정수여야 한다.

기본: `1000`

### HTML_SELECT_CUTOFF_TEXT
`html_cutoff_text`의 전역 설정을 나타내는 문자열.

기본: `"More than {count} items..."`

## Miscellaneous settings
### EXCEPTION_HANDLER
주어진 예외에 대한 응답을 반환할 때 사용되어야 하는 함수를 표현하는 문자열. 함수가 `None`을 반환하면 500 오류가 발생한다.

이 설정은 기본 `{"detail": "Failure..."}` 응답 이외의 오류 응답을 지원하기 위해 변경될 수 있다. 예를 들어, `{"errors": [{"message": "Failure...", "code": ""} ...]}`와 같은 API 응답을 제공하기 위해 사용할 수 있다.

다음 시그니처를 가지는 함수여야 한다:

```
exception_handler(exc, context)
```

- `exc`: 예외

기본: `'rest_framework.views.exception_handler'`

### NON_FIELD_ERRORS_KEY
특정 필드를 참조하지 않지만 일반적인 오류인 시리얼라이저 오류에 사용되는 키를 표현하는 문자열.

기본: `'non_field_errors'`

### URL_FIELD_NAME
`HyperlinkedModelSerializer`가 생성하는 URL 필드에 사용되는 키를 표현하는 문자열.

기본: `'url'`

### NUM_PROXIES
API가 실행되는 애플리케이션 프록시의 수를 명시하는데 사용되는 0 이상의 정수. 스로틀링이 클라이언트 IP 주소를 더 정확하게 식별하게 한다. `None`으로 설정되면 스로틀 클래스가 덜 엄격한 IP 일치가 사용된다.

기본: `None`