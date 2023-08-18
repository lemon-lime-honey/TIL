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