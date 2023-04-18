# $\texttt{ManyToManyField(to, **options)}$
- M:N 관계 설정 시 사용하는 모델 필드
- 모델 필드의 RelatedManager를 사용하여 관련 개체를 추가, 제거 또는 생성
- $\texttt{add()}$, $\texttt{remove()}$, $\texttt{create()}$, $\texttt{clear()}$ 등

## ManyToManyField's Arguments
1. related_name
역참조시 사용하는 manager name을 변경한다.
  ```python
  class Patient(models.Model):
      doctors = models.ManyToManyField(Doctor, related_name='patients')
      name = models.TextField()

  # 변경 전
  doctor.patient_set.all()

  # 변경 후
  doctor.patients.all()
  ```
2.through
- 중개 테이블을 직접 작성하는 경우, through 옵션을 사용하여 중개 테이블을 나타내는 Django 모델을 지정한다.
- 일반적으로 중개 테이블에 추가 데이터를 사용하는 다대다 관계와 연결하려는 경우 (extra data with a many-to-many relationship)에 사용된다.
3.symmetrical
- ManyToManyField가 동일한 모델을 가리키는 정의에서만 사용한다.
- 기본 값: `True`
  ```python
  class Person(models.Model):
      friends = models.ManyToManyField('self')
      # friends = models.ManyToManyField('self', symmetrical=False)
  ```
- `True`일 경우
  - `_set` 매니저를 추가하지 않는다.
  - source 모델의 인스턴스가 target 모델의 인스턴스를 참조하면 자동으로 target 모델 인스턴스도 source 모델 인스턴스를 자동으로 참조하도록 한다.(대칭)
  - 즉, 내가 당신의 친구라면 당신도 내 친구가 된다.
- 대칭을 원하지 않는 경우 False로 설정한다.

## M:N에서의 methods
- $\texttt{add()}$<br>
  - 지정된 객체를 관련 객체 집합에 추가한다.
  - 이미 존재하는 관계에 사용하면 관계가 복제되지 않는다.
- $\texttt{remove}$<br>
  - 관련 객체 집합에서 지정된 모델 개체를 제거한다.
<br><br>

# Article & User
## 모델 관계 설정
1. ManyToManyField 작성
  ```python
  # articles/models.py

  class Article(models.Model):
      user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
      like_users = models.ManyToManyField(settings.AUTH_USER_MODEL)
      title = models.CharField(max_length=10)
      content = models.TextField()
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
  ```
2. Migration 진행 후 에러 확인
3. 에러 원인과 해결 방법
  - `like_users` 필드 생성 시 자동으로 역참조에는 `.article_set`매니저가 생성된다.
  - 그러나 이전 N:1(Article-User) 관계에서 이미 해당 매니저를 사용 중이다.
    - `user.article_set.all()` $\rightarrow$ 해당 유저가 작성한 모든 게시글 조회
  - user가 작성한 글(`user.article_set`)과 user가 좋아요를 누른 글(`user.article_set`)을 구분할 수 없게 된다.
  - user와 관계된 ForeignKey 혹은 ManyToManyField 중 하나에 related_name을 작성해야 한다.
4. `related_name` 작성 후 Migration
  ```python
  # articles/models.py

  class Article(models.Model):
      user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
      like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles')
      title = models.CharField(max_length=10)
      content = models.TextField()
      created_at = models.DateTimeField(auto_now_add=True)
      updated_at = models.DateTimeField(auto_now=True)
  ```

## User - Article 간 사용 가능한 related manager 정리
- $\texttt{article.user}$<br>
  - 게시글을 작성한 유저 `N:1`
- $\texttt{user.article}$ _ $\texttt{set}$<br>
  - 유저가 작성한 게시글(역참조) `N:1`
- $\texttt{article.like}$ _ $\texttt{users}$<br>
  - 게시글을 좋아요한 유저 `M:N`
- $\texttt{user.like}$ _ $\texttt{articles}$<br>
  - 유저가 좋아요한 게시글(역참조) `M:N`

