# [The Browsable API](https://www.django-rest-framework.org/topics/browsable-api/)
```
우리가 무얼 하고 있는지 생각하는 습관을 길러야 한다는 것은... 매우 잘못된 진리이다.
정확히 그 반대를 해야 한다.
문명은 우리가 생각하지 않고 수행할 수 있는 중요한 작업의 수를 확장하는 것으로 발전한다.
- Alfred North Whitehead, An Introduction to Mathematics (1911)
```

API는 Application *Programming* Interface의 줄임말이지만, 인간 또한 API를 읽을 수 있어야 한다. 누군가는 프로그래밍을 해야 하니까 말이다. Django REST Framework는 `HTML` 포맷이 요청되었을 때 각 리소스에 대한 인간 친화적인 HTML 출력이 생성되는 것을 지원한다. 이 페이지들은 `POST`, `PUT`, `DELETE`를 사용해 리소스에 데이터를 제출하기 위한 폼 뿐만이 아니라 리소스를 쉽게 탐색하게 해준다.

## URLs
리소스 출력에 정규화된 URL을 포함한다면 사람이 쉽게 탐색할 수 있게 하기 위해 'url화'되며 클릭할 수 있게 된다. `rest_framework` 패키지는 이 목적을 위한 `reverse` 헬퍼를 포함한다.

## Formats
기본적으로 API는 브라우저가 HTML인 경우 헤더가 명시하는 포맷을 반환한다. 포맷은 요청에서 `?format=`을 사용하여 명시되며, 그렇게 하면 URL에 `?format=json`을 추가하여 브라우저에서 가공되지 않은 JSON 응답을 볼 수 있다. [Firefox](https://addons.mozilla.org/en-US/firefox/addon/jsonview/)와 [Chrome](https://chrome.google.com/webstore/detail/chklaanhfefbnpoihckbnefhakgolnmc)에는 JSON을 볼 수 있는 유용한 확장 기능이 있다.