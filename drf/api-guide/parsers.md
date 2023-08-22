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

# API Reference
## JSONParser
`JSON` 요청 컨텐츠를 파싱한다. `request.data`는 데이터 딕셔너리로 채워진다.

**.media_type**: `application/json`

## FormParser
HTML 폼 컨텐츠를 파싱한다. `request.data`는 데이터의 `QueryDict`로 채워진다.

보통 HTML 폼 데이터를 온전히 지원하기 위해 `FormParser`와 `MultiPartParser`를 같이 사용한다.

**.media_type**: `application/x-www-form-urlencoded`

## MultiPartParser
파일 업로드를 지원하는 multipart HTML 폼 컨텐츠를 파싱한다. 두 `request.data` 모두 `QueryDict`로 채워진다.

보통 HTML 폼 데이터를 온전히 지원하기 위해 `FormParser`와 `MultiPartParser`를 같이 사용한다.

**.media_type**: `multipart/form-data`

## FileUploadParser
원시 파일 업로드 컨텐츠를 파싱한다. `request.data` 속성은 업로드된 파일을 포함하는 하나의 키 `file`를 가지는 딕셔너리이다.

만약 `FileUploadParser`와 같이 사용되는 뷰가 `filename` URL 키워드 인자로 호출된다면 그 인자가 파일 이름으로 사용된다.

만약 `filename` URL 키워드 인자 없이 호출된다면, 클라이언트는 HTTP 헤더의 `Content-Disposition` 안에 파일 이름을 설정해야 한다. 예를 들면, `Content-Disposition: attachment; filename=upload.jpg`처럼.

**.media_type**: `*/*`

- Notes:<br>
  -  `FileUploadParser`는 파일을 원시 데이터 요청으로 업로드할 수 있는 네이티브 클라이언트에서 사용하기 위한 것이다. 웹 기반 업로드 또는 multipart 업로드 지원이 가능한 네이티브 클라이언트에서는 `MultiPartParser`를 사용하는 것이 좋다.
  - 이 parser의 `media_type`은 어떤 컨텐츠 타입에도 매치가 되기 때문에 `FileUploadParser`는 하나의 API 뷰에서 사용되는 유일한 parser여야 한다.
  - `FileUploadParser`는 Django의 표준 `FILE_UPLOAD_HANDLERS` 설정과 `request.upload_handlers` 속성을 존중한다. 자세한 사항은 [Django 문서](https://docs.djangoproject.com/en/stable/topics/http/file-uploads/#upload-handlers)에서 확인할 수 있다.

기본 사용 예시:
```python
# views.py
class FileUploadView(views.APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        # ...
        # do some stuff with uploaded file
        # ...
        return Response(status=204)

# urls.py
urlpatterns = [
    # ...
    re_path(r'^upload/(?P<filename>[^/]+)$^', FileUploadView.as_view()),
]
```

# Custom parsers
사용자 정의 parser를 구현하려면 `BaseParser`를 override하고 `.media_type` 속성을 설정해야하며 `.parse(self, stream, media_type, parser_context)` 메서드를 구현해야 한다.

메서드는 `request.data` 속성을 채우기 위한 데이터를 반환해야 한다.

`.parse()`로 전달되는 인자는 다음과 같다.

### Stream
요창의 바디를 나타내는 stream과 유사한 객체

### media_type
선택인자. 주어진다면 들어오는 요청 컨텐츠의 미디어 유형이 된다.

요청의 `Content-Type:` 헤더에 따라 정해지는데 렌더러의 `media_type` 속성보다 더 구체적일 수 있으며 미디어 유형 인자를 포함할 수 있다. 예를 들면 `"text/plain; charset=utf-8"`.

### parser_context
선택인자. 주어진다면 요청 컨텐츠를 parse하는데 요구되는 추가적인 컨텍스트를 포함하는 딕셔너리가 된다.

기본값으로 다름의 키를 포함한다: `view`, `request`, `args`, `kwargs`

## Example
다음은 요청의 바디를 나타내는 문자열로 `request.data` 속성을 채우는 plaintext parser의 예시이다.

```python
class PlainTextParser(BaseParser):
    """
    Plain text parser.
    """
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Simply return a string representing the body of the request.
        """
        return stream.read()
```

# Thrid party packages
다음의 서드파티 패키지 또한 사용할 수 있다.

## YAML
[REST framework YAML](https://jpadilla.github.io/django-rest-framework-yaml/)은 [YAML](http://www.yaml.org/) parsing과 렌더링 지원을 제공한다. 이전에는 REST framework 패키지에 직접 포함되어 있었지만 지금은 서드파티 패키지로 지원된다.

### Installation & configuration
pip을 이용해 설치한다.
```bash
$ pip install djangorestframework-yaml
```

REST framework 설정을 변경한다.
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
[REST Framework XML](https://jpadilla.github.io/django-rest-framework-xml/)은 간단한 약식 XML 포맷을 제공한다. 이전에는 REST framework에 직접 포함되어 있었으나 지금은 서드파티 패키지로 지원된다.

### Installation & configuration
pip을 이용해 설치한다.
```bash
$ pip install djangorestframework-xml
```

REST framework 설정을 변경한다.
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

## MessagePack
[MessagePack](https://github.com/juanriaza/django-rest-framework-msgpack)은 빠르고 효율적인 바이너리 serialization 포맷이다. [Juan Riaza](https://github.com/juanriaza)가 REST framework에 MessagePack 렌더러와 parser 지원을 제공하는 [djangorestframework-msgpack](https://github.com/juanriaza/django-rest-framework-msgpack) 패키지를 관리한다.

## CamelCase JSON
[djangorestframework-camel-case](https://github.com/vbabiy/djangorestframework-camel-case)는 REST framework를 위한 카멜케이스 JSON 렌더러와 parser를 제공한다. 이는 serializer가 파이썬식 필드 명을 사용하게 하지만 API에서는 자바스크립트식 카멜 케이스 필드 명으로 보이게 한다. [Vitaly Babiy](https://github.com/vbabiy)가 관리한다.