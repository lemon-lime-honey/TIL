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
```
<br><br>

# [Using mixins with class-based views](https://docs.djangoproject.com/en/3.2/topics/class-based-views/mixins/)
Django의 클래스 기반 뷰는 많은 기능을 제공하지만 부분적으로만 사용하고 싶을 수 있다. 예를 들어, HTTP 응답을 생성하기 위해 템플릿을 렌더링하는 뷰를 써야 하는데 [`TemplateView`](https://docs.djangoproject.com/en/3.2/ref/class-based-views/base/#django.views.generic.base.TemplateView)를 사용할 수 없는 상황이다. `GET`이 나머지 동작을 하고, `POST`에서만 템플릿을 렌더링 해야할 수도 있다. [`TemplateResponse`](https://docs.djangoproject.com/en/3.2/ref/template-response/#django.template.response.TemplateResponse)를 직접적으로 사용할 수 있지만 코드가 중복된다.

이러한 이유로 Django는 좀 더 분리된 기능을 제공하는 몇 개의 mixin을 제공한다. 예를 들어 템플릿 렌더링은 [`TemplateResponseMixin`](https://docs.djangoproject.com/en/3.2/ref/class-based-views/mixins-simple/#django.views.generic.base.TemplateResponseMixin)으로 압축된다. Django 참고문서는 [모든 mixin에 관한 문서](https://docs.djangoproject.com/en/3.2/ref/class-based-views/mixins/)를 포함한다.

## 컨텍스트와 템플릿 응답
클래스 기반 뷰에서 템플릿을 다루기 위한 일관된 인터페이스를 제공하는데 도움이 되는 두 개의 중심 mixin이 제공된다.

### [`TemplateResponseMixin`](https://docs.djangoproject.com/en/3.2/ref/class-based-views/mixins-simple/#django.views.generic.base.TemplateResponseMixin)
`TemplateResponse`를 반환하는 모든 빌트인 뷰는 `TemplateResponseMixin`이 제공하는 `render_to_response()` 메서드를 호출한다. 대개 사용자를 위해 호출될 것이다. (예를 들어 `TemplateView`와 `DetailView` 둘 모두에 의해 구현되는 `get()` 메서드에 의해 호출된다.) 비슷하게, 응답이 Django 템플릿을 통해 렌더링되지 않는 것을 반환하게 하고 싶어 override하고 싶더라도 그럴 필요가 없다. 이 예시를 보려면 [JSONResponseMixin example](https://docs.djangoproject.com/en/3.2/topics/class-based-views/mixins/#jsonresponsemixin-example)을 확인한다.

`render_to_response()`는 기본적으로 클래스 기반 뷰에서 `template_name`을 조회하는 `get_template_names()`를 호출한다. 두 개의 다른 mixin([`SingleObjectTemplateResponseMixin`](https://docs.djangoproject.com/en/3.2/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectTemplateResponseMixin)과 [`MultipleObjectTemplateResponseMixin`](https://docs.djangoproject.com/en/3.2/ref/class-based-views/mixins-multiple-object/#django.views.generic.list.MultipleObjectTemplateResponseMixin))은 실제 객체를 다룰 때 좀 더 유연한 기본값을 제공하기 위해 이를 override한다.

### [`ContextMixin`](https://docs.djangoproject.com/en/3.2/ref/class-based-views/mixins-simple/#django.views.generic.base.ContextMixin)
템플릿을 렌더링(위의 `TemplateResponseMixin`을 포함하여)할 때와 같이 컨텍스트를 필요로 하는 모든 빌트인 뷰는 확인하고 싶은 모든 키워드 인자를 통과하게 하는 `get_context_data()`를 호출해야 한다. `get_context_data()`는 딕셔너리를 반환한다. `ContextMixin`은 자신의 키워드 인자를 반환하지만 딕셔너리의 원소를 더 추가하기 위해 이를 override하는 것이 일반적이다. [`extra_context`](https://docs.djangoproject.com/en/3.2/ref/class-based-views/mixins-simple/#django.views.generic.base.ContextMixin.extra_context) 속성을 사용할 수도 있다.

## Building up Django's generic class-based views
Django의 두 가지 generic 클래스 기반 뷰가 어떻게 분리된 기능을 제공하는 mixin을 조합하는지 알아본다. 객체의 *디테일* 뷰를 렌더링하는 [`DetailView`](https://docs.djangoproject.com/en/3.2/ref/class-based-views/generic-display/#django.views.generic.detail.DetailView)와 보통 queryset으로부터 객체의 리스트를 렌더링하고 paginate할 수도 있는 [`ListView`](https://docs.djangoproject.com/en/3.2/ref/class-based-views/generic-display/#django.views.generic.list.ListView)를 본다. 하나 혹은 여러 개의 Django 객체를 다룰 때 유용한 기능을 제공하는 네 개의 mixin에 대해 알게 될 것이다.

Generic edit 뷰([`FormView`](https://docs.djangoproject.com/en/3.2/ref/class-based-views/generic-editing/#django.views.generic.edit.FormView), 그리고 모델별 뷰인 [`CreateView`](https://docs.djangoproject.com/en/3.2/ref/class-based-views/generic-editing/#django.views.generic.edit.CreateView), [`UpdateView`](https://docs.djangoproject.com/en/3.2/ref/class-based-views/generic-editing/#django.views.generic.edit.UpdateView), [`DeleteView`](https://docs.djangoproject.com/en/3.2/ref/class-based-views/generic-editing/#django.views.generic.edit.DeleteView))나 날짜 기반 generic 뷰에 관한 mixin도 있다. 이들은 [mixin reference documentaion](https://docs.djangoproject.com/en/3.2/ref/class-based-views/mixins/)에서 다룬다.

### `DetailView`: working with a single Django object
객체의 디테일을 보여주려면 기본적으로 두 가지 일을 해야한다. 객체를 조회해야하고, 이를 컨텍스트로 갖는 적절한 템플릿으로 `TemplateResponse`를 생성해야 한다.

객체를 찾기 위해 `DetailView`는 요청의 URL에 기반해 객체를 찾는 `get_object()` 메서드(URLConf에서 선언된 `pk`와 `slug` 키워드 인자를 토대로 찾고, 뷰의 `model` 속성이나 `queryset` 속성이 있다면 이에 관해서도 조회한다)를 제공하는 `SingleObjectMixin`에 의존한다.

또한 `SingleObjectMixin`은 템플릿 렌더링을 위한 컨텍스트 데이터를 제공하기 위해 Django의 모든 빌트인 클래스 기반 뷰에서 사용되는 `get_context_data()`를 override한다.

그 다음에 `TemplateResponse`를 생성하기 위해 `DetailView`는 위에서 언급된 `get_template_names()`를 override하기 위해 `TemplateResponseMixin`을 확장한 `SingleObjectTemplateResponseMixin`을 사용한다. 꽤 정교한 선택사항 모음이지만 가장 많이 사용되는 것은 `<app_label>/<model_name>_detail.html`이다. 서브클래스에서 `template_name_suffix`를 설정하면 `_detail` 부분을 변경할 수 있다. (예를 들어, [generic edit views](https://docs.djangoproject.com/en/3.2/topics/class-based-views/generic-editing/)는 create, update 뷰에서는 `_form`을, delete 뷰에서는 `_confirm_delete'를 사용한다.)

