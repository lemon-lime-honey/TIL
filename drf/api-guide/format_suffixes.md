# [Format suffixes](https://www.django-rest-framework.org/api-guide/format-suffixes/)
```
섹션 6.2.1에서는 언제나 컨텐츠 협상을 사용해야 한다고 언급하지 않았다.
- Roy Fielding, REST discuss mailing list
```

주어진 미디어 타입을 위한 엔드포인트를 제공하기 위해 URL에서 파일명 확장자를 사용하는 것은 웹 API의 일반적인 패턴이다. 예를 들어, 'http://example.com/api/users.json'은 JSON 표현을 제공한다.

API URLconf의 각 개별 엔트리에 포맷 접미사 패턴을 추가하는 것은 오류가 발생하기 쉽고, DRY하지 않기 때문에 REST framework는 URLConf에 이러한 패턴을 추가하는 손쉬운 방법을 제공한다.

## format_suffix_patterns
**Signature**: `format_suffix_patterns(urlpatterns, suffix_required=False, allowed=None)`

주어진 각 URL 패턴에 추가된 포맷 접미사 패턴을 포함하는 URL 패턴 리스트를 반환한다.

Arguments:<br>
- `urlpatterns`<br>
  필수. URL 패턴 리스트
- `suffix_required`<br>
  선택. URL의 접미사가 필수인지 아닌지를 지시하는 불리언. 기본값은 `False`인데, 이는 기본적으로 접미사가 옵션이라는 것을 의미한다.
- `allowed`<br>
  선택. 유효한 포맷 접미사의 리스트 또는 튜플. 주어지지 않는다면 와일드카드 포맷 접미사 패턴이 사용된다.

Example:

```python
from rest_framework.urlpatterns import format_suffix_patterns
from blog import views

urlpatterns = [
    path('', views.apt_root),
    path('comments/', views.comment_list),
    path('comments/<int:pk>/', views.comment_detail)
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
```

`format_suffix_patterns`를 사용할 때에는 대응되는 뷰에 `'format'` 키워드 인자를 추가해야 한다. 예를 들어:

```python
@api_view(['GET', 'POST'])
def comment_list(request, format=None):
    # do stuff...
```

클래스 기반 뷰를 사용하면:

```python
class CommentList(APIView):
    def get(self, request, format=None):
        # do stuff...


    def post(self, request, format=None):
        # do stuff...
```

키워드 인자의 이름은 `FORMAT_SUFFIX_KWARG` 설정을 사용해 변경할 수 있다.

`format_suffix_patterns`가 `include` URL 패턴의 안까지 지원하지는 않는다는 점에 유의한다.

### Using with `i18n_patterns`
`format_suffix_patterns` 뿐만이 아니라 Django가 제공하는 `i18n_patterns` 함수를 사용한다면 `i18n_patterns` 함수는 최종적으로, 혹은 가장 바깥에 있는 함수에 적용되어야 한다. 예를 들어:

```python
urlpattens = [
    ...
]

urlpatterns = i18n_patterns(
    format_suffix_patterns(urlpatterns, allowed=['json', 'html'
    ])
)
```

## Query parameter formats
포맷 접미사의 대체로는 쿼리 파라미터의 요청된 포맷을 포함하는 방법이 있다. REST ,framework는 이 옵션을 기본으로 제공하며, 이 옵션은 서로 다른 사용 가능한 표현 사이에서 전환하기 위해 브라우징 가능한 API에서 사용된다.

표현을 짧은 포맷을 사용하여 선택하려면 `format` 쿼리 파라미터를 사용한다. 예를 들어: `http://example.com/organizations/?format=csv`

이 쿼리 파라미터의 이름은 `URL_FORMAT_OVERRIDE` 설정을 이용하여 변경할 수 있다. 이 동작을 비활성화하려면 값을 `None`으로 설정한다.

## Accept headers vs. format suffixes
파일명 확장자가 RESTful한 패턴이 아니며 대신 언제나 `HTTP Accept` 헤더가 사용되는 뷰가 어떤 웹 커뮤니티 사이에서 언급된다.

이는 잘못된 접근이다. 예를 들어, 파일 확장자 미디어 타입 지시자에 대한 쿼리 파라미터 미디어 타입 지시자의 상대적인 이점에 관해 논하는 Roy Fielding의 다음 인용문을 확인한다:

"이것이 바로 내가 언제나 확장자를 선호하는 이유이다. 둘 다 REST와는 관계가 없다." - Roy Fielding, [REST discuss mailing list](https://groups.yahoo.com/neo/groups/rest-discuss/conversations/topics/14844)

인용문은 Accept 헤더를 언급하고 있지 않지만, 포맷 접미사가 허용 가능한 패턴으로 간주되어야 한다는 점을 명확히 하고 있다.