# [Content negotiation](https://www.django-rest-framework.org/api-guide/content-negotiation/)
```
HTTP는 "컨텐츠 협상"을 위한 여러 매커니즘에 관한 조항을 가지고 있다.
(컨텐츠 협상: 여러 표현이 가능할 때 주어진 응답을 위한 최적의 표현을 선택하는 프로세스)
- RFC 2616, Fielding et al.
```

컨텐츠 협상은 클라이언트나 서버의 선호에 기반하여 복수의 가능한 표현 중 클라이언트에게 반환하기 위한 하나를 선택하는 프로세스이다.

## Determining the accepted renderer
REST framework는 사용 가능한 렌더러, 그 렌더러의 우선순위, 클라이언트의 `Accept:` 헤더에 기반하여 어느 미디어 타입이 클라이언트에게 반환되어야 하는지 결정하기 위해 단순한 형식의 컨텐츠 협상을 사용한다. 사용된 형식은 부분적으로는 클라이언트 기반, 부분적으로는 서버 기반이다.

1. 덜 구체적인 미디어 타입보다 더 구체적인 미디어 타입이 선호된다.
2. 복수의 미디어 타입이 같은 특성을 가지면 선호도는 주어진 뷰에서 설정된 렌더러의 순서에 기반한다.

예를 들어, 다음의 `Accept` 헤더가 주어졌을 때:

```
application/json; indent=4, application/json, application/yaml, text/html, */*
```

주어진 각 미디어 타입의 우선순위는 다음과 같을 것이다:

- `application/json; indent=4`
- `application/json`, `application/yaml`, `text/html`
- `*/*`

요청된 뷰가 `YAML`과 `HTML`을 위한 렌더러로만 설정되었다면, REST framework는 `renderer_classes` 리스트 또는 `DEFAULT_RENDERER_CLASSES` 설정에 처음으로 포함된 렌더러를 선택한다.

`HTTP Accept` 헤더에 관한 자세한 사항은 [RFC 2616](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html)에서 확인한다.

**Note**:<br>
REST framework가 선호도를 결정할 때 "q" 값은 고려되지 않는다. "q"값 사용은 캐싱에 부정적인 영향을 주며, 원문 작성자의 의견으로는 컨텐츠 협상에 대한 불필요하고 지나치게 복합한 접근이다.

HTTP 사양이 클라이언트 기반 선호도와 비교하여 서버가 어떻게 서버 기반 선호도에 가중치를 주어야 할지를 의도적으로 과소 지정하기 때문에 유효한 접근이다.

# Custom content negotiation
REST framework를 위한 사용자 정의 컨텐츠 협상 스킴을 제공할 필요가 거의 없지만, 필요한 경우 할 수 있다. 사용자 정의 컨텐츠 스킴을 구현하려면 `BaseContentNegotiation`을 override한다.

REST framework의 컨텐츠 협상 클래스는 요청을 위한 적절한 parser와 응답을 위한 적절한 렌더러 선택 모두를 다루기 때문에 `.select_parser(request, parsers)`와 `.select_renderer(request, renderers, format_suffix)` 메서드를 모두 구현해야 한다.

`select_parser()` 메서드는 가능한 parser 리스트에서 하나의 parser 인스턴스를 반환하거나 들어오는 요청을 다룰 수 있는 parser가 없다면 `None`을 반환해야 한다.

`select_renderer()` 메서드는 (렌더러 인스턴스, 미디어 타입) 튜플 쌍을 반환하거나 `NotAcceptable` 예외를 발생시켜야 한다.

## Example
다음은 적절한 parser 또는 렌더러를 선택할 때 클라이언트 요청을 무시하는 사용자 정의 컨텐츠 협상 클래스이다.

```python
from rest_framework.negotiation import BaseContentNegotiation


class IgnoreClientNegotiation(BaseContentNegotiation):
    def select_parser(self, request, parsers):
        """
        Select the first parser in the `.parser_classes` list.
        """
        return parsers[0]


    def select_renderer(self, request, renderers, format_suffix):
        """
        Select the first renderer in the `.renderer_classes` list.
        """
        return (renderers[0], renderers[0].media_type)
```

## Setting the content negotiation
기본 컨텐츠 협상 클래스는 `DEFAULT_CONTENT_NEGOTIATION_CLASS` 설정을 사용해 전역적으로 설정될 수 있다. 예를 들어, 다음은 예시 `IgnoreClientContentNegotiation` 클래스를 사용하는 설정이다.

```python
REST_FRAMEWORK = {
    'DEFAULT_CONTENT_NEGOTIATION_CLASS': 'myapp.negotiation.IgnoreClientContentNegotiation',
}
```

`APIView` 클래스 기반 뷰를 사용하여 각 뷰 또는 viewset에 사용되는 컨텐츠 협상을 설정할 수도 있다.

```python
from myapp.negotiation import IgnoreClientContentNegotiation
from rest_framework.response import Response
from rest_framework.views import APIView


class NoNegotiationView(APIView):
    """
    An example view that does not perform content negotiation.
    """
    content_negotiation_class = IgnoreClientContentNegotiation


    def get(self, request, format=None):
        return Response({
            'accepted media type': request.accepted_renderer.media_type
        })
```