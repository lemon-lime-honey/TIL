# [Routers](https://www.django-rest-framework.org/api-guide/routers/)
```
리소스 라우팅을 사용하면 주어진 resourceful controller를 위한 모든 공통 경로를 빠르게 선언할 수 있다.
인덱스에 대해 분리된 경로를 선언하는 대신...영리한 경로는 한 줄의 코드로 그 모두를 선언한다.
- Ruby on Rails 문서
```

Rails 같은 웹 프레임워크에서는 어플리케이션이 들어오는 요청을 논리에 매핑하는 URL을 자동으로 결정하는 기능을 제공한다.

REST framework는 Django에 자동 URL 라우팅 지원을 추가해 뷰 로직에 URL 집합을 간단하고 빠르게 일관적으로 연결하는 방법을 제공한다.

## Usage
다음은 `SimpleRouter`를 사용하는 간단한 URL 구성의 예시이다.

```python
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'accounts', AccountViewSet)
urlpattenrs = router.urls
```

`register()` 메서드에는 두 개의 필수 인자가 있다:

- `prefix`: 이 경로 집합에 사용될 URL 접두사
- `viewset`: viewset 클래스

선택사항으로 추가적인 인자를 명시할 수도 있다:

- `basename`: 생성되는 URL 이름의 기초. 정하지 않으면 뷰셋의 `queryset` 속성을 하나 가질 때에는 그에 기반해 자동으로 basename이 생성된다. 만약 뷰셋이 `queryset` 속성을 가지지 않으면 뷰셋을 등록할 때 반드시 `basename`을 설정해야 한다.

위의 예시는 다음과 같은 URL 패턴을 생성한다.
| URL 패턴 | 이름 |
| --- | --- |
| `^users/$` | user-list |
| `^users/{pk}/$` | user-detail |
| `^accounts/$` | account-list |
| `^accounts/{pk}/$` | account-detail |

---

**Note**: `basename` 인자는 뷰 이름 패턴의 초기 부분을 명시하기 위해 사용된다. 위의 예시에서는 `user` 또는 `account`이다.

보통은 `basename`인자를 명시할 *필요가 없지만* 사용자 정의 `get_queryset` 메서드를 정의한 뷰셋이라면 그 뷰셋이 `.queryset` 속성 집합을 가지지 않을 수 있다. 이럴 때 뷰셋을 등록하려 하면 이런 오류가 발생한다.

```
'basename' argument not specified, and could not automatically determine the name from the viewset, as it does not have a '.queryset' attribute.
```

이는 모델명으로부터 자동으로 `basename`을 지정할 수 없으므로 뷰셋을 등록할 때 `basename` 인자를 명시적으로 설정해야 함을 의미한다.

---

## Using `include` with routers
라우터 인스턴스의 `.urls` 속성은 URL 패턴의 표준 리스트이다. 이 URL을 포함시키는 방법은 다양하다.

예를 들어 존재하는 뷰 리스트에 `router.urls`를 추가할 수 있다:

```python
router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'accounts', AccountViewSet)

urlpatterns = [
    path('forgot-password/', ForgotPasswordFormView.as_view()),.
]

urlpatterns += router.urls
```

또는 다음과 같이 Django의 `include` 함수를 사용할 수도 있다:

```python
urlpatterns = [
    path('forgot-password/', ForgotPasswordFormView.as_view()),
    path('', include(router.urls)),
]
```

애플리케이션 namespace와 `include`를 같이 쓸 수도 있다:

```python
urlpatterns = [
    path('forgot-password/', ForgotPasswordFormView.as_view()),
    path('api/', include((router.urls, 'app_name'), namespave='instance_name')),
]
```

