# [Parsers](https://www.django-rest-framework.org/api-guide/parsers/)
```
웹 서비스와 상호작용 하는 기기는 데이터를 송신할 때 form-encoded보다 좀 더 구조화된 포맷을 사용하는 경향이 있는데,
이는 단순한 폼보다 더 복잡한 데이터를 송신하기 때문이다.
- Malcom Tredinnick, Django developers group
```

REST framework는 다양한 미디어 유형의 요청을 허용할 수 있게 해주는 여러 빌트인 Parser 클래스를 제공한다. 또한 API가 허용할 미디어 유형을 디자인하기 위한 유연함을 제공하는 사용자 정의 parser를 정의할 수 있게 한다.

## How the parser is determined
뷰에 유효한 parser 설정은 언제나 클래스 리스트로 정의된다. `request.data`에 접근하게 될 때, REST framework는 들어오는 요청의 `Content-Type` 헤더를 검사하고 요청 내용을 parse하기 위해 어느 parser를 사용할지 결정한다.

- Note<br>
  클라이언트 어플리케이션을 개발할 때 HTTP 요청에서 데이터를 송신할 때 `Content-Type` 헤더를 설정해야 한다.<br>
  만약 컨텐츠 유형을 설정하지 않는다면, 대부분의 클라이언트는 기본값으로 `application/x-www-form-urlencoded`를 사용한다.<br>
  예를 들어, jQuery의 [.ajax() 메서드](https://api.jquery.com/jQuery.ajax/)를 사용해 인코딩된 `json` 데이터를 송신할 때, `contentType: 'application/json'` 설정을 반드시 포함해야 한다.

## Setting the parsers
Parser의 기본값은 `DEFAULT_PARSER_CLASSES` 설정을 사용해 전역적으로 설정될 것이다. 예를 들어, 다음의 설정은 기본값인 JSON 또는 폼 데이터가 아닌 `JSON` 컨텐츠를 가진 요청만 허용한다.

```python
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ]
}
```

`APIView` 클래스 기반 뷰를 사용해 개별적인 뷰, viewset를 위한 parser를 설정할 수 있다.

```python
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

class ExampleView(APIView):
    """
    A view that can accept POST requests with JSON content.
    """
    parser_classes = [JSONParser]

    def post(self, request, format=None):
        return Response({'received data': request.data})
```

또는 함수 기반 뷰에 `@api_view` 데코레이터를 사용할 수도 있다.

```python
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser

@api_view(['POST'])
@parser_classes([JSONParser])
def example_view(request, format=None):
    """
    A view that can accept POST requests with JSON content.
    """
    return Response({'received data': request.data})
```