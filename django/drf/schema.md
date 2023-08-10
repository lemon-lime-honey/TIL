# [Schema](https://www.django-rest-framework.org/api-guide/schemas/)
```
기계가 읽을 수 있는 [스키마]는 API를 통해 어떤 리소스가 사용 가능한지, 리소스의 URL은 무엇이고, 리소스가 어떻게 표현되며 지원하는 연산은 무엇인지 나타낸다.
- Heroku, JSON Schema for the Heroku Platform API
```

API 스키마는 레퍼런스 문서 생성이나 API와 상호작용할 수 있는 동적 클라이언트 라이브러리를 구동하는 등 다양한 사용 사례를 위한 유용한 도구이다.

Django REST Framework는 [OpenAPI](https://github.com/OAI/OpenAPI-Specification) 스키마 자동 생성 지원을 제공한다.

## Overview
스키마 생성은 여러 움직이는 부분을 가진다. 다음을 살펴보면 좋다:

- `SchemaGenerator`는 설정된 URL 패턴을 확인하고, `APIView` 서브클래스를 찾고 그 스키마 표현을 조회하고, 최종 스키마 객체를 컴파일하는 최상위 클래스이다.
- `AutoSchema`는 뷰당 스키마 조회에 필요한 모든 세부사항을 캡슐화한다. `schema` 속성을 통해 각 뷰에 첨부된다. 스키마를 커스터마이즈하기 위해 `AutoSchema`의 서브클래스를 작성한다.
- `generateschema` 관리 명령은 오프라인으로 정적 스키마를 생성할 수 있게 한다.
- 스키마를 동적으로 생성하고 제공하기 위해 `SchemaView`를 라우팅할 수 있다.
- `settings.DEFAULT_SCHEMA_CLASS`를 사용하여 프로젝트 기본값으로 사용할 `AutoSchema` 서브클래스를 지정할 수 있다.

다음 섹션에서는 자세한 사항을 설명한다.

## Generating an OpenAPI Schema
### Install dependencies
```
pip install pyyaml uritemplate
```

- `pyyaml`은 YAML 기반 OpenAPI 형식으로 스키마를 생성하기 위해 사용된다.
- `uritemplate`는 경로 파라미터를 얻기 위해 내부적으로 사용된다.

### Generating a static schema with the `generateschema` management command
스키마가 정적이라면 `generateschema` 관리 명령을 사용할 수 있다:

```
./manage.py generateschema --file openapi-schema.yml
```

일단 이 방법으로 스키마를 생성했다면 스키마 생성기에서 자동으로 추론될 수 없는 추가 정보로 스키마에 주석을 달 수 있다.

API 스키마를 버전 관리로 확인하고 새로운 릴리스마다 갱신하거나 사이트의 정적 미디어로부터 API 스키마를 제공할 수 있다.

### Generating a dynamic schema with `SchemaView`
외래키 선택이 데이터베이스 값에 의존하는 등의 이유로 동적 스키마를 필요로 한다면 필요로 하는 스키마를 생성하고 제공하는 `SchemaView`를 라우팅할 수 있다.

`SchemaView`를 라우팅하려면 `get_schema_view()` 헬퍼를 사용한다.

`urls.py`:

```python
from rest_framework.schemas import get_schema_view

urlpatterns = [
    #...
    # Use the `get_schema_view()` helper to add a `SchemaView` to project URLs.
    #   * `title` and `description` parameters are passed to `SchemaGenerator`.
    #   * Provide view name for use with `reverse()`.
    path('openapi', get_schema_view(
        title="Your Project",
        description="API for all things ...",
        version="1.0.0"
    ), name='openapi-schema'),
    # ...
]
```

#### `get_schema_view()`
`get_schema_view()` 헬퍼는 다음의 키워드 인자를 가진다.

- `title`<br>
  스키마 정의의 서술적인 제목을 제공하기 위해 사용될 수 있다.
- `description`<br>
  더 긴 설명 텍스트.
- `version`<br>
  API의 버전.
- `url`<br>
  스키마를 위한 표준 기본 URL을 전달하기 위해 사용될 수 있다.
  ```python
  schema_view = get_schema_view(
      title='Server Monitoring API',
      url='https://www.example.org/api/'
  )
  ```
- `urlconf`<br>
  API 스키마를 생성할 URL 설정에 대한 가져오기 경로를 표현하는 문자열. 기본값은 Django의 `ROOT_URLCONF` 설정의 값이다.
  ```python
  schema_view = get_schema_view(
      title='Server Monitoring API',
      url='https://www.example.org/api/',
      urlconf='myproject.urls'
  )
  ```
- `patterns`<br>
  스키마 확인을 제한하기 위한 url 패턴 리스트. 스키마에서 `myproject.api` url만이 노출되기를 바란다면:
  ```python
  schema_url_patterns = [
      path('api/', include('myproject.api.urls')),
  ]

  schema_view = get_schema_view(
      title='Server Monitoring API',
      url='https://www.example.org/api/',
      patterns=schema_url_patterns,
  )
  ```
- `generator_class`<br>
  `SchemaView`로 전달되기 위한 `SchemaGenerator` 서브클래스를 명시하는데 사용될 수 있다.
- `authentication_classes`<br>
  스키마 엔드포인트에 적용되는 인증 클래스 리스트를 명시하기 위해 사용될 수 있다. 기본값은 `settings.DEFAULT_AUTHENTICATION_CLASSES`
- `permission_classes`<br>
  스키마 엔드포인트에 적용되는 권한 클래스 리스트를 명시하기 위해 사용될 수 있다. 기본값은 `settings.DEFAULT_PERMISSION_CLASSES`
- `renderer_classes`<br>
  API 루트 엔드포인트를 렌더링하기 위해 사용되는 렌더러 클래스 집합을 전달하기 위해 사용될 수 있다.