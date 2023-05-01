# [Introduction to class-based views](https://docs.djangoproject.com/en/3.2/topics/class-based-views/intro/)
## Class-based view 사용하기
- 클래스 기반 뷰는 하나의 뷰 함수 안에서 코드를 조건에 따라 분기하는 것 대신 다른 HTTP 응답 메서드를 다른 클래스 인스턴스 메서드로 응답할 수 있게 한다.
  ```python
  # before
  from django.http import HttpResponse

  def my_view(request):
      if request.method == 'GET':
          # <view logic>
          return HttpResponse

  # after
  from django.http import HttpResponse
  from django.views import View

  class MyView(View):
      def get(self, request):
          # <view logic>
          return HttpResponse('result')
  ```
- 장고의 URL resolver가 *request*, 그에 관한 인자를 클래스가 아닌 호출 가능한 함수로 보내기로 정해져 있기 때문에 클래스 기반 뷰 함수는 요청이 연관된 패턴과 일치하는 URL을 얻기 위해 도착할 때 호출할 수 있는 함수를 반환하는 `as_view()` 클래스 메서드를 가진다.
- 이 함수는 클래스의 인스턴스를 생성하고 그 속성을 초기화하기 위해 `setup()`을 호출한 후 `dispatch()` 메서드를 호출한다.
- `dispatch`는 요청이 `GET`인지 `POST`인지 혹은 다른 메서드인지 판정하고 판별이 되었다면 일치하는 메서드로 넘기지만 그렇지 않다면 `HttpResponseNotAllowed`를 발생시킨다.
  ```python
  # urls.py

  from django.urls import path
  from myapp.views import MyView

  urlpatterns = [
      path('about/', MyView.as_view()),
  ]
  ```
- 메서드가 반환하는 것은 함수 기반 뷰에서 반환하는 것, 즉 일부 형식의 *HttpResponse*와 동일하다. 이는 http shortcuts 또는 *TemplateResponse* 객체를 클래스 기반 뷰에서 사용할 수 있다는 것을 의미한다.
- 최소 클래스 기반 뷰는 작업을 수행하는데 어떠한 클래스 속성도 필요로 하지 않지만 클래스 속성은 많은 클래스 기반 디자인에서 유용하며 클래스 속성을 구성하거나 설정하는데 두 가지 방법이 존재한다.
- 첫번째는 표준적인 파이썬 방식인 subclassing과 서브클래스의 속성과 메서드 overriding이다. 그러므로 부모 클래스가 `greeting`속성을 다음과 같이 가지고 있다고 해보자.
  ```python
  from django.http import HttpResponse
  from django.views import View

  class GreetingView(View):
      greeting = "Good Day"

      def get(self, request):
          return HttpResponse(self.greeting)
  ```
  서브클래스에서 override할 수 있다.
  ```python
  class MorningGreetingView(GreetingView):
      greeting = "Morning to ya"
  ```
- 또다른 옵션은 URLconf에서 `as_view()`를 호출할 때 키워드 인자로 클래스 속성을 설정하는 것이다.
  ```python
  urlpatterns = [
      path('about/', GreetingView.as_view(greeting="G'day"))
  ]
  ```
- 클래스가 전송된 각각의 요청에 관해 인스턴스화되는 동안 `as_view()` entry point를 통해 정해진 클래스 속성은 URL을 가져올 때 단 한 번만 구성된다.
<br><br>

