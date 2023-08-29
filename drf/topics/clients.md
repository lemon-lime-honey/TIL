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

# Python client library
`coreapi` 파이썬 패키지는 지원되는 스키마 포맷을 노출하는 모든 API와 programmatically하게 상호작용할 수 있게 한다.

## Getting started
시작하기 전에 `pip`을 사용해 `coreapi` 패키지를 설치한다.

```bash
$ pip install coreapi
```

API 작업을 시작하려면 먼저 `Client` 인스턴스가 필요하다. 클라이언트는 API와 상호할 때 어떤 코덱과 전송이 지원되는지에 관한 설정을 가지고 있어 더 발전된 유형의 동작을 제공할 수 있게 한다.

```python
import coreapi
client = coreapi.Client()
```

일단 `Client` 인스턴스를 가지게 되면 네트워크에서 API 스키마를 불러올 수 있다.

```python
schema = client.get('https://api.example.org/')
```

이 호출에서 반환되는 객체는 API 스키마를 나타내는 `Document` 인스턴스가 된다.

## Authentication
클라이언트를 인스턴스화할 때 인증 자격을 제공할 수 있다.

### Token authentication
`TokenAuthentication` 클래스는 Oauth와 JWT 스킴 뿐만이 아니라 REST framework의 빌트인 `TokenAuthentication`을 지원하기 위해 사용될 수 있다.

```python
auth = coreapi.auth.TokenAuthentication(
    scheme='JWT',
    token='<token>'
)
client = coreapi.Client(auth=auth)
```

TokenAuthentication을 사용할 때 CoreAPI 클라이언트를 사용하는 로그인 플로우를 구현할 수도 있다.

이를 위해 제안되는 패턴으로는 초기에 "토큰 가져오기" 엔드포인트에 인증되지 않은 클라이언트 요청을 생성하는 것이 있다.

예를 들어, "Django REST framework JWT" 패키지를 사용하는 경우:

```python
client = coreapi.Client()
schema = client.get('https://api.example.org/')

action = ['api-token-auth', 'create']
params = {"username": "example", "password": "secret"}
result = client.action(schema, action, params)

auth = coreapi.auth.TokenAuthentication(
    scheme='JWT',
    token=result['token']
)
client = coreapi.Client(auth=auth)
```

### Basic authentication
`BasicAuthentication` 클래스는 HTTP 기본 인증을 지원하기 위해 사용될 수 있다.

```python
auth = coreapi.auth.BasicAuthentication(
    username='<username>',
    password='<password>'
)
client = coreapi.Client(auth=auth)
```

## Interacting
클라이언트가 있고, 스키마 `Document`를 불러왔으므로 API와의 상호작용을 시작할 수 있다:

```python
users = client.action(schema, ['users', 'list'])
```

어떤 엔드포인트는 선택 또는 필수 사항이 될 수 있는 명명된 파라미터를 가질 수 있다:

```python
new_user = client.action(schema, ['users', 'create'], params={"username": "max"})
```

## Codecs
코덱은 문서 인코딩과 디코딩을 수행한다.

디코딩 프로세스는 API 스키마 정의의 bytestring을 가져와 인터페이스를 나타내는 Core API 문서를 반환하는데 사용된다.

코덱은 `'application/coreapi+json'`과 같이 특정 미디어 타입과 연관되어야 한다.

이 미디어 타입은 응답에서 어떤 종류의 데이터가 반환되는지를 지시하기 위해 응답의 `Content-Type` 헤더의 서버에서 사용한다.

### Configuring codecs
사용할 수 있는 코덱은 클라이언트를 인스턴스화할 때 구성될 수 있다. 클라이언트의 맥락에서 코덱은 응답을 *디코딩*하기 위해서만 사용되기 때문에 여기서 사용되는 키워드 인자는 `decoders`이다.

다음의 예시에서는 클라이언트가 오직 `Core JSON`과 `JSON` 응답만을 받도록 설정한다. 이는 Core JSON 스키마를 받고 디코딩할 수 있게 하며, 그 다음에 API에 대해 생성된 JSON 응답을 받을 수 있게 한다.

```python
from coreapi import codecs, Client

decoders = [codecs.CoreJSONCodec(), codecs.JSONCodec()]
client = Client(decoders=decoders)
```

### Loading and saving schemas
존재하는 스키마 정의를 불러오고 결과 `Document`를 반환하기 위해 직접 코덱을 사용할 수 있다.

```python
input_file = open('my-api-schema.json', 'rb')
schema_definition = input_file.read()
codec = codecs.CoreJSONCodec()
schema = codec.load(schema_definition)
```

`Document` 인스턴스가 주어졌을 때  스키마 정의를 생성하기 위해 직접 코덱을 사용할 수도 있다:

```python
schema_definition = codec.dump(schema)
output_file = open('my-api-schema.json', 'rb')
output_file.write(schema_definition)
```

## Transports
전송은 네트워크 요청 생성을 수행한다. 클라이언트가 설치한 전송 집합은 어떤 네트워크 프로토콜이 지원 가능한지를 결정한다.

현재 `coreapi` 라이브러리는 오직 HTTP/HTTPS 전송 만을 포함하지만 다른 프로토콜 또한 지원할 수 있다.

### Configuring transports
클라이언트가 인스턴스화될 때 사용되는 전송을 설정하여 네트워크 계층의 동작을 커스터마이즈 할 수 있다.

```python
import requests
from coreapi import transports, Client

credentials = {'api.example.org': 'Token 3bd44a009d16ff'}
transports = transports.HTTPTransport(credentials=credentials)
client = Client(transports=transports)
```

기본 `requests.Session` 인스턴스를 수정하여 나가는 요청을 수정하는 [전송 어댑터를 연결](http://docs.python-requests.org/en/master/user/advanced/#transport-adapters)하는 것과 같은 더 복잡한 커스터마이즈 또한 수행할 수 있다.