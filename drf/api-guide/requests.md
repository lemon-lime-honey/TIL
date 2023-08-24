# [Requests](https://www.django-rest-framework.org/api-guide/requests/)
```
만약 REST 기반 웹 서비스에 관한 일을 하고 있다면...request.POST는 무시하는게 좋습니다.
- Malcom Tredinnick, Django 개발자 모임
```

REST framework의 `Request` 클래스는 기본 `HttpRequest`를 확장하여 REST framework의 유연한 요청 파싱과 요청 인증을 위한 지원을 추가한다.

---

# Request Parsing
REST framework의 요청 객체는 일반적으로 폼 데이터를 다루는 것과 같은 방식으로 요청을 JSON 데이터나 다른 미디어 유형으로 다룰 수 있게 해주는 유연한 요청 파싱을 제공한다.

## .data
`request.data`는 요청 바디의 파싱된 컨텐츠을 반환한다. 이는 다음의 특징을 제외하면 표준 `request.POST`와 `request.FILES` 속성과 유사하다:

- *파일*과 *파일이 아닌* 입력을 포함하여 모든 파싱된 컨텐츠을 포함한다.
- `POST` 이외의 HTTP 메서드의 컨텐츠 파싱을 지원한다. 즉, `PUT`과 `PATCH` 요청의 컨텐츠에 접근할 수 있게 된다.
- 단순하게 폼 데이터를 지원하는 것 대신, REST framework의 유연한 요청 파싱을 지원한다. 예를 들어 [폼 데이터](parsers.md/#formparser) 입력을 다루는 것과 유사하게 [JSON 데이터](parsers.md/#jsonparser)를 다룰 수 있게 된다.

자세한 사항은 [파서 문서](parsers.md)에서 확인할 수 있다.

## .query_params
`request.query_params`는 `request.GET`을 더 정확히 명명한 것이다.

코드 내부의 투명성을 위해 Django의 표준 `request.GET` 대신 `request.query_params`를 사용하는 것을 권장한다. 이렇게 하면 코드베이스를 더 정확하고 명백하게 유지할 수 있다. `GET` 요청 만이 아닌 모든 HTTP 메서드 타입이 쿼리 파라미터를 포함할 수 있게 된다.

## .parsers
`APIView` 클래스 혹은 `@api_view` 데코레이터는 뷰에 설정된 `parser_classes` 또는 `DEFAULT_PARSER_CLASSES` 설정에 기반하여 이 속성이 자동으로 `Parser` 인스턴스 리스트로 설정되게 한다.

보통은 이 속성에 접근할 필요가 없다.

---

**Note**<br>
만약 클라이언트가 비정상적인 컨텐츠를 발신한다면, `request.data`에 접근하는 것이 `ParseError`를 발생시킬 수 있다. 기본적으로 REST framework의 `APIView` 클래스 혹은 `@api_view` 데코레이터가 오류를 감지해 `400 Bad Request` 응답을 반환할 것이다.

만약 클라이언트가 파싱될 수 없는 타입의 컨텐츠를 가진 요청을 발신한다면, `UnsupportedMediaType` 예외가 발생하는데, 이는 기본으로 감지되는 것이며 `415 Unsupported Media Type` 응답을 반환한다.

---

# Content negotiation
요청은 컨텐츠 협상 단계의 결과를 결정하게 하는 몇몇 속성을 노출한다. 이는 미디어 타입에 따라 서로 다른 직렬화 스킴을 선택하는 등의 동작을 구현할 수 있게 한다.

## .accepted_renderer
컨텐츠 협상 단계에서 선택된 렌더러 인스턴스

## .accepted_media_type
컨텐츠 협상 단계에서 수용된 미디어 타입을 나타내는 문자열

---

# Authentication
REST framework는 다음을 할 수 있게 하는 유연한 요청별 인증을 제공한다:

- API의 서로 다른 부분에 다른 인증 정책을 적용한다.
- 복수의 인증 정책 사용을 지원한다.
- 들어오는 요청에 관한 사용자와 토큰 정보를 둘 다 제공한다.

## .user
`request.user`의 동작은 사용되는 인증 정책에 따르지만 대체로 `django.contrib.auth.models.User`의 인스턴스를 반환한다.

만약 요청이 인증되지 않았다면 `request.user`의 기본값은 `django.contrib.auth.models.AnonymousUser`의 인스턴스이다.

자세한 사항은 [인증 문서](authentication.md)에서 확인할 수 있다.

## .auth
`request.auth`는 추가적인 인증 컨텍스트를 반환한다. `request.auth`의 정확한 동작은 사용되는 인증 정책에 따라 다르지만 보통은 요청이 인증된 토큰의 인스턴스이다.

만약 요청이 인증되지 않았거나 추가적인 컨텍스트가 없다면 `request.auth`의 기본값은 `None`이다.

자세한 사항은 [인증 문서](authentication.md)에서 확인할 수 있다.

## .authenticators
`APIView` 클래스 또는 `@api_view` 데코레이터는 뷰에서 설정된 `authentication_classes` 또는 `DEFAULT_AUTHENTICATION` 설정에 기반하여 속성이 자동적으로 `Authentication` 인스턴스 리스트로 설정되게 한다.

보통은 이 속성에 접근할 필요가 없다.

---

**Note**:<br>
`.user` 또는 `.auth` 속성을 호출할 때 `WrappedAttributeError`가 발생할 수 있다. 이러한 에러는 인증자에서 표준 `AttributeError`로 발생하지만, 외부에서의 속성 접근에 의해 억제되지 않도록 다른 예외 유형으로 다시 발생시켜야 한다. 파이썬은 `AttributeError`가 인증자에서 기인한다는 것을 인식하지 못하는 대신 응답 객체가 `.user` 또는 `.auth` 속성을 가지지 않은 것으로 가정한다. 인증자가 수정되어야 한다.

---

# Browser enhancements
REST framework는 브라우저 기반 `PUT`, `PATCH`, `DELETE` 폼과 같은 몇 가지 브라우저 향상을 지원한다.

## .method
`request.method`는 **대문자로 변환**된 요청의 HTTP 메서드의 문자열 표현을 반환한다.

브라우저 기반 `PUT`, `PATCH`, `DELETE` 폼은 투명하게 지원된다.

자세한 사항은 [브라우저 향상 문서](../topics/enhancements.md)에서 확인할 수 있다.

## .content_type
`request.content_type`는 HTTP 요청의 바디의 미디어 타입을 나타내는 문자열 객체, 미디어 타입이 제공되지 않은 경우 빈 문자열을 반환한다.

보통은 REST framework의 기본 요청 파싱 동작에 의존하기 때문에 직접적으로 요청의 컨텐츠 타입에 접근할 필요가 없다.

만약 요청의 컨텐츠 타입에 접근할 필요가 있다면 `request.META.get('HTTP_CONTENT_TYPE')`을 사용하는 것보다 브라우저 기반의 폼이 아닌 컨텐츠를 투명하게 지원하는 `.content_type` 속성을 사용하는 것이 좋다.

자세한 사항은 [브라우저 향상 문서](../topics/enhancements.md)에서 확인할 수 있다.

## .stream
`request.stream`은 요청 바디의 컨텐츠를 나타내는 스트림을 반환한다.

보통은 REST framework의 기본 요청 파싱 동작에 의존하므로 요청의 컨텐츠에 직접 접근할 필요가 없다.

# Standard HttpRequest attributes
REST framework의 `Request`가 Django의 `HTTPRequest`를 확장하므로 모든 다른 표준 속성과 메서드 또한 사용 가능하다. 예를 들어 `request.META`와 `request.session` 딕셔너리를 정상적으로 사용할 수 있다.

구현 상의 이유로 `Request` 클래스는 `HttpRequest` 클래스를 상속하지는 않지만 대신 구성을 사용하여 클래스를 확장한다는 점에 유의한다.