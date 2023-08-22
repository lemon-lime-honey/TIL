# [Pagination](https://www.django-rest-framework.org/api-guide/pagination/)
```
Django는 페이지가 매겨진 데이터(즉, "이전/다음" 링크로 여러 페이지에 걸쳐 나뉜 데이터)를 다루는데 도움이 되는 몇 개의 클래스를 제공한다.
- Django 공식문서
```

REST framework는 커스터마이즈 가능한 페이지 매김 형식 지원을 포함한다. 이는 결과 모음을 어떤 크기로 데이터의 개별 페이지로 나눌지 수정하게 한다.

페이지 분할 API는 다음을 지원할 수 있다.

- 응답 컨텐츠의 일부로 주어지는 페이지 매김 링크
- `Content-Range` 또는 `Link`와 같이 응답 헤더에 포함된 페이지 매김 링크

모든 빌트인 형식은 현재 응답 내용의 일부로 포함된 링크를 사용한다. 이 형식은 브라우징 가능한 API를 사용할 때 좀 더 접근하기 좋다.

페이지 매김은 제네릭 뷰나 viewset을 사용할 때에만 자동으로 동작한다. 일반적인 `APIView`를 사용한다면 페이지가 매겨진 응답을 반환하기 위해 페이지 매김 API를 호출해야 한다. `mixins.ListModelMixin`과 `generics.GenericAPIView` 클래스의 소스코드를 예시로 참고한다.

pagination 클래스를 `None`으로 설정하여 페이지 매김을 하지 않을 수 있다.

## Setting the pagination style
`DEFAULT_PAGINATION_CLASS`와 `PAGE_SIZE` 설정 키를 사용해 페이지 매김 형식을 전역적으로 설정할 수 있다. 예를 들어, 빌트인 페이지 매김 제한/오프셋을 사용하려면 다음과 같이 작성한다:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}
```

pagination 클래스와 사용될 페이지 크기를 둘 다 설정해야 한다는 점에 유의한다. `DEFAULT_PAGINATION_CLASS`와 `PAGE_SIZE`의 기본값은 `None`이다.

`pagination_class` 속성을 사용해 각각의 뷰에 pagination 클래스를 설정할 수 있다. 뷰당 기반으로 기본 또는 최대 페이지 크기와 같은 페이지 매김의 개별적인 요소를 다르게 하고 싶을지라도 보통은 API를 통틀어 같은 페이지 매김 형식을 사용한다.

## Modifying the pagination style
페이지 매김 형식의 특정 부분을 수정해야 한다면 pagination 클래스 중 하나를 override하고 변경하고 싶은 속성을 설정하면 된다.

```python
class LargeResultSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class StandardResultSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000
```

그 다음 `pagination_class` 속성을 사용해 뷰에 새 형식을 적용한다.

```python
class BillingRecordsView(generics.ListAPIView):
    queryset = Billing.objects.all()
    serializer_class = BillingRecordsSerializer
    pagination_class = LargeResultsSetPagination
```

`DEFAULT_PAGINATION_CLASS` 설정 키를 사용해 전역적으로 형식을 적용할 수 있다. 예를 들어:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'apps.core.pagination.StandardResultsSetPagination'
}
```

# API Reference
## PageNumberPagination
이 페이지 매김 형식은 요청의 쿼리 파라미터 중 하나의 숫자인 페이지 숫자를 허용한다.

**Request**:

```
GET https://api.example.org/accounts/?page=4
```

**Response**:

```
HTTP 200 OK
{
  "count": 1023,
  "next": "https://api.example.org/accounts/?page=5",
  "previous": "https://api.example.org/accounts/?page=3",
  "results": [
    ...
  ]
}
```

