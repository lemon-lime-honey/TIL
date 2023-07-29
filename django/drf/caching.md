# [Caching](https://www.django-rest-framework.org/api-guide/caching/)
```
어떤 여성은 매우 날카로운 정신을 가졌지만 기억을 거의 하지 못했다...
일하기 충분할 정도로는 기억을 했고, 일을 열심히 했다.
- Lydia Davis
```

REST Framework의 캐싱은 Django에서 제공되는 캐시 유틸리티로 잘 작동된다.

## Using cache with apiview and viewsets
Django는 데코레이터를 클래스 기반 뷰와 같이 쓸 수 있도록 `method_decorator`를 제공한다. 이는 `cache_page`, `vary_on_cookie`, `vary_on_headers`와 같은 다른 캐시 데코레이터와 함께 사용될 수 있다.

```python
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets


class UserViewSet(viewsets.ViewSet):
    # With cookie: cache requested url for each user for 2 hours
    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_cookie)
    def list(self, request, format=None):
        content = {
            'user_feed': request.user.get_user_feed()
        }
        return Response(content)


class ProfileView(APIView):
    # With auth: cache requested url for each user for 2 hours
    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_headers("Authorization",))
    def get(self, request, format=None):
        content = {
            'user_feed': request.user.get_user_feed()
        }
        return Response(content)


class PostView(APIView):
    # Cache page for the requested url
    @method_decorator(cache_page(60*60*2))
    def get(self, request, format=None):
        content = {
            'title': 'Post title',
            'body': 'Post content'
        }
        return Response(content)
```

**NOTE**: `cache_page` 데코레이터는 상태 200인 `GET`과 `HEAD` 응답만 캐싱한다.