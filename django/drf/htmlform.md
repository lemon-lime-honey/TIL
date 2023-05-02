# HTML & Forms
REST framework는 API 양식 응답과 일반적인 HTML 페이지를 모두 반환하는데 적합하다. 추가적으로 serializer를 HTML 폼으로 사용하고 템플릿으로 렌더링할 수 있다.

## Rendering HTML
HTML 응답을 반환하려면 `TemplateHTMLRenderer` 혹은 `StaticHTMLRenderer`가 필요하다.

`TemplateHTMLRenderer` 클래스는 응답에 컨텍스트 데이터 딕셔너리를 포함해야하며 뷰 또는 응답에 명시되어야 하는 템플릿에 기반한 HTML 페이지를 렌더링한다.

`StaticHTMLRenderer` 클래스는 응답에 렌더링 되지 않은 HTML 내용이 문자열로 포함되어야 한다.

정적 HTML 페이지가 보통은 API 응답과는 다르게 동작하기 때문에 빌트인 generic view에 의존하는 것보다 HTML 뷰를 작성할 필요가 있다.

여기 HTML 템플릿에 렌더링된 *프로필* 인스턴스 리스트를 반환하는 뷰 예시가 있다.

```python
# views.py

from my_project.example.models import Profile
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

class ProfileList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'profile_list.html'

    def get(self, request):
        queryset = Profile.objects.all()
        return Response({'profiles': queryset})
```
```html
# profile_list.html

<html>
  <body>
    <h1>Profiles</h1>
    <ul>
      {% for profile in profiles %}
      <li>{{ profile.name }}</li>
      {% endfor %}
    </ul>
  </body>
</html>
```

## Rendering Forms
Serializer는 `render_form` 템플릿 태그를 사용해 폼으로 렌더링할 수 있으며, serializer 인스턴스를 템플릿의 컨텍스트로 포함한다.

다음의 뷰는 모델 인스턴스를 읽고 업데이트하기 위해 템플릿 안의 serializer를 사용하는 예를 보여준다.

```python
# views.py

from django.shortcuts import get_object_or_404
from my_project.example.models import Profile
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView

class ProfileDetail(APIView):
    renderer_class = [TemplateHTMLRenderer]
    template_name = 'profile_detail.html'

    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        serializer = ProfileSerializer(profile)
        return Response({'serializer': serializer, 'profile': profile})

    def post(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        serializer = ProfileSerializer(profile, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'profile': profile})
        serializer.save()
        return redirect('profile-list')
```
```html
{% load rest_framework %}

<html>
  <body>
    <h1>Profile - {{ profile.name }}</h1>

    <form action="{% url 'profile-detail' pk=profile.pk %}" method="POST">
      {% csrf_token %}
      {% render_form serializer %}
      <input type="submit" value="Save">
    </form>
  </body>
</html>
```

### Using template packs
`render_form` 태그는 폼과 폼 필드를 렌더링할 때 사용할 템플릿 디렉토리를 명시하는 `template_pack` 선택 인자를 가진다.

REST framework는 부트스트랩 3에 기반한 세 가지 빌트인 템플릿 팩을 포함한다. 빌트인 스타일은 `horizontal`, `vertical`, `inline`이다. 기본 스타일은 `horizontal`이다. 셋 중 어느 것이라도 사용하고 싶다면 부트스트랩 3 CSS를 불러와야 한다.

다음의 HTML은 부트스트랩 3 CSS CDN으로 연결한다.

```html
<head>
  …
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
</head>
```

서드파티 패키지가 필요한 폼과 필드 템플릿을 포함하는 템플릿 디렉토리를 묶은 또다른 템플릿 팩을 포함할 수도 있다.

어떻게 세 가지 템플릿 팩을 렌더링할지 보자. 이 예시에서는 *로그인* 폼을 표현하기 위한 한 개의 serializer를 사용한다.

```python
# serializers.py

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=100,
        style={'placeholder': 'Email', 'autofocus': True}
    )
    password = serializers.CharField(
        max_length=100,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    remember_me = serializers.BooleanField()
```

