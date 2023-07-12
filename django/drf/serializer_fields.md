# [Serializer fields](https://www.django-rest-framework.org/api-guide/fields/)
```
폼 클래스의 각 필드는 데이터의 유효성을 검증하는 것 뿐만 아니라 깨끗하게 하는 데에도 책임이 있다.
즉, 데이터를 올바른 포맷으로 정규화해야 한다.
- Django 공식 문서
```

시리얼라이저 필드는 원시 값과 내부 데이터형 사이의 변환을 다룬다. 또한 입력 값의 유효성 뿐만 아니라 부모 객체의 값을 찾고 설정하는 것 또한 다룬다.

- **Note**:<br>
  시리얼라이저 필드는 `fields.py`에서 선언되나, 관습적으로는 `from rest_framework import serializer`로 불러와 필드를 `serializers.<FieldName>`으로 참조한다.

## Core arguments
각 시리얼라이저 필드 클래스 생성자는 최소한 이 인자들을 필요로 한다. 몇몇 필드 클래스는 추가적인, 필드에 구체적인 인자를 가지지만 다음은 언제나 수용되어야 한다.

### `read_only`
읽기 전용 필드는 API 출력에 포함되지만 생성 또는 갱신 연산 도중의 입력에는 포함되지 않아야 한다. 시리얼라이저 입력에 부정확하게 포함된 'read_only' 필드는 무시된다.

표현을 serialize할 때 해당 필드가 사용됨을 보장하기 위해 `True`로 설정되지만, deserialize하는 동안 인스턴스를 생성하거나 갱신할 때에는 사용되지 않는다.

기본값: `False`

### `write_only`
인스턴스를 갱신하거나 생성할 때 필드가 사용되는 것을 보장하기 위해 `True`로 설정되지만, 표현을 serialize할 때에는 포함되지 않는다.

기본값: `False`

### `required`
일반적으로는 deserialize 과정 중에 필드가 제공되지 않으면 오류를 발생시킨다. Deserialize 과정 중 해당 필드가 존재하지 않아도 된다면 `False`로 설정한다.

또한 이를 `False`로 설정하는 것은 객체 속성이나 딕셔너리 키가 인스턴스를 serialize할 때 출력에서 생략될 수 있도록 허용하게 한다. 키가 존재하지 않는다면 단순히 출력 표현에 포함시키지 않는다.

기본값: `True`

