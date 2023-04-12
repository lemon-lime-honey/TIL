# Comment and Article
## 모델 관계 설정
### Many-To-One Relationships
한 테이블의 0개 이상의 레코드가 다른 테이블의 레코드 한 개와 관련된 관계

### Comment 모델 정의
```python
# articles/models.py

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```
- `ForeignKey()` 클래스의 인스턴스 이름은 참조하는 모델 클래스 이름의 단수형(소문자)으로 작성하는 것을 권장한다.
- ForeignKey 클래스는 작성하는 위치와 관계없이 필드 마지막에 생성된다.

#### ForeignKey(to, on_delete)
- Django에서 N:1 관계를 설정할 수 있는 모델 필드
- `to`: 참조하는 모델 클래스 이름
- `on_delete`: 외래키가 참조하는 객체가 사라졌을 때 외래키를 가진 객체를 어떻게 처리할지 정의하는 설정
  - `CASCADE`: 참조된 객체가 삭제될 때 이를 참조하는 객체도 삭제한다.

#### 댓글 생성 연습하기
1. Shell_plus 실행 및 게시글 작성
  ```bash
  $ python manage.py shell_plus

  # 게시글 생성
  Article.objects.create(title='title', content='content')
  ```
2. 댓글 생성
  ```bash
  # Comment 클래스의 인스턴스 comment 생성
  comment = Comment()

  # 인스턴스 변수 저장
  comment.content = 'first comment'

  # DB에 댓글 저장
  comment.save()

  # 에러 발생
  django.db.utils.IntegrityError: NOT NULL constraint failed: articles_comment.article_id
  # articles_comment 테이블의 ForeignKeyField, article_id 값이 저장 시 누락되었기 때문
  ```
3. 댓글 생성
  ```bash
  # 게시글 조회
  article = Article.objects.get(pk=1)

  # 외래키 데이터 입력
  comment.article = article

  # DB에 댓글 저장 및 확인
  comment.save()
  ```
4. comment 인스턴스를 통한 article 값 접근하기
  ```bash
  comment.pk
  > 1

  comment.content
  > 'first comment'

  # 클래스 변수명인 article로 조회 시 해당 참조하는 게시물 객체를 조회할 수 있다.
  comment.article
  > <Article: Article object (1)>

  # article_pk는 존재하지 않는 필드이기 때문에 사용 불가
  comment.article_id
  > 1
  ```
5. 댓글 생성
  ```bash
  # 1번 댓글이 작성된 게시물의 pk 조회
  comment.article.pk
  > 1

  # 1번 댓글이 작성된 게시물의 content 조회
  comment.article.content
  > 'content'
  ```
6. 두 번째 댓글 작성해보기
  ```bash
  comment = Comment(content='second comment', article=article)
  comment.save()

  comment.pk
  > 2

  comment
  > <Comment: Comment object (2)>

  comment.article.pk
  > 1
  ```

## 관계 모델 참조
### 역참조
- 참조되는 테이블이 참조하는 테이블을 참조하는 것
- N:1 관계에서 1이 N을 참조하는 상황

### Related Manager
```bash
article.comment_set.all()

# 모델 인스턴스: article
# related manager: comment_set
# QuerySet API: all()
```
N:1 혹은 M:N 관계에서 역참조 시에 사용하는 manager

#### related manager가 필요한 이유
- Article 클래스에 Comment에 관한 관계가 작성되어 있지 않기 때문에 article.comment 형식으로는 댓글 객체를 참조할 수 없다.
- Django가 역참조할 수 있는 `comment_set` manager를 자동으로 생성하면 `article.comment_set` 형태로 댓글 객체를 참조할 수 있다.
- N:1 관계에서 생성되는 related manager의 이름은 참조하는 `모델명_set`으로 만들어진다.

#### Related Manager 연습하기
1. shell_plus 실행 및 1번 게시글 조회
  ```bash
  $ python manage.py shell_plus

  article = Article.objects.get(pk=1)
  ```
2. 1번 게시글에 작성된 모든 댓글 조회하기(역참조)
  ```python
  >>> article.comment_set.all()
  <QuerySet [<Comment: Comment object (1)>, <Comment: Comment object (2)>]>
  ```
3. 1번 게시글에 작성된 모든 댓글 출력하기
  ```python
  comments = article.comment_set.all()

  for comment in comments:
      print(comment.content)
  ```

## 댓글 기능 구현
### Comment CREATE
```python
# articles/urls.py

urlpatterns = [
    ...,
    path('<int:pk>/comments/', views.comments_create, name='comment_create'),
]


# articles/forms.py

from .models import Article, Comment


class CommentForm(form.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)


# articles/views.py

from .forms import ArticleForm, CommentForm


def detail(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm()
    context = {
        'article': article,
        'comment_form': comment_form,
    }
    return render(request, 'articles/detail.html', context)


def comments_create(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        # DB에 저장하지 않고 인스턴스만 반환한 후
        # 외래키 데이터를 받아온다
        comment = comment_form.save(commit=False)
        comment.article = article
        comment_form.save()
        return redirect('articles:detail', article.pk)
    context = {
        'article': article,
        'comment_form': comment_form,
    }
    return render(request, 'articles/detail.html', context)
```
```html
<!-- articles/detail.html -->

<form action="{% url 'articles:comments_create' article.pk %}" method="POST">
  {% csrf_token %}
  {{ comment_form }}
  <input type="submit">
</form>
```

