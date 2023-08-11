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

## SchemaGenerator
#### Schema-level customization
```python
from rest_framework.schemas.openapi import SchemaGenerator
```

`SchemaGenerator`는 라우팅된 URL 패턴 리스트를 확인하고 각 뷰를 위한 스키마를 요청하며 결과 OpenAPI 스키마를 대조하는 클래스이다.

보통은 직접 `SchemaGenerator`를 인스턴스화할 필요가 없지만 필요한 경우 이렇게 하면 된다:

```python
generator = SchemaGenerator(title='Stock Prices API')
```

##### 인자:
- `title`<br>
  **필수**: API의 이름
- `description`<br>
  더 긴 설명 텍스트
- `version`<br>
  API의 버전. 기본값 `0.1.0`
- `url`<br>
  API 스키마의 루트 URL. 스키마가 경로 접두사 아래에 포함된 것이 아니라면 이 선택인자는 필요하지 않다.
- `patterns`<br>
  스키마를 생성할 때 조회해야 할 URL 리스트. 기본값은 프로젝트의 URL 설정
- `urlconf`<br>
  스키마를 생성할 때 사용할 URL 설정 모듈명. 기본값은 `settings.ROOT_URLCONF`

최상위 스키마를 커스터마이즈하려면 `rest_framework.schemas.openapi.SchemaGenerator`의 서브클래스를 작성하고 서브클래스를 `generateschema` 명령이나 `get_schema_view()` 헬퍼 함수의 인자로 제공한다.

### get_schema(self, request=None, public=False)
OpenAPI 스키마를 표현하는 딕셔너리를 반환한다:

```python
generator = SchemaGenerator(title='Stock Prices API')
schema = generator.get_schema()
```

`request` 인자는 옵션이며 스키마 생성 결과에 사용자당 권한을 부여할 때 사용할 수 있다.

