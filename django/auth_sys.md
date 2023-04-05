# Django Authentication System
- 사용자 인증에 관한 기능을 모아 놓은 시스템
- 인증과 권한 부여를 함께 제공하고 처리한다.
- Authentication: 사용자 인증
- Authorization: 권한 부여

## 사전 설정
Django 내부에서는 `auth`와 관련된 경로나 키워드를 `accounts`라는 이름으로 사용하기 때문에 `accounts`로 지정하는 것이 좋다.
```python
# accounts/urls.py

from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
]


# PROJECT_NAME/urls.py

urlpatterns = [
    ...,
    path('accounts/', include('accounts.urls')),
]
```
<br><br>

# Custom User Model
## User model을 Custom User model로 대체하기
- Django에서 기본적으로 제공하는 User model: 내장된 `auth` 모듈의 `User` 클래스를 사용한다.
- 기본 모델은 별도의 설정 없이 사용할 수 있어 간편하나 직접 수정할 수 없어 Custom User model로 대체한다.

### $\texttt{{\it{class}} models.AbstractUser}$
- 관리자 권한과 함께 완전한 기능을 가지고 있는 User model을 구현하는 추상 기본 클래스
- Abstract base class(추상 기본 클래스)
  - 몇 가지 공통 정보를 여러 다른 모델에 넣을 때 사용하는 클래스
  - 데이터베이스 테이블을 만드는 데 사용되지 않으며, 대신 다른 모델의 기본 클래스로 사용되는 경우 해당 필드가 하위 클래스의 필드에 추가된다.

### 01
```python
# accounts/models.py

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
```
- `AbstractUser`를 상속받는 커스텀 `User` 클래스를 작성한다.
- 기존 `User` 클래스도 `AbstractUser`를 상속받기 때문에 커스텀 `User` 클래스도 같은 모습을 가지게 된다.

### 02
```python
# settings.py

AUTH_USER_MODEL = 'accounts.User'
```
- Django 프로젝트가 사용하는 기본 `User` 모델을 사용자 정의 `User` 모델로 지정한다.
- 수정 전 기본값: `auth.User`

### 03
```python
# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)
```
기본 `User` 모델이 아니므로 등록을 해야 `admin site`에 출력된다.

## 주의
- 프로젝트 중간에 `AUTH_USER_MODEL`을 변경할 수 없다.
- 중간에 변경할 경우 데이터베이스를 초기화하고 진행해야 한다.

## User Model을 대체하는 이유
- Django는 새 프로젝트를 시작할 때 기본 User 모델이 충분해도 커스텀 User 모델을 설정하는 것을 강력히 권장한다.
- 커스텀 User 모델은 기본 User 모델과 동일하게 작동하지만 필요한 경우 이후에 설정을 바꿀 수 있다.

:star: User 모델 대체 작업은 프로젝트의 모든 `migrations` 혹은 첫 `migrate`를 실행하기 전에 해야 한다.
<br><br>

# Login
세션을 생성하는 과정

## 로그인 페이지 작성
```python
# accounts/urls.py

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
]


# accounts/views.py

from django.contrib.auth.forms import AuthenticationForm

def login(request):
    if request.method == 'POST':
        pass
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)
```
```html
<!-- accounts/login.html -->

<h1>로그인</h1>
<form action="{% url 'accounts:login' %}" method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit">
</form>
```

## 로그인 로직 작성
```python
# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login

def login(request):
    if request.method == 'POST':
        # AuthenticationForm(): 로그인을 위한 built-in form
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # login(request, user): 인증된 사용자를 로그인하는 함수
            # get_user(): AuthenticationForm의 인스턴스 메서드
            #             유효성 검사를 통과했을 경우 로그인한 사용자 객체 반환
            auth_login(request, form.get_user())
            return redirect('articles:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)
```

## 세션 데이터 확인하기
- 로그인 후 개발자 도구와 DB에서 Django로부터 발급받은 세션을 확인한다.(로그인은 관리자 계정을 만든 후 진행)
1. `django_session` 테이블에서 확인
2. 브라우저에서 확인: `개발자도구 - Application - Cookies`