## 좋아요 구현
1. url 및 view 함수 작성
  ```python
  # articles/urls.py

  urlpatterns = [
      ...,
      path('<int:article_pk>/likes/', views.likes, name='likes'),
  ]

  # articles/views.py

  @login_required
  def likes(request, article.pk):
      article = Article.objects.get(pk=article.pk)
      if request.user in article.like_users.all():
          article.like_users.remove(request.user)
      else:
          article.like_users.add(request.user)
      return redirect('articles:index')
  ```
2. index 템플릿에서 각 게시글에 좋아요 버튼 출력
  ```html
  <!-- articles/index.html -->

  {% for article in articles %}
    ...
    <form action="{% url 'articles:likes' article.pk %}" method="POST">
      {% csrf_token %}
      {% if request.user in article.like_users.all %}
        <input type="submit" value="좋아요 취소">
      {% else %}
        <input type="submit" value="좋아요">
      {% endif %}
    </form>
    <hr>
  {% endfor %}
  ```

## $\texttt{.exists()}$
- QuerySet에 결과가 포함되어 있으면 `True`를 반환하고 그렇지 않으면 `False`를 반환한다.
- 특히 큰 QuerySet에 있는 특정 개체의 존재와 관련된 검색에 유용하다.
<br><br>

# Profile 구현
1. 자연스러운 follow 흐름을 위한 프로필 페이지 작성
  ```python
  # accounts.py

  urlpatterns = [
      ...,
      path('profile/<username>/', views.profile, name='profile'),
  ]

  # accounts/views.py

  from django.contrib.auth import get_user_model

  def profile(request, username):
      User = get_user_model()
      person = User.objects.get(username=username)
      context = {
          'person': person,
      }
      return render(request, 'accounts/profile.html', context)
  ```
2. 템플릿 작성
  ```html
  <!-- accounts/profile.html -->

  <h1>{{ person.username }}님의 프로필</h1>
  <hr>
  <h2>{{ person.username }}'s 게시글</h2>
  {% for article in person.article_set.all %}
    <div>{{ comment.content }}</div>
  {% endfor %}
  <hr>
  <h2>{{ person.username }}'s 댓글</h2>
  {% for comment in person.comment_set.all %}
    <div>{{ comment.content }}</div>
  {% endfor %}
  <hr>
  <h2>{{ person.username }}'s 좋아요한 게시글</h2>
  {% for article in person.like_articles.all %}
    <div>{{ article.title }}</div>
  {% endfor %}
  ```
3. 프로필 템플릿으로 이동할 수 있는 하이퍼 링크 작성
  ```html
  <!-- articles/index.html -->

  <a href="{% url 'accounts:profile' article.user.username %}">{{ article.user }}</a></p>
  ```
<br><br>

# User & User
## Follow 구현
1. ManyToManyField 작성 및 Migration 진행
  ```python
  # accounts/models.py

  class User(AbstractUser):
      followings = models.ManyToManyField('self', symmetrical= False, related_name='followers')
  ```
2. url 및 view 함수 작성
  ```python
  # accounts/urls.py

  urlpatterns = [
      ...,
      path('<int:user_pk>/follow/', views.follow, name='follow'),
  ]

  # accounts/views.py

  @login_required
  def follow(request, user_pk):
      User = get_user_model()
      person = User.objects.get(pk=user_pk)
      if person != request.user:
          if person.followers.filter(pk=request.user.pk).exists():
              person.followers.remove(request.user)
          else:
              person.followers.add(request.user)
      return redirect('accounts:profile', person.username)
  ```
4. 프로필 유저의 팔로잉, 팔로워 수, 팔로우, 언팔로우 버튼 작성
  ```html
  <!-- accounts/profile.html -->

  <div>
    <div>
      팔로잉: {{ person.followings.all|length }} / 팔로워: {{ person.followers.all|length }}
    </div>
    {% if request.user != person %}
      <div>
        <form action="{% url 'accounts:follow' person.pk %}" method="POST">
          {% csrf_token %}
          {% if request.user in person.followers.all %}
            <input type="submit" value="Unfollow">
          {% else %}
            <input type="submit" value="Follow">
          {% endif %}
        </form>
      </div>
    {% endif %}
  </div>
  ```