자세한 내용은 Django의 [URL namespaces 문서](https://docs.djangoproject.com/en/4.0/topics/http/urls/#url-namespaces)와 [`include` API 레퍼런스](https://docs.djangoproject.com/en/4.0/ref/urls/#include)를 참조한다.

---

**Note**: 만약 하이퍼링크된 시리얼라이저와 함께 namespace를 사용한다면 시리얼라이저에 있는 `view_name` 매개변수가 namespace를 정확히 반영하는지 확인해야 한다. 위의 예시에서는 사용자 상세 뷰에 하이퍼링크된 시리얼라이저 필드에 `view_name='app_name:user-detail'`과 같은 매개변수를 포함해야 한다.

자동 `view_name` 생성은 `%(model_name)-detail`과 같은 패턴을 사용한다. 모델 이름이 정말 충돌하는 것이 아니라면 하이퍼링크된 시리얼라이저를 사용할 때에는 Django REST Framework 뷰에 namespace를 사용하지 않는 게 좋다.

---

## Routing for extra actions
뷰셋은 `@action` 데코레이터를 사용한 메서드로 [라우팅을 위한 추가 동작 표시](viewsets.md/#marking-extra-actions-for-routing)를 할 수 있다. 예를 들어 `UserViewSet` 클래스에 `set_password` 메서드가 주어졌다고 하자:

```python
from myapp.permissions import IsAdminOrIsSelf
from rest_framework.decorators import action

class UserViewSet(ModelViewSet):
    ...
    @action(methods=['post'], detail=True, permission_classes=[IsAdminOrIsSelf])
    def set_password(self, request, pk=None):
        ...
```

다음 경로가 생성된다:

- URL 패턴: `^users/{pk}/set_password/$`
- URL 이름: `user-set-password`

기본적으로 URL 패턴은 메서드의 이름에 기반하고 URL 이름은 `ViewSet.basename`과 하이픈이 붙은 메서드 이름의 조합이다. 이러한 값을 사용하고 싶지 않다면 `@action` 데코레이터에 `url_path`와 `url_name` 인자를 제공하면 된다.

예를 들어 사용자 정의 동작의 URL을 `^users/{pk}/change-password/$`로 바꾸려면:

```python
from myapp.permissions import IsAdminOrIsSelf
from rest_framework.decorators import action

class UserViewSet(ModelViewSet):
    ...
    @action(methods=['post'], detail=True, permission_classes=[IsAdminOrIsSelf],
    url_path='change-password', url_name='change_password')
    def set_password(self, request, pk=None):
        ...
```

위의 예시는 다음과 같은 URL 패턴을 생성한다.

- URL 주소: `^users/{pk}/change-password/$`
- URL 이름: `'user-change_password'`
<br><br>

# API GUIDE
## SimpleRouter
이 라우터는 `list`, `create`, `retrieve`, `update`, `partial_update`, `destroy` 동작의 표준 집합을 위한 경로를 포함한다. 또한 뷰셋은 `@action` 데코레이터를 사용해 경로가 필요한 추가적인 메서드를 표시할 수 있다.

| URL Style | HTTP Method | Action | URL Name |
| --- | --- | --- | --- |
| {prefix}/ | GET | list | {basename}-list |
| {prefix}/ | POST | create | {basename}-list |
| {prefix}/{url_path}/ | GET, or as specified by `methods` argument | `@action(detail=False)` decorated method | {basename}-{url-name} |
| {prefix}/{lookup}/ | GET | retrieve | {basename}-detail |
| {prefix}/{lookup}/ | PUT | update | {basename}-detail |
| {prefix}/{lookup}/ | PATCH | partial_update | {basename}-detail |
| {prefix}/{lookup}/ | DELETE | destroy | {basename}-detail |
| {prefix}/{lookup}/{url_path}/ | GET, or as specified by `methods` argument | `@action(detail=True)` decorated method | {basename}-{url_name} |

`SimpleRouter`로 생성된 URL은 기본적으로 트레일링 슬래시와 함께 추가된다. 이러한 현상은 라우터를 설정할 때 `trailing_slash` 인자를 `False`로 설정하면 바꿀 수 있다.

```python
router = SimpleRouter(trailing_slash=False)
```

트레일링 슬래시는 Django에서는 관습이지만 Rails와 같은 다른 프레임워크에서는 기본값으로 사용되지 않는다. 일부 자바스크립트 프레임워크가 특정 라우팅 스타일을 기대하더라도 어느 스타일을 고를지는 선호의 문제이다.

라우터는 슬래시와 온점을 제외한 모든 문자를 포함하는 조회 값을 찾을 것이다. 좀 더 엄격한(또는 느슨한) 조회 패턴을 사용하려면 뷰셋에서 `look_up_value_regex` 속성을 설정한다. 예를 들어, 조회 대상을 유효한 UUID로 제한할 수 있다:

```python
class MyModelViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    lookup_field = 'my_model_id'
    lookup_value_regex = '[0-9a-f]{32}'
```

## DefaultRouter
이 라우터는 위의 `SimpleRouter`와 유사하지만 모든 리스트 뷰의 하이퍼링크를 포함하는 응답을 반환하는 API 루트 뷰 기본값을 포함한다. 또한 선택적인 `.json` 스타일 포맷 접미사가 있는 경로를 생성한다.

| URL Style | HTTP Method | Action | URL Name |
| --- | --- | --- | --- |
| [.format] | GET | automatically generated root view | api-root |
| {prefix}/[.format] | GET | list | {basename}-list |
| {prefix}/[.format] | POST | create | {basename}-list |
| {prefix}/{url_path}/[.format] | GET, or as specified by `methods` argument | `@action(detail=False)` decorated method | {basename}-{url-name} |
| {prefix}/{lookup}/[.format] | GET | retrieve | {basename}-detail |
| {prefix}/{lookup}/[.format] | PUT | update | {basename}-detail |
| {prefix}/{lookup}/[.format] | PATCH | partial_update | {basename}-detail |
| {prefix}/{lookup}/[.format] | DELETE | destroy | {basename}-detail |
| {prefix}/{lookup}/{url_path}/[.format] | GET, or as specified by `methods` argument | `@action(detail=True)` decorated method | {basename}-{url_name} |

`SimpleRouter`처럼 라우터를 설정할 때 `trailing_slash` 인자를 `False`로 설정하면 경로의 트레일링 슬래시를 제거할 수 있다.

```python
router = DefaultRouter(trailing_slash=False)
```

## Custom Routers
사용자 정의 라우터를 구현하는 것은 자주 요구되는 일은 아니지만 API 구조를 위한 URL에 특별한 요구사항이 있을 때 유용하다. 이렇게 하면 새로운 뷰마다 URL 패턴을 명시하지 않아도 되는, 재사용이 가능한 방향으로 URL 구조를 압축할 수 있다.

사용자 정의 라우터를 구현하는 가장 단순한 방법은 존재하는 라우터 클래스 중 하나의 서브클래스를 생성하는 것이다. `.routes` 속성은 각 뷰셋에 매핑될 URL 패턴 템플릿을 만드는데 사용된다. `.route` 속성은 `Route` 명명된 튜플의 리스트이다.

`Route` 명명된 튜플의 인자는 다음과 같다.

- url: 연결되어야 하는 URL을 나타내는 문자열. 다음 포맷 문자열을 포함할 수 있다.
  - {prefix}: 이 경로 세트에 사용되는 URL 접두어
  - {lookup}: 하나의 인스턴스를 찾기 위해 사용되는 조회 필드
  - {trailing_slash}: 인자 값에 따라 '/' 또는 빈 문자열
- mapping: 뷰 메서드에 매핑된 HTTP 메서드 이름
- name: `reverse` 호출에 사용되는 URL 이름. 다음 포맷 문자열을 포함할 수 있다.
  - {basename}: 생성되는 URL 이름의 기초
- initkwargs: 뷰를 인스턴스화할 때 전달해야 하는 추가적인 인자 딕셔너리. `detail`, `basename`, `suffix` 인자는 뷰셋 내부 확인 용으로 예약되어 있으며 탐색 가능한 API가 뷰 이름과 브레드크럼스 링크를 생성할 때에도 사용한다.

## Customizing dynamic routes
`@action` 데코레이터가 어떻게 라우팅될 수 있는지도 정할 수 있다. `.routes` 리스트의 `DynamicRoute` 명명된 튜플을 포함하고 리스트 기반 그리고 상세 기반 경로에 적절한 `detail` 인자를 설정한다. `DynamicRoute`의 인자는 `detail` 외에도 다음이 있다.

- url: 연결되어야 할 URL을 나타내는 문자열. `Route`와 동일한 형식의 문자열을 포함할 수 있으며 `{url_path}` 포맷 문자열을 추가로 사용할 수 있다.
- name: `reverse` 호출에 사용되는 URL의 이름. 다음 포맷 문자열을 포함할 수 있다.
  - `{basename}`: 생성되는 URL 이름의 기초
  - `{url_name}`: `@action`에 제공되는 `url_name`
- initkwargs: 뷰를 인스턴스화할 때 전달되어야 하는 추가 인자 딕셔너리

## Example
다음 예시는 `list`, `retrieve` 동작만 연결하며 트레일링 슬래시를 사용하지 않는다.

```python
from rest_framework.routers import Route, DynamicRoute, SimpleRouter

class CustomReadOnlyRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}$',
            mapping={'get': 'list'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/{lookup}$',
            mapping={'get': 'retrieve'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        )
    ]
```

`CustomReadOnlyRouter`가 간단한 뷰셋에 생성하는 경로를 보자.

- `views.py`
  ```python
  class UserViewSet(viewsets.ReadOnlyModelViewSet):
      """
      표준 동작을 제공하는 뷰셋
      """
      queryset = User.objects.all()
      serializer_class = UserSerializer
      lookup_field = 'username'

      @action(detail=True)
      def group_names(self, request, pk=None):
          """
          주어진 사용자가 속한 모든 그룹 명의 리스트를 반환한다.
          """
          user = self.get_object()
          groups = user.groups.all()
          return Response([group.name for group in groups])
  ```
- `urls.py`
  ```python
  router = CustomReadOnlyRouter()
  router.register('users', UserViewSet)
  urlpattenrs = router.urls
  ```

다음과 같은 매핑이 생성될 것이다.

| URL | HTTP Method | Action | URL Name |
| --- | --- | --- | --- |
| /users | GET | list | user-list |
| /users/{username} | GET | retrieve | user-detail |
| /users/{username}/group_names | GET | group_names | user-group-names |

`.routes` 속성을 설정하는 다른 예시를 확인하려면 `SimpleRouter` 클래스의 소스코드를 참조한다.

## Advanced custom Routers
완전한 사용자 정의 동작을 제공하려면 `BaseRouter`를 재정의하고 `get_urls(self)` 메서드를 재정의한다. 메서드는 등록된 뷰셋을 검사하고 URL 패턴 리스트를 반환해야 한다. 등록된 접두사, 뷰셋, basename 튜플은 `self.registry` 속성에 접근해 검사할 수 있다.

또한 `get_default_basename(self, viewset)` 메서드를 재정의하거나 뷰셋을 라우터에 등록할 때 언제나 `basename` 인자를 명시적으로 설정할 수 있다.
<br><br>

# Third Party Packages
다음의 서드파티 패키지를 사용할 수도 있다.

## DRF Nested Routers
[drf-nested-routers 패키지](https://github.com/alanjds/drf-nested-routers)는 중첩된 리소스로 작업하기 위한 라우터와 관계 필드를 제공한다.

## ModelRouter(wq.db.rest)
[wq.db 패키지](https://wq.io/wq.db)는 `register_model()` API로 `DefaultRouter`를 확장하는 심화된 [ModelRouter](https://wq.io/docs/router) 클래스를 제공한다. Django의 `admin.site.register`처럼 `rest.router.register_model`이 요구하는 유일한 인자는 모델 클래스이다. URL 접두사, 시리얼라이저, 뷰셋에 관한 합리적인 기본값은 모델과 글로벌 구성에서 유래한다.

```python
from wq.db import rest
from myapp.models import MyModel

rest.router.register_model(MyModel)
```

## DRF-extensions
[`DRF-extensions` 패키지](https://chibisov.github.io/drf-extensions/docs/)는 [사용자 정의 가능한 엔드포인트 이름](https://chibisov.github.io/drf-extensions/docs/#controller-endpoint-name)을 가진 [중첩 뷰셋](https://chibisov.github.io/drf-extensions/docs/#nested-routes), [컬렉션 수준 컨트롤러](https://chibisov.github.io/drf-extensions/docs/#collection-level-controllers)를 생성하기 위한 [라우터](https://chibisov.github.io/drf-extensions/docs/#routers)를 제공한다.