## 로그인 링크 작성
```html
<!-- articles/index.html -->

<h1>Articles</h1>
<a href="{% url 'accounts:login' %}">Login</a>
<a href="{% url 'accounts:create' %}">NEW</a>
<hr>
```
<br><br>

# Logout
세션을 삭제하는 과정

## 로그아웃 로직 작성
```python
# accounts/urls.py

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]


# accounts/views.py

from django.contrib.auth import logout as auth_logout


def logout(request):
    auth_logout(request)
    return redirect('articles:index')
```
```html
<!-- articles/index.html -->

<h1>Articles</h1>
<a href="{% url 'accounts:login' %}">Login</a>
<form action="{% url 'accounts:logout' %}" method="POST">
  {% csrf_token %}
  <input type="submit" value="Logout">
</form>
```
<br><br>

# Template with Authentication Data
템플릿에서 인증 관련 데이터를 출력하는 방법

## 현재 로그인 되어 있는 유저 정보 출력하기
```html
<!-- articles/index.html -->

<h3>Hello, {{ user }}</h3>
```
- 로그인이 되어 있을 때: `Hello, (계정명)`
- 로그인이 되어 있지 않을 때: `Hello, AnonymousUser`

## Context Processors
- 템플릿이 렌더링 될 때 호출 가능한 컨텍스트 데이터 목록
- 작성된 컨텍스트 데이터는 기본적으로 템플릿에서 사용 가능한 변수로 포함된다.
- Django에서 자주 사용하는 데이터 목록을 미리 템플릿에 로드 해둔 것
```python
# settings.py

TEMPLATES = [
    {
        ...,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
<br><br>

# 회원가입
`User` 객체 생성

## 커스텀 Form 작성
```python
# accounts/forms.py

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()


class CustomUerChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name')
```
- $\texttt{get}$ _ $\texttt{user}$ _ $\texttt{model()}$<br>
  현재 프로젝트에서 활성화된 사용자 모델(active user model)을 반환한다.

### User 모델을 직접 참조하지 않는 이유
- User 모델을 $\texttt{get}$ _ $\texttt{user}$ _ $\texttt{model()}$을 사용해 참조하면 커스텀 User 모델을 자동으로 반환한다.
- Django에서는 User 클래스를 직접 참조하는 대신 $\texttt{get}$ _ $\texttt{user}$ _ $\texttt{model()}$을 사용해 참조하는 것을 강조한다.

## 회원 가입 페이지 작성
```python
# accounts.urls.py

app_name = 'accounts'
urlpatterns = [
    ...,
    path('signup/', views.signup, name='signup'),
]


# accounts/views.py

from .forms import CustomUserCreationForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)
```
```html
<!-- accounts/signup.html -->

<h1>회원가입</h1>
<form action="{% url 'accounts:signup' %}" method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit">
</form>
```
- 회원가입 후 로그인까지 진행하려면 `views.py`의 `signup`을 다음과 같이 변경한다.
```python
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('articles:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)
```
<br><br>

# 회원탈퇴
`User` 객체 삭제

## 회원 탈퇴 로직 생성
```python
# accounts.urls.py

app_name = 'accounts'
urlpatterns = [
    ...,
    path('delete/', views.delete, name='delete'),
]


# accounts/views.py

def delete(request):
    request.user.delete()
    return redirect('articles:index')
```
```html
<!-- accounts/index.html -->

<form action="{% url 'accounts:delete' %}" method="POST">
  {% csrf_token %}
  <input type="submit" value="회원탈퇴">
</form>
```
- 탈퇴하면서 유저의 세션 정보도 함께 지우고 싶을 경우 `views.py`의 `delete`를 다음과 같이 변경한다.
```python
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('articles:index')
```
- 반드시 탈퇴 후 로그아웃 순서로 행해야 한다.
- 먼저 로그아웃을 하게 되면 해당 요청 객체 정보가 없어지기 때문에 탈퇴에 필요한 유저 정보 또한 없어진다.
<br><br>

# 회원정보 수정
`User` 객체 갱신

## 빌트인 모델폼 $\texttt{UserChangeForm()}$ 사용 시 문제점
- admin 인터페이스에서 사용되는 ModelForm이므로 일반 사용자가 접근해서는 안 될 정보들(fields)까지 모두 수정이 가능하다.
- CustomUserchangeForm에서 접근 가능한 필드를 조정해야 한다.

## 회원정보 수정 페이지 작성
```python
# accounts.urls.py

app_name = 'accounts'
urlpatterns = [
    ...,
    path('update/', views.update, name='update'),
]


# accounts/views.py

from .forms import CustomUserChangeForm

def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)
```
```html
<!-- accounts/update.html -->

