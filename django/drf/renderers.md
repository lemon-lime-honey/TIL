# [Renderers](https://www.django-rest-framework.org/api-guide/renderers/)
```
TemplateResponse 인스턴스는 클라이언트에게 반환되기 전에 렌더링되어야 한다.
렌더링 프로세스는 템플릿과 컨텍스트의 intermediate representation을 가져와 클라이언트에게 제공될 최종 바이트 스트림으로 변환한다.
- Django documentation
```

REST framework는 다양한 미디어 유형을 가지는 응답을 반환할 수 있게 하는 여러 Renderer 클래스를 포함한다. 미디어 유형을 디자인할 수 있는 유연성을 제공하는 사용자 정의 renderer 작성 또한 제공한다.

## How the renderer is determined
뷰를 위한 유효한 renderer 설정은 언제나 클래스 리스트로 정의된다. 뷰가 입력되면, REST framework는 들어오는 요청의 컨텐츠 협상을 진행할 것이며, 요청을 만족시키는 가장 적절한 renderer를 결정한다.

컨텐츠 협상의 기본 프로세스는 응답에 어떤 미디어 유형이 있어야 하는지 결정하기 위해 요청의 `Accept`헤더를 검사하는 것이 포함된다. 선택사항으로 특정 표현을 명시적으로 요청하기 위해 URL에서 포맷 접미사를 사용할 수도 있다. 예를 들어 URL `http://example.com/api/users_count.json`은 언제나 JSON 데이터를 반환하는 엔드포인트이다.

