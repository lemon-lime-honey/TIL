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