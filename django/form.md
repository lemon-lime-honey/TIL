# Django Form
- 사용자 입력 데이터를 수집하고 처리 및 유효성 검증을 수행하기 위한 도구
- 유효성 검사를 단순화하고 자동화 할 수 있는 기능을 제공한다.

## Form class 선언
```python
# articles/forms.py

from django import forms


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=10)
    content = forms.CharField()
```

## Form class를 적용한 new 로직
```python
# articles/views.py

form .forms import ArticleForm


def new(request):
    form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/new.html', context)
```
```html
<!-- articles/new.html -->

<h1>NEW</h1>
<form action="{% url 'articles:create' %}" method="POST">
  {% csrf_token %}
  {{ form }}
  <input type="submit">
</form>
```

### Form rendering option
```html
<!-- articles/new.html -->

<h1>NEW</h1>
<form action="{% url 'articles:create' %}" method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit">
</form>
```
<br><br>

# Widgets
```python
# articles/forms.py

from django import forms


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=10)
    content = forms.CharField(widget=forms.Textarea)
```
- HTML 'input' element의 표현을 담당한다.
- 단순히 input 요소의 속성 및 출력되는 부분을 변경한다.
<br><br>

# Django ModelForm
- Form: 사용자 입력 데이터를 DB에 저장하지 않을 때(예: 로그인)
- ModelForm: 사용자 입력 데이터를 DB에 저장해야 할 때(예: 회원가입)

## ModelForm class 선언
```python
# articles/forms.py

from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
```

### Meta class
- ModelForm의 정보를 작성한다.

### fields 및 exclude 속성
exclude 속성을 사용하여 모델에서 포함하지 않을 필드를 지정할 수 있다.

```python
# articles/forms.py

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        # 포함
        fields = ('title',)
        # 제외
        exclude = ('content',)
```

## ModelForm을 적용한 create 로직
```python
# articles/views.py

form .forms import ArticleForm


def create(request):
    form = ArticleForm(request.POST)
    if form.is_valid():
        article = form.save()
        return redirect('articles:detail', article.pk)
    context = {
        'form': form,
    }
    return render(request, 'articles/new.html', context)
```

## ModelForm을 적용한 edit 로직
```python
# articles/views.py

def edit(request, pk):
    article = Article.objects.get(pk=pk)
    form = ArticleForm(instance=article)
    context = {
        'article': article,
        'form': form,
    }
    return render(request, 'articles/edit.html', context)
```
```html
<!-- articles/edit.html -->

<h1>EDIT</h1>
<form action="{% url 'articles:update' article.pk %}" method="POST">
  {% csrf_token %}
  {{ form.as_p }}
  <input type="submit">
</form>
```

## ModelForm을 적용한 update 로직
```python
# articles/views.py

def update(request, pk):
    article = Article.objects.get(pk=pk)
    form = ArticleForm(request.POST, instance=article)
    if form.is_valid():
        form.save()
        return redirect('articles:detail', article.pk)
    context = {
        'form': form,
    }
    return render(request, 'articles/edit.html', context)
```

### $\texttt{save()}$
```python
# CREATE
form = ArticleForm(request.POST)
form.save()

# UPDATE
form = ArticleForm(request.POST, instance=article)
form.save()
```

- 데이터베이스 객체를 만들고 저장한다.
- 키워드 인자 instance의 존재 여부를 통해 생성할지 수정할지를 결정한다.