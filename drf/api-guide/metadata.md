# [Metadata](https://www.django-rest-framework.org/api-guide/metadata/)
```
`OPTIONS` 메서드는 클라이언트가 리소스 동작을 수반하거나 리소스 회수를 시작하지 않고 리소스 또는 서버 용량과 관련된 옵션 그리고/또는 요구사항을 결정하게 한다.
- RFC7231, Section 4.3.7
```

REST framework는 API가 어떻게 `OPTIONS` 요청에 응답해야할지 결정하는 구성 가능한 매커니즘을 가지고 있다. 이는 API 스키마 또는 다른 리소스 정보를 반환할 수 있게 한다.

현재 HTTP `OPTIONS` 요청에 반환되어야 할 응답의 정확한 형식에 관한 널리 적용된 규칙이 없기 때문에 유용한 정보를 반환하는 애드혹 형식을 제공한다.

다음은 기본적으로 반환되는 정보를 보여주는 예시 응답이다.

```
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json

{
  "name": "To Do List",
  "description": "List existing 'To Do' items, or create a new item.",
  "renders": [
    "application/json",
    "text/html"
  ],
  "parses" [
    "application/json",
    "application/x-www-form-urlencoded",
    "multipart/form-data"
  ],
  "actions": {
    "POST": {
      "note": {
        "type": "string",
        "required": false,
        "read_only": false,
        "label": "title",
        "max_length": 100
      }
    }
  }
}
```

## Setting the metadatea scheme
`'DEFAULT_METADATA_CLASS'` 설정 키를 사용해 전역적으로 메타데이터 클래스를 설정할 수 있다:

```python
REST_FRAMEWORK = {
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata'
}
```

뷰에서 개별적으로 메타데이터 클래스를 설정할 수도 있다.

```python
class APIRoot(APIView):
    metadata_class = APIRootMetadata


    def get(self, request, format=None):
        return Response({
            ...
        })
```

REST framework 패키지는 `SimpleMetadata`라는 이름의 단일 메타데이터 클래스 구현만을 가진다. 다른 형식을 사용하려면 사용자 정의 메타데이터 클래스를 구현해야 한다.

## Creating schema endpoints
정규 `GET` 요청에 접근하는 스키마 엔드포인트를 생성하기 위한 구체적인 요구사항이 있다면 메타데이터 API 재사용을 고려한다.

예를 들어, 다음의 추가 경로는 연결 가능한 스키마 엔드포인트를 제공하기 위해 viewset에서 사용될 수 있다.

```python
@action(methods=['GET'], detail=False)
def api_schema(self, request):
    meta = self.metadata_class()
    data = meta.determine_metadata(request, self)
    return Response(data)
```

`OPTIONS` 응답이 [캐시 불가능](https://www.mnot.net/blog/2012/10/29/NO_OPTIONS)하다는 점을 포함하여 이 접근을 선택할 여러 이유가 있다.

# Custom metadata classes
사용자 정의 메타데이터 클래스를 제공하려면 `BaseMetadata`를 override하고 `determine_metadata(self, request, view)` 메서드를 구현해야 한다.

유용한 작업으로는 [JSON schema](https://json-schema.org/)와 같은 형식을 사용하여 스키마 정보를 반환하거나 관리자에게 디버그 정보를 반환하는 것 등이 있다.

## Example
다음의 클래스는 `OPTIONS` 요청에 대해 반환되는 정보를 제한하기 위해 사용될 수 있다.

```python
class MinimalMetadata(BaseMetadata):
    """
    Don't include field and other information for `OPTIONS` requests.
    Just return the name and description.
    """
    def determine_metadata(self, request, view):
        return {
            'name': view.get_view_name(),
            'description': view.get_view_description()
        }
```

그 다음 이 사용자 정의 클래스를 사용하기 위해 설정을 구성한다.

```python
REST_FRAMEWORK = {
    'DEFAULT_METADATA_CLASS': 'myproject.apps.core.MinimalMetadata'
}
```

# Third party packages
다음의 서드 파티 패키지는 추가적인 메타데이터 구현을 제공한다.

## DRF-schema-adapter
[drf-schema-adapter](https://github.com/drf-forms/drf-schema-adapter)는 프론트엔드 프레임워크와 라이브러리에 스키마 정보를 더 쉽게 제공할 수 있게 해주는 도구 모음이다. 여러 라이브러리가 읽을 수 있는 스키마 정보, [json-schema](https://json-schema.org/)를 생성하기에 적합한 두 메타데이터 클래스와 여러 어댑터 뿐만 아니라 메타데이터 mixin을 제공한다

특정 프론트엔드와 함께 사용할 수 있는 어댑터를 직접 작성할 수도 있다. 또한 이러한 스키마 정보를 json 파일로 내보낼 수 있는 exporter를 제공한다.