### Comment READ
```python
# articles/views.py

from .models import Article, Comment


def detail(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm()
    comments = article.comment_set.all()
    context = {
        'article': article,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'articles/detail.html', context)
```
```html
<!-- articles/detail.html -->

<h4>댓글 목록</h4>
<ul>
  {% for comment in comments %}
    <li>{{ comment.content }}</li>
  {% endfor %}
</ul>
```

### Comment DELETE
```python
# articles/urls.py

app_name = 'articles'
urlpatterns = [
    ...,
    path('<int:article_pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),
]


# articles/views.py

def comments_delete(request, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('articles:detail', article_pk)
```
```html
<!-- articles/detail.html -->

<ul>
  {% for comment in comments %}
    <li>
      {{ comment.content }}
      <form action="{% url 'articles:comments_delete' article.pk comment.pk %}" method="POST">
        {% csrf_token %}
        <input type="submit" value="DELETE">
      </form>
    </li>
  {% endfor %}
</ul>
```
<br><br>

# Article and User
## 모델 관계 설정
### User 외래 키 정의
```python
# articles/models.py

from django.conf import settings


class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### User 모델 참조 방법
1. $\texttt{get}$ _ $\texttt{user}$ _ $\texttt{model()}$
- 반환 값: `User Object`(객체)
- `models.py`가 아닌 다른 모든 곳에서 참조할 때 사용한다.
2. $\texttt{settings.AUTH}$ _ $\texttt{USER}$ _ $\texttt{MODEL}$
- 반환 값: `accounts.User`(문자열)
- `models.py`의 모델 필드에서 참조할 때 사용한다.

## CRUD 구현
### Article CREATE
1. ArticleForm 출력 필드 수정
  ```python
  # articles/forms.py

  class ArticleForm(forms.ModelForm):
      class Meta:
        model = Article
        fields = ('title', 'content')
  ```
2. 게시글 작성 시 작성자 정보가 함께 저장될 수 있도록 `save`의 `commit` 옵션을 활용한다.
  ```python
  # articles/views.py

  @login_required
  def create(request):
      if request.method == 'POST':
          form = ArticleForm(request.POST)
          if form.is_valid():
              article = form.save(commit=False)
              article.user = request.user
              article.save()
              return redirect('articles:detail', article.pk)
      else:
          ...
  ```

### Article READ
```html
<!-- articles/index.html -->

{% for article in articles %}
  <p>작성자: {{ article.user }}</p>
  <p>글 번호: {{ article.pk }}</p>
  <a href="{% url 'articles:detail' article.pk %}">
    <p>글 제목: {{ article.title }}</p>
  </a>
  <p>글 내용: {{ article.content }}</p>
  <hr>
{% endfor %}


<!-- articles/detail.html -->
<h2>DETAIL</h2>
<h3>{{ article.pk }} 번째 글</h3>
<hr>
<p>작성자: {{ article.user }}</p>
<p>제목: {{ article.title }}</p>
<p>내용: {{ article.content }}</p>
<p>작성 시각: {{ article.created_at }}</p>
<p>수정 시각: {{ article.updated_at }}</p>
```

### Article UPDATE
본인 게시글만 수정할 수 있게 한다.
```python
# articles/views.py

@login_required
def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user == article.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                form.save()
                return redirect('articles:detail', article.pk)
        else:
            form = ArticleForm(instance=article)
    else:
        return redirect('articles:index')
    ...
```
```html
<!-- articles/detail.html -->

{% if request.user == article.user %}
  <a href="{% url 'articles:update' article.pk %}">UPDATE</a><br>
  <form action="{% url 'articles:delete' article.pk %}" method="POST">
    {% csrf_token %}
    <input type="submit" value="DELETE">
  </form>
{% endif %}
```

### Article DELETE
본인 게시글만 삭제할 수 있게 한다.
```python
# articles/views.py

@login_required
def delete(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user == article.user:
        article.delete()
    return redirect('articles:index')
```
<br><br>

# Comment and User
## 모델 관계 설정
### User 외래키 정의
```python
# articles/models.py

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## CRD 구현
### Comment CREATE
```python
# articles/views.py

def comments_create(request, pk):
    article = Article.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = article
        comment.user = request.user
        comment_form.save()
        return redirect('articles:detail', article.pk)
```

### Comment READ
```html
<!-- articles/detail.html -->

{% for comment in comments %}
  <li>
    {{ comment.user }} - {{ comment.content }}
    ...
  </li>
{% endfor %}
```

### Comment DELETE
본인 댓글만 삭제할 수 있게 한다.
```python
# articles/views.py

def comments_delete(request, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('articles:detail', article_pk)
```
```html
<!-- articles/detail.html -->

<ul>
  <li>
    {{ comment.user }} - {{ comment.content }}
    {% if request.user == comment.user %}
      <form action="{% url 'articles:comments_delete' article.pk comment.pk %}" method="POST">
        {% csrf_token %}
        <input type="submit" value="DELETE">
      </form>
    {% endif %}
  </li>
</ul>
```