더 많은 정보는 [content negotiation](https://www.django-rest-framework.org/api-guide/content-negotiation/) 문서에서 확인할 수 있다.

## Setting the renderers
Renderer 기본 설정은 `DEFAULT_RENDERER_CLASSES` 설정을 사용해 전역적으로 설정될 수 있다. 예를 들어 다음 설정은 `JSON`을 주된 미디어 유형으로 사용하고 self describing API를 포함한다.

```python
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}
```

또한 `APIView` 클래스 기반 뷰를 사용해 개별적인 뷰, viewset에 사용되는 renderer를 설정할 수도 있다.

```python
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

class UserCountView(APIView):
    """
    A view that returns the count of active users in JSON.
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
    A view that returns the count of active users in JSON.
    """
    user_count = User.objects.filter(active=True).count()
    content = {'user_count': user_count}
    return Response(content)
```

## Ordering of renderer classes
API에 사용할 renderer 클래스를 명시할 때 각 미디어 유형에 따른 우선순위를 어떻게 정할지 고려해야 한다. 클라이언트가 `Accept: */*` 헤더를 보내거나 `Accept`헤더를 포함하지 않는 등 받을 수 있는 미디어 유형을 명시하지 않는다면 REST framework는 응답을 위해 리스트의 첫번째 renderer를 선택한다.

예를 들어 API가 요청에 따라 일반적인 웹페이지와 API 응답을 모두 다룰 수 있는 뷰를 가진다면 [broken accept headers](http://www.gethifi.com/blog/browser-rest-http-accept-headers)를 보내는 오래된 브라우저를 잘 다루기 위해 `TemplateHTMLRenderer`를 기본 renderer로 설정하는 것을 고려해야 한다.

# API Reference
## JSONRenderer
utf-8 인코딩을 사용해 요청 데이터를 `JSON`으로 렌더링한다.

기본 스타일은 유니코드 문자를 포함하며 불필요한 공백이 없는 압축된 스타일을 이용해 응답을 렌더링한다.

```
{"unicode black star":"★", "value":999}
```

클라이언트는 반환된 `JSON`이 들여쓰기 되는 경우 `'indent'`  미디어 유형 인자를 추가적으로 포함시킨다. 예를 들면 `Accept: application/json; indent=4`.

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
Django의 표준 템플릿 렌더링을 사용해 데이터를 HTML로 렌더링한다. 다른 renderer와 다르게, `Response`로 전달되는 데이터는 serialize될 필요가 없다. 또한 다른 renderer와 다르게, `Response`를 생성할 때 `template_name` 인자를 추가할 수 있다.

TemplateHTMLRenderer는 `responser.data`를 컨텍스트 딕셔너리로 사용해 `RequestContext`를 생성하며 컨텍스트를 렌더링하기 위해 사용되는 템플릿 이름을 결정한다.

- Note<br>
  Serializer를 사용하는 뷰에서 사용될 때 렌더링을 위해 송신되는 `Response`가 딕셔너리가 아니므로 TemplateHTMLRenderer가 렌더링하게 하기 위해 반환하기 전에 딕셔너리로 감싸야 한다. 예를 들면,
  ```python
  response.data = {'results': response.data}
  ```

템플릿 이름은 다음에 의해 (선호도 순서로) 결정된다.

1. 요청에 전달된 명시적인 `template_name` 인자
2. 해당 클래스에서 명시적으로 설정된 `.template_name` 속성
3. `view.get_template_names()`가 호출된 결과 반환하는 것

다음은 `TemplateHTMLRenderer`를 사용하는 뷰의 예시이다.

```python
class UserDetail(generics.RetrieveAPIView):
    """
    A view that returns a templated HTML representation of a given user.
    """
    queryset = User.objects.all()
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return Response({'user': self.object}, template_name='user_detail.html')
```

REST framework를 사용하는 일반적인 HTML 페이지를 반환하거나 하나의 엔드포인트에서 HTML과 API 응답을 반환하게 할 때, 두 경우 모두 `TemplateHTMLRenderer`를 사용할 수 있다.

만약 다른 renderer 클래스와 함께 `TemplateHTMLRenderer`를 사용하는 웹사이트를 작성 중이라면 `TemplateHTMLRenderer`를 `renderer_classes` 리스트의 가장 첫 클래스로 입력해 형편없이 생성된 `ACCEPT:` 헤더를 보내는 브라우저에서도 `TemplateHTMLRenderer`가 가장 처음으로 선택되게 하는 것을 고려해야 한다.

`TemplateHTMLRenderer` 사용의 다른 예시는 [HTML & Forms Topic Page](https://www.django-rest-framework.org/topics/html-and-forms/)에서 확인할 수 있다.

**.media_type**: `text/html`<br>
**.format**: `'html'`<br>
**.charset**: `utf-8`<br>

See also: `StaticHTMLRenderer`

## StaticHTMLRenderer
미리 렌더링된 HTML을 단순히 반환하는 단순한 renderer. 다른 renderer와는 달리 응답 객체로 전달되는 데이터는 반환되는 컨텐츠를 나타내는 문자열이어야 한다.

`StaticHTMLRenderer`를 사용하는 뷰의 예시이다.

```python
@api_view(['GET'])
@renderer_classes([StaticHTMLRenderer])
def simple_html_view(request):
    data = '<html><body><h1>Hello, world</h1></body></html>'
    return Response(data)
```

REST framework를 사용하는 일반적인 HTML 페이지를 반환하거나 하나의 엔드포인트에서 HTML과 API 응답을 둘 다 반환하게 하는데 `StaticHTMLRenderer`를 사용할 수 있다.

**.media_type**: `text/html`<br>
**.format**: `'html'`<br>
**.charset**: `'utf-8'`<br>

See also: `TemplateHTMLRenderer`

## BrowsableAPIRenderer
브라우징 가능한 API를 위한 HTML로 데이터를 렌더링한다.

![BrowsableAPIRenderer 사용 예시](https://www.django-rest-framework.org/img/quickstart.png)

이 renderer는 어느 다른 renderer가 가장 높은 우선순위를 가지는지 결정하고, 그것을 HTML 페이지를 위한 API 스타일 응답에 사용한다.

**.meida_type**: `text/html`<br>
**.format**: `'api'`<br>
**.charset**: `utf-8`<br>
**.template**: `'rest_framework/api.html'`

### Customizing BrowsableAPIRenderer
기본적으로 응답 컨텐츠는 `BrowsableAPIRenderer`를 제외한 가장 높은 우선순위를 가진 renderer로 렌더링된다. 만약 기본 반환 포맷으로 HTML을 사용하지만 브라우징 가능한 API에서는 JSON을 사용하는 것과 같이 이런 동작을 커스터마이즈해야 한다면 `get_default_renderer()` 메서드를 override해서 구현할 수 있다. 예를 들면:

```python
class CustomBrowsableAPIRenderer(BrowsableAPIRenderer):
    def get_default_renderer(self, view):
        return JSONRenderer()
```

## AdminRenderer
관리 페이지 같은 화면으로 데이터를 HTML로 렌더링한다.

![AdminRenderer 사용예시](https://www.django-rest-framework.org/img/admin.png)

이 renderer는 데이터를 관리하기 위한 사용자 친화적인 인터페이스를 표현하는 CRUD 스타일 웹 API에 적합하다.

HTML 폼이 적절하게 지원하지 못하는 만큼, 입력에 시리얼라이저에 포함된 시리얼라이저나 나열된 시리얼라이저를 가지는 뷰는 `AdminRenderer`와 잘 동작하지 못한다는 점에 주의한다.

Note: `AdminRenderer`는 오직 적절하게 설정된 `URL_FIELD_NAME`(기본값 `url`) 속성이 데이터에 존재할 때에만 디테일 페이지에 링크를 추가할 수 있다. `HyperlinkModelSerializer`가 한 예가 되겠지만, `ModelSerializer`나 단순한 `Serializer` 클래스에서는 필드를 명시적으로 추가해야 한다. 여기 모델에 `get_absolute_url` 메서드를 사용하는 예시가 있다.

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