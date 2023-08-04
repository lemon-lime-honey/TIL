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
이 페이지 매김 형식은 복수의 데이터베이스 기록을 조회할 때 사용되는 구문을 반영한다.클라이언트는 "limit"과 "offset" 쿼리 파라미터를 둘 다 포함한다. limit는 반환할 아이템의 최대 숫자를 지시하며, 다른 형식의 `page_size`와 동등하다. offset은 페이지 매김이 되지 않은 아이템의 전체 집합과 비교한 쿼리의 시작 지점을 지시한다.

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