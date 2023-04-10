# Static Files 제공하기
## Static Files
- 서버 측에서 변경되지 않고 고정적으로 제공되는 파일
- 이미지, JS, CSS 파일 등이 있다.

## 기본 경로 static file 제공하기
- 기본 경로: `app/static/`
- static tag를 사용해 이미지 파일에 대한 url을 제공한다.
  ```html
  <!-- articles/index.html -->

  {% load static %}

  <img src="{% static 'articles/image.png' %}" alt="image">
  ```

### $\texttt{STATIC}$ _ $\texttt{URL}$
```python
# settings.py

STATIC_URL = '/static/'
```
- 기본 경로 및 추가 경로에 위치한 정적 파일을 참조하기 위한 url
- 실제 파일이나 디렉토리가 아니며, url로만 존재한다.
- 비어 있지 않은 값으로 설정한다면 반드시 `/`로 끝나야 한다.
- `URL + STATIC_URL + 정적파일 경로`

## 추가 경로 static file 제공하기
- 추가 경로 지정하기
  ```python
  # settings.py

  STATICFILES_DIRS = [
      BASE_DIR / 'static',
  ]
  ```
- static tag를 사용해 이미지 파일에 대한 url을 제공한다.
  ```html
  <!-- articles/index.html -->

  {% load static %}

  <img src="{% static 'image.png' %}" alt="image">
  ```

### $\texttt{STATICFILES}$ _ $\texttt{DIRS}$
- 정적 파일의 기본 경로 외의 추가적인 경로 목록을 정의하는 리스트
<br><br>

# Media Files
- 사용자가 웹에서 업로드하는 정적 파일
- $\texttt{ImageField()}$
  - 이미지 업로드에 사용하는 모델 필드
  - 이미지 객체가 직접 저장되는 것이 아니라 이미지 파일의 경로 문자열이 DB에 저장된다.
  - `upload_to` 인자를 사용하면 미디어 파일의 추가 경로를 설정할 수 있다.
    ```python
    # 1
    image = models.ImageField(blank=True, upload_to='images/')

    # 2
    image = models.ImageField(blank=True, upload_to='%Y/%m/%d/')

    # 3
    def articles_image_path(instance, filename):
        return f'images/{instance.user.username}/{filename}'
    
    image = models.ImageField(blank=True, upload_to=articles_image_path)
    ```

## 미디어 파일 제공 전 준비
1. `settings.py`에 `MEDIA_ROOT`, `MEDIA_URL` 설정
2. 작성한 `MEDIA_ROOT`와 `MEDIA_URL`에 대한 url 지정

### $\texttt{MEDIA}$ _ $\texttt{ROOT}$
미디어 파일이 위치하는 디렉토리의 절대 경로
```python
# settings.py

MEDIA_ROOT = BASE_DIR / 'media'
```

### $\texttt{MEDIA}$ _ $\texttt{URL}$
- `MEDIA_ROOT`에서 제공되는 미디어 파일에 대한 주소를 생성한다.
- `STATIC_URL`과 동일한 역할을 한다.
```python
# settings.py

MEDIA_URL = 'media/'
```

## `MEDIA_ROOT`와 `MEDIA_URL`에 대한 url 지정
```python
# crud/urls.py

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles', include('articles.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
- 업로드 된 파일의 url: `settings.MEDIA_URL`
- 위 url을 통해 참조하는 파일의 실제 위치: `settings.MEDIA_ROOT`
<br><br>

# 이미지 업로드 및 제공하기
## 이미지 업로드
1. `blank=True` 속성으로 빈 문자열이 저장될 수 있게 설정한다.
  ```python
  # articles/models.py

  class Article(models.Model):
      title = models.CharField(max_length=10)
      content = models.TextField()
      # 기존 필드 사이에 작성해도 실제 테이블 생성 시에는 가장 우측(뒤)에 추가된다.
      image = models.ImageField(blank=True)
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
  ```
2. `migration` 진행하기
  ```bash
  # ImageField를 사용하려면 Pillow 라이브러리가 필요하다.

  $ pip install pillow
  $ python manage.py makemigrations
  $ python manage.py migrate
  $ pip freeze > requirements.txt
  ```
3. `form` 요소에 `enctype` 속성 추가하기
  ```html
  <!-- articles/create.html -->

  <h1>CREATE</h1>
  <form action="{% url 'articles:create' %}" method="POST" enctpye="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit">
  </form>
  ```
4. `view 함수`에서 업로드 파일에 대한 추가 코드 작성하기
  ```python
  # articles/views.py

  def create(request):
      if request.method == 'POST':
          form = ArticleForm(request.POST, request.FILES)
  ```

## 이미지 제공하기
1. url 속성을 통해 업로드 파일의 경로 값을 얻는다.
  ```html
  <!-- articles/detail.html -->

  <img src="{{ article.image.url }}" alt="img">
  ```
  - $\texttt{article.image.url}$: 업로드 파일의 경로
  - $\texttt{article.image}$: 업로드 파일의 파일명
2. 이미지 데이터가 있는 경우에만 이미지를 출력할 수 있게 처리한다.
  ```html
  <!-- articles/detail.html -->

  {% if article.image %}
    <img src="{{ article.image.url }}" alt="img">
  {% endif %}
  ```

## 업로드된 이미지 수정하기
1. 수정 페이지 `form` 요소에 `enctype` 속성 추가하기
  ```html
  <!-- articles/update.html -->

  <h1>UPDATE</h1>
  <form action="{% url 'articles:update' article.pk %}" method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit">
  </form>
  ```
2. `view 함수`에서 업로드 파일에 대한 추가 코드 작성하기
  ```python
  def update(request, pk):
      article = Article.objects.get(pk=pk)
      if request.method == 'POST':
          form.ArticleForm(request.POST, request.FILES, instance=article)
  ```