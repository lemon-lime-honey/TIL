# [Throttling](https://www.django-rest-framework.org/api-guide/throttling/)
```
HTTP/1.1 420 Enhance Your Calm
- Twitter API rate limiting response
```
~~X가 된 트위터~~

스로틀링은 요청이 인증되어야 하는지를 결정한다는 점에서 [권한](https://github.com/lemon-lime-honey/TIL/blob/main/django/drf/permissions.md)과 유사하다. 스로틀은 임시 상태를 지시하고 클라이언트가 API에 생성할 수 있는 요청의 속도를 제어하는데 사용된다.

권한에서 그러하듯이, 복수의 스로틀을 사용할 수 있다. API가 인증되지 않은 요청에는 엄격한 스로틀을, 인증된 요청에는 덜 엄격한 스로틀을 가질 수 있다.

특히 자원 집약적인 일부 서비스로 인해 API의 서로 다른 부분에 서로 다른 제한을 두어야 하는 경우 다중 스로틀을 사용한다.

다중 스로틀은 스로틀링 비율 버스트와 지속된 스로틀링 비율을 동시에 도입할 때에도 사용할 수 있다. 예를 들어 사용자가 분당 최대 60개의 요청, 일당 최대 1000개의 요청을 보내도록 제한할 수 있다.

스로틀은 요청 비율 제한만을 의미하지는 않는다. 예를 들어 스토리지 서비스 또한 대역폭에 대한 스로틀을 필요로 할 수 있고, 유료 데이터 서비스는 엑세스 되는 특정 레코드의 수에 대해 스로틀을 필요로 할 수 있다.

**REST framework가 제공하는 애플리케이션 수준의 스로틀링은 브루트 포싱이나 서비스 거부 공격에 대한 보안 조치 또는 보호로 간주되어서는 안 된다. 신중하게 악의적인 행위자는 언제나 IP 오리진을 속일 수 있다. 이에 더해, 빌트인 스로틀링 구현은 Django의 캐시 프레임워크를 사용해 구현되었으며 요청 속도를 결정하기 위해 비원자성 연산을 사용해 불분명한 결과를 낼 수 있다. 

REST framework가 제공하는 애플리케이션 수준 스로틀링은 서로 다른 비즈니스 티어나 서비스 과용에 대한 기본 보호 같은 정책을 구현하기 위해 의도되었다.**

## How throttling is determined
권한과 인증에서 그러했듯이, REST framework의 스로틀링은 언제나 클래스 리스트로 정의된다.

뷰의 메인 바디를 실행하기 전에 리스트의 각 스로틀이 체크된다. 만약 스로틀 체크에 실패하면 `exceptions.Throttled` 예외가 발생하며, 뷰의 메인 바디는 실행되지 않는다.

## Setting the throttling policy
`DEFAULT_THROTTLE_CLASSES`와 `DEFAULT_THROTTLE_RATES` 설정을 사용해 기본 스로틀링 정책을 전역적으로 설정할 수 있다. 예를 들어:

```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    }
}
```

`DEFAULT_THROTTLE_RATES`에서 사용된 비율 설명은 스로틀 주기에 따라 `second`, `minute`, `hour` 또는 `day`를 포함할 수 있다.

`APIView` 클래스 기반 뷰를 사용해 뷰당 혹은 viewset당 기반의 스로틀링 정책을 설정할 수 있다.

```python
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView


class ExampleView(APIView):
    throttle_classes = [UserRateThrottle]


    def get(self, request, format=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)
```

함수 기반 함수와 함께 `@api_view` 데코레이터를 사용한다면 다음 데코레이터를 쓰면 된다.

```python
@api_view(['GET'])
@throttle_classes([UserRateThrottle])
def example_view(request, format=None):
    content = {
        'status': 'request was permitted'
    }
    return Response(content)
```

`@action` 데코레이터를 사용해 생성된 경로를 위한 스로틀 클래스를 설정할 수 있다. 이 방식으로 설정된 스로틀 클래스는 모든 viewset 수준 클래스 설정을 override한다.

```python
@action(detail=True, methods=["post"], throttle_classes=[UserRateThrottle])
def example_adhoc_method(request, pk=None):
    content = {
        'status': 'request was permitted'
    }
    return Response(content)
```

## How clients are identified
스로틀링을 위해 클라이언트 IP 주소를 고유하게 식별하기 위해 `X-Forwarded-For` HTTP 헤더와 `REMOTE_ADDR` WSGI 변수가 사용된다. `X-Forwarded-For` 헤더가 존재한다면 그것이 사용되며, 그렇지 않다면 WSGI 환경의 `REMOTE_ADDR` 변수의 값이 사용된다.

고유한 클라이언트 IP 주소를 엄격히 식별해야 한다면 우선 `NUM_PROXIES` 설정을 설정해 API가 실행되는 애플리케이션 프록시의 수를 설정해야 한다. 이 설정은 0 이상의 정수여야 한다. 0이 아닌 수로 설정되었을 때 애플리케이션 프록시 IP 주소가 처음으로 제외되면 클라이언트 IP는 `X-Forwarded-For` 헤더의 마지막 IP주소로 식별된다. 0으로 설정되면 `REMOTE_ADDR` 값이 언제나 IP 주소를 식별하는데 사용된다.

`NUM_PROXIES` 설정을 설정했을 때 고유한 [NAT'd](https://en.wikipedia.org/wiki/Network_address_translation) 게이트웨이 뒤에 있는 모든 클라이언트가 하나의 클라이언트로 취급된다는 점을 이해하는 것이 중요하다.

[여기](http://oxpedia.org/wiki/index.php?title=AppSuite:Grizzly#Multiple_Proxies_in_front_of_the_cluster)에서 `X-Forwarded-For` 헤더가 어떻게 작동하는지와 원격 클라이언트 IP 식별하기에 관한 더 많은 정보를 찾을 수 있다.

## Setting up the cache
REST framework가 제공하는 스로틀 클래스는 Django의 캐시 백엔드를 사용한다. 적절한 [캐시 설정](https://docs.djangoproject.com/en/stable/ref/settings/#caches)을 설정하는 것이 중요하다. 기본값인 `LocMemCache` 백엔드는 단순한 설정을 위해서는 괜찮다. 자세한 사항은 Django의 [캐시 문서](https://docs.djangoproject.com/en/stable/topics/cache/#setting-up-the-cache)를 확인한다.

`'default'` 이외의 캐시를 사용해야 한다면, 사용자 정의 스로틀 클래스를 생성하고 `cache` 속성을 설정한다. 예를 들면:

```python
from django.core.cache import caches


class CustomAnonRateThrottle(AnonRateThrottle):
    cache = caches['alternate']
```

`'DEFAULT_THROTTLE_CLASSES` 설정 키 또는 `throttle_classes` 뷰 속성을 사용해 사용자 정의 스로틀 클래스를 설정해야 한다.

## A note on concurrency
빌트인 스로틀 구현은 [경쟁 상태](https://en.wikipedia.org/wiki/Race_condition#Data_race)에 개방되어 있으므로, 높은 동시성에서는 약간의 추가 요청을 허용할 수 있다.

프로젝트가 경쟁 요청 시 요청의 숫자를 보장해야 하는 경우 스로틀 클래스를 직접 구현해야 한다. 자세한 사항은 [5181번 이슈](https://github.com/encode/django-rest-framework/issues/5181)에서 확인할 수 있다.

# API Reference
## AnonRateThrottle
`AnonRateThrottle`은 인증되지 않은 사용자만 제한한다. 들어오는 요청의 IP 주소는 제한할 고유키를 생성하는데 사용된다.

허용 요청 비율은 다음에 의해 결정된다(우선순위 순서).

- `AnonRateThrottle`을 override하거나 속성을 설정해 제공되는 클래스의 `rate` 속성
- `DEFAULT_THROTTLE_RATES['anon']` 설정

`AnonRateThrottle`은 알 수 없는 출처로부터의 요청 비율을 제한하고 싶을 때 적절하다.

## UserRateThrottle
`UserRateThrottle`은 API 전체에서 주어진 요청 비율로 사용자를 제한한다. 유저 id는 제한할 고유키를 생성하는데 사용된다. 인증되지 않은 요청은 들어오는 요청의 IP 주소를 사용해 제한할 고유키를 생성하는 것으로 되돌아간다.

허용 요청 비율은 다음에 의해 결정된다(우선순위 순서).

- `UserRateThrottle`을 override하거나 속성을 설정해 제공되는 클래스의 `rate` 속성
- `DEFAULT_THROTTLE_RATES['user']` 설정

API는 동시에 복수의 `UserRateThrottle`를 가질 수 있다. 그렇게 하려면 `UserRateThrottle`을 override하고 각 클래스의 고유한 '범위'를 설정한다.

예를 들어, 다중 사용자 스로틀 비율은 다음 클래스와...

```python
class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'


class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'
```

...다음 설정을 사용해 구현할 수 있다.

```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'example.throttles.BurstRateThrottle',
        'example.throttles.SustainedRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'burst': '60/min',
        'sustained': '1000/day'
    }
}
```

사용자별 간단한 전역 비율 제한을 필요로 한다면 `UserRateThrottle`이 적당하다.

## ScopedRateThrottle
`ScopedRateThrottle` 클래스는 API의 특정 부분에 접근하는 것을 제한하기 위해 사용될 수 있다. 이 스로틀은 접근되는 뷰가 `.throttle_scope` 속성을 포함할 때에만 적용된다. 그 다음 요청의 '범위'와 고유한 사용자 id 또는 IP 주소를 연결해 고유한 스로틀 키가 형성된다.

허용 요청 비율은 요청 '범위'의 키를 사용한 `DEFAULT_THROTTLE_RATES` 설정을 사용해 결정된다.

예를 들어, 다음의 뷰와...

```python
class ContactListView(APIView):
    throttle_scope = 'contacts'
    ...


class ContactDetailView(APIView):
    throttle_scope = 'contacts'
    ...


class UploadView(APIView):
    throttle_scope = 'uploads'
    ...
```

...다음의 설정을 참고한다.

```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'contacts': '1000/day',
        'uploads': '20/day'
    }
}
```

`ContactListView` 또는 `ContactDetailView`에 대한 사용자 요청은 하루에 총 1000개의 요청으로 제한된다. `UploadView`에 대한 사용자 요청은 하루에 20개의 요청으로 제한된다.

# Custom throttles
사용자 정의 스로틀을 생성하려면, `BaseThrottle`을 override하고 `.allow_request(self, request, view)`를 구현한다. 이 메서드는 요청이 허용되어야 하면 `True`를, 아니면 `False`를 반환한다.

선택적으로 `.wait()` 메서드를 override할 수 있다. 구현되었다면 `.wait()`는 다음 요청을 시도하기 전에 대기해야 할 권장 시간(초)이나 `None`을 반환해야 한다. `.wait()` 메서드는 앞서 `.allow_request()`가 `False`를 반환했을 때에만 호출된다.

`.wait()` 메서드가 구현되었고, 요청이 스로틀되었다면 응답에 `Retry-After` 헤더가 포함된다.

## Example
다음은 매 10개의 요청마다 하나를 무작위로 스로틀하는 비율 스로틀의 예시이다.

```python
import random


class RandomRateThrottle(throttling.BaseThrottle):
    def allow_request(self, request, view):
        return random.randint(1, 10) != 1
```