생성된 딕셔너리를 커스터마이즈할 때 override하는 것이 좋다. 다음은 [최상위 `info` 객체](https://swagger.io/specification/#infoObject)에 서비스 약관을 추가하는 예시이다:

```python
class TOSSchemaGenerator(SchemaGenerator):
    def get_schema(self, *args, **kwargs):
        schema = super().get_schema(*args, **kwargs)
        schema["info"]["termsOfService"] = "https://example.com/tos.html"
        return schema
```

## AutoSchema
#### Per-View Customization
```python
from rest_framework.schemas.openapi import AutoSchema
```

기본적으로 뷰 조회는 `APIView`의 `schema` 속성을 통해 접근할 수 있는 `AutoSchema` 인스턴스에 의해 수행된다.

```python
auto_schema = some_view.schema
```

`AutoSchema`는 각 뷰, 요청 메서드와 경로에 필요한 OpenAPI 요소를 제공한다:

- [OpenAPI 구성요소](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#componentsObject) 리스트. DRF에서는 요청과 응답 바디를 표현하는 시리얼라이저의 매핑이다.
- 엔드포인트를 설명하는 경로, 페이지 매김과 필터링을 위한 쿼리 파라미터 등을 포함한 적절한 [OpenAPI 작업 객체](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#operationObject)

```python
components = auto_schema.get_components(...)
operation = auto_schema.get_operation(...)
```

스키마 컴파일 과정에서 `SchemaGenerator`는 각 뷰, 허용된 메서드, 경로마다 `get_components()`와 `get_operation()`을 호출한다.

**Note**: 컴포넌트와 많은 작업 파라미터의 자동 조회는 `get_serializer()`, `pagination_class`, `filter_backends`등과 같은 `GenericAPIView`의 연관있는 속성과 메서드에 의존한다. 이런 이유로 기본 `APIView` 서브클래스에 대한 기본 조회는 URL 키워드 인자 경로 파라미터로 제한된다.

`AutoSchema`는 스키마 생성에 필요한 뷰 조회를 캡슐화한다. 이 때문에 모든 스키마 생성 논리는 이미 광범위한 뷰, 시리얼라이저, 필드 API에 분산되지 않고 한 곳에 보관된다.

이 패턴을 유지하려면 스키마 생성을 커스터마이즈할 때 스키마 논리가 뷰, 시리얼라이저, 필드에 유출되지 않도록 해야 한다. 다음과 같은 것을 하고 싶을 수 있다:

```python
class CustomSchema(AutoSchema):
    """
    AutoSchema subclass using schema_extra_info on the view.
    """
    ...


class CustomView(APIView):
    schema = CustomSchema()
    schema_extra_info = ... some extra info ...
```

여기, 뷰에서 `schema_extra_info`를 찾는 `AutoSchema`의 서브클래스가 있다. 이렇게 해도 *괜찮지만* 이는 스키마 논리가 여러 다른 지점에 퍼지는 결과를 낳는다.

`extra_info`가 뷰 밖으로 유출되지 않는 `AutoSchema` 서브클래스를 작성한다:

```python
class BaseSchema(AutoSchema):
    """
    AutoSchema subclass that knows how to use extra_info.
    """
    ...

class CustomSchema(BaseSchema):
    extra_info = ... some extra info ...

class CustomView(APIView):
    schema = CustomSchema()
```

이 형식은 아주 약간 더 장황하기는 하지만 스키마 연관 코드의 캡슐화를 유지한다. *형식* 면에서 더 *응집성*이 있다. 나머지 API 코드를 더 깔끔하게 유지한다.

각 뷰에 대한 특정 서브클래스를 생성하는 대신 많은 뷰 클래스에 옵션을 적용한다면 직접 작성한 기본 `AutoSchema` 서브클래스에서 그 옵션을 `__init__()`의 키워드 인자로 명시한다:

```python
class CustomSchema(BaseSchema):
    def __init__(self, **kwargs):
        # store extra_info for later
        self.extra_info = kwargs.pop("extra_info")
        super().__init__(**kwargs)

class CustomView(APIView):
    schema = CustomSchema(
        extra_info=... some extra info ...
    )
```

이는 일반적으로 사용되는 옵션을 위한 사용자 정의 서브클래스를 생성하지 않아도 되게 한다.

모든 `AutoSchema` 메서드가 연관된 `__init__()` 키워드 인자를 노출하는 것은 아니지만 일반적으로 필요한 옵션에 관한 메서드는 노출된다.

### `AutoSchema` methods
#### `get_components()`
요청과 응답 바디를 표현하는 OpenAPI 구성요소를 생성해 시리얼라이저에서 그 속성을 유도한다.

구성요소 이름을 생성된 표현으로 매핑한 딕셔너리를 반환한다. 기본적으로 하나의 쌍을 가지지만 뷰가 복수의 시리얼라이저를 사용한다면 `get_componenets()`를 override하여 복수의 쌍을 반환하게 할 수 있다.

#### `get_component_name()`
시리얼라이저에서 구성요소의 이름을 산출한다.

API가 중복되는 구성요소 이름을 가진다면 경고를 보게 된다. 그렇게 된다면 `get_component_name()`을 override하거나 다른 이름을 제공하기 위해 (아래에서 언급되는) `component_name` `__init__()` 키워드 인자를 전달한다.

#### `get_reference()`
시리얼라이저 구성요소의 레퍼런스를 반환한다. `get_schema()`를 override할 때 유용하다.

#### `map_serializer()`
OpenAPI 표현에 시리얼라이저를 매핑한다.

대부분의 시리얼라이저는 표준 OpenAPI `object` 타입에 따라야 하지만 `map_serializer()`나 다른 시리얼라이저 수준 필드를 커스터마이즈하기 위해 `map_serializer()`를 override할 수 있다.

#### `map_field()`
스키마 표현에 각각의 시리얼라이저 필드를 매핑한다. 기본 구현은 Django REST Framework가 제공하는 기본 필드를 다룬다.

스키마를 알 수 없는 `SerializerMethodField` 인스턴스 또는 사용자 정의 필드 서브클래스의 경우 올바른 스키마를 생성하기 위하여 `map_field()`를 override해야 한다.

```python
class CustomSchema(AutoSchema):
    """Extension of ``AutoSchema`` to add support for custom field schemas."""

    def map_field(self, field):
        # Handle SerializerMethodFields or custom fields here...
        # ...
        return super().map_field(field)
```

서드파티 패키지 제작자는 사용자들이 사용자 정의 필드를 위한 스키마를 쉽게 생성하기 위해 `map_field()`를 override하는 `AutoSchema` 서브클래스, mixin를 제공하는데에 초점을 맞추어야 한다.

#### `get_tags()`
OpenAPI 모음은 태그에 의해 동작한다. 기본적으로 태그는 라우팅된 URL의 첫 경로 부분에서 가져온다. 예를 들어 `/users/{id}/`와 같은 URL은 `users` 태그를 생성한다.

수동으로 태그를 명시하기 위해 `__init__()` 키워드 인자를 전달하거나(아래 참조) 사용자 정의 논리를 제공하기 위해 `get_tags()`를 override할 수 있다.

#### `get_operation()`
경로, 페이지 매김과 필터링을 위한 쿼리 파라미터 등을 포함하는 엔드포인트를 설명하는 [OpenAPI 작업 객체](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#operationObject)를 반환한다.

`get_components()`와 함께, 이것은 뷰 조회의 주 엔트리 포인트이다.

#### `get_operation_id()`
각 작업마다 고유한 [operationid](https://www.django-rest-framework.org/api-guide/schemas/openapi-operationid)가 있다. 기본적으로 `operationId`는 모델의 이름, 시리얼라이저의 이름 또는 뷰의 이름으로부터 추론된다. operationid는 "listItems", "retrieveItem", "updateItem"과 같다. `operationId`는 관습적으로 camelCase이다.

#### `get_operation_id_base()`
같은 모델 이름을 가진 여러 뷰를 가진다면 중복되는 operationId를 보게 된다.

이를 다루려면 ID의 이름 부분에 다른 기초를 제공하기 위해 `get_operation_id_base()`를 override한다.

#### `get_serializer()`
만약 뷰가 구현된 `get_serializer()`를 가진다면 그 결과를 반환한다.

#### `get_request_serializer()`
기본적으로 `get_serializer()`를 반환하지만 요청과 응답 객체를 구별하기 위해 override될 수 있다.

#### `get_response_serializer()`
기본적으로 `get_serializer()`를 반환하지만 요청과 응답 객체를 구별하기 위해 override될 수 있다.

### `AutoSchema.__init__()` kwargs
`AutoSchema`는 기본으로 생성된 값이 적절하지 않은 경우 일반적인 커스터마이즈에 사용되는 여러 `__init__()` 키워드 인자를 제공한다.

사용 가능한 키워드 인자는 다음과 같다:

-`tags`: 태그 리스트를 명시한다.
- `component_name`: 구성요소 이름을 명시한다.
- `operation_id_base`: 작업 ID의 리소스 이름 부분을 명시한다.

뷰에서 `AutoSchema` 인스턴스를 선언할 때 키워드 인자를 전달한다:

```python
class PetDetailView(generics.RetrieveUpdateDestroyAPIView):
    schema = AutoSchema(
        tags=['Pets'],
        component_name='Pet',
        operation_id_base='Pet',
    )
    ...
```

Pet 모델과 PetSerializer 시리얼라이저를 가정할 때 이 예시의 키워드 인자는 필요하지 않을 수 있다. 그럼에도 불구하고 종종 같은 모델을 목표로 하는 복수의 뷰나 동일한 이름의 시리얼라이저를 사용하는 복수의 뷰를 가질 때 키워드 인자를 전달할 필요가 있다.

뷰가 자주 필요한 연관된 사용자 지정을 가지는 경우 각 뷰에 `AutoSchema`의 서브클래스를 생성하지 않도록 프로젝트에 추가적인 `__init__()` 키워드 인자를 가지는 기본 `AutoSchema` 서브클래스를 작성할 수 있다.