## *mixin* 사용하기
- Mixin은 여러 부모 클래스의 동작과 속성을 결합할 수 있는 다중 상속의 한 형태이다.
- 예를 들어 일반적인 클래스 기반 뷰에는 `render_to_response`라는 메서드를 정의하는 것이 주 목적인 *TemplateResponseMixin*이라는 *mixin*이 있다. 뷰 기본 클래스의 동작과 결합했을 때, 적절하게 일치하는 메서드(뷰 기본 클래스에서 정의된 동작)로 요청을 보내고 *TemplateResponse* 객체(*TemplateResponseMixin*에서 정의된 동작)를 반환하기 위한 `template_name` 속성을 사용하는 `render_to_response()` 메서드를 가진 *TemplateView* 클래스가 결과이다.
- Mixin은 여러 클래스에 걸쳐 코드를 재사용하는 훌륭한 방법이지만 대가가 있다. Mixin을 통해 코드가 분산될 수록 자식 클래스를 읽고 그것이 정확히 무엇을 하는지 알기 어려워지며 만약 상속 트리가 깊은 것을 subclassing할 때 어느 mixin의 어느 메서드를 override해야할지도 알기 어렵다.
- 또한 하나의 일반 뷰만 상속할 수 있다는 것에 유의한다. 즉, `View`로부터 상속받을 수 있는 클래스는 단 하나이며 (만약 있다면) 다른 것은 mixin이어야 한다. 두 개 이상의 클래스를 `View`에서 상속받으려고 하는 것(가령, 리스트 가장 위의 폼을 사용하고 *ProcessFormView*와 *ListView*를 결합하는 것)은 예상대로 동작하지 않을 것이다.
<br><br>

## 클래스 기반 뷰로 폼 다루기
폼을 다루는 기본적인 함수 기반 뷰는 대략 다음과 같다.
```python
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import MyForm

def myview(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/success/')
    else:
        form = MyForm(initial={'key': 'value'})

    return render(request, 'form_template.html', {'form': form})
```
같은 역할을 하는 클래스 기반 뷰는 다음과 같을 것이다.
```python
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from .forms import MyForm

class MyFormView(View):
    form_class = MyForm
    initial = {'key': 'value'}
    template_name = 'form_template.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/success/')
        
        return render(request, self.template_name, {'form': form})
```
<br><br>

## 클래스 기반 뷰에 데코레이터 사용하기
클래스 기반 뷰의 확장은 mixin 사용에 한정되지 않는다. 데코레이터 또한 사용할 수 있다. 클래스 기반 뷰가 함수가 아니므로, `as_view()`를 사용하거나 서브 클래스를 생성하는가에 따라 데코레이터를 사용하는 것이 다르게 동작한다.

### URLconf에 데코레이터 사용하기
`as_view()` 메서드의 결과에 데코레이터를 사용하는 것으로 클래스 기반 뷰를 조정할 수 있다. 이를 가장 쉽게 할 수 있는 곳은 뷰 함수를 전개하는 URLconf이다.
```python
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView

from .views import VoteView

urlpatterns = [
    path('about/', login_required(TemplateView.as_view(template_name='secret.html'))),
    path('vote/', permission_required('polls.can_vote')(VoteView.as_view())),
]
```
이러한 접근은 인스턴스 단위로 데코레이터를 적용한다. 만약 뷰의 모든 인스턴스에 데코레이터를 사용하려면 다른 방식으로 접근해야 한다.

### 클래스에 데코레이터 사용하기
클래스 기반 뷰의 모든 인스턴스에 데코레이터를 사용하려면 클래스 정의 자체에 데코레이터를 사용해야 한다. 이렇게 하면 클래스의 `dispatch()` 메서드에 데코레이터를 적용하게 된다.

클래스의 메서드는 단독 함수와 크게 같은 편은 아니므로 메서드에 그냥 데코레이터를 적용할 수는 없다. 메서드 데코레이터에 먼저 옮겨야 한다. 데코레이터 `method_decorator`는 함수 데코레이터를 메서드 데코레이터로 변환시켜 인스턴스 메서드에서 사용할 수 있게 한다.

```python
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

class ProtectedView(TemplatedView):
    template_name = 'secret.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
```

또는 좀 더 간결하게 대신 클래스에 데코레이터를 사용하고 키워드 인수 이름으로 데코레이터를 사용할 메서드의 이름을 전달할 수 있다.

```python
@method_decorator(login_required, name='dispatch')
class ProtectedView(TemplateView):
    template_name = 'secret.html'
```

여러 곳에서 사용되는 공통의 데코레이터 집합이 있는 경우 데코레이터 리스트 또는 튜플을 정의하고 `method_decorator()`를 여러 번 호출하는 대신 그것을 사용할 수 있다. 다음의 두 클래스는 동일하다.