### Setup
`PageNumberPagination` 형식을 전역적으로 사용할 수 있게 하려면 다음의 설정을 사용하고 원하는 `PAGE_SIZE`를 설정한다.

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100
}
```

`GenericAPIView` 서브클래스에서는 뷰당 기반의 `PageNumberPagination`을 선택하기 위해 `pagination_class` 속성을 설정할 수 있다.

### Configuration
`PageNumberPagination` 클래스는 페이지 매김 형식을 변경하기 위해 override될 수 있는 여러 속성을 가지고 있다.

이 설정을 설정하려면 `PageNumberPagination` 클래스를 override하고 위에서와 같이 사용자 정의 pagination 클래스를 사용할 수 있게 하면 된다.

- `django_paginator_class`<br>
  사용하고자 하는 Django Paginator 클래스. 기본값은 대부분의 경우 사용하기 좋은 `django.core.paginator.Paginator`
- `page_size`<br>
  페이지 크기를 지시하는 숫자 값. 설정되었다면 `PAGE_SIZE` 설정을 override한다. 기본값은 `PAGE_SIZE` 설정 키와 같은 값
- `page_query_param`<br>
  페이지 매김 제어에 사용되는 쿼리 파라미터의 이름을 지시하는 문자열 값
- `page_size_query_param`<br>
  설정된다면 클라이언트가 요청 당 기반으로 페이지 크기를 설정할 수 있게 허용하는 쿼리 파라미터의 이름을 지시하는 문자열 값이 된다. 기본값은 `None`으로, 클라이언트가 요청된 페이지 크기를 제어하지 못하는 것을 가리킨다.
- `max_page_size`<br>
  설정된다면 최대로 허용 가능한 요청된 페이지의 크기를 지시하는 숫자 값이 된다. 이 속성은 `page_size_query_param`이 설정되었을 때에만 유효하다.
- `last_page_strings`<br>
  모음의 마지막 페이지를 요청하기 위해 `page_query_param`과 함께 사용될 수 있는 값을 지시하는 문자열 값의 리스트 또는 튜플. 기본값은 `('last',)`
- `template`<br>
  페이지 매김 렌더링이 브라우징 가능한 API를 제어할 때 사용하기 위한 템플릿의 이름. 렌더링 형식을 변경하기 위해 override되거나 HTML 페이지 매김 제어를 완전히 비활성화하기 위해 `None`으로 설정될 수 있다. 기본값은 `"rest_framework/pagination/numbers.html"`

## LimitOffsetPagination
이 페이지 매김 형식은 복수의 데이터베이스 기록을 조회할 때 사용되는 구문을 반영한다.클라이언트는 "limit"과 "offset" 쿼리 파라미터를 둘 다 포함한다. limit는 반환할 항목의 최대 숫자를 지시하며, 다른 형식의 `page_size`와 동등하다. offset은 페이지 매김이 되지 않은 항목의 전체 집합과 비교한 쿼리의 시작 지점을 지시한다.

**Request**:
```
GET https://api.example.org/accounts/?limit=100&offset=400
```

**Response**:
```
HTTP 200 OK
{
  "count": 1023,
  "next": "https://api.example.org/accounts/?limit=100&offset=500",
  "previous": "https://api.example.org/accounts/?limit=100&offset=300",
  "results": [
    ...
  ]
}
```

### Setup
전역적으로 `LimitOffsetPagination` 형식을 사용할 수 있게 하려면 다음 설정을 사용한다:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination'
}
```

선택적으로 `PAGE_SIZE` 키를 설정할 수 있다. `PAGE_SIZE` 파라미터가 사용된다면 `limit` 쿼리 파라미터는 선택인자가 될 것이며, 클라이언트에 의해 무시될 수 있다.

`GenericAPIView` 서브클래스에서는 뷰당 기반에서 `LimitOffsetPagination`을 선택하기 위해 `pagination_class` 속성을 설정할 수 있다.

### Configuration
`LimitOffsetPagination` 클래스는 페이지 매김 형식을 변경하기 위해 override될 수 있는 여러 속성을 가지고 있다.

이 설정을 설정하려면 `LimitOffsetPagination` 클래스를 override하고 위에서와 같이 사용자 정의 pagination 클래스를 사용할 수 있게 하면 된다.

- `default_limit`<br>
  쿼리 파라미터에서 클라이언트가 한계를 지정하지 않았을 때 사용하기 위한 한계값을 지시하는 숫자값. 기본값은 `PAGE_SIZE` 설정 키와 같은 값
- `limit_querys_param`<br>
  "limit" 쿼리 파라미터의 이름을 지시하기 위한 문자열 값. 기본값은 `'limit'`
