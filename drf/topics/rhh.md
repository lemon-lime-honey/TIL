# [REST, Hypermedia & HATEOAS](https://www.django-rest-framework.org/topics/rest-hypermedia-hateoas/)

```
당신은 계속 그 단어, "REST"를 사용합니다. 나는 그것이 당신이 생각하는 의미라고 생각하지 않습니다.
- Mike Amundsen, REST fest 2012 keynote.
```

먼저, 면책 조항이다. "Django REST framework"라는 이름은 2011년 초반에 정해졌으며, 개발자들이 쉽게 이 프로젝트를 찾게 하기 위해 선택되었다. 문서를 통틀어 좀 더 단순하고 기술적으로 올바른 "웹 API" 용어를 사용하기 위해 노력하고 있다.

만약 당신이 하이퍼미디어 API 설계에 진지하게 생각한다면 설계 선택에 관해 알려주는데 도움을 주는 자료들을 이 문서 밖에서 살펴봐야 한다.

다음은 "필수 탐독" 구분에 들어간다.

- Roy Fielding의 글 - [Architectural Styles and the Design of Network-based Software Architectures](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm)
- Roy Fielding의 블로그 게시글 - [REST APIs must be hypertext-driven](https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven)
- Leonard Richardson과 Mike Amundsen의 [RESTful Web APIs](http://restfulwebapis.org/)
- Mike Amundsen의 [Building Hypermedia APIs with HTML5 Node](https://www.amazon.com/Building-Hypermedia-APIs-HTML5-Node/dp/1449306578)
- Steve Klabnik의 [Designing Hypermedia APIs](http://designinghypermediaapis.com/)
- [Richardson Maturity Model](https://martinfowler.com/articles/richardsonMaturityModel.html)

더 많고 자세한 배경 지식을 얻고 싶다면 Klabnik의 [Hypermedia API reading list](http://blog.steveklabnik.com/posts/2012-02-27-hypermedia-api-reading-list)를 확인한다.

## Building Hypermedia APIs with REST framework
REST framework는 독립적인 웹 API 툴킷이다. 이는 잘 연결이 된 API를 구축하는데 도움이 되며 적절한 미디어 종류를 설계하기 쉽게 하지만 어떤 특정 설계 스타일을 엄격하게 적용하지는 않는다.

## What REST framework provides.
REST framework가 하이퍼미디어 API를 구축할 수 있게 하는 것은 명백하다. 제공하는 탐색 가능한 API는 웹의 하이퍼미디어 언어인 HTML로 생성된다.

REST framework는 적절한 미디어 유형을 개발하는 것을 쉽게 하는 `serialization`과 `parser`/`renderer` 요소, 잘 연결된 시스템을 개발하기 위한 [하이퍼 링크 관계](../api-guide/serializer_fields.md), [컨텐츠 협상](../api-guide/content_negotiation.md)을 위한 많은 지원 또한 포함한다.

## What REST framework doesn't provide.
REST framework는 [HAL](http://stateless.co/hal_specification.html), [Collection+JSON](http://www.amundsen.com/media-types/collection/), [JSON API](http://jsonapi.org/) 또는 HTML [microformats](http://microformats.org/wiki/Main_Page)와 같은 기계 판독이 가능한 하이퍼미디어 포맷 기본 제공이나 하이퍼미디어 기반의 폼 설명과 의미적으로 라벨링된 하이퍼링크를 포함하는 온전한 HATEOAS 스타일 API를 자동으로 생성하게 하지 않는다.