```python
decorators = [never_cache, login_required]

@method_decorator(decorators, name='dispatch')
class ProtectedView(TemplateView):
    template_name = 'secret.html'

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
class ProtectedView(TemplateView):
    template_name = 'secret.html'
```

데코레이터 집합은 데코레이터로 전달된 순서대로 요청을 처리할 것이다. 위의 예시에서 `never_cache()` 먼저 요청을 처리하고 `login_required()`가 그 다음에 요청을 처리한다.

위의 예시에서 `ProtectedView`의 모든 인스턴스는 로그인을 필요로 한다. 여기서는 `login_required`를 사용했지만 `LoginRequiredMixin`을 사용해도 같은 결과를 얻을 수 있다.

`method_decorator`는 클래스 안의 대상이 되는 메서드에 인수로 `*args`와 `**kwargs`를 전달한다. 만약 메서드가 호환되는 인수 집합을 받아들이지 못한다면 `TypeError` 예외가 발생할 것이다.
<br><br>

# [Built-in class-based generic views](https://docs.djangoproject.com/en/3.2/topics/class-based-views/generic-display/)

웹 어플리케이션을 작성하는 것은 특정 패턴을 계속 반복하고 반복하기 때문에 단조로울 수 있다. Django는 모델과 템플릿 레이어에서 그런 단조로움을 덜어내려고 노력하지만 웹 개발자는 뷰 레벨에서도 그러한 지루함을 경험한다.

Django의 *generic views*는 이런 고통을 경감하기 위해 개발되었다. 뷰 개발에서 발견한 특정한 공통 양식과 패턴을 가지고 추상화 시켜 너무 많은 코드를 작성하지 않고도 빠르게 데이터의 공통적인 뷰를 작성할 수 있게 한다.

객체 리스트를 보이는 것과 같이 특정한 공통 작업을 인식하고 어떤 객체의 리스트라도 출력할 수 있는 코드를 작성할 수 있다. 그러면 그 모델은 *URLconf*에 추가 인수로 전달될 수 있다.

Django는 다음의 동작을 위해 generic view를 제공한다.

- 리스트와 하나의 객체를 위한 상세 페이지 출력. 만약 컨퍼런스 관리를 위한 어플리케이션을 제작 중일 때 리스트 뷰의 예시로는 `TalkListView`와 `RegisteredUserListView`가 있다. 하나의 발표 페이지는 *상세* 뷰의 예시가 된다.
- 연/월/일 기록 페이지의 날짜 기반 객체, 연관된 상세 정보, 그리고 *최신* 페이지를 나타낸다.
- 권한을 가지고, 혹은 가지지 않고 사용자가 객체를 생성하거나 수정하거나 삭제할 수 있게 한다.

종합하면, 이러한 뷰는 개발자가 직면하는 가장 일반적인 작업을 수행할 수 있는 인터페이스를 제공한다.
<br><br>

## Generic View 확장하기
Generic view를 사용하면 개발 속도를 크게 높일 수 있다. 그러나 대부분의 프로젝트에서는 generic view만으로는 더이상 충분하지 않은 순간이 온다. 사실 새로운 Django 개발자들이 가장 많이 하는 질문은 더 다양한 상황을 다루는 generic view를 어떻게 만들 수 있는가이다.

이는 1.3 버전에서 generic view가 재설계된 이유 중 하나이다. 이전의 generic view는 혼란스러운 옵션 배열을 가진 뷰 함수였다. 현재, 많은 양의 설정을 URLconf에서 전달하는 것보다 generic view를 확장시키는 권장하는 방법은 서브클래스를 만들고 속성이나 메서드를 override하는 것이다.

Generic view에는 한계가 있다. 뷰를 generic view의 서브클래스로 구현하는 것이 어렵다면 사용자 정의 클래스 기반 혹은 함수 기반 뷰를 사용해 필요한 코드를 직접 작성하는 것이 더 효율적일 수 있다.

