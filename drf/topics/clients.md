# [API Clients](https://www.django-rest-framework.org/topics/api-clients/)
API 클라이언트는 어떻게 네트워크 요청이 생성되며 어떻게 응답이 디코딩되는지에 대한 기본적인 세부 사항을 처리한다. 개발자가 네트워크 인터페이스로 직접 작업하게 하는 대신 작업하게 될 애플리케이션 인터페이스를 제공한다.

여기에서 설명된 API 클라이언트는 Django REST framework로 구축된 API에 제한되지 않는다. 지원되는 스키마 포맷을 노출하는 모든 API와 함께 사용할 수 있다.

예를 들어, [Heroku 플랫폼 API](https://devcenter.heroku.com/categories/platform-api)는 JSON Hyperschema 포맷의 스키마를 노출한다. 그 결과로 Core API 명령줄 클라이언트와 파이썬 클라이언트 라이브러리를 [Heroku API와 상호작용하기 위해 사용할 수 있다.](https://www.coreapi.org/tools-and-resources/example-services/#heroku-json-hyper-schema).

## Client-side Core API
[Core API](https://www.coreapi.org/)는 API를 설명하기 위해 사용되는 문서 사양이다. REST framework의 [스키마 생성](../api-guide/schema.md)과 같이 서버 측에서 사용하거나, 여기서 설명하는 것처럼 클라이언트 측에서 사용할 수 있다.

클라이언트 측에서 사용되는 경우, Core API는 지원되는 스키마 또는 하이퍼미디어 포맷을 노출하는 모든 API와 상호작용할 수 있는 *동적으로 동작하는 클라이언트 라이브러리*를 허용한다.

동적으로 동작하는 클라이언트를 사용하는 것은 HTTP 요청을 직접 구축하는 API와 상호작용하는 것과 비교했을 때 여러 이점을 가진다.

### More meaningful interaction
API 상호작용이 더 의미있는 방식으로 표현된다. 네트워크 인터페이스 레이어가 아닌 애플리케이션 인터페이스 레이어에서 작업한다.

### Resilience & evolvability
클라이언트는 어느 엔드포인트가 사용 가능한지, 각 특정 엔트포인트에 대해 어떤 파라미터가 존재하는지, HTTP 요청이 어떻게 형성되는지 결정한다.

또한 이를 통해 API의 발전 가능성의 정도를 정할 수 있다. 투명하게 클라이언트가 업그레이드되는 동안 URL은 존재하는 클라이언트를 중단하지 않고 수정될 수 있고, 유선 상에서 더 효율적인 인코딩이 사용될 수 있다.

### Self-descriptive APIs
동적으로 작동되는 클라이언트는 최종 사용자에게 API에 관한 문서를 제공할 수 있다. 이 문서는 사용자가 사용 가능한 엔드포인트와 파라미터를 찾을 수 있게 하며, 사용하는 API에 대해 더 잘 이해할 수 있게 한다.

API 스키마에 기반하여 문서가 작성되므로 언제나 서비스의 가장 최신 배포 버전으로 업데이트 된다.

# Command line client
명령줄 클라이언트는 지원되는 스키마 포맷을 노출하는 모든 API를 조회하고 그와 상호작용할 수 있게 한다.

## Getting started
Core API 명령줄 클라이언트를 설치하려면 `pip`을 사용한다.

명령줄 클라이언트가 파이썬 클라이언트 라이브러리의 별개의 패키지라는 점에 유의한다. `coreapi-cli`를 설치한다.

```bash
$ pip install coreapi-cli
```

API를 조회하고 그와 상호작용하려면 네트워크에서 스키마를 불러와야 한다.

```bash
$ coreapi get http://api.example.org/
<Pastebin API "http://127.0.0.1:8000/">
snippets: {
    create(code, [title], [linenos], [language], [style])
    destroy(pk)
    highlight(pk)
    list([page])
    partial_update(pk, [title], [code], [lineos], [language], [style])
    retrieve(pk)
    update(pk, code, [title], [lineos], [language], [style])
}
users: {
    list([page])
    retrieve(pk)
}
```

이는 스키마를 로드하여 결과 `Document`를 보여준다. 이 `Document`는 API에 대해 작성될 수 있는 사용 가능한 상호작용을 모두 포함한다.

API와 상호작용하려면 `action` 명령을 사용한다. 이 명령은 링크로 인덱싱하기 위해 사용되는 키의 리스트를 요구한다.

```bash
$ coreapi action users list
[
    {
        "url": "http://127.0.0.1:8000/users/2/",
        "id": 2,
        "username": "aziz",
        "snippets": []
    },
    ...
]
```

기본 HTTP 요청과 응답을 조회하려면 `--debug` 플래그를 사용한다.

```bash
$ coreapi action users list --debug
> GET /users/ HTTP/1.1
> Accept: application/vnd.coreapi+json, */*
> Authorization: Basic bWF4Om1heA==
> Host: 127.0.0.1
> User-Agent: coreapi
< 200 OK
< Allow: GET, HEAD, OPTIONS
< Content-Type: application/json
< Date: Thu, 30 Jun 2016 10:51:46 GMT
< Server: WSGIServer/0.1 Python/2.7.10
< Vary: Accept, Cookie
<
< [{"url":"http://127.0.0.1/users/2/","id":2,"username":"aziz","snippets":[]},{"url":"http://127.0.0.1/users/3/","id":3,"username":"amy","snippets":["http://127.0.0.1/snippets/3/"]},{"url":"http://127.0.0.1/users/4/","id":4,"username":"max","snippets":["http://127.0.0.1/snippets/4/","http://127.0.0.1/snippets/5/","http://127.0.0.1/snippets/6/","http://127.0.0.1/snippets/7/"]},{"url":"http://127.0.0.1/users/5/","id":5,"username":"jose","snippets":[]},{"url":"http://127.0.0.1/users/6/","id":6,"username":"admin","snippets":["http://127.0.0.1/snippets/1/","http://127.0.0.1/snippets/2/"]}]

[
    ...
]
```

어떤 동작들은 선택 또는 필수 파라미터를 포함한다.

```bash
$ coreapi action users create --param username=example
```

`--param`을 사용할 때 입력의 타입은 자동으로 결정된다.

파라미터 타입을 더 명백하게 하고 싶다면 모든 null, 숫자, 불리언, 리스트 또는 객체 입력에 대해서는 `--data`, 문자열 입력에 대해서는 `--string`을 사용한다.

```bash
$ coreapi action users edit --string username=lime --date is_admin=true
```