[모델 시리얼라이저](https://www.django-rest-framework.org/api-guide/serializers/#modelserializer)를 사용하고, `Model`의 필드에 `blank=True`, `default` 또는 `null=True`를 명시했다면 기본값은 `False`이다.

### `default`
설정되었다면, 입력 값이 주어지지 않았을 때 필드에 사용될 기본값을 제공한다. 기본 동작을 설정하지 않는 것은 속성을 채우지 않는 것이다.

`default`는 부분 갱신 연산에서는 적용되지 않는다. 부분 갱신의 경우 입력 데이터에서 주어진 필드만이 반환된 유효한 값을 가지게 된다.

사용될 때마다 값이 계산되어야 하는 경우 함수 또는 그 이외의 호출 가능한 것으로 설정될 수 있다. 호출되었을 때, 인자를 받지 않는다. 만약 호출 가능한 것이 `requires_context=True` 속성을 가진다면, 시리얼라이저 필드가 인자로 전달된다.

예를 들면:

```python
class CurrentUserDefault:
    """
    May be applied as a `default=...` value on a serializer field.
    Returns the current user.
    """
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['request'].user
```

인스턴스를 serialize할 때 인스턴스에 객체 속성이나 딕셔너리 키가 존재하지 않는다면 기본값이 사용될 것이다.

`default` 값을 설정하는 것은 필드가 필수가 아니라는 것을 암시한다는 점에 유의한다. `default`와 `required` 키워드 인자를 둘 다 포함하게 되는 것은 유효하지 않으며 오류를 발생시킨다.

### `allow_null`
일반적으로 `None`이 시리얼라이저 필드로 전달되었을 때 오류가 발생한다. `None`이 유효한 값으로 여겨지려면 이 키워드 인자를 `True`로 설정한다.

명시적인 `default`가 없다면 이 인자를 `True`로 설정하는 것은 serialize 출력의 `default` 값이 `null`이라는 것을 암시하지만, 입력 deserialize의 기본값을 암시하는 것은 아니라는 점에 유의한다.

기본값: `False`

### `source`
필드를 채우기 위해 사용될 속성의 이름. `URLField(source='get_absolute_url')`과 같은 `self` 인자만을 가지는 메서드가 되거나 혹은 `EmailField(source='user.email')`과 같은 속성을 선택하는 점을 찍는 표기법을 사용할 수 있다.

필드를 점을 찍는 표기법으로 serialize할 때 속성 선택 중 객체가 존재하지 않거나 비었을 경우 `default` 값을 제공해야 할 수 있다. 관계 orm 모델에 접근한다면 소스 속성을 사용할 때 발생할 수 있는 `n + 1 문제`에 주의한다. 예를 들면:

```python
class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField(source="user.email")
```

는 유저 객체가 prefetch되지 않았을 때 데이터베이스로부터 가져오는 것을 필요로 할 수 있다. 원치 않는다면 `prefetch_related`와 `select_related` 메서드를 적절히 사용한다. 메서드에 관해서는 [Django 공식 문서](https://docs.djangoproject.com/en/3.2/ref/models/querysets/#django.db.models.query.QuerySet.select_related)에서 확인할 수 있다.

`source='*`는 특별한 의미를 가지며, 객체 전체가 필드로 전달되어야 한다는 것을 의미한다. 이는 중첩된 표현을 생성할 때 혹은 출력 표현을 결정하기 위해 온전한 객체에 접근해야 하는 필드에 유용하다.

기본값: 필드의 이름

### `validators`
들어오는 필드 입력에 적용되어야 하고, 유효성 검증 오류를 발생시키거나 단순히 반환하는 유효성 검사 함수 리스트. 유효성 검사 함수는 보통 `serializers.ValidationError`를 발생시키지만, Django의 빌트인 `ValidationError`는 Django 코드베이스나 서드파티 Django 패키지에서 정의된 유효성 검사 함수의 호환을 지원한다.

### `error_messages`
오류 코드에 해당하는 오류 메시지 딕셔너리

### `label`
HTML 폼 필드의 필드 또는 다른 기술(記述)적인 원소의 이름에 사용되는 짧은 텍스트 문자열

### `help_text`
HTML 폼 필드의 필드 또는 다른 기술적인 원소의 설명에 사용되는 텍스트 문자열

### `initial`
HTML 폼 필드의 값을 미리 채우는데 사용되는 값. 일반적인 Django `Field`에서 그러하듯이 호출 가능한 것을 전달해도 된다.

```python
import datetime
from rest_framework import serializers
class ExampleSerializer(serializers.Serializer):
    day = serializers.DateField(initial=datetime.date.today)
```

### `style`
렌더러가 어떻게 필드를 렌더링할지 제어하는데 사용되는 키-값 쌍 딕셔너리

여기있는 두 예시는 `'input_type'`과 `'base_template'`이다.

```python
# Use <input type="password"> for the input.
password = serializers.CharField(
    style={'input_type': 'password'}
)

# Use a radio input instead of a select input.
color_channel = serializers.ChoiceField(
    choices=['red', 'green', 'blue']
    style={'base_template': 'radio.html'}
)
```

[HTML & Forms](https://www.django-rest-framework.org/topics/html-and-forms/) 문서에서 더 많은 정보를 확인할 수 있다.

# Boolean fields
## BooleanField
불리언 표현.

인코딩된 HTML 폼 입력을 사용할 때 값을 생략하는 것은 `default=True` 옵션이 있더라도 언제나 필드를 `False`로 설정하는 것으로 여겨진다는 것에 유의한다. HTML 체크박스 입력이 체크되지 않은 상태를 값을 생략하는 것으로 표현하기 때문에, REST framework는 생략을 빈 체크박스 입력처럼 다룬다.

Django 2.1에서 `models.BooleanField`의 `blank` 키워드 인자를 제거했다는 점에 유의한다. Django 2.1 이전에서는 `models.BooleanField` 필드는 언제나 `blank=True`였다. 그러므로 Django 2.1부터 기본 `serializers.BooleanField` 인스턴스는 Django의 이전 버전에서 기본 `BooleanField` 인스턴스가 `required=False` 옵션을 가지고 생성되었던 것과는 대조적으로 `required` 키워드 인자(예를 들어 `required=True`와 동등한) 없이 생성될 것이다. 만약 이 동작을 직접 제어하고 싶다면 시리얼라이저에서 `BooleanField`를 명시적으로 선언하거나 `required` 플래그를 설정하기 위해 `extra_kwargs` 옵션을 사용한다.

`django.db.models.fields.BooleanField`에 대응된다.

**Signature**: `BooleanField()`