#### `rest_framework/vertical`
기본 부트스트랩 레이아웃을 사용해 해당하는 컨트롤 입력 위에 라벨을 표시한다.

*이것이 기본 템플릿 팩이다.*

```html
{% load rest_framework %}

...

<form action="{% url 'login' %}" method="post" novalidate>
  {% csrf_token %}
  {% render_form serializer template_pack='rest_framework/vertical' %}
  <button type="submit" class="btn btn-default">Sign in</button>
</form>
```
![vertical](https://www.django-rest-framework.org/img/vertical.png)

#### `rest_framework/horizontal`
2/10으로 열을 나누어 라벨과 컨트롤을 나란히 둔다.

*이것은 탐색 가능한 API와 관리자 렌더러에 사용되는 폼 스타일이다.*

```html
{% load rest_framework %}

...

<form class="form-horizontal" action="{% url 'login' %}" method="post" novalidate>
  {% csrf_token %}
  {% render_form serializer %}
  <div class="form-group">
    <div class="col-sm-offset-2 col-sm-10">
      <button type="submit" class="btn btn-default">Sign in</button>
    </div>
  </div>
</form>
```

![horizontal](https://www.django-rest-framework.org/img/horizontal.png)

#### `rest_framework/inline`
모든 컨트롤을 한 줄에 두는 압축된 스타일.

```html
{% load rest_framework %}

...

<form class="form-inline" action="{% url 'login' %}" method="post" novalidate>
  {% csrf_token %}
  {% render_form serializer template_pack='rest_framework/inline' %}
  <button type="submit" class="btn btn-default">Sign in</button>
</form>
```

![inline](https://www.django-rest-framework.org/img/inline.png)

## Field Styles
Serializer 필드의 `style` 키워드 인자를 사용해 렌더링 스타일을 변경할 수 있다. 이 인자는 사용된 템플릿과 레이아웃을 컨트롤하는 옵션들을 모아놓은 딕셔너리이다.

필드 스타일을 변경하는 가장 일반적인 방법은 `base_template` 스타일 키워드 인자를 사용해 템플릿 팩의 어느 템플릿을 사용할 것인지 정하는 것이다.

예를 들어, 기본 HTML 입력 대신 HTML textarea로 `CharField`를 렌더링 하려면 이런 설정이 필요하다.

```python
details = serializers.CharField(
    max_length=1000,
    style={'base_template': 'textarea.html'}
)
```

대신 포함된 템플릿에 없는 사용자 지정 템플릿을 사용해 필드를 렌더링하고 싶다면 템플릿 이름을 온전히 명시하기 위해 `template` 스타일 옵션을 사용한다.

```python
details = serializers.CharField(
    max_length=1000,
    style={'template': 'my-field-templates/custom-input.html'}
)
```

필드 템플릿은 그 종류에 따라 추가적인 스타일 속성을 추가할 수 있다. 예를 들어, `textarea.html` 템플릿은 컨트롤의 크기에 영향을 줄 수 있는 `rows` 속성을 받을 수 있다.

```python
details = serializers.CharField(
    max_length=1000,
    style={'base-template': 'textarea.html', 'rows': 10}
)
```

다음은 `base_template` 옵션과 그에 연관된 스타일 옵션 리스트이다.

| base_template | Valid field types | Additional style options |
| --- | --- | --- |
| input.html | Any string, numeric or date/time field | input_type, placeholder, hide_label, autofocus |
| textarea.html | `CharField` | rows, placeholder, hide_label |
| select.html | `ChoiceField` or relational field types | hide_label |
| radio.html | `ChoiceField` or relational field types | inline, hide_label |
| select_multiple.html | `MultipleChoiceField` or relational fields with `many=True` | hide_label |
| checkbox_multiple.html | `MultipleChoiceField` or relational fields with `many=True` | inline, hide_label |
| checkbox.html | `BooleanField` | hide_label |
| fieldset.html | Nested Serializer | hide_label |
| list_fieldset.html | `ListField` or nested serializer with `many=True' | hide_label |