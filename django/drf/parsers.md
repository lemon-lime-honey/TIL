# [Parsers](https://www.django-rest-framework.org/api-guide/parsers/)
```
웹 서비스와 상호작용 하는 기기는 데이터를 송신할 때 form-encoded보다 좀 더 구조화된 포맷을 사용하는 경향이 있는데,
이는 단순한 폼보다 더 복잡한 데이터를 송신하기 때문이다.
- Malcom Tredinnick, Django developers group
```

REST framework는 다양한 미디어 유형의 요청을 허용할 수 있게 해주는 여러 빌트인 Parser 클래스를 제공한다. 또한 API가 허용할 미디어 유형을 디자인하기 위한 유연함을 제공하는 사용자 정의 parser를 정의할 수 있게 한다.