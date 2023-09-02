# [Browser Enhancements](https://www.django-rest-framework.org/topics/browser-enhancements/)
```
오버로드된 POST에는 논란의 여지가 없는 두 용도가 있다.
첫번째는 PUT 또는 DELETE를 지원하지 않는 웹 브라우저와 같은 클라이언트를 위한 HTTP의 똑같은 인터페이스를 시뮬레이션하는 것이다.
- RESTful Web Services, Leonard Richardson & Sam Ruby
```

브라우징 가능한 API를 동작시키기 위해 REST framework가 제공해야할 몇 가지 브라우저 향상 기능이 있다.

버전 3.3.0 이후에는 [ajax-form](https://github.com/tomchristie/ajax-form) 라이브러리를 이용해 자바스크립트로 활성화할 수 있다.

## Browser based PUT, DELETE, etc...
[AJAX 폼 라이브러리](https://github.com/tomchristie/ajax-form)는 HTML 폼에서의 브라우저 기반 `PUT`, `DELETE`와 다른 메서드를 지원한다.

라이브러리를 포함시킨 후, 다음과 같이 `data-method` 속성을 폼에 사용한다:

```html
<form action="/" data-method="PUT">
  <input name='foo' />
  ...
</form>
```

3.3.0 이전에는 이 지원이 자바스크립트 기반이 아닌 서버 측이었다는 점에 유의한다. ([Ruby on Rails](https://guides.rubyonrails.org/form_helpers.html#how-do-forms-with-put-or-delete-methods-work)에서 사용되는 것과 같은) 메서드 재정의 방식은 요청 파싱에서 발생하는 미묘한 문제로 인해 더 이상 지원되지 않는다.

## Browser based submission of non-form content
JSON 형식과 같은 컨텐츠 타입의 브라우저 기반 제출은 폼 필드를 `data-override='content-type'`과 `data-override='content'` 속성과 함께 사용하는 방식으로 [AJAX 폼 라이브러리](https://github.com/tomchristie/ajax-form)에서 지원된다.

예를 들어:

```html
<form action="/">
  <input data-override='content-type' value='application/json' type='hidden'/>
  <textarea data-override='content'>{}</textarea>
  <input type="submit"/>
</form>
```

3.3.0 이전에는 이 지원이 자바스크립트 기반이 아닌 서버 측이었다는 점에 유의한다.

## URL based format suffixes
REST framework는 `?format=json` 형식의 URL 파라미터를 사용할 수 있는데, 이는 어떤 컨텐츠 타입이 뷰에서 반환되어야 하는지를 결정하는 유용하고 쉬운 방법이다.

이 동작은 `URL_FORMAT_OVERRIDE` 설정을 사용해 제어할 수 있다.

## HTTP header based method overriding
3.3.0 버전 이전에 반 확장 헤더 `X-HTTP-Method-Override`가 요청 메서드를 재정의하기 위해 사용되었다. 이 동작은 더 이상 코어에 없지만 필요하다면 미들웨어를 사용해 추가할 수 있다.

예를 들어:

```python
METHOD_OVERRIDE_HEADER = 'HTTP_X_HTTP_METHOD_OVERRIDE'

class MethodOverrideMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    

    def __call__(self, request):
        if request.method == 'POST' and METHOD_OVERRIDE_HEADER in request.META:
            request.method = request.META[METHOD_OVERRIDE_HEADER]
        return self.get_response(request)
```

## URL based accept headers
버전 3.3.0 전까지 REST framework는 `Accept` 헤더를 재정의할 수 있게 해주는 `?accept=application/json` 형식의 URL 파라미터에 대한 빌트인 지원을 포함했다.

컨텐츠 협상 API의 도입으로 이 동작은 더 이상 코어에 포함되지 않지만 필요하다면 사용자 정의 컨텐츠 협상 클래스를 사용해 추가할 수 있다.

예를 들어:

```python
from rest_framework.negotiation import DefaultContentNegotiation


class AcceptQueryParamOverride(DefaultContentNegotiation):
    def get_accept_list(self, request):
        header = request.META.get('HTTP_ACCEPT', '*/*')
        header = request.query_params.get('_accept', header)
        return [token.strip() for token in header.split(',')]
```

## Doesn't HTML5 support PUT and DELETE forms?
지원하지 않는다. 한때 `PUT`과 `DELETE` 폼 지원 의도가 있었으나 이후에 [사양에서 삭제](https://www.w3.org/TR/html5-diff/#changes-2010-06-24)되었다. 폼 인코딩된 데이터 이외의 컨텐츠 타입을 어떻게 지원하는 것 뿐만 아니라 `PUT`과 `DELETE`에 대한 지원을 추가하는 것에 대한 [진행 중인 논의](http://amundsen.com/examples/put-delete-forms/)가 남아 있다.