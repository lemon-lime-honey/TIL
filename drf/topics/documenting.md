# [Documenting your API](https://www.django-rest-framework.org/topics/documenting-your-api/)
```
REST API는 리소스를 표현하고 애플리케이션 상태를 구동하는데 사용되는 미디어 타입을 정의하는데 거의 모든 서술적인 노력을 기울여야 한다.
- Roy Fielding, REST APIs must be hypertext driven
```

REST framework는 API 문서를 작성하는 도구와 함께 사용할 수 있는 OpenAPI 스키마 생성을 위한 빌트인 지원을 제공한다.

사용 가능한 여러 훌륭한 서드파티 문서화 패키지도 있다.

## Generating documentation from OpenAPI schemas
OpenAPI 스키마로부터 HTML 문서 페이지를 생성할 수 있게 해주는 여러 패키지가 있다.

대표적으로 [Swagger UI](https://swagger.io/tools/swagger-ui/)와 [ReDoc](https://github.com/Rebilly/ReDoc)이 있다.

둘 모두 정적 스키마 파일이나 동적 `SchemaView` 엔드포인트의 위치 정도만 필요로 한다.

### A minimal example with Swagger UI
동적 `SchemaView` 라우팅을 위해 [schema](../api-guide/schema.md) 문서의 예시를 따른다고 할 때, Swagger UI 사용을 위한 최소한의 Django 템플릿은 다음과 같다:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Swagger</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" href="//unpkg.com/swagger-ui-dist@3/swagger-ui.css" />
  </head>
  <body>
    <div id="swagger-ui"></div>
    <script src="//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js"></script>
    <script>
    const ui = SwaggerUIBundle({
      url: "{% url schema_url %}",
      dom_id: '#swagger-ui',
      presets: [
        SwaggerUIBundle.presets.apis,
        SwaggerUIBundle.SwaggerUIStandalonePreset
      ],
      layout: "BaseLayout",
      requestInterceptor: (request) => {
        request.headers['X-CSRFToken'] = "{{ csrf_token }}"
        return request;
      }
    })
    </script>
  </body>
</html>
```

이를 `swagger-ui.html`으로 템플릿 폴더에 저장한다. 그 다음 프로젝트의 URL 설정에서 `Template` 뷰를 라우팅한다.

```python
from django.views.generic import TemplateView

urlpatterns = [
    # ...
    # Route TemplateView to serve Swagger UI template.
    #   * Provide `extra_context` with view name of `SchemaView`.
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
]
```

자세한 사용법은 [Swagger UI 문서](https://swagger.io/tools/swagger-ui/)에서 확인할 수 있다.

### A minimal example with ReDoc.
동적 `SchemaView` 라우팅을 위해 [schema](../api-guide/schema.md) 문서의 예시를 따른다고 할 때, ReDoc 사용을 위한 최소한의 Django 템플릿은 다음과 같다:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>ReDoc</title>
    <!-- needed for adaptive design -->
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
    <!-- ReDoc doesn't change outer page styles -->
    <style>
      body {
        margin: 0;
        padding: 0;
      }
    </style>
  </head>
  <body>
    <redoc spec-url='{% url schema_url %}'></redoc>
    <script src="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"> </script>
  </body>
</html>
```

이를 `redoc.html`으로 템플릿 폴더에 저장한다. 그 다음 프로젝트의 URL 설정에서 `Template` 뷰를 라우팅한다.

```python
from django.views.generic import TemplateView

urlpatterns = [
    # ...
    # Route TemplateView to serve ReDoc template.
    #   * Provide `extra_context` with view name of `SchemaView`.
    path('redoc/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='redoc'),
]
```

자세한 사용법은 [ReDoc 문서](https://github.com/Rebilly/ReDoc)에서 확인할 수 있다.

## Third party packages
API 문서를 제공하기 위한 완성된 여러 서드파티 패키지가 있다.

### drf-yasg - Yet Another Swagger Generator
[drf-yasg](https://github.com/axnsan12/drf-yasg/)는 Django Rest Framework에 의한 스키마 생성을 사용하지 않고 구현된 [Swagger](https://swagger.io/) 생성 도구이다.

중첩된 스키마, 명명된 모델, 응답 바디, enum/pattern/min/max 유효성 검사지, 폼 파라미터 등과 같이 [OpenAPI](https://openapis.org/) 명세를 가능한 한 최대한 구현하는 것과 `swagger-codegen`과 같은 코드 생성 도구와 함께 사용할 수 있는 문서를 생성하는 것이 목표이다.

또한 매우 유용한 대화형 문서 뷰어를 `swagger-ui` 형식으로 변환한다:

![drf-yasg](https://www.django-rest-framework.org/img/drf-yasg.png)

### drf-spectacular - Sane and flexible OpenAPI 3.0 schema generation for Django REST framework
[drf-spectacular](https://github.com/tfranzel/drf-spectacular/)는 확장성, 커스터마이즈 가능성 그리고 클라이언트 생성에 명시적인 초점을 둔 [OpenAPI 3](https://openapis.org/) 스키마 생성 도구이다. 사용 패턴은 [drf-yasg](https://github.com/axnsan12/drf-yasg/)와 매우 유사하다.

쉬운 커스터마이즈를 위해 데코레이터와 확장을 제공하며 가능한 한 최대한의 스키마 정보를 추출하는 것을 목표로 한다. [swagger-codegen](https://swagger.io/), [SwaggerUI](https://swagger.io/tools/swagger-ui/), [Redoc](https://github.com/Rebilly/ReDoc), i18n, 버전 작성, 인증, 다형성(동적 요청과 응답), 쿼리/경로/헤더 파라미터, 문서화 등을 명시적으로 지원한다. DRF용으로 인기있는 여러 플러그인 또한 지원한다.

## Self describing APIs
REST framework가 지원하는 브라우징 가능한 API는 작성한 API가 완전히 자기 설명을 할 수 있게 한다. 각 API 엔드포인트의 문서는 간단히 브라우저에서 해당하는 URL을 방문하는 것으로 제공된다.

![self-describing](https://www.django-rest-framework.org/img/self-describing.png)

### Setting the title
브라우징 가능한 API에서 사용되는 제목은 뷰 클래스 이름이나 함수 이름에서 생성된다. 따라 붙는 `View` 또는 `ViewSet` 접미사는 제거되며, 문자열의 대문자/소문자 경계나 언더스코어는 공백으로 분리된다.

예를 들어, 뷰 `UserListView`는 브라우징 가능한 API에서 `User List`로 나타난다.

Viewset을 사용하는 경우 각각의 생성된 뷰에 적절한 접미사가 붙는다. 예를 들어 뷰 집합 `UserViewSet`은 `User List`와 `User Instance`라는 이름의 뷰를 생성한다.

### Setting the description
브라우징 가능한 API에서의 설명은 뷰 또는 viewset의 문서 문자열로부터 생성된다.

파이썬 `Markdown` 라이브러리가 설치되었다면 문서 문자열에서 [마크다운 문법](https://daringfireball.net/projects/markdown/syntax)이 사용될 수 있으며, 브라우징 가능한 API에서 HTML로 변환된다. 예를 들어:

```python
class AccountListView(views.APIView):
    """
    Returns a list of all **active** accounts in the system.

    For more details on how accounts are activated please [see here][ref].

    [ref]: http://example.com/activating-accounts
    """
```

Viewset을 사용할 때 모든 생성된 뷰에 기본 문서 문자열이 사용된다는 점에 유의한다. list와 retrieve 뷰와 같이 각 뷰에 설명을 제공하려면 [스키마 문서의 예시들](../api-guide/schema.md)에서 설명된 문서 문자열 섹션을 사용한다.

### The `OPTIONS` method
REST framework API는 `OPTIONS` HTTP 메서드를 사용하는 프로그램적으로 접근할 수 있는 설명 또한 지원한다. 뷰는 `OPTIONS` 요청을 이름, 설명, 그리고 허용하며 응답하는 여러 미디어 타입을 포함한 메타데이터로 응답한다.

제네릭 뷰를 사용할 때, `OPTIONS` 요청은 시리얼라이저에 있는 필드를 설명하는 사용 가능한 `POST` 또는 `PUT` 동작에 대한 메타데이터를 추가적으로 응답한다.

`options` 뷰 메서드를 override하고 또는/그리고 사용자 정의 메타데이터 클래스를 제공하여 `OPTIONS` 요청에 대한 응답 동작을 수정할 수 있다. 예를 들어:

```python
def options(self, request, *args, **kwargs):
    """
    Don't include the view description in OPTIONS responses.
    """
    meta = self.metadata_class()
    data = meta.determine_metadata(request, self)
    data.pop('description')
    return Response(data=data, status=status.HTTP_200_OK)
```

자세한 사항은 [메타데이터 문서](../api-guide/metadata.md)에서 확인할 수 있다.

## The hypermedia approach
완전히 RESTful하려면 API는 발신하는 응답에서 사용 가능한 동작을 하이퍼미디어 컨트롤로 표현해야 한다.

이 접근에서는 사용 가능한 API 엔드포인트를 미리 문서화하는 대신 사용되는 미디어 타입에 대해 설명한다. 주어진 URL에서 사용할 수 있는 동작은 엄격히 고정된 것은 아니지만, 반환된 문서의 링크와 폼 컨트롤의 존재로 사용 가능하게 된다.

하이퍼미디어 API를 구현하려면 API를 위한 적절한 미디어 타입을 결정하고 그 미디어 타입을 위한 사용자 정의 렌더러와 parser를 구현해야 한다. [REST, Hypermedia & HATEOAS](rhh.md) 섹션은 다양한 하이퍼미디어 포맷에 대한 링크 뿐만이 아니라 배경 읽기에 대한 포인터를 포함한다.