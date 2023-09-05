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

### Blocks
`api.html`에서 사용할 수 있는 브라우징 가능한 API 베이스 템플릿에서 유효한 블록

- `body`: html `<body>` 전체
- `bodyclass`: 기본적으로 비어있는 `<body>`의 클래스 속성
- `bootstrap_theme`: Bootstrap 테마를 위한 CSS
- `bootstrap_navbar_variant`: navbar를 위한 CSS 클래스
- `branding`: navbar의 브랜딩 섹션. [Bootstrap 구성요소](https://getbootstrap.com/2.3.2/components.html#navbar)를 확인한다.
- `breadcrumbs`: 사용자가 상위 리소스로 갈 수 있도록 리소스 중첩을 보여주는 링크. 두는 것을 
권장하지만 breadcrumbs 블록을 사용해 override할 수 있다.
- `script`: 페이지를 위한 JavaScript 파일
- `style`: 페이지를 위한 CSS 스타일시트
- `title`: 페이지의 제목
- `userlinks`: 헤더 오른쪽에 위치한 기본적으로 로그인/로그아웃 링크를 포함하는 링크 리스트. 링크를 대체하는 대신 추가하려면 인증 링크를 보존하기 위해 `{{ block.super }}`를 사용한다.

#### Components
모든 표준 [Bootstrap 구성요소](https://getbootstrap.com/2.3.2/components.html)를 사용할 수 있다.

#### Tooltips
브라우징 가능한 API는 Bootstrap 툴팁 구성요소를 사용한다. `js-tooltip` 클래스와 `title` 속성을 가진 모든 요소는 타이틀 컨텐츠가 툴팁을 표시하는 hover 이벤트를 가진다.

### Login Template
브랜딩을 추가하고 로그인 템플릿의 외관과 느낌을 변경하고 싶다면 `login.html`이라는 템플릿을 생성하고 프로젝트에 추가한다: 예) `templates/rest_framework/login.html`. 이 템플릿은 `rest_framework/login_base.html`을 확장하여야 한다.

브랜딩 블록을 포함시켜 사이트 이름이나 브랜딩을 추가할 수 있다.

```html
{% extends "rest_framework/login_base.html" %}

{% block branding %}
  <h3 style="margin: 0 0 20px;">My Site Name</h3>
{% endblock %}
```

`api.html`의 경우와 유사하게 `bootstrap_theme` 또는 `style` 블록을 추가하여 스타일을 변경할 수 있다.

### Advanced Customization
#### Context
템플릿에서 사용 가능한 컨텍스트:

- `allowed_methods`: 리소스에 의해 허용되는 메서드 리스트
- `api_settings`: API 설정
- `available_formats`: 리소스에 의해 허용되는 포맷 리스트
- `breadcrumblist`: 중첩된 리소스의 연쇄적인 링크 리스트
- `content`: API 응답의 내용
- `description`: 리소스의 문서 문자열에서 생성된 설명
- `name`: 리소스의 이름
- `post_form`: (허용된다면) POST 폼에서 사용하는 폼 인스턴스
- `put_form`: (허용된다면) PUT 폼에서 사용하는 폼 인스턴스
- `display_edit_forms`: POST, PUT, PATCH 폼이 표시될지 여부를 가리키는 불리언
- `request`: 요청 객체
- `response`: 응답 객체
- `version`: Django REST Framework 버전
- `view`: 요청을 다루는 뷰
- `FORMAT_PARAM`: 포맷 재정의를 수락하는 뷰
- `METHOD_PARAM`: 메서드 재정의를 수락하는 뷰

템플릿에 전달되는 컨텍스트를 수정하려면 `BrowsableAPIRenderer.get_context()`를 재정의한다.

#### Not using base.html
Bootstrap 기반이 아니거나 사이트의 나머지 부분과 더 긴밀하게 통합된 경우와 같은 심화된 수정을 하려면 `api.html`이 `base.html`을 확장하지 않게 하면 된다. 그러면 페이지 컨텐츠와 성능이 온전히 작성자에 달린다.

#### Handling `ChoiceField` with large numbers of items.
관계 또는 `ChoiceField`가 너무 많은 항목을 가지고 있을 때, 모든 옵션을 포함하는 위젯을 렌더링하면 매우 느려질 수 있고 브라우징 가능한 API 렌더링이 형편없이 동작하는 원인이 된다.

이 경우 사용할 수 있는 가장 쉬운 방법은 선택 입력을 표준 텍스트 입력으로 대체하는 것이다. 예를 들어:

```python
author = serializers.HyperlinkedRelatedField(
    queryset=User.objects.all(),
    style={'base_template': 'input.html'}
)
```

#### Autocomplete
더 복잡한 다른 방법으로는 필요한 대로 사용 가능한 옵션의 부분집합만을 불러오고 렌더링하는, 입력을 자동완성 위젯으로 대체하는 방법이 있다. 그렇게 하려면 사용자 정의 자동완성 HTML 템플릿을 구축하기 위해 몇 가지 작업을 해야한다.

[django-autocomplete-light](https://github.com/yourlabs/django-autocomplete-light)와 같은 참고할 만한 [자동완성 위젯을 위한 여러 패키지](https://www.djangopackages.com/grids/g/auto-complete/)가 있다. 단순하게 표준 위젯으로 이런 구성 요소를 포함할 수는 없고, 명시적으로 HTML 템플릿을 작성해야 한다는 점에 유의한다. 이는 REST framework 3.0이 이제 템플릿화된 HTML 생성을 사용하기 때문에 더 이상 `widget` 키워드 인자를 지원하지 않기 때문이다.