### `ListView`: working with many Django objects
객체 리스트 또한 비슷한 패턴을 따라간다. 보통 `QuerySet`인 (아마도 paginate된) 객체 리스트가 필요하고, 그 객체 리스트를 사용하는 적절한 템플릿으로 `TemplateResponse`를 생성해야 한다.

객체를 찾기 위해 `ListView`는 `get_queryset()`과 `paginate_queryset()`을 제공하는 `MultipleObjectMixin`을 사용한다. `SingleObjectMixin`과는 다르게 목적하는 queryset을 찾기 위해 URL의 일부를 확인할 필요가 없으므로 기본적으로 뷰 클래스의 `queryset`이나 `model` 속성을 사용한다. 여기서 `get_queryset()`을 override`하는 일반적인 이유는 객체를 동적으로 변경하기 위함이다.

`MultipleObjectMixin`은 pagination을 위한 적절한 컨텍스트 변수를 포함하기 위해(pagination이 비활성화 된 경우 더미 제공) `get_context_data`를 override한다. 이는 `ListView`가 정렬하고 키워드 인자로 전달되는 `object_list`에 의존한다.

`TemplateResponse`를 생성하기 위해 `ListView`는 그 다음에 `MultipleObjectTemplateResponseMixin`을 사용한다. 위의 `SingleObjectTemplateResponseMixin`처럼 이 mixin 또한 가장 흔하게 쓰이는 `template_name_suffix` 속성으로 `_list`를 제거할 수 있는 `<app_label>/<model_name>_list.html`을 포함하는 [선택 조건의 범위](https://docs.djangoproject.com/en/3.2/ref/class-based-views/mixins-multiple-object/#django.views.generic.list.MultipleObjectTemplateResponseMixin)을 제공하기 위해 `get_template_names()`을 override한다. (날짜 기반 generic 뷰는 다양하게 특화된 날짜 기반 리스트 뷰를 위한 다른 템플릿을 사용하기 위해 `_archive`, `_archive_year`와 같은 접미사를 사용한다.)

## Using Django's class-based view mixins
주어진 mixind을 Django의 generic 클래스 기반 뷰가 어떻게 사용하는지 보았으니 이제 그것들을 조합하는 다른 방법을 알아보자. 빌트인 클래스 기반 뷰 혹은 다른 generic 클래스 기반 뷰와 조합할 것이지만 Django가 제공하는 것 이외의 해결할 수 있는 더 드문 문제가 있다.


### 경고
모든 mixin이 같이 사용될 수 있는 것은 아니며, 모든 generic 클래스 기반 뷰가 모든 다른 mixin과 사용될 수 있는 것도 아니다. 여기에서는 작동하는 몇 가지 예시만을 다룬다. 만약 다른 조합으로 다른 기능을 얻고 싶다면 사용하는 다른 클래스 간에 겹치는 속성과 메서드의 상호작용을 고려해야 하며 [메서드 결정 순서](https://www.python.org/download/releases/2.3/mro/) 어떤 버전의 메서드를 어떤 순서로 호출하는가에 어떻게 영향을 미치는지도 고려해야 한다.

Django의 [클래스 기반 뷰](https://docs.djangoproject.com/en/3.2/ref/class-based-views/)와 [클래스 기반 뷰 mixin](https://docs.djangoproject.com/en/3.2/ref/class-based-views/mixins/) 공식문서가 서로 다른 클래스와 mixin 사이에서 어느 속성과 메서드가 충돌을 일으킬 가능성이 있는지 이해할 수 있게 할 것이다.

의심스럽다면 그만 두고 작업을 `View`나 `TemplateView` 또는 `SingleObjectMixin`과 `MultipleObjectMixin`을 기반으로 수행한다. 코드를 더 작성하게 되겠지만 이후에 작업하는 사람이 더 명확하게 이해할 수 있으며 걱정할 상호작용은 더 적어 생각할 거리를 줄일 수 있다. (물론 문제 해결의 영감을 위해 언제든지 Django의 generic 클래스 기반 뷰 구현에 발을 들여도 된다.)

## Using `SingleObjectMixin` with `View`
`POST`에만 응답하는 클래스 기반 뷰를 작성하고 싶다면 `View`의 서브클래스를 만들고 그 안에서 `post()` 메서드를 작성하면 된다. 만약 URL로부터 식별된 특정 객체에 관한 작업을 진행하고 싶다면 `SingleObjectMixin`이 제공하는 기능을 사용한다.

[Generic class-based views introduction](https://github.com/lemon-lime-honey/TIL/blob/main/django/cbv.md#built-in-class-based-generic-views)에서 사용했던 `Author` 모델을 사용한다.

```python
# views.py

