# [Renderers](https://www.django-rest-framework.org/api-guide/renderers/)
```
TemplateResponse 인스턴스는 클라이언트에게 반환되기 전에 렌더링되어야 한다.
렌더링 프로세스는 템플릿과 컨텍스트의 중간 표현을 가져와 클라이언트에게 제공될 최종 바이트 스트림으로 변환한다.
- Django documentation
```

REST framework는 다양한 미디어 타입을 가진 응답을 반환할 수 있게 해주는 여러 개의 빌트인 렌더러 클래스를 가진다. 또한 커스텀 렌더러 정의를 지원해 미디어 타입을 디자인할 수 있는 유연함을 제공한다.

## How the renderer is determined
뷰를 위한 유효한 렌더러 집합은 항상 클래스 리스트로 정의된다. 뷰가 입력되면 REST framewok는 들어오는 요청에 대해 컨텐츠 협상을 수행하며 요청을 만족시키는 가장 적절한 렌더러를 결정한다.

컨텐츠 협상의 기본 프로세스는 응답에 어떤 미디어 타입이 있어야 하는지 결정하기 위해 요청의 `Accept` 헤더를 검사하는 것이 포함된다. 선택사항으로 특정 표현을 명시적으로 요청하기 위해 URL에서 포맷 접미사를 사용할 수도 있다. 예를 들어 URL `http://example.com/api/users_count.json`은 언제나 JSON 데이터를 반환하는 엔드포인트이다.

자세한 사항은 [컨텐츠 협상](content_negotiation.md) 문서에서 확인할 수 있다.

## Setting the renderers
`DEFAULT_RENDERER_CLASSES` 설정을 사용해 렌더러 기본 집합을 전역적으로 설정할 수 있다. 예를 들어 다음 설정은 `JSON`을 주된 미디어 타입으로 사용하고 self describing API를 포함한다.

```python
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}
```

또한 `APIView` 클래스 기반 뷰를 사용해 개별적인 뷰, 뷰셋에 사용되는 렌더러를 설정할 수도 있다.

```python
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class UserCountView(APIView):
    """
    활성 사용자 수를 JSON으로 반환하는 뷰
    """
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        user_count = User.objects.filter(active=True).count()
        content = {'user_count': user_count}
        return Response(content)
```

또는 함수 기반 뷰와 함께 `@api_view` 데코레이터를 사용할 수도 있다.

```python
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def user_count_view(request, format=None):
    """
    활성 사용자 수를 JSON으로 반환하는 뷰
    """
    user_count = User.objects.filter(active=True).count()
    content = {'user_count': user_count}
    return Response(content)
```

## Ordering of renderer classes
API에 사용할 렌더러 클래스를 명시할 때 각 미디어 타입에 따른 우선순위를 어떻게 정할지 고려해야 한다. 클라이언트가 `Accept: */*` 헤더를 보내거나 `Accept`헤더를 포함하지 않는 등 받을 수 있는 미디어 타입을 명시하지 않는다면 REST framework는 응답을 위해 리스트의 첫번째 렌더러를 선택한다.