Generic view의 더 많은 예시는 서드파티 어플리케이션에서 확인하거나 사용자가 필요한 것을 직접 작성할 수 있다.
<br><br>

## 객체의 Generic View
`TemplateView`는 확실히 유용하지만 Django의 generic view는 사용자 데이터베이스 내용 뷰를 만들 때 빛을 본다. 일반적인 작업이므로 Django는 객체의 리스트와 상세 뷰를 생성하는데 도움을 주기 위해 몇 개의 빌트인 generic view를 제공한다.

객체의 리스트나 각 개체를 보여주는 예시를 통해 알아보자.

이러한 모델을 사용한다.

```python
# models.py
from django.db import models

class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    class Meta:
        ordering = ['-name']
    
    def __str__(self):
        return self.name


class Author(models.Model):
    salutation = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    headshot = models.ImageField(upload_to='author_headshots')

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField('Author')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    publication_date = models.DateField()
```

뷰를 정의한다.

```python
# views.py
from django.views.generic import ListView
from books.models import Publisher

class PublisherListView(ListView):
    model = Publisher
```

마지막으로 url에 뷰를 연결한다.

```python
# urls.py
from django.urls import path
from book.views import PublisherListView

urlpatterns = [
    path('publishers/', PublisherListView.as_view()),
]
```

템플릿 작성을 해야하지만, 이것이 작성해야 할 파이썬 코드의 전부다. 뷰에 `template_name` 속성을 더해 어느 템플릿을 사용할지 명시할 수도 있지만 명시적으로 템플릿을 언급하지 않는다면 Django는 객체 이름으로부터 템플릿을 찾을 것이다.

이 경우, 템플릿은 `books/publisher_list.html`이 될 것이다. `books`는 모델을 정의하는 앱의 이름으로부터, `publisher`는 모델의 이름을 소문자화 한 것으로부터 유래한다.

그러므로 `TEMPLATES`의 `DjangoTemplates` 벡엔드의 `APP_DIRS` 옵션이 `True`로 설정되었을 때 위 예시에서의 템플릿 위치는 다음과 같다:<br>
`path/to/project/books/templates/books/publisher_list.html`

이 템플릿은 모든 publisher 객체를 포함하는 `object_list` 변수를 포함하는 컨텍스트에 대해 렌더링된다. 템플릿은 대략 이렇게 생겼다.

```html
{% extends "base.html" %}

{% block content %}
  <h2>Publishers</h2>
  <ul>
    {% for publisher in object_list %}
      <li>{{ publisher.name }}</li>
    {% endfor %}
  </ul>
{% end block %}
```