<h1>회원정보 수정</h1>
<form action="{% url 'accounts:update' %}" method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit">
</form>
```
<br><br>

# 비밀번호 변경
## 비밀번호 변경 페이지
- Django는 비밀번호 변경 페이지를 회원정보 수정 form에서 별도 주소로 안내한다.
- `/accounts/password/`

## 비밀번호 변경 페이지 작성
```python
# accounts.urls.py

app_name = 'accounts'
urlpatterns = [
    ...,
    path('password/', views.change_password, name='change_password'),
]


# accounts/views.py

from django.contrib.auth import update_session_auth_hash
from .forms import PasswordChangeForm

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('articles:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)
```
```html
<!-- accounts/change_password.html -->

<h1>비밀번호 변경</h1>
<form action="{% url 'accounts:change_password' %}" method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit">
</form>
```
- $\texttt{update}$ _ $\texttt{session}$ _ $\texttt{auth}$ _ $\texttt{hash(request, user)}$
  - 암호 변경 시 세션 무효화 방지
  - 암호가 변경되어도 로그아웃 되지 않도록 새로운 비밀번호의 세션 데이터로 기존 세션을 업데이트 한다.
  - 암호 변경 시 세션 무효화
    - 비밀번호가 변경되면 기존 세션과의 회원 인증 정보가 일치하지 않게 되어 로그인 상태가 유지되지 않는 상황
<br><br>

# 로그인 여부에 따른 접근 제한
## $\texttt{is}$ _ $\texttt{authenticated}$
- 사용자가 인증되었는지 여부를 알 수 있는 User Model의 속성
- 모든 User 인스턴스에 대해서는 항상 `True`, AnonymousUser에 대해서는 항상 `False`인 읽기 전용 속성
- 권한(permission)과는 관련이 없으며, 사용자가 활성화 상태(active)이거나 유효한 세션(valid session)을 가지고 있는지는 확인하지 않는다.

### 사용 예시
1. 로그인/비로그인 상태에서 출력되는 링크를 다르게 설정하기
```html
<!-- articles/index.html -->

{% if request.user.is_authenticated %}
  <h3>Hello, {{ user }}</h3>
  <form action="{% url 'accounts:logout' %}" method="POST">
    {% csrf_token %}
    <input type="submit" value="Logout">
  </form>
  <form action="{% url 'accounts:delete' %}" method="POST">
    {% csrf_token %}
    <input type="submit" value="회원탈퇴">
  </form>
  <a href="{% url 'accounts:update' %}">회원정보수정</a>
{% else %}
  <a href="{% url 'accounts:login' %}">Login</a>
  <a href="{% url 'accounts:signup' %}">Signup</a>
{% endif %}
```
2. 인증된 사용자라면 로그인/회원가입 로직을 수행할 수 없도록 처리하기
```python
# accounts/views.py

def login(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    ...


def signup(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    ...
```

## $\texttt{login}$ _ $\texttt{required}$
- 인증된 사용자에 대해서만 view 함수를 실행시키는 데코레이터
- 로그인하지 않은 사용자의 경우 `/accounts/login/`으로 redirect 시킨다.

### 사용 예시
1. 인증된 사용자만 게시글을 작성, 수정, 삭제할 수 있도록 수정
```python
# articles/views.py

from django.contrib.auth.decorators import login_required


@login_required
def create(request):
    pass


@login_required
def delete(request, article_pk):
    pass


@login_required
def update(request, article_pk):
    pass
```
2. 인증된 사용자만 로그아웃, 탈퇴, 회원정보 수정, 비밀번호 변경 할 수 있도록 수정
```python
# accounts/views.py

from django.contrib.auth.decorators import login_required


@login_required
def logout(request):
    pass


@login_required
def delete(request):
    pass


@login_required
def update(request):
    pass


@login_required
def change_password(request):
    pass
```