from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from books.models import Author

class RecordInterestView(SingleObjectMixin, View):
    """Records the current user's interest in an author."""
    model = Author

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        
        # Look up the author we're interested in.
        self.object = self.get_object()
        # Actually record interest somehow here!

        return HttpResponseRedirect(reverse('author-detail', kwargs={'pk': self.object.pk}))
```

실제로는 관계형 데이터베이스 대신 키-값 쌍에 저장하고 싶을 것이니 해당 부분은 생략한다. `SingleObjectMixin`을 사용할 때 뷰에 관해 걱정할 부분은 `self.get_object()`를 호출해 실행하는 관심 있는 작가를 조회하는 부분이다. 나머지는 mixin이 알아서 한다.

이를 URL에서 간단하게 연결할 수 있다.

```python
# urls.py

from django.urls import path
from books.views import RecordInterestView

urlpatterns = [
    ...
    path('author/<int:pk>/interest/', RecordInterestView.as_view(), name='author-interest'),
]
```

`get_object`가 `Author` 인스턴스를 조회하기 위해 사용하는 `pk`에 주의한다. `slug`나 `SingleObjectMixin`의 다른 특성을 사용할 수도 있다.

## Using `SingleObjectMixin` with `ListView`
`ListView`는 빌트인 pagination을 지원하지만 다른 객체에 (외래키로) 연결된 객체의 리스트를 paginate할 수도 있다. 출판 예시에서, 특정 출판사에서 출간된 책을 paginate해보자.

이를 구현하는 방법 중 하나는 `ListView'와 `SingleObjectMixin`을 조합하여 책의 paginate된 리스트의 queryset이 단일 객체로 발견된 출반사에 연결하는 것이다. 이렇게 하려면 두 개의 다른 queryset이 필요하다.