- `offset_query_param`<br>
  "offset" 쿼리 파라미터의 이름을 지시하기 위한 문자열 값. 기본값은 `'offset'`
- `max_limit`<br>
  설정된다면 클라이언트에 의해 요청되는 최대 허용 가능한 한계를 지시하는 숫자값이 된다. 기본값은 `None`
- `template`<br>
  페이지 매김 렌더링이 브라우징 가능한 API를 제어할 때 사용하기 위한 템플릿의 이름. 렌더링 형식을 변경하기 위해 override되거나 HTML 페이지 매김 제어를 완전히 비활성화하기 위해 `None`으로 설정될 수 있다. 기본값은 `"rest_framework/pagination/numbers.html"`

## CursorPagination
커서 기반 페이지 매김은 클라이언트가 결과 집합에 걸쳐 페이지를 생성하기 위해 사용할 수 있는 불투명한 "커서" 지표를 나타낸다.이 페이지 매김 형식은 순방향과 역방향 제어만 표시하며, 클라이언트가 임의의 위치를 탐색하는 것을 허용하지 않는다.

커서 기반 페이지 매김을 사용하려면 결과 집합의 항목이 고유하고 바뀌지 않는 순서를 가지고 있어야 한다. 이 순서는 일반적으로 페이지 매김을 하기 위한 일관적인 순서를 나타내는 레코드에 대한 생성 타임스탬프가 될 수 있다.

커서 기반 페이지 매김은 다른 스킴보다 복잡하다. 또한 결과 집합이 고정된 순서를 가지는 것을 필요로 하며, 클라이언트가 결과 집합에 임의의 색인을 만드는 것을 허용하지 않는다. 그러나 다음의 이점을 제공한다.

- 일관적인 페이지 매김 뷰를 제공한다. `CursorPagination`을 적절히 사용하면 페이지 매김 과정 중 다른 클라이언트에 의해 새로운 항목이 삽입될 때마저도 클라이언트가 레코드를 통해 페이지를 생성할 때 같은 항목을 두 번 보지 않는 것을 보장한다.
- 매우 큰 데이터 모음 사용을 지원한다. 극단적으로 큰 데이터 모음에서 사용할 때, 오프셋 기반 페이지 매김 형식을 사용하는 페이지 매김은 비효율적이거나 사용할 수 없게 된다. 커서 기반 페이지 매김 스킴은 대신 고정 시간 속성을 가지며, 데이터 모음의 크기가 증가해도 느려지지 않는다.

### Details and limitations
커서 기반 페이지 매김의 올바르게 사용하려면 세부사항에 약간의 주의를 가져야 한다. 스킴이 어떤 순서로 적용되어야 할지에 관해 생각해야 한다. 기본은 `"-created"`로 정렬되는 것이다. 이는 모델 인스턴스에 **'created' 타임스탬프 필드가 반드시 존재**한다는 것을 가정하는 것이며, 가장 최근에 추가된 항목을 우선으로 하는 "타임라인" 형식 뷰를 표현한다.

pagination 클래스의 `'ordering'` 속성을 override하거나 `CursorPagination`과 함께 `OrderingFilter` 필터 클래스를 사용하여 정렬 기준을 바꿀 수 있다. `OrderingFilter`를 사용하는 경우 사용자가 정렬 기준으로 선택할 필드를 제한하는 것을 강하게 고려해야 한다.

커서 페이지 매김의 올바른 사용은 다음을 만족하는 정렬 기준 필드를 가지고 있어야 한다:

- 타임스탬프, 슬러그 또는 생성 당시 단 한 번 설정되는 필드여야 한다.
- 고유하거나 거의 고유해야 한다. 밀리초 수준의 정밀도를 가진 타임스탬프가 좋은 예시이다. 이 커서 페이지 매김 구현은 엄밀하게는-고유하지-않은 값을 정렬 기준으로 적절하게 지원하는 것을 허용하는 영리한 "position plus offset" 형식을 사용한다.
- 문자열로 강제될 수 있는 null이 아닌 값
- 부동소수점 숫자가 아니어야 한다. 정확도 오류는 쉽게 부정확한 결과로 유도된다. 힌트: decimal을 대신 사용한다. (만약 이미 부동소수점 필드를 가지고 있고, 그에 관해 페이지 매김을 해야 한다면 [정밀도를 제한하기 위해 decimal을 사용하는 `CursorPagination` 서브클래스의 예시가 여기 있다.](https://gist.github.com/keturn/8bc88525a183fd41c73ffb729b8865be#file-fpcursorpagination-py))
- 필드는 데이터베이스 색인을 가져야 한다.

이 제한을 만족하지 못하는 정렬 필드를 사용하더라도 보통 동작하지만, 커서 페이지 매김의 이점 일부를 잃게 된다.

커서 페이지 매김에 사용하는 구현의 기술적인 세부 사항에 관해서는 블로그 포스트 ["Building cursors for the Disqus API"](https://cra.mr/2011/03/08/building-cursors-for-the-disqus-api)가 기본 접근에 관한 좋은 개요를 제공한다.

### Setup
`CursorPagination` 형식을 전역적으로 사용하려면 다음의 설정을 사용하고 원하는 대로 `PAGE_SIZE`를 변경한다.

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.CursorPagination',
    'PAGE_SIZE': 100
}
```

`GenericAPIView` 서브클래스에서는 뷰당 기반의 `CursorPagination`을 선택하기 위해 `pagination_class` 속성을 설정한다.

### Configuration
`CursorPagination` 클래스는 페이지 매김 형식을 변경하기 위해 override될 수 있는 여러 속성을 포함한다.

이 속성을 설정하려면 `CursorPagination` 클래스를 override하고 위와 같이 사용자 정의 pagination 클래스를 사용 가능하게 한다.

- `page_size`<br>
  페이지 크기를 지시하는 숫자값. 설정되었다면 `PAGE_SIZE` 설정을 override한다. 기본값은 `PAGE_SIZE` 설정 키와 같은 값이다.
- `cursor_query_param`<br>
  "커서" 쿼리 파라미터의 이름을 지시하는 문자열 값. 기본값은 `'cursor'`
- `ordering`<br>
  커서 기반 페이지 매김이 적용될 필드를 지시하는 문자열이나 문자열의 리스트. (예: `ordering = 'slug`) 기본값은 `-created`. 뷰에서 `OrderingFilter`를 사용하면 override된다.
- `template`<br>
  브라우징 가능한 API에서 페이지 매김 컨트롤을 렌더링할 때 사용하는 템플릿의 이름. 렌더링 형식을 변경하기 위해 override되거나 HTML 페이지 매김 컨트롤을 완전히 비활성화하기 위해 `None`으로 설정될 수 있다. 기본값은 `"rest_framework/pagination/previous_and_next.html"`

# Custom pagination styles
사용자 정의 페이지 매김 시리얼라이저 클래스를 생성하려면, 서브클래스 `pagination.BasePagination`를 상속하고 `paginate_queryset(self, queryset, request, view=None)`과 `get_paginated_response(self, data)` 메서드를 override해야 한다:

- `paginate_queryset` 메서드는 초기 queryset에 전달되고 순회 가능한 객체를 반환해야 한다. 객체는 요청된 페이지에 있는 데이터만을 가져야 한다.
- `get_paginated_response` 메서드는 serialize된 페이지 데이터로 전달되고 `Response` 인스턴스를 반환해야 한다.

`paginate_queryset` 메서드가 이후에 `get_paginated_response` 메서드에 의해 사용될 pagination 인스턴스의 상태를 설정할 수 있다는 점에 유의한다.

## Example
중첩된 'links' 키 아래 다음과 이전 링크가 있는 변경된 형식을 가지는 기본 페이지 매김 출력 형식을 대체해야 할 때, 다음과 같은 사용자 정의 pagination 클래스를 명시한다:

```python
class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })
```

그 다음 설정에서 사용자 정의 클래스를 설정한다.

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'my_project.apps.core.pagination.CustomPagination',
    'PAGE_SIZE': 100
}
```

브라우징 가능한 API의 응답에서 키의 정렬이 어떻게 표현되는지에 관해 고려한다면 페이지 매김된 응답의 바디를 구성할 때 `OrderedDict` 사용할 수 있지만 선택사항이다.

## Using your custom pagination class
사용자 정의 pagination 클래스가 기본으로 사용되게 하려면 `DEFAULT_PAGINATION_CLASS` 설정을 사용한다.

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'my_project.apps.core.pagination.LinkHeaderPagination',
    'PAGE_SIZE': 100
}
```

리스트 엔드포인트를 위한 API 응답은 응답의 바디의 일부로 페이지 매김 링크를 포함하는 대신 다음 예시처럼 `Link` 헤더를 가지게 된다:

![link_header_pagination](https://www.django-rest-framework.org/img/link-header-pagination.png)

*'Link' 헤더를 사용하는 사용자 정의 페이지 매김 형식*

## Pagination & schemas
`get_schema_fields()` 메서드를 구현하여 REST framework가 제공하는 스키마 자동생성에 페이지 매김 컨트롤을 사용할 수 있게 할 수 있다. 이 메서드는 다음 시그니처를 가진다:

`get_schema_fields(self, view)`

이 메서드는 `coreapi.Field` 인스턴스의 리스트를 반환해야 한다.

# HTML pagination controls
기본적으로 pagination 클래스를 사용하면 브라우징 가능한 API에 HTML 페이지 매김 컨트롤이 표시된다. 두 가지 빌트인 표시 형식이 있다. `PageNumberPagination`과 `LimitOffsetPagination` 클래스는 이전과 이후 컨트롤을 가지는 페이지 숫자의 리스트를 표시한다. `CursorPagination` 클래스는 오직 이전과 이후 컨트롤을 표시하는 더 단순한 형식을 표시한다.

## Customizing the controls
HTML 페이지 매김 컨트롤을 렌더링하는 템플릿을 override할 수 있다. 두 개의 빌트인 형식은 다음과 같다:

- `rest_framework/pagination/numbers.html`
- `rest_framework/pagination/previous_and_next.html`

전역 템플릿 디렉토리에 있는 이 경로 중 하나의 템플릿을 제공하면 pagination 클래스에 연관된 기본 렌더링이 override된다.

또는 존재하는 클래스의 서브클래스를 작성해 `template = None` 속성을 설정해 HTML 페이지 매김 컨트롤을 완전히 비활성화할 수 있다.

### Low-level API
pagination 클래스가 컨트롤을 표시할지 여부를 결정하는 저수준 API는 pagination 인스턴스의 `display_page_controls` 속성으로 노출된다. 사용자 정의 pagination 클래스는 HTML 페이지 매김 컨트롤이 표시되어야 할 때 `paginate_queryset`에서 `True`로 설정되어야 한다.

`.to_html()`과 `.get_html_context` 메서드는 컨트롤이 컨트롤이 렌더링 되는 방식을 추가로 커스터마이즈하기 위해 사용자 정의 pagination 클래스에서 override될 수 있다.

# Third party packages
다음의 서드파티 패키지를 사용할 수도 있다.

## DRF-extensions
[`DRF-extensions` 패키지](https://chibisov.github.io/drf-extensions/docs/)는 API 클라이언트가 최대 허용 페이지 숫자를 얻기 위해 `?page_size=max`를 명시하게 허용하는 [`PaginatedByMaxMixin` mixin 클래스](https://chibisov.github.io/drf-extensions/docs/#paginatebymaxmixin)를 포함한다.

## drf-proxy-pagination
[`drf-proxy-pagination` 패키지](https://github.com/tuffnatty/drf-proxy-pagination)는 쿼리 파라미터로 pagination 클래스를 선택할 수 있게 하는 `ProxyPagination` 클래스를 포함한다.

## link-header-pagination
[`django-rest-framework-link-header-pagination` 패키지](https://github.com/tbeadle/django-rest-framework-link-header-pagination)는 [GitHub REST API 문서](https://docs.github.com/en/rest/guides/traversing-with-pagination)에서 기술된 대로 HTTP의 `Link` 헤더를 경유해 페이지 매김을 제공하는 `LinkHeaderPagination` 클래스를 포함한다.