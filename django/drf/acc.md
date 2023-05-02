# [Working with AJAX, CSRF, CORS](https://www.django-rest-framework.org/topics/ajax-csrf-cors/)
```
웹사이트에서 발생할 수 있는 CSRF/XSRF 취약점을 살펴보세요.
이들은 최악의 취약점입니다. 공격자가 악용하기는 매우 쉽지만
소프트웨어 개발자는 적어도 이 취약점에 당하기 전까지는 
직관적으로 이해하기가 쉽지 않습니다.
- Jeff Atwood
```

## Javascript clients
만약 웹 API와 소통할 자바스크립트 클라이언트를 작성 중이라면 클라이언트가 웹사이트의 나머지에서 사용되는 인증 정책과 같은 것을 사용할 수 있는지 고려해야 하며 CSRF 토큰이나 CORS 헤더를 사용할지 정해야 한다.

소통 중인 API와 같은 컨텍스트 내에서 생성된 AJAX 요청은 보통 `SessionAuthentication`을 사용할 것이다. 이는 사용자가 한 번 로그인하면 이후에 생성된 어떤 AJAX 요청도 웹사이트의 나머지에서 사용되는 것과 같은 세션 기반 인증을 사용해 인증이 된다는 것을 의미한다.

통신 중인 API와 다른 사이트에서 생성된 AJAX 요청은 보통 `TokenAuthentication`과 같은 세션을 기반으로 하지 않는 인증 체계를 사용해야 한다.

## CSRF protection
[사이트 간 요청 위조](https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)) 보호는 사용자가 로그아웃을 하지 않고 계속 유효한 세션을 가질 때 발생할 수 있는 특정 종류의 공격에 대해 보호하는 메커니즘이다. 이런 상황에서 악성 사이트는 로그인이 된 세션의 컨텍스트로 타겟 사이트에서 작업을 수행할 수 있다.

이런 공격을 방어하려면 두 가지를 해야한다.

1. `GET`, `HEAD`, `OPTIONS`와 같은 *안전한* HTTP 동작이 어떤 서버단 상태도 바꿀 수 없게 한다.
2. `POST`, `PUT`, `PATCH`, `DELETE`와 같은 *안전하지 않은* HTTP 동작이 언제나 유효한 CSRF 토큰을 필요로 하게 한다.

만약 `SessionAuthentication`을 사용한다면 `POST`, `PUT`, `PATCH`, `DELETE` 동작에는 유효한 CSRF 토큰을 포함시켜야 한다.

AJAX 요청을 생성하려면 [Django 공식 문서에서 설명](https://docs.djangoproject.com/en/stable/ref/csrf/#ajax)하듯이 HTTP 헤더에 CSRF 토큰을 추가해야 한다.

## CORS
[교차 출처 리소스 공유](https://www.w3.org/TR/cors/)는 클라이언트가 다른 도메인에 호스팅된 API와 상호작용할 수 있게 하는 메커니즘이다. CORS는 서버에 브라우저가 교차 도메인 요청을 허용할지와 언제 허용할지를 결정하는 특정 헤더 집합을 요구하는 것으로 동작한다.

REST framework에서 CORS를 다루는 가장 좋은 방법은 middleware에 요구되는 응답 헤더를 추가하는 것이다. 이는 뷰를 변경하지 않고 CORS가 투명하게 지원되게 한다.

[Adam Johnson](https://github.com/adamchainz)이 REST framework API와 같이 잘 동작하는 [django-cors-headers](https://github.com/adamchainz/django-cors-headers) 패키지를 관리한다.