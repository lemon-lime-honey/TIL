# view 함수의 변화
## new와 create 결합
```python
# NEW
def new(request):
    form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/new.html', context)

# CREATE
def create(request):
    form = ArticleForm(request.POST)
    if form.is_valid():
        article = form.save()
        return redirect('articles:detail', article.pk)
    context = {
        'form': form,
    }
    return render(request, 'articles/new.html', context)

# NEW + CREATE -> CREATE
def create(request):
    if request.method = 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()
    context = {
      'form': form,
    }
    return render(request, 'articles/new.html', context)
```

## new url 정리
```python
# articles/views.py

app_name = 'articles'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    # path('new/', views.new, name='new'),
    path('create/', views.create, name='create'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('<int:pk>/update/', views.update, name='update'),
]
```

## 기존 new 관련 코드 수정
```html
<!-- articles/index.html -->

<h1>Articles</h1>
<a href="{% url 'articles:create' %}">CREATE</a>
<hr>
...


<!-- articles/create.html -->

<h1>CREATE</h1>
<form action="{% url 'articles:create' %}" method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit">
</form>
```
```python
# articles/views.py

def create(request):
    if request.method = 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm()
    context = {
      'form': form,
    }
    return render(request, 'articles/create.html', context)
```

## 새로운 update view 함수
```python
# articles/views.py

def update(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method = 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', article.pk)
    else:
        form = ArticleForm(instance=article)
    context = {
      'article': article,
      'form': form,
    }
    return render(request, 'articles/update.html', context)
```

## edit url 정리
```python
# articles/views.py

app_name = 'articles'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    # path('new/', views.new, name='new'),
    path('create/', views.create, name='create'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    # path('<int:pk>/edit/', views.edit, name='edit'),
    path('<int:pk>/update/', views.update, name='update'),
]
```

## 기존 edit 관련 코드 수정
```html
<!-- articles/detail.html -->

<h2>DETAIL</h2>
<h3>{{ article.pk }} 번째 글</h3>
<hr>
<p>제목: {{ article.title }}</p>
<p>내용: {{ article.content }}</p>
<p>작성 시각: {{ article.created_at }}</p>
<p>수정 시각: {{ article.updated_at }}</p>
<hr>
<a href="{% url 'articles:update' article.pk %}">UPDATE</a><br>
<form action="{% url 'articles:delete' article.pk %}" method="POST">
  {% csrf_token %}
  <input type="submit" value="DELETE">
</form>


<!-- articles/update.html -->

<h1>UPDATE</h1>
<form action="{% url 'articles:update' article.pk %}" method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit">
</form>
```