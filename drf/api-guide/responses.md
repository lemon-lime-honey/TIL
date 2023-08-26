# Responses
```
기본 HttpResponse 객체와는 다르게, TemplateResponse 객체는 응답을 산출하기 위해 뷰에서 제공된 컨텍스트의 특징을 유지한다.
응답의 최종 출력은 이후 응답 프로세스에서 필요하기 전까지 산출되지 않는다.
- Django documentation
```

REST framework는 클라이언트 요청에 따라 여러 종류의 컨텐츠 타입으로 렌더링될 수 있는 컨텐츠를 반환할 수 있도록 하는 `Response` 클래스를 제공하여 HTTP 컨텐츠 협상을 지원한다.

`Response` 클래스는 Django의 `SimpleTemplateResponse`의 서브클래스이다. `Response` 객체는 네이티브 파이썬 원시 타입으로 구성된 데이터로 초기화된다. 그 다음 REST framework는 최종 응답 컨텐츠를 어떻게 렌더링해야할지 정하기 위해 표준 HTTP 콘텐츠 협상을 사용한다.

`Response` 클래스를 사용하기 위한 요구사항은 없으며, 만약 필요하다면 뷰로부터 일반적인 `HttpResponse`나 `StreamingHttpResponse` 객체를 반환할 수도 있다. `Response` 클래스를 사용하면 여러 포맷으로 렌더링 될 수 있으며 컨텐츠 협상이 된 웹 API 응답 반환을 위한 나은 인터페이스를 제공할 수 있다.

어떠한 이유로 REST framework를 깊게 커스터마이즈 하는 것이 아니라면, `Response` 객체를 반환하는 뷰를 위해 `APIView` 클래스나 `@api_view` 함수를 사용해야 한다. 그렇게 하면 뷰가 컨텐츠 협상을 할 수 있으며 뷰로부터 반환되기 전의 응답에 적절한 렌더러를 선택할 수 있다.

## Creating responses
### Response()
**Signature:** `Response(data, status=None, template_name=None, headers=None, content_type=None)`

일반적인 `HttpResponse` 객체와는 달리 `Response` 객체는 렌더링된 컨텐츠로 인스턴스화하지 않는다. 파이썬 원시 타입을 포함할 수 있는 렌더링되지 않은 데이터로 전달한다.

`Response` 클래스에서 사용되는 렌더러는 기본 상태에서는 Django 모델 인스턴스와 같은 복잡한 데이터 유형을 다룰 수 없으므로 `Response` 객체를 생성하기 전에 데이터를 원시 데이터 타입으로 직렬화해야 한다.

데이터 직렬화 또는 사용자 정의 직렬화를 수행하기 위해 REST framework의 `Serializer` 클래스를 사용할 수 있다.

인자:

- `data`: 응답을 위해 직렬화된 데이터
- `status`: 응답을 위한 상태 코드. 기본적으로는 200. [상태 코드](status_codes.md)를 확인한다.
- `template_name`: `HTMLRenderer`가 선택되었을 때 사용하는 템플릿 이름
- `headers`: 응답에서 사용하는 HTTP 헤더의 딕셔너리
- `content_type`: 응답의 컨텐츠 종류. 보통 컨텐츠 협상에 의해 결정되는 렌더러에 의해 자동으로 설정되지만, 컨텐츠 종류를 직접 명시해야하는 경우가 있다.

## Attributes
### .data
응답의 렌더링되지 않은, 직렬화된 데이터

### .status_code
HTTP 응답의 숫자 상태 코드

### .content
응답의 렌더링된 컨텐츠. `.content`가 접근 가능한 상태가 되기 전에 반드시 `.render()` 메서드가 호출되어야 한다.

### .template_name
만약 제공되었다면, `template_name`. `HTMLRenderer` 또는 다른 사용자 전의 템플릿 렌더러가 응답을 위한 렌더러로 선택되었을 때에만 필요하다.

### .accepted_renderer
응답을 렌더링하기 위해 사용될 렌더러 인스턴스.

응답이 뷰에서 반환되기 직전에 `APIView` 또는 `@api_view`에 의해 자동으로 설정된다.

### .accepted_media_type
콘텐츠 협상 단계에서 선택된 미디어 유형

응답이 뷰에서 반환되기 직전에 `APIView` 또는 `@api_view`에 의해 자동으로 설정된다.

### .renderer_context
렌더러의 `.render()` 메서드로 전달될 추가 컨텍스트 정보의 딕셔너리

응답이 뷰에서 반환되기 직전에 `APIView` 또는 `@api_view`에 의해 자동으로 설정된다.

## Standard HttpResponse attributes
`Response` 클래스는 `SimpleTemplateResponse`를 확장하며, 모든 일반적인 속성과 메서드 또한 응답에서 사용할 수 있다. 예를 들어 표준적인 방법으로 응답에 대한 헤더를 설정할 수 있다.

```python
response = Response()
response['Cache-Control'] = 'no-cache'
```

### .render()
**Signature:** `.render()`

다른 `TemplateResponse`처럼 이 메서드는 응답의 직렬화된 데이터를 최종 응답 컨텐츠로 렌더링할 때 호출된다. `.render()`가 호출되면 응답 컨텐츠는 `accepted_renderer` 인스턴스에서 `.render(data, accepted_media_type, renderer_context())` 메서드를 호출한 결과로 설정된다.

Django의 표준 응답 사이클에 의해 다루어지기 때문에 보통은 `.render()`를 직접 호출하지 않아도 된다.