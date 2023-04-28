# Introduction to class-based views
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