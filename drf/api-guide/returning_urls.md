# [Returning URLs](https://www.django-rest-framework.org/api-guide/reverse/)
```
REST 아키텍처 형식을 다른 네트워크 기반 형식과 구별하는 가장 핵심적인 특징은 구성요소 간의 일관적인 인터페이스를 강조한다는 점이다.
- Roy Fielding, Architectural Styles and the Design of Network-based Software Architectures
```

원칙적으로는 웹 API가 `/foobar`와 같은 상대 URI를 반환하는 것보다 `http://example.com/foobar`와 같은 절대 URI를 반환하는 것이 더 좋을 것이다.

그렇게 하는 것의 이점은:

- 더 명시적이다.
- API 클라이언트의 부담을 덜 수 있다.
- 네이티브 URI 타입을 가지지 않는 JSON과 같은 표현에서 발견되었을 떄 문자열의 의미가 모호하지 않다.
- 하이퍼링크를 가진 마크업 HTML 표현과 같은 작업을 쉽게 수행할 수 있다.

REST framewor는 두 유틸리티 함수를 제공해 웹 API가 절대 URI를 쉽게 반환하게 한다.

이를 꼭 사용할 필요는 없지만, 사용하게 되면 자기 설명 API가 자동으로 출력을 하이퍼링크로 만들어 API를 더 쉽게 브라우징할 수 있게 한다.

## reverse
**Signature**: `reverse(viewname, *args, **kwargs)`

요청을 사용해 호스트와 포트를 결정해 정규화된 URL를 반환한다는 점을 제외하면 `django.urls.reverse`와 같은 동작을 가진다.

다음과 같이 함수에 **요청을 키워드 인자로 포함**해야 한다:

```python
from rest_framework.reverse improt reverse
from rest_framework.views import APIView
from django.utils.timezone import now

class APIRootView(APIView):
    def get(self, request):
        year = now().year
        data = {
            ...
            'year-summary-url': reverse('year-summary', args=[year], request=request)
        }
        return Response(data)
```

## reverse_lazy
**Signature**: `reverse_lazy(viewname, *args, **kwargs)`

요청을 사용해 호스트와 포트를 결정해 정규화된 URL를 반환한다는 점을 제외하면 `django.urls.reverse_lazy`와 같은 동작을 가진다.

`reverse`함수처럼 다음과 같이 함수에 **요청을 키워드 인자로 포함**해야 한다:

```python
api_root = reverse_lazy('api-root', request=request)
```