- `ListView`에서 사용하는 `Book` queryset<br>
  리스트로 만들고 싶은 책들의 `Publisher`에 접근해야 하므로, `get_queryset()`을 override하고 `Publisher`의 [역참조 매니저](https://docs.djangoproject.com/en/3.2/topics/db/queries/#backwards-related-objects)를 사용한다.
- `get_object()`에서 사용하는 `Publisher` queryset<br>
  알맞는 `Publisher` 객체를 가져오기 위해 `get_object()`의 기본 구현에 의존한다. 그러나 `queryset` 인자를 명시적으로 `pass`해야 하는데, 그렇게 하지 않으면 `get_object()`의 기본 구현이 `Publisher`가 아닌 `Book`개체를 반환하게 override한 `get_queryset()`을 호출하기 때문이다.
<br><br>

- note
`get_context_data()`에 관해서는 주의해야 한다. `SingleObjectMixin`과 `ListView` 둘 모두 `context_object_name`이 설정되었을 때 그 값 아래의 컨텍스트 데이터에 데이터를 넣을 것이기 때문에 대신 컨텍스트 데이터에 `Publisher`가 들어간다는 것을 명시한다. `ListView`는 사용자가 `super()`를 호출하는 것을 떠올린다면 알맞는 `page_obj`와 `paginator`를 추가할 것이다.
<br><br>

이제 새로운 `PublisherDetailView`를 작성할 수 있다.

```python
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from books.models import Publisher

class PublisherDetailView(SingleObjectMixin, ListView):
    paginate_by = 2
    template_name = "books/publisher_detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Publisher.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publisher'] = self.object
        return context

    def get_queryset(self):
        return self.object.book_set.all()
```

`get()`에서 `self.object`를 설정해 `get_context_data()`와 `get_queryset()`에서 다시 사용한 것에 주목한다. 만약 `template_name`을 정하지 않았다면 템플릿은 일반적인 `ListView` 선택에 의해 기본값이 정해질 것이다. 이 경우에는 책의 리스트이므로 `"books/book_list.html"`이 된다. `ListView`는 `SingleObjectMixin`에 관해서는 아무것도 모르기 때문에 이 뷰가 `Publisher`를 가지고 무얼 하는지 모른다.

pagination이 동작하는지 확인하기 위해 많은 책을 생성하지 않도록 이 예시에서 `paginate_by`는 의도적으로 작은 값을 가진다. 템플릿은 다음과 같다.

```html
{% extends "base.html" %}

{% block content %}
  <h2>Publisher {{ publisher.name }}</h2>

  <ol>
    {% for book in page_obj %}
      <li>{{ book.title }}</li>
    {% endfor %}
  </ol>

  <div class="pagination">
    <span class="step-links">
      {% if page_obj.has_previous %}
        <a href="?page={{ page_obj.previous_page_number }}">previous</a>
      {% endif %}

      <span class="current">
        Page {{ page_obj.number }} of {{ paginator.num_pages }}.
      </span>

      {% if page_obj.has_next%}
        <a href="?page={{ page_obj.next_page_number }}">next</a>
      {% endif %}
    </span>
  </div>
{% endblock %}
```

## Avoid anything more complex
일반적으로 `TemplateResponseMixin`과 `SingleObjectMixin`의 기능이 필요하면 이를 사용할 수 있다. 위에서 보듯이, 약간의 주의를 기울이면 `SingleObjectMixin`과 `ListView`를 조합해 사용할 수도 있다. 그러나 그렇게 할 수록 더 복잡해지기 때문에 다음을 염두에 두는게 좋다.

- Hint<br>
  각각의 뷰는 오직 detail, list, editing, date처럼 한 종류의 generic 클래스 기반 뷰의 종류에 속한 mixin이나 view를 사용해야 한다. 예를 들어 `TemplateView`(빌트인 뷰)와 `MultipleObjectMixin`(generic list)를 조합하는 것은 괜찮지만 `SingleObjectMixin`(generic detail)과 `MultipleObjectMixin`(generic list)를 조합하면 문제가 발생할 수 있다.

더 복잡해질 때 무슨 일이 일어나는지 보기 위해 더 단순한 해결책에는 존재했던 가독성과 유지가능성을 희생한 예시를 살펴본다. 처음에는 `DetailView`와 `FormMixin`을 조합해 `DetailView`를 사용해 객체를 보여주는 URL을 통해 Django `Form`을 `POST`하려는 시도를 본다.

### Using `FormMixin` with `DetailView`
`View`와 `SingleObjectMixin`을 사용했던 이전의 예시를 돌이켜보자. 특정 작가에 대한 사용자의 관심을 기록하고 있었다. 왜 사용자들이 작가들을 좋아하는지 메시지를 남기기를 원한다고 하자. 또다시, 관계형 데이터베이스가 아닌 여기서 걱정하지 않을 더 난해한 것에 저장한다고 가정한다.

이 지점에서, 사용자의 브라우저가 Django로 보낸 정보를 압축하기 위한 폼에 도달하는 것은 자연스러운 일이다. 또한 REST에 많이 신경썼기 때문에 작가를 보여줄 때와 사용자의 메시지를 포착할 때 같은 URL을 사용하려고 한다. 그렇게 하기 위해 `AuthorDetailView`를 다시 작성한다.

템플릿에서 렌더링 할 수 있도록 컨텍스트 데이터를 폼에 추가하게 되겠지만 `DetailView`의 `GET` 처리는 남겨둘 것이다. 또한 `FormMixin`이 폼 처리를 하게 하고 약간의 코드를 작성해 `POST`에서 폼이 적절하게 호출되게 한다.

- Note<br>
  (이미 적당한 `post()`를 제공하는 )`DetailView`와 `FormView`를 조합하는 대신 `FormMixin`를 사용해 `post()`를 구현하는데, 이는 둘 다 `get()`을 구현하므로 그렇게 하면 더 혼란스럽기 때문이다.

새로운 `AuthorDetailView`는 다음과 같다.

```python
# CAUTION: you almost certainly do not want to do this.
# It is provided as part of a discussion of problems you can
# run into when combining different generic class-based view
# functionality that is not designed to be used together.

from django import forms
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from books.models import Author

class AuthorInterestForm(forms.Form):
    message = forms.CharField()

class AuthorDetailView(FormMixin, DetailView):
    model = Author
    form_class = AuthorInterestForm

    def get_success_url(self):
        return reverse('author-detail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        # Here, we would record the user's interest using the message
        # passed in form.cleaned_data['message']
        return super().form_valid(form)
```

`get_success_url()`은 리다이렉트 되는 위치를 제공하며, 이는 `form_valid()`의 기본 구현에 사용된다. 앞서 말한 `post()`를 직접 구현해 제공해야 한다.

### A better solution
`FormMixin`과 `DetailView`의 미묘한 상호작용은 이들을 다루는 능력을 시험한다. 이런 종류의 클래스를 작성하고 싶어하는 경우는 드물 것이다.

이 경우, `Form`을 다루는 코드를 작성하는 것이 많은 중복을 일으킬지라도 `DetailView`를 유일한 generic 기능으로 남겨두고 직접 `post()` 메서드를 작성할 수 있다.

또는, 별다른 문제 없이 `DetailView`와 구분되는 `FormView`를 사용할 수 있게 폼을 처리하는 분리된 뷰를 작성하는 것이 위의 접근방식보다 작업량이 적다.

### An alternative better solution
여기서는 같은 URL에 연결된 두 개의 다른 클래스 기반 뷰를 사용할 것이다. 그렇게 해보자. 여기에는 아주 명확한 구분이 있다. `GET` 요청은 컨텍스트 데이터에 `Form`을 추가하는 `DetailView`를, `POST` 요청은 `FormView`를 가져와야 한다. 이 뷰 먼저 작성한다.

`AuthorDetailView`는 [처음으로 AuthorDetailView](https://github.com/lemon-lime-honey/TIL/blob/main/django/cbv.md#%EC%B6%94%EA%B0%80-%EC%9E%91%EC%97%85-%EC%88%98%ED%96%89%ED%95%98%EA%B8%B0)를 도입했을 때와 거의 같다. 템플릿에 사용 가능한 `AuthorInterestForm`을 만들기 위해 `get_context_data()`를 직접 써야 한다. 명확함을 위해 `get_object()`를 override하는 것은 생략한다.

```python
from django import forms
from django.views.generic import DetailView
from books.models import Author

class AuthorInterestForm(forms.Form):
    message = forms.CharField()

class AuthorDetailView(DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AuthorInterestForm()
        return context
```

이제 `AuthorInterestForm`은 `FormView`이지만 찾는 작가를 조회하기 위해 `SingleObjectMixin`을 가져와야 하고 `template_name`을 설정해 폼 에러가 `AuthorDetailView`가 `GET`에서 사용하는 것과 같은 템플릿을 렌더링하게 한다.

```python
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin

class AuthorInterestFormView(SingleObjectMixin, FormView):
    template_name = 'books/author_detail.html'
    form_class = AuthorInterestForm
    model = Author

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('author-detail', kwargs={'pk': self.object.pk})
```

마지막으로, 새로운 `AuthorView`에 이를 가져온다. 클래스 기반 뷰를 `as_view()`로 호출하는 것이 함수 기반 뷰처럼 동작하게 한다는 것을 알기 때문에 두 개의 서브 뷰 사이에서 선택할 때 그렇게 할 수 있다.

다른 URL에서도 `AuthorInterestFormView`의 동작이 나타나지만 다른 템플릿을 사용하기를 원할 때와 같이 URLconf에서 하는 것과 같은 방식으로 `as_view()`에 키워드 인자를 넣어 전달할 수 있다.

```python
from django.views import View

class AuthorView(View):

    def get(self, request, *args, **kwargs):
        view = AuthorDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = AuthorInterestFormView.as_view()
        return view(request, *args, **kwargs)
```

이 접근 방식은 다른 뷰를 가능한 분리해서 유지하기 때문에 다른 generic 클래스 기반 뷰나 `View` 또는 `TemplateView`를 직접 상속받는 사용자 정의 클래스 기반 뷰에서도 사용할 수 있다.

## More than just HTML
클래스 기반 뷰는 같은 것을 여러 번 반복하기를 원할 때 빛을 본다. API를 쓰는 중이며, 모든 뷰가 렌더링된 HTML이 아니라 JSON을 반환해야 한다고 하자.

모든 뷰에서 사용할 수 있는, 한 번에 JSON으로의 변환을 다루는 mixin 클래스를 만들 수 있다.

예를 들어, JSON mixin은 다음과 같다.

```python
from django.http import JsonResponse

class JSONResponseMixin:
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(
            self.get_data(context),
            **responsive_kwargs
        )

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serailized as JSON.
        return context
```

- Note<br>
Django 모델과 queryset을 JSON으로 변환하는 올바른 방법에 관한 정보를 얻으려면 [Serializing Django objects](https://docs.djangoproject.com/en/3.2/topics/serialization/)를 확인한다.

이 mixin은 `render_to_response()`와 같은 특징을 가진 `render_to_json_response()` 메서드를 제공한다. 이를 사용하려면 예를 들어 `TemplateView`와 조합을 하고 `render_to_json_response()`를 대신 호출하기 위해 `render_to_response()`를 override한다.

```python
from django.views.generic import TemplateView

class JSONView(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)
```

그 다음 이 뷰는 응답의 양식을 제외한 다른 `DetailView`의 특징을 가지고 그와 같은 방식으로 확장할 수 있다.

도전적이라면, `DetailView`의 서브 클래스를 조합해 쿼리 인자나 HTTP 헤더처럼 HTTP 요청의 어떤 속성에 따라 HTML과 JSON 둘 다 반환하게 할 수도 있다. `JSONResponseMixin`과 `SingleObjectTemplateResponseMixin`을 조합하고 `render_to_response()`의 구현을 override해 사용자가 요청한 응답 유형에 따라 적절한 렌더링 방식으로 연기한다.

```python
from django.views.generic.detail import SingleObjectTemplateResponseMixin

class HybridDetailView(JSONResponseMixin, SingleObjectTemplateResponseMixin, BaseDetailView):
    def render_to_response(self, context):
        # Look for a 'format=json' GET argument
        if self.request.GET.get('format') == 'json':
            return self.render_to_json_response(context)
        else:
            return super().render_to_response(context)
```
Python이 메서드 오버로드를 해결하는 방식 때문에 `super().render_to_response(context)` 호출은 `TemplateResponseMixin`의 `render_to_response()` 구현을 호출한다.