이게 전부다. Generic view의 모든 멋진 특징은 generic view의 속성 집합을 변경하는 데에서 온다. [Generic view 참고 문서](https://docs.djangoproject.com/en/3.2/ref/class-based-views/)는 모든 generic view와 그 옵션을 상세히 문서화한 것이다. 이 문서의 나머지는 generic view 확장과 커스터마이징을 할 수 있는 몇 가지 일반적인 방법을 소개한다.

### *친절한* 템플릿 컨텍스트 만들기
예시로 만든 출판사 리스트 템플릿은 모든 출판사를 `object_list` 변수에 저장한다. 동작에는 문제가 없어보이지만 작가 템플릿을 만드는 데에는 *친절*해보이지 않는다. 출판사 관련해서는 여기서 작업을 해야한다는 것을 *그냥* 알아야만 한다.

만약 모델 객체를 다루고 있다면 이건 이미 끝난 일이다. 객체 또는 queryset을 다루는 중이라면 Django는 모델 클래스 이름의 소문자화 된 버전을 사용해 컨텍스트를 옮길 수 있다. 기본적인 `object_list` 엔트리에 더해 제공되지만 `publisher_list`와 같이 정확히 같은 데이터를 포함한다.

만약 이것이 여전히 좋은 짝이 아니라면 수동으로 컨텍스트 변수의 이름을 정할 수 있다. Generic view의 `context_object_name` 속성은 사용하려는 컨텍스트 변수를 구체화한다.

```python
# views.py
from django.views.generic import ListView
from books.models import Publisher

class PublisherListView(ListView):
    model = Publisher
    context_object_name = 'my_favorite_publishers'
```

유용한 `context_object_name`을 제공하는 것은 좋은 발상이다. 템플릿을 설계하는 동료들이 고마워 할 것이다.

### 추가적인 컨텍스트 더하기
때로 generic view에서 제공되는 것 이상의 추가 정보를 나타낼 필요가 있다. 예를 들어 각 출판사 상세 페이지의 모든 책의 리스트를 나타내는 것을 생각해보자. `DetailView` generic view는 컨텍스트에 출판사를 제공하겠지만 그 템플릿에서 어떻게 추가 정보를 얻을 수 있을까?

`DetailView`에 서브클래스를 만들고 `get_context_data`메서드를 구현해 제공하는 방법이 있다. 기본 구현은 템플릿에 표출되는 객체를 추가하지만 좀 더 많이 보낼 수 있게 override할 수 있다.

```python
from django.views.generic import DetailView
from books.models import Book, Publisher

class PublisherDetailView(DetailView):
    model = Publisher

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['book_list'] = Book.objects.all()
        return context
```

일반적으로 `get_context_data`는 부모 클래스의 컨텍스트 데이터와 현 클래스의 컨텍스트 데이터를 병합할 것이다. 컨텍스트를 바꾸고 싶은 사용자 정의 클래스의 이런 특성을 보존하고 싶다면 `super` 클래스의 `get_context_data`를 호출해야 한다. 같은 키를 정의하려는 두 클래스가 있는게 아니라면 이는 예상된 결과를 제공할 것이다. 그러나 만약 부모 클래스가 키를 설정한 후(super를 호출한 이후)에 어떤 클래스가 그 키를 override하려고 한다면 그 클래스의 자식 클래스 또한 super 이후에 모든 상위 클래스를 override할 것인지 명시적으로 설정해야 한다. 만약 문제가 있다면 뷰의 메서드 순서를 확인한다.

클래스 기반 뷰의 컨텍스트 데이터가 이전에 컨텍스트를 제공한 것의 데이터를 override한다는 점 또한 고려해야 한다. 예시를 보려면 [`get_context_data()`](https://docs.djangoproject.com/en/3.2/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_context_data)를 확인한다.

### 객체의 하위집합 view
지금까지 사용하고 있던 `model` 인수를 확인해보자. 뷰가 동작할 데이터베이스 모델을 구체화하는 `model` 인수는 하나의 객체 또는 객체의 모음 위에서 동작하는 모든 generic view에서 사용할 수 있다. 그러나 뷰가 동작할 객체를 명시아는 방법에는 `model` 인수만 있는 것은 아니다. `queryset` 인수를 사용해서 객체의 리스트를 명시하는 방법도 있다.

```python
from django.views generic import DetailView
from books.models import Publisher

class PublisherDetailView(DetailView):
    context_object_name = 'publisher'
    queryset = Publisher.objects.all()
```

`model = Publisher`라 명시하는 것은 `queryset = Publisher.objects.all()`을 더 간결하게 표현하는 것이다. 그런데 객체의 필터링된 리스트를 정의하기 위해 `queryset`을 사용하면 뷰에서 볼 수 있는 객체를 더 구체화할 수 있다. ([`QuerySet`](https://docs.djangoproject.com/en/3.2/ref/models/querysets/#django.db.models.query.QuerySet) 객체에 관한 더 많은 정보를 보려면 [Making queries](https://docs.djangoproject.com/en/3.2/topics/db/queries/)를, 디테일 완성을 위해서는 [classed-based views reference](https://docs.djangoproject.com/en/3.2/ref/class-based-views/) 참조)

예시를 들기에 앞서, 책 리스트를 출판일자 내림순으로 정렬한다.

```python
from django.views.generic import ListView
from books.models import Book

class BookListView(ListView):
    queryset = Book.objects.order_by('-publication_date')
    context_object_name = 'book_list'
```

최소한의 예시이지만 발상을 멋지게 묘사했다. 보통 객체를 재정렬 하는 것보다 더 많은 것을 원할 것이다. 만약 특정 출판사에서 나온 책의 리스트를 구하고 싶다면 다음 방법을 사용한다.

```python
from django.views.generic import ListView
from books.models import Book

class AcmeBookListView(ListView):
    context_object_name = 'book_list'
    queryset = Book.objects.filter(publisher__name='ACME Publishing')
    template_name = 'books/acme_list.html'
```

필터링된 `queryset`과 더불어 사용자 정의 템플릿 이름을 사용할 수 있다. 만약에 그렇게 하지 않는다면 generic view는 *바닐라* 객체 리스트와 같은 템플릿을 선택할 것이고, 그것은 사용자가 별로 원하지 않는 일일 수 있다.

또한 이것은 출판사-특정 책 리스트를 구하는데 썩 고상하지 못한 방법이다. 만약 다른 출판사 페이지를 추가하고 싶다면 URLconf에 또다른 몇 줄을 작성해야 할 것이고, 그게 단순히 몇 개 수준이 아닌 더 많은 수의 출판사라면 합리적이지 못할 것이다. 다음 섹션에서 이 문제를 다룰 것이다.

만약 `/books/acme/`를 요청했을 때 404 에러가 발생한다면, 리스트 속 출판사 이름이 정확히 *ACME Publising*인지 확인한다. Generic view는 이런 경우를 위해 `allow_empty` 인수를 가지고 있다. 더 자세한 사항은 [class-based views reference](https://docs.djangoproject.com/en/3.2/ref/class-based-views/) 참조.

### 동적 필터링
또다른 일반적인 요구사항은 리스트 페이지에 주어진 객체들을 URL 안의 어떤 키로 필터링하는 것이다. 앞에서는 URLconf 안의 출판사 이름을 하드코딩했는데 만약 어떤 임의의 출판사의 책을 전부 출력하는 뷰를 작성하고 싶다면 어떻게 해야할까?

편리하게도, `ListView`는 override 할 수 있는 `get_queryset()` 메서드를 가진다. 기본적으로, 이는 `queryset` 속성의 값을 반환하지만 좀 더 논리를 추가할 수 있다.

이 작업의 가장 중요한 부분은 클래스 기반 뷰가 호출되었을 때 다양한 유용한 것들이 `self`에 저장이 된다는 것이다. 또한 위치에 관한 `(self.args)`와 이름에 기반한 `(self.kwargs)` 인수를 포함하는 요청 `(self.request)`는 URLconf에서 포착할 수 있다.

여기 하나의 포착된 그룹이 있는 URLconf가 있다.

```python
# urls.py
from django.urls import path
from books.views import PublisherBookListView

urlpatterns = [
    path('books/<publisher>/', PublisherBookListView.as_view()),
]
```

다음으로는 `PublisherBookListView`를 작성한다.

```python
# views.py
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from books.models import Book, Publisher

class PublishserBookListView(ListView):
    template_name = 'books/books_by_publisher.html'

    def get_queryset(self):
        self.publisher = get_object_or_404(Publisher, name=self.kwargs['publisher'])
        return Book.objects.filter(publisher=self.publisher)
```

Queryset 선택을 위해 논리를 추가하는데 `get_queryset`을 사용하는 것은 강력한 만큼 편리하다. 예를 들어 만약 원한다면 현재 사용자를 이용해 필터링하기 위해 `self.request.user`를 사용하거나 다른 더 복잡한 논리를 사용할 수 있다.

또한 동시에 출판사를 컨텍스트에 추가해 템플릿에서 사용하게 할 수도 있다.

```python
# ...

def get_context_data(self, **kwargs):
    # call the base implementation first to get a context
    context = super().get_context_data(**kwargs)
    # Add in the publisher
    context['publisher'] = self.publisher
    return context
```

### 추가 작업 수행하기
마지막 일반적인 패턴은 generic view 호출 이전이나 이후에 추가적인 작업을 필요로 한다.

`Author` 모델에 누군가가 언제 마지막으로 그 작가에 관해 살펴봤는지 추적하기 위한 `last_accessed` 필드가 존재한다고 하자.

```python
# models.py
from django.db import models

class Author(models.Model):
    salutation = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    headshot = models.ImageField(upload_to='author_headshots')
    last_accessed = models.DateTimeField()
```

Generic `DetailView` 클래스는 이 필드에 관해서는 아무것도 모르지만 그 필드의 갱신 상태를 유지하기 위해 사용자 정의 뷰를 작성할 수 있다.

먼저 사용자 정의 뷰를 가리키기 위해 URLconf에 작가 상세를 추가할 필요가 있다.

```python
from django.urls import path
from book.views import AuthorDetailView

urlpatterns = [
    #...
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
]

그 다음 새로운 뷰를 작성한다. (`get_object`는 객체를 찾기 위한 메서드이다.) 그러면 이를 override하고 호출을 감쌀 수 있다.

```python
from django.utils import timezone
from django.views.generic import DetailView
from books.models import Author

class AuthorDetailView(DetailView):
    queryset = Author.objects.all()

    def get_object(self):
        obj = super().get_object()
        # Record the last accessed date
        obj.last_accessed = timezone.now()
        obj.save()
        return obj
```

여기 있는 URLconf는 `pk`라는 이름의 그룹을 사용한다. 이 이름은 `DetailView`가 queryset을 필터링할 때 사용하는 기본 키의 값을 찾는데 사용하는 기본 이름이다.

만약 그룹을 다르게 호출하고 싶다면 뷰에서 [`pk_url_kwarg`](https://docs.djangoproject.com/en/3.2/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.pk_url_kwarg)를 설정할 수 있다.
<br><br>

# [Form handling with class-based views](https://docs.djangoproject.com/en/3.2/topics/class-based-views/generic-editing/)
폼 처리에는 보통 세 가지 갈래가 있다.
- 초기 GET (비어있거나 작성 전인 폼)
- 유효하지 않은 데이터를 가진 POST (보통 에러를 표기해 폼을 다시 보여준다)
- 유효한 데이터를 가진 POST(데이터를 처리하고 보통 리다이렉트한다)
이를 직접 구현하는 것은 때로 수 많은 반복된 형식적인 코드([Using a form in a view](https://docs.djangoproject.com/en/3.2/topics/forms/#using-a-form-in-a-view) 참조)를 작성하게 한다. 이런 상황을 피하기 위해 Django는 폼 처리를 위한 generic 클래스 기반 뷰의 모음을 제공한다.
<br><br>

## Basic forms
주어진 연락 폼

```python
# forms.py
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass
```

뷰는 `FormView`를 사용해 작성할 수 있다.

```python
# views.py
from myapp.forms import ContactForm
from django.views.generic.edit import FormView

class ContactFormView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)
```

- `FormView`는 `TemplateResponseMixin`을 상속하므로 `template_name`을 사용할 수 있다.
- `form_valid()`의 기본 구현은 단순히 `success_url`로 리다이렉트하는 것이다.
<br><br>

## Model forms
Generic View는 모델과 함께 사용할 때 빛을 본다. Generic view는 어떤 모델 클래스를 사용할지 확인할 수 있는 동안에는 자동으로 `ModelForm`을 생성한다.

- 만약 `model` 속성이 주어졌다면 그 모델을 사용한다.
- 만약 `get_object`가 객체를 반환한다면 그 객체의 클래스를 사용한다.
- 만약 `queryset`이 주어졌다면 그 queryset의 모델을 사용한다.

모델 폼 뷰는 모델을 자동으로 저장하는 `form_valid()` 구현을 제공한다. 만약 다른 요구사항이 있다면 override할 수 있다. 아래에 예시가 있다.

`CreateView`나 `UpdateView`를 위해 `success_url`을 제공할 필요도 없다. 만약 사용가능하다면 모델 객체의 `get_absolute_url()`을 사용할 것이다.

만약 사용자 정의 `ModelForm`(예를 들어 추가적인 유효성을 더하고 싶을 때)을 사용하고 싶다면 뷰에 `form_class`를 설정한다.

사용자 정의 폼 클래스를 명시할 때 `form_class`가 `ModelForm`일지라도 모델을 명시해야 한다.

먼저 `Author` 클래스에 `get_absolute_url()`을 추가해야 한다.
```python
# models.py
from django.db import models
from django.urls import reverse

class Author(models.Model):
    name = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'pk': self.pk})
```

그 다음 `CreateView`와 친구들을 실제 작업에 사용할 수 있다. 여기서는 그저 generic 클래스 기반 뷰를 설정할 뿐이다. 논리를 직접 작성할 필요가 없다.

```python
# views.py
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from myapp.models import Author

class AuthorCreateView(CreateView):
    model = Author
    fields = ['name']

class AuthorUpdateView(UpdateView):
    model = Author
    fields = ['name']

class AuthorDeleteView(DeleteView):
    model = Author
    success_url = reverse_lazy('author-list')
```

파일을 가져올 때 url이 로드되지 않기 때문에 `reverse()` 대신 `reverse_lazy()`를 사용한다.

`fields` 속성은 `ModelForm`의 내부 `Meta` 클래스의 `fields` 속성과 같은 방식으로 작동한다. 폼 클래스를 다른 방식으로 정의하는 것이 아니라면 이 속성이 요구되며 없을 때에는 뷰가 `ImproperlyConfigured` 예외를 발생시킬 것이다.

만약 `fields`와 `form_class` 둘 다 명시한다면 `ImproperlyConfigured` 예외가 발생할 것이다.

마지막으로 URLconf에 새로운 뷰를 연결한다.

```python
# urls.py
from django.urls import path
from myapp.views import AuthorCreateView, AuthorDeleteView, AuthorUpdateView

urlpatterns = [
    # ...
    path('author/add/', AuthorCreateView.as_view(), name='author-add'),
    path('author/<int:pk>/', AuthorUpdateView.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', AuthorDeleteView.as_view(), name='author-delete'),
]
```

이러한 뷰는 `template_name`을 모델 기반으로 생성하기 위해 `template_name_suffix`를 사용하는 `SingleObjectTemplateResponseMixin`을 상속한다.

이 예시에서는

- `CreateView`와 `UpdateView`는 `myapp/author_form.html`을 사용한다.
- `DeleteView`는 `myapp/author_confirm_delete.html`을 사용한다.

만약 `CreateView`와 `UpdateView`의 템플릿을 분리하고 싶다면 뷰 클래스에 `template_name`이나 `template_name_suffix`를 설정하면 된다.
<br><br>

## Models and request.user
`CreateView`를 사용해 객체를 생성한 사용자를 추적하기 위해 사용자 정의 `ModelForm`을 사용할 수 있다. 먼저 모델에 외래 키를 추가한다.

```python
# models.py
from django.contrib.auth.models import User
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # ...
```

뷰에서 수정할 필드 목록에 `created_by`를 추가하지 않았는지 확인하고 사용자를 추가하기 위해 `form_valid()`를 override한다.

```python
# views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from myapp.models import Author

class AuthorCreateView(LoginRequiredMixin, CreateView):
    model = Author
    fields = ['name']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
```

`LoginRequiredMixin`은 로그인하지 않은 사용자가 폼에 접근하는 것을 방지한다. 이를 제외한다면 `form_valid()`에서 권한이 없는 사용자를 다루어야 한다.
<br><br>

## Content negotiation example
*일반* 양식 POST 뿐만 아니라 API 기반 워크플로우에서도 작동하는 폼을 구현하는 방법을 보여주는 예시이다.
```python
from django.http import JsonResponse
from django.views.generic.edit import CreateView
from myapp.models import Author

class JsonableResponseMixin:
    # Mixin to add JSON support to a form.
    # Must be used with an object-based FormView (e.g. CreateView)
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            return JsonResponse(form.errors, status=400)
    
    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing
        # (in the case of CreateView, it will call form.save())
        response = super().form_valid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)

class AuthorCreateView(JsonableResponseMixin, CreateView):
    model = Author
    fields = ['name']