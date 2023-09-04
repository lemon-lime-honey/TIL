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

## Customizing
브라우징 가능한 API는 [트위터의 Bootstrap](https://getbootstrap.com/)(버전 3.3.5)로 구축되어 외관과 느낌을 커스터마이즈하기 쉽다.

기본 스타일을 변경하려면 `rest_framework/base.html`를 확장하는 `rest_framework/api.html` 템플릿을 생성한다. 예를 들어:

**templates/rest_framework/api.html**
```html
{% extends "rest_framework/base.html" %}

... # Override blocks with required customizations
```

### Overriding the default theme
기본 테마를 대체하려면 `api.html`에 `bootstrap_theme` 블록을 추가하고 원하는 Bootstrap 테마 css 파일의 `link`를 넣는다. 이는 포함된 테마를 완전히 대체한다.

```html
{% block bootstrap_theme %}
  <link rel="stylesheet" href="/path/to/my/bootstrap.css" type="text/css">
{% endblock %}
```

[Bootswatch](https://bootswatch.com/)에서 사용 가능한 적절한 대체 테마를 찾을 수 있다. Bootswatch 테마를 사용하려면 테마의 `bootstrap.min.css` 파일을 다운로드 받고, 프로젝트에 추가한 후 위와 같이 기본 테마를 대체한다.

`bootstrap_navbar_variant` 블록을 사용하여, `navbar-inverse`가 기본인 navbar variant를 변경할 수 있다. 비어있는 `{% block bootstrap_navbar_variant %}{% endblock %}`는 원본 Bootstrap navbar 스타일을 사용한다.

전체 예시:
```html
{% extends "rest_framework/base.html" %}

{% block bootstrap_theme %}
  <link rel="stylesheet" href="https://bootswatch.com/flatly/bootstrap.min.css" type="text/css">
{% endblock %}

{% block bootstrap_navbar_variant %}{% endblock %}
```

단순히 기본 Bootstrap 테마를 override하는 것이 아니라 구체적으로 CSS를 변경하고 싶다면 `style` 블록을 override하면 된다.

![Bootswatch 'Cerulean' theme](https://www.django-rest-framework.org/img/cerulean.png)

*Bootswatch 'Cerulean' 테마*

![Bootswatch 'Slate' theme](https://www.django-rest-framework.org/img/slate.png)

*Bootswatch 'Slate' theme'*