예를 들어 API가 요청에 따라 일반적인 웹페이지와 API 응답을 모두 다룰 수 있는 뷰를 가진다면 [broken accept headers](http://www.gethifi.com/blog/browser-rest-http-accept-headers)를 보내는 오래된 브라우저를 잘 다루기 위해 `TemplateHTMLRenderer`를 기본 렌더러로 설정하는 것을 고려해야 한다.

# API Reference
## JSONRenderer
utf-8 인코딩을 사용해 요청 데이터를 `JSON`으로 렌더링한다.

기본 스타일은 유니코드 문자를 포함하며 불필요한 공백이 없는 압축된 스타일을 이용해 응답을 렌더링한다:

```
{"unicode black star":"★", "value":999}
```

클라이언트는 반환된 `JSON`이 들여쓰기 되는 경우 `'indent'`  미디어 타입 인자를 추가적으로 포함시킨다. 예를 들면 `Accept: application/json; indent=4`.

```
{
  "unicode black star": "★",
  "value": 999
}
```

기본 JSON 인코딩 스타일은 `UNICODE_JSON`, `COMPACT_JSON` 설정 키를 사용해 바꿀 수 있다.

**.media_type**: `application/json`<br>
**.format**: `'json'`<br>
**.charset**: `None`

## TemplateHTMLRenderer
Django의 표준 템플릿 렌더링을 사용해 데이터를 HTML로 렌더링한다. 다른 렌더러와 다르게 `Response`로 전달되는 데이터는 직렬화 될 필요가 없다. 또한 다른 렌더러와 다르게 `Response`를 생성할 때 `template_name` 인자를 추가할 수 있다.

TemplateHTMLRenderer는 `responser.data`를 컨텍스트 딕셔너리로 사용해 `RequestContext`를 생성하며 컨텍스트를 렌더링하기 위해 사용되는 템플릿 이름을 결정한다.

---

**Note**<br>
시리얼라이저를 사용하는 뷰에서 사용될 때, 렌더링을 위해 송신되는 `Response`는 딕셔너리가 아니며 그러므로 TemplateHTMLRenderer가 렌더링할 수 있도록 반환하기 전에 딕셔너리로 감싸야 한다. 예를 들어:

```python
response.data = {'results': response.data}
```

---

템플릿 이름은 다음에 의해 (선호도 순서로) 결정된다.

1. 요청에 전달된 명시적인 `template_name` 인자
2. 해당 클래스에서 명시적으로 설정된 `.template_name` 속성
3. `view.get_template_names()`의 호출 결과로 반환된 것

다음은 `TemplateHTMLRenderer`를 사용하는 뷰의 예시이다.

```python
class UserDetail(generics.RetrieveAPIView):
    """
    주어진 사용자의 템플릿화된 HTML 표현을 반환하는 뷰
    """
    queryset = User.objects.all()
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return Response({'user': self.object}, template_name='user_detail.html')
```

REST framework를 사용하는 일반적인 HTML 페이지를 반환하거나 하나의 엔드포인트에서 HTML과 API 응답을 반환하게 하는 경우, 둘 모두 `TemplateHTMLRenderer`를 사용할 수 있다.

만약 다른 렌더러 클래스와 함께 `TemplateHTMLRenderer`를 사용하는 웹사이트를 작성 중이라면 `TemplateHTMLRenderer`를 `renderer_classes` 리스트의 가장 첫 클래스로 입력해 잘 생성되지 못한 `ACCEPT:` 헤더를 보내는 브라우저에서도 `TemplateHTMLRenderer`가 가장 처음으로 선택되게 하는 것을 고려해야 한다.

`TemplateHTMLRenderer` 사용의 다른 예시는 [HTML과 폼 토픽 페이지](../topics/htmlform.md)에서 확인할 수 있다.

**.media_type**: `text/html`<br>
**.format**: `'html'`<br>
**.charset**: `utf-8`<br>

See also: `StaticHTMLRenderer`

## StaticHTMLRenderer
미리 렌더링된 HTML을 단순히 반환하는 간단한 렌더러. 다른 렌더러와는 달리 응답 객체로 전달되는 데이터는 반환되는 컨텐츠를 나타내는 문자열이어야 한다.

다음은 `StaticHTMLRenderer`를 사용하는 뷰의 예시이다:

```python
@api_view(['GET'])
@renderer_classes([StaticHTMLRenderer])
def simple_html_view(request):
    data = '<html><body><h1>Hello, world</h1></body></html>'
    return Response(data)
```

REST framework를 사용하는 일반적인 HTML 페이지를 반환하거나 하나의 엔드포인트에서 HTML과 API 응답을 둘 다 반환하게 하는 경우 `StaticHTMLRenderer`를 사용할 수 있다.

**.media_type**: `text/html`<br>
**.format**: `'html'`<br>
**.charset**: `'utf-8'`<br>

See also: `TemplateHTMLRenderer`

## BrowsableAPIRenderer
브라우징 가능한 API를 위한 HTML로 데이터를 렌더링한다:

![BrowsableAPIRenderer 사용 예시](https://www.django-rest-framework.org/img/quickstart.png)

이 렌더러는 어느 다른 렌더러가 가장 높은 우선순위를 가지는지 결정하고,API 스타일 응답을 HTML 페이지로 표시하기 위해 사용한다.

**.meida_type**: `text/html`<br>
**.format**: `'api'`<br>
**.charset**: `utf-8`<br>
**.template**: `'rest_framework/api.html'`

### Customizing BrowsableAPIRenderer
기본적으로 응답 컨텐츠는 `BrowsableAPIRenderer`를 제외한 가장 높은 우선순위를 가진 렌더러로 렌더링된다. 만약 기본 반환 포맷으로 HTML을 사용하지만 브라우징 가능한 API에서는 JSON을 사용하는 것과 같이 이런 동작을 커스터마이즈해야 한다면 `get_default_renderer()` 메서드를 override해서 구현할 수 있다. 예를 들면:

```python
class CustomBrowsableAPIRenderer(BrowsableAPIRenderer):
    def get_default_renderer(self, view):
        return JSONRenderer()
```

## AdminRenderer
관리 페이지와 유사한 화면으로 데이터를 HTML로 렌더링한다:

![AdminRenderer 사용예시](https://www.django-rest-framework.org/img/admin.png)

이 렌더러는 데이터를 관리하기 위한 사용자 친화적인 인터페이스를 표현하는 CRUD 스타일 웹 API에 적합하다.

입력을 위한 중첩되거나 리스트 시리얼라이저를 가지는 뷰는 HTML 폼이 그러한 시리얼라이저를 적절히 지원하지 못하기 때문에 `AdminRenderer`와 함께 잘 동작하지 않는다는 점에 유의한다.

**Note**: `AdminRenderer`는 오직 적절하게 구성된 `URL_FIELD_NAME`(기본값 `url`) 속성이 데이터에 존재할 때에만 디테일 페이지에 링크를 포함할 수 있다. `HyperlinkModelSerializer`가 한 예가 되겠지만, `ModelSerializer`나 단순한 `Serializer` 클래스에서는 필드를 명시적으로 추가해야 한다. 다음은 모델에 `get_absolute_url` 메서드를 사용하는 예시이다:

```python
class AccountSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Account
```

**.media_type**: `text/html`<br>
**.format**: `'admin'`<br>
**.charset**: `utf-8`<br>
**.template**: `'rest_framework/admin.html`

## HTMLFormRenderer
시리얼라이저가 반환하는 데이터를 HTML 폼으로 렌더링한다. 이 렌더러의 출력은 `<form>` 태그나 숨겨진 CSRF 입력, 또는 제출 버튼을 포함하지 않는다.

이 렌더러는 직접적인 사용을 의도로 하지는 않지만 대신 시리얼라이저 인스턴스를 `render_form` 템플릿 태그로 전달해 사용할 수 있다.

```python
{% load rest_framework %}

<form action="/submit-report/" method="post">
  {% csrf_token %}
  {% render_form serializer %}
  <input type="submit" value="Save" />
</form>
```

더 많은 정보는 [HTML & 폼](../topics/htmlform.md) 문서에서 확인할 수 있다.

**.media_type**: `text/html`<br>
**.format**: `'form'`<br>
**.charset**: `utf-8`<br>
**.template**: `'rest_framework/horizontal/form.html`

## MultiPartRenderer
HTML multipart 폼 데이터를 렌더링할 때 사용하는 렌더러. **응답 렌더러로는 적합하지 않지만** REST framework의 [테스트 클라이언트와 테스트 요청 팩토리](testing.md)를 사용해 테스트 요청을 생성하는데 사용된다.

**.media_type**: `multipart/form-data; boundary=BoUnDaRyStRiNg`<br>
**.format**: `'multipart'`<br>
**.charset**: `utf-8`

# Custom renderers
사용자 정의 렌더러를 구현하려면 `BaseRenderer`를 재정의하고 `.media_type`, `.format` 속성을 설정해야 하며 `.render(self, data, accepted_media_type=None, renderer_context=None)` 메서드를 구현해야 한다.

메서드는 HTTP 응답의 바디로 사용될 바이트 문자열을 반환해야 한다.

`.render()` 메서드로 전달되는 인자는 다음과 같다.
  - `data`<br>
    `Response()` 초기화에 의해 설정된 요청 데이터
  - `accepted_media_type=None`<br>
    선택인자. 주어진다면, 컨텐츠 협상 단계에서 결정되는 허용 가능한 미디어 타입이 된다.<br>
    클라이언트의 `Accept` 헤더에 따라 다르지만 렌더러의 `media_type` 속성보다 더 구체적일 수 있고, 미디어 타입 파라미터를 포함할 수도 있다. 예를 들면 `"application/json; nested=true"`
  - `renderer_context=None`<br>
    선택인자. 주어진다면, 뷰에 의해 제공되는 컨텍스트 정보를 가지는 딕셔너리가 된다.<br>
    기본적으로 다음의 키를 가진다: `view`, `request`, `response`, `args`, `kwargs`

## Example
다음은 응답 컨텐츠로 `data` 파라미터를 가지는 응답을 반환하는 플레인 텍스트 렌더러의 예시이다.

```python
from django.utils.encoding import smart_text
from rest_framework import renderers

class PlainTextRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return smart_text(data, encoding=self.charset)
```

## Setting the character set
기본적으로 렌더러 클래스는 `UTF-8` 인코딩을 사용한다고 간주된다. 다른 인코딩을 사용하려면 렌더러에 `charset` 속성을 설정하면 된다.

```python
class PlainTextRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'
    charset = 'iso-8859-1'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data.encode(self.charset)
```

렌더러 클래스가 유니코드 문자열을 반환하면, 응답 컨텐츠가 인코딩을 결정하는데 사용되는 렌더러에 설정된 `charset` 속성으로 `Response` 클래스에 의해 바이트 문자열로 강제된다는 점에 유의한다.

렌더러가 미가공 바이너리 컨텐츠를 표현하는 바이트 문자열을 반환하면 응답의 `Content-Type` 헤더가 `charset` 값 집합을 가지지 않도록 보장하기 위해 `charset` 값을 `None`으로 설정해야 한다.

`render_style` 속성을 `binary`로 설정할 수도 있다. 그렇게 하면 브라우징 가능한 API는 바이너리 컨텐츠를 문자열로 표현하지 않는다.

```python
class JPEGRenderer(renderers.BaseRenderer):
    media_type = 'image/jpeg'
    format = 'jpg'
    charset = None
    render_style = 'binary'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data
```

# Advanced renderer usage
REST framework의 렌더러를 사용하여 몇 가지 꽤 유연한 일을 할 수 있다. 다음은 그 예시이다.

- 요청받은 미디어 타입에 따라 같은 엔드포인트에서 단순한, 또는 중첩된 표현을 제공한다.
- 같은 엔드포인트에서 일반적인 HTML 웹페이지와 JSON 기반 API 응답을 모두 제공한다.
- `media_type = 'images/*'`를 사용하는 식으로 렌더러의 미디어 타입을 추상화하고, 응답의 인코딩을 다르게 하기 위해 `Accept` 헤더를 사용한다.

## Varying behaviour by media type
뷰가 허용된 미디어 타입에 따라 서로 다른 직렬화 방식을 사용하게 할 수 있다. 그렇게 하려면 응답에 사용된 협상된 렌더러를 결정하기 위해 `request.accepted_renderer`에 접근한다.

예를 들어:

```python
@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def list_users(request):
    """
    시스템 사용자에 대한 JSON 또는 HTML 표현을 반환할 수 있는 뷰
    """
    queryset = Users.objects.filter(active=True)

    if request.accepted_renderer.format = 'html':
        # TemplateHTMLRenderer는 컨텍스트 딕셔너리를 가지며,
        # 추가적으로 `template_name`을 필요로 한다.
        # 직렬화를 필요로 하지 않는다.
        data = {'users': queryset}
        return Response(data, template_name='list_users.html')

    # JSONRenderer는 일반적인 경우와 같이 직렬화된 데이터를 필요로 한다.
    serializer = UserSerializer(instance=queryset)
    data = serializer.data
    return Response(data)
```

## Underspecifying the media type
렌더러가 여러 미디어 타입을 다루게 할 수도 있다. 그렇게 하려면 `media_type` 값을 `image/*` 또는 `*/*`로 설정해 응답할 미디어 타입을 추상화한다.

렌더러의 미디어 타입을 추상화하면 `content_type` 속성을 사용해 응답을 반환할 때 미디어 타입을 명시적으로 구체화해야 한다. 예를 들면:

```python
return Response(data, content_type='image/png')
```

## Designing your media types
많은 웹 API의 경우, 하이퍼링크 관계에 있는 단순한 `JSON` 응답이면 충분하다. 만약 온전한 RESTful 디자인과 [HATEOAS](http://timelessrepo.com/haters-gonna-hateoas)를 포용하고 싶다면 미디어 타입의 설계와 사용 타입을 좀 더 구체적으로 고려해야 한다.

[Roy Fielding의 말](https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven)에 의하면, "REST API는 리소스와 실행 중인 애플리케이션의 상태를 표현하는데 사용되는 미디어 타입을 정의하거나, 확장된 관계명 그리고/또는 존재하는 표준 미디어 타입을 위한 하이퍼텍스트-가능한 마크업을 정의하는데 그 대부분의 서술적인 노력을 기울여야 한다".

사용자 정의 미디어 타입의 좋은 예시로는 GitHub의 사용자 정의 [application/vnd.github+json](https://developer.github.com/v3/media/) 미디어 타입 사용이나 Mike Amundsen의 IANA approved [application/vnd.collection+json](http://www.amundsen.com/media-types/collection/) JSON 기반 하이퍼미디어가 있다.

## HTML error views
일반적으로 렌더러는 일반적인 응답이나 `Http404`나 `PermissionDenied` 예외, 또는 `APIException`의 서브클래스와 같은 예외 발생으로 인한 응답을 같은 방식으로 대한다.

만약 `TemplateHTMLRenderer`나 `StaticHTMLRenderer`를 사용하고 있고 예외가 발생한다면 동작이 약간 달라지며, [Django의 기본 에러 뷰 다루기](https://docs.djangoproject.com/en/stable/topics/http/views/#customizing-error-views)처럼 동작한다.

HTML 렌더러에 의해 발생되고 다루어지는 예외는 우선순위에 따라 다음 중 한 가지 방법으로 렌더링을 시도한다.

- `{status_code}.html`이라는 이름의 템플릿을 불러오고 렌더링한다.
- `api_exception.html`이라는 이름의 템플릿을 불러오고 렌더링한다.
- "404 Not Found"처럼 HTTP 상태 코드와 문자열을 렌더링한다.

템플릿은 `status_code`와 `details` 키를 포함하는 `RequestContext`를 가지고 렌더링할 것이다.

**Note**: `DEBUG=True`라면, HTTP 상태 코드와 문자열을 렌더링하는 대신 Django의 표준 traceback 에러 페이지가 나타날 것이다.

# Third party packages
다음의 서드파티 패키지를 사용할 수도 있다.

## YAML
[REST framework YAML](https://jpadilla.github.io/django-rest-framework-yaml/)은 [YAML](http://www.yaml.org/) 파싱과 렌더링 지원을 제공한다. 이전에는 REST framework 패키지에 직접 포함되어 있었지만, 지금은 서드파티 패키지로 제공된다.

### Installation & configuration
#### pip을 사용해 설치한다.
```bash
$ pip install djangorestframework-yaml
```

#### REST framework 설정을 바꾼다.
```python
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework_yaml.parsers.YAMLParser',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework_yaml.renderers.YAMLRenderer',
    ],
}
```

## XML
[REST Framework XML](https://jpadilla.github.io/django-rest-framework-xml/)는 간단한 약식 XML 포맷을 제공한다. 이전에는 REST framework 패키지에 직접 포함되어 있었지만, 지금은 서드파티 패키지로 지원된다.

### Installation & configuration
#### pip을 사용해 설치한다.
```bash
$ pip install djangorestframework-xml
```

#### REST framework 설정을 바꾼다.
```python
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework_xml.parsers.XMLParser',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework_xml.renderers.XMLRenderer',
    ],
}
```

## JSONP
[REST framework JSONP](https://jpadilla.github.io/django-rest-framework-jsonp/)는 JSONP 렌더링 지원을 제공한다. 이전에는 REST framework 패키지에 직접 포함되어 있었지만, 지금은 서드파티 패키지로 지원된다.

---

**주의**: 만약 교차 도메인 AJAX 요청을 필요로 한다면, `JSONP` 대신 좀 더 현대적인 [CORS](https://www.w3.org/TR/cors/) 접근법을 사용해야 한다. 자세한 사항은 [CORS 문서](../topics/acc.md)에서 확인할 수 있다.

`jsonp` 접근법은 근본적으로 브라우저 핵이며, `GET` 요청이 인증되지 않고 어떠한 사용자 권한도 필요로 하지 않는 [전역적으로 읽기 가능한 API 엔드포인트에서만 적절하다.](https://stackoverflow.com/questions/613962/is-jsonp-safe-to-use)

---

### Installation & configuration
#### pip을 사용해 설치한다.
```bash
$ pip install djangorestframework-jsonp
```

#### REST framework 설정을 바꾼다.
```python
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework_jsonp.renderers.JSONPRenderer',
    ],
}
```

## MessagePack
[MessagePack](https://msgpack.org/)은 빠르고 효율적인 이진 직렬화 포맷이다. [Juan Riaza](https://github.com/juanriaza)가 REST framework에 MessagePack 렌더러와 파서를 지원하는 [djangorestframework-msgpack](https://github.com/juanriaza/django-rest-framework-msgpack) 패키지를 관리한다.

## Microsoft Excel: XLSX (Binary Spreadsheet Endpoints)
XLSX는 세계에서 가장 인기있는 이진 스프레드시트 포맷이다. [The Wharton School](https://github.com/wharton)의 [Tim Allen](https://github.com/flipperpa)이 OpenPyXL을 사용하는 XLSX 스트레드시트를 엔드포인트로 렌더링하고, 클라이언트가 다운로드 할 수 있게 하는 [drf-excel](https://github.com/wharton/drf-excel)을 관리한다. 스프레드시트는 뷰당 기반으로 스타일링 될 수 있다.

### Installation & configuration
#### pip을 사용해 설치한다.
```bash
$ pip install drf-excel
```

#### REST framework 설정을 바꾼다.
```python
REST_FRAMEWORK = {
    ...
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'drf_excel.renderes.XLSXRenderer',
    ],
}
```

파일이 이름 없이 (브라우저가 때로 기본값으로 확장자 없이 파일이름을 "download"로 설정하게 된다.) 스트리밍되는 것을 방지하려면, `Content-Disposition` 헤더를 재정의하는 mixin을 사용해야 한다. 만약 파일명이 주어지지 않는다면, 기본값인 `export.xlsx`로 지정된다. 예를 들어:

```python
from rest_framework.viewsets import ReadOnlyModelViewSet
from drf_excel.mixins import XLSXFileMixin
from drf_excel.renderers import XLSXRenderer

from .models import MyExampleModel
from .serializers import MyExampleSerializer

class MyExampleViewSet(XLSXFileMixin, ReadOnlyModelViewSet):
    queryset = MyExampleModel.objects.all()
    serializer_class = MyExampleSerializer
    renderer_classes = [XLSXRenderer]
    filename = 'my_export.xlsx'
```

## CSV
반점으로 구분된 값은 쉽게 스프레드시트 애플리케이션으로 가져올 수 있는 표와 같은 일반 텍스트 포맷이다. [Mjumbe Poe](https://github.com/mjumbewu)가 REST framework에 CSV 렌더러 지원을 제공하는 [djangorestframework-csv](https://github.com/mjumbewu/django-rest-framework-csv) 패키지를 관리한다.

## UltraJSON
[UltraJSON](https://github.com/esnme/ultrajson) 현저하게 빠른 JSON 렌더링을 제공하는 최적화된 C JSON 인코더이다. [Adam Mertz](https://github.com/Amertz08)가 UJSON 패키지를 사용한 JSON 렌더링을 구현하는, 지금은 관리되지 않고 있는 [drf-ujson-renderer](https://github.com/gizmag/drf-ujson-renderer)의 포크인 [drf-ujson2](https://github.com/Amertz08/drf_ujson2)를 관리한다.

## CamelCase JSON
[djangorestframework-camel-case](https://github.com/vbabiy/djangorestframework-camel-case)는 REST framework를 위한 카멜케이스 JSON 렌더러와 파서를 제공한다. 이는 시리얼라이저가 파이썬식 필드 명을 사용하게 하지만 API에서는 자바스크립트식 카멜 케이스 필드 명으로 보이게 한다. [Vitaly Babiy](https://github.com/vbabiy)가 관리한다.

## Pandas (CSV, Excel, PNG)
[Django REST Pandas](https://github.com/wq/django-rest-pandas)는 추가적인 데이터 가공과 [Pandas](https://pandas.pydata.org/) 데이터프레임 API를 통한 결과물을 지원하는 시리얼라이저와 렌더러를 제공한다. Django REST Pandas는 Pandas 스타일 CSV 파일, 엑셀 파일(`.xls`와 `.xlsx` 둘 모두), 그리고 여러 [다른 포맷](https://github.com/wq/django-rest-pandas#supported-formats)을 위한 렌더러를 포함한다. [wq Project](https://github.com/wq)의 일부로 [S. Andrew Sheppard](https://github.com/sheppard)가 관리한다.

## LaTeX
[REST Framework Latex](https://github.com/mypebble/rest-framework-latex)는 Laulatex를 사용한 PDF 결과물을 렌더링하는 렌더러를 제공한다. [Pebble (S/F Software)](https://github.com/mypebble)가 관리한다.