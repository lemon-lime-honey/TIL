# annotate
- SQL의 GROUP BY절을 활용한다.
```python
# before
# html
{{ article.comment_set.count }}

# views.py
articles = Article.objects.order_by('-pk')


# after
# html
{{ article.comment__count }}

# views.py
articles = Article.objects.annotate(Count('comment')).order_by('-pk')
```
<br><br>

# select_related
- 1:1 또는 N:1 참조 관계에서 사용한다.
- SQL의 INNER JOIN절을 활용한다.
```python
# html
{% for article in articles %}
  <h3>작성자: {{ article.user.username }}</h3>
  <p>제목: {{ article.title }}</p>
  <hr>
{% endfor %}


# before
# views.py
articles = Article.objects.order_by('-pk')

# after
# views.py
articles = Article.objects.select_related('user').order_by('-pk')
```
<br><br>

# prefetch_related
- M:N 또는 N:1 역참조 관계에서 사용한다.
- SQL이 아닌 Python을 사용한 JOIN이 진행된다.
```python
# html
{% for article in articles %}
  <p>제목: {{ article.title }}</p>
  <p>댓글 목록</p>
  {% for comment in article.comment_set.all %}
    <p>{{ comment.content }}</p>
  {% endfor %} 
  <hr>
{% endfor %}


# before
# views.py
articles = Article.objects.order_by('-pk')

# after
# views.py
articles = Article.objects.prefetch_related('comment_set').order_by('-pk')
```
<br><br>

# select_related & prefetch_related
```python
# html
{% for article in articles %}
  <p>제목: {{ article.title }}</p>
  <p>댓글 목록</p>
  {% for comment in article.comment_set.all %}
    <p>{{ comment.content }}</p>
  {% endfor %} 
  <hr>
{% endfor %}


# before
# views.py
articles = Article.objects.order_by('-pk')

# after
# views.py
articles = Article.objects.prefetch_related(Prefetch('comment_set', queryset=Comment.objects.select_related('user'))).order_by('-pk')
```