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

## Authentication & headers
요청의 `Authentication:` 헤더를 관리하기 위해 `credentials` 명령어가 사용된다. 추가된 모든 자격은 언제나 특정 도메인에 연결되어 서로 다른 API 사이에 그 자격이 유출되지 않도록 한다.

새 자격을 추가하기 위한 포맷은 다음과 같다:

```bash
$ coreapi credentials add <domain> <credentials string>
```

예시:

```bash
$ coreapi credentials add api.example.org "Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

옵션으로 사용할 수 있는 `--auth` 플래그는 인증의 종류를 특정하여 추가해 인코딩을 처리할 수 있게 한다. 현재 사용 가능한 유일한 옵션은 `"basic"`이다. 예를 들어:

```bash
$ coreapi credentials add api.example.org tomchristie:foobar --auth basic
```

`headers` 명령어를 사용하여 요청 헤더를 구체적으로 추가할 수 있다:

```bash
$ coreapi headers add api.example.org x-api-version 2
```

`coreapi credentials --help` 또는 `coreapi headers --help`를 사용하면 더 많은 정보와 사용 가능한 하위 명령 리스트를 확인할 수 있다.

## Codecs
기본적으로 명령줄 클라이언트는 Core JSON 스키마를 읽기 위한 지원만을 포함하지만 추가적인 코덱을 설치하기 위한 플러그인 시스템 또한 포함하고 있다.

```bash
$ pip install openapi-codec jsonhyperschema-codec hal-codec
$ coreapi codecs show
Codecs
corejson        application/vnd.coreapi+json encoding, decoding
hal             application/hal+json         encoding, decoding
openapi         application/openapi+json     encoding, decoding
jsonhyperschema application/schema+json      decoding
json            application/json             data
text            text/*                       data
```

## Utilities
명령줄 클라이언트는 기억할 수 있는 이름에 API URL을 북마크하는 기능을 가지고 있다. 예를 들어, 다음과 같이 존재하는 API를 북마크할 수 있다:

```bash
$ coreapi bookmarks add accountmanagement
```

API URL이 접근된 기록을 통해 이전 혹은 이후를 탐색하는 기능도 있다.

```bash
$ coreapi history show
$ coreapi history back
```

`coreapi bookmarks --help` 또는 `coreapi history --help`를 사용하면 더 많은 정보와 사용 가능한 하위 명령 리스트를 확인할 수 있다.

## Other commands
현재 `Document`를 표시하려면:

```bash
$ coreapi show
```

네트워크에서 현재 `Documment`를 다시 로드하려면:

```bash
$ coreapi reload
```

디스크에서 스키마 파일을 로드하려면:

```bash
$ coreapi load my-api-schema.json --format corejson
```

콘솔에 주어진 포맷으로 현재 `Document`를 덤프하려면:

```bash
$ coreapi dump --format openapi
```

저장된 모든 기록과 자격, 헤더, 북마크와 함께 현재 `Document`를 삭제하려면:

```bash
$ coreapi clear
```