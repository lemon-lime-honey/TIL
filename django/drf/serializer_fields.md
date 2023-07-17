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

# String fields
## CharField
텍스트 표현. 조건이 주어지면 `max_length`보다 짧고 `min_length`보다 긴 텍스트의 유효성을 검사한다.

`django.db.models.fields.CharField` 또는 `django.db.models.fields.TextField`에 대응된다.

**Signature**: `CharField(max_length=None, min_length=None, allow_blank=False, trim_whitespace=True)`

- `max_length`<br>
  이 길이를 넘지 않는 개수의 문자를 포함하는 입력의 유효성을 검증한다.
- `min_length`<br>
  이 길이보다 적지 않은 개수의 문자를 포함하는 입력의 유효성을 검증한다.
- `allow_blank`<br>
  `True`로 설정된다면 빈 문자열이 유효한 값으로 간주된다. `False`로 설정된다면 빈 문자열이 유효하지 않은 값으로 간주되며 유효성 오류를 일으킨다. 기본값은 `False`.
- `trim_whitespace`<br>
  `True`로 설정된다면 양 끝의 공백이 제거된다. 기본값은 `True`.

`allow_blank`의 선호도로 잘 사용되지는 않지만 문자열 필드에 `allow_null` 옵션 또한 사용할 수 있다. `allow_blank=True`와 `allow_null=True`를 함께 사용하는 것도 가능하지만 이렇게 하면 문자열 표현에 있어 허용되는 빈 값이 서로 다른 두 종류가 되지 때문에 데이터가 비일관성과 미묘한 애플리케이션 버그가 발생할 수 있다.

## EmailField
텍스트 표현. 텍스트가 유효한 전자우편 주소인지 검증한다.

`django.db.models.fields.EmailField`에 대응된다.

**Signature**: `EmailField(max_length=None, min_length=None, allow_blank=False)`

## RegexField
텍스트 표현. 주어진 값이 특정 정규표현식과 일치하는지 검증한다.

`django.forms.fields.RegexField`에 대응된다.

**Signature**: `RegexField(regex, max_length=None, min_length=None, allow_blank=False)`

필수 `regex` 인자는 문자열 또는 컴파일된 파이썬 정규표현 객체가 될 수 있다.

유효성 검증에 Django의 `django.core.validators.RegexValidator`를 사용한다.

## SlugField
입력이 패턴 `[a-zA-Z0-9_-]+`과 일치하는지 검증하는 `RegexField`

`django.db.models.fields.SlugField`에 대응된다.

**Signature**: `SlugField(max_length=50, min_length=None, allow_blank=False)`

## URLField
입력이 URL 매핑 패턴과 일치하는지 검증하는 `RegexField`. `http://<host>/<path>` 형식의 정규화된 URL이어야 한다.

`django.db.models.fields.URLField`에 대응된다. 유효성 검증에 Django의 `django.core.validators.URLValidator`를 사용한다.

## UUIDField
입력이 유효한 UUID 문자열임을 보장하는 필드. `to_internal_value` 메서드가 `uuid.UUID` 인스턴스를 반환한다. 출력 시 필드는 다음과 같은 정규 하이픈 형식의 문자열을 반환한다.

```
"de305d54-75b4-431b-adb2-eb6b9e546013"
```

**Signature**: `UUIDField(format='hex_verbose')`

- `format`: uuid 값의 표현 형식을 결적힌다.
  - `'hex_verbose`<br>
    하이픈을 포함한 정규 16진법 표현: `"5ce0e9a5-5ffa-654b-cee0-1238041fb31a"`
  - `'hex'`<br>
    하이픈을 포함하지 않은 UUID의 압축된 16진법 표현: `"5ce0e9a55ffa654bcee01238041fb31a"`
  - `'int'`<br>
    UUID의 128 비트 정수 표현: `"123456789012312313134124512351145145114"`
  - `'urn'`<br>
    UUID의 RFC 4122 URN 표현: `"urn:uuid:5ce0e9a5-5ffa-654b-cee0-1238041fb31a"`<br>
    `format` 인자의 변경은 표현 값에만 영향을 준다. 모든 포맷은 `to_internal_value`에 의해 수용된다.

## FilePathField
파일시스템의 특정 디렉토리 안의 파일 이름으로 선택이 한정된 필드.

`django.forms.fields.FilePathField`에 대응된다.

**Signature**: `FilePathField(path, match=None, recursive=False, allow_files=True, allow_folders=False, required=None, **kwargs)`

- `path`<br>
  이 FilePathField가 위치를 저장해야 할 파일이 있는 디렉토리의 절대경로
- `match`<br>
  FilePathField가 파일 이름을 필터링하기 위해 사용할 문자열 정규 표현식
- `recursive`<br>
  경로의 모든 서브 디렉토리를 포함시킬지 여부. 기본값은 `False`
- `allow_files`<br>
  명시된 위치에 있는 파일을 포함시킬지 여부. 기본값은 `True`. 이 조건 또는 `allow_folders`은 `True`여야 한다.
- `allow_folders`<br>
  명시된 위치에 있는 폴더를 포함시킬지 여부. 기본값은 `False`. 이 조건 또는 `allow_files`는 `True`여야 한다.

## IPAddressField
입력이 유효한 IPv4 또는 IPv6 문자열임을 보장하는 필드.

`django.forms.fields.IPAddressField`와 `django.forms.fields.GenericIPAddressField`에 대응된다.

**Signature**: `IPAddressField(protocol='both', unpack_ipv4=False, **options)`

- `protocol`는 명시된 프로토콜로 유효한 입력을 제한한다. 수용 가능한 값으로는 'both'(기본값), 'IPv4', 'IPv6'이 있다. 대소문자를 구분하지 않고 일치하는 것을 찾는다.
- `unpack_ipv4`는 ::ffff:192.0.2.1과 같은 IPv4로 매핑된 주소를 unpack한다. 이 옵션이 활성화되면 언급한 주소가 192.0.2.1로 unpack된다. 기본값은 비활성화. 프로토콜이 'both'로 설정되어 있을 때에만 사용할 수 있다.

# Numeric fields
## IntegerField
정수형 표현.

`django.db.models.fields.IntegerField`, `django.db.models.fields.SmallIntegerField`, `django.db.models.fields.PositiveIntegerField`, `django.db.models.fields.PositiveSmallIntegerField`에 대응된다.

**Signature**: `IntegerField(max_value=None, min_value=None)`

- `max_value`: 주어진 숫자가 이 값보다 크지 않은지 검증한다.
- `min_value`: 주어진 숫자가 이 값보다 작지 않은지 검증한다.

## FloatField
부동 소수점 표현.

`django.db.models.fields.FloatField`에 대응된다.

**Signature**: `FloatField(max_value=None, min_value=None)`

- `max_value`: 주어진 숫자가 이 값보다 크지 않은지 검증한다.
- `min_value`: 주어진 숫자가 이 값보다 작지 않은지 검증한다.

## DecimalField
`Decimal` 인스턴스에 의해 파이썬에서 표현되는 십진 고정 소수점 및 부동 소수점 표현.

`django.db.models.fields.DecimalField`에 대응된다.

**Signature**: `DecimalField(max_digits, decimal_places, coerce_to_string=None, max_value=None, min_value=None)`

- `max_digits`<br>
  숫자에서 허용되는 최대 자리수. `None`이거나 `decimal_places` 이상인 정수여야 한다.
- `decimal_places`<br>
  숫자를 저장하기 위한 자리의 개수
- `coerce_to_string`<br>
  문자열 값으로 반환되어야 한다면 `True`, `Decimal` 객체가 반환되어야 한다면 `False`로 설정한다. 기본값은 override되지 않는다면 `True`인 `CORECE_DECIMAL_TO_STRING` 설정 키와 같은 값이다. 시리얼라이저가 `Decimal` 객체를 반환하면 최종 출력 포맷은 렌더러에 의해 결정된다. `localize`를 설정하면 `True`로 강제된다는 점에 주의한다.
- `max_value`<br>
  주어진 숫자가 이 값보다 크지 않은지 검증한다.
- `min_value`<br>
  주어진 숫자가 이 값보다 작지 않은지 검증한다.
- `localize`<br>
  현재 로케일에 기반해 입력과 출력을 로컬라이즈하려면 `True`로 설정한다. 그러면 `coerce_to_string` 또한 강제로 `True`가 된다. 기본값은 `False`이다. 설정 파일에서 `USE_L10N=True`를 설정했다면 데이터 포맷팅이 가능하다는 점에 주의한다.
- `rounding`<br>
  양자화 시 설정된 정밀도로 반올림 모드를 설정한다. 유효한 값은 [`decimal` 모듈 반올림 모드](https://docs.python.org/3/library/decimal.html#rounding-modes)이다. 기본값은 `None`.

### Example usage
999까지의 수를 decimal 두 자리수의 해상도로 유효하게 하려면 이렇게 작성한다.

```python
serializers.DecimalField(max_digits=5, decimal_places)
```

10억 이하의 숫자를 decimal 10자리수의 해상도로 유효하게 하려면 이렇게 작성한다.

```python
serializer.DecimalField(max_digits=19, decimal_places=10)
```

# Date and time fields
## DateTimeField
날짜와 시간 표현.

`django.db.models.fields.DateTimeField`에 대응된다.

**Signature**: `DateTimeField(format=api_settings.DATETIME_FORMAT, input_formats=None, default_timezone=None)`

- `format`<br>
  출력 형식을 나타내는 문자열. 주어지지 않았을 때, 설정되지 않았다면 기본값은 `'iso-8601`이 되는 `DATETIME_FORMAT` 설정 키와 같은 값이 된다. 형식 문자열 설정은 `to_representation`의 반환값이 문자열 출력에서 무조건 적용되어야 하는 것을 의미한다. 이 값을 `None`으로 설정하는 것은 파이썬 `datetime` 객체가 `to_representation`에 의해 반환되어야 한다는 것을 의미한다. 이 경우 datetime 인코딩은 렌더러에 의해 결정된다.
- `input_formats`<br>
  날짜를 파싱할 때 사용될 수 있는 입력 형식을 나타내는 문자열의 리스트. 주어지지 않는다면 `['iso-8601']`을 기본값으로 갖는 `DATETIME_INPUT_FORMATS` 설정이 사용된다.
- `default_timezone`<br>
  시간대를 나타내는 `tzinfo` 서브 클래스(`zoneinfo` 또는 `pytz`). 주어지지 않았고, `USE_TZ` 설정이 활성화되었다면 [현재 시간대](https://docs.djangoproject.com/en/stable/topics/i18n/timezones/#default-time-zone-and-current-time-zone)가 기본값이 된다. `USE_TZ`가 비활성화되었다면 datetime 객체는 naive하다.

### `DateTimeField` format strings
형식 문자열은 형식을 명시적으로 구체화하는 [파이썬 strftime formats](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior)이나 [ISO 8601](https://www.w3.org/TR/NOTE-datetime) 형식 날짜와 시간(예: `'2013-01-29T12:34:56.000000Z'`)이 사용되어야 함을 가리키는 특수 문자열 `'iso-8601'`이 될 수 있다.

형식에 `None` 값이 사용된다면 `datetime` 객체는 `to_representation`에 의해 반환될 것이며 최종 출력 표현은 렌더러 클래스에 의해 결정될 것이다.

### `auto_now` and `auto_now_add` model fields
`ModelSerializer` 혹은 `HyperlinkedModelSerializer`를 사용할 때, `auto_now=True` 또는 `auto_now_add=True`인 모델 필드는 기본적으로 `read_only=True`인 시리얼라이저 필드를 사용한다는 점에 주의한다.

이런 동작을 override하고 싶다면, 시리얼라이저에 `DateTimeField`를 명시적으로 선언해야 한다. 예를 들면:

```python
class CommentSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField()

    class Meta:
        model = Comment
```

## DateField
날짜 표현.

`django.db.models.fields.DateField`에 대응된다.

**Signature**: `DateField(format=api_settings.DATE_FORMAT, input_formats=None)`

- `format`<br>
  출력 형식을 표현하는 문자열. 주어지지 않는다면 따로 설정되지 않는 한 `'iso-8601'`인 `DATE_FORMAT` 설정 키와 같은 값을 기본값으로 갖는다. 형식 문자열을 설정하는 것은 `to_representation`의 반환 값이 문자열 출력에서 무조건 적용되어야 한다는 것을 의미한다. 형식 문자열은 아래에서 설명된다. 이 값을 `None`으로 설정하는 것은 파이썬 `date` 객체가 `to_representation`에 의해 반환되어야 한다는 것을 의미한다. 이 경우 날짜 인코딩은 렌더러에 의해 결정된다.
- `input_formats`<br>
  날짜를 파싱하기 위해 사용되는 입력 형식을 나타내는 문자열의 리스트. 주어지지 않는다면 `['iso-8601']`을 기본값으로 가지는 `DATE_INPUT_FORMATS` 설정이 사용된다.

### `DateField` format strings
형식 문자열은 형식을 명시적으로 구체화하는 [파이썬 strftime formats](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior)이나 [ISO 8601](https://www.w3.org/TR/NOTE-datetime) 형식 날짜(예: `'2013-01-29'`)가 사용되어야 함을 가리키는 특수 문자열 `'iso-8601'`이 될 수 있다.

## TimeField
시간 표현.

`django.db.models.fields.TimeField`에 대응된다.

**Signature**: `TimeField(format=api_settings.TIME_FORMAT, input_formats=None)`

- `format`<br>
  출력 형식을 표현하는 문자열. 주어지지 않는다면 따로 설정되지 않는 한 `'iso-8601'`인 `DATE_FORMAT` 설정 키와 같은 값을 기본값으로 갖는다. 형식 문자열을 설정하는 것은 `to_representation`의 반환 값이 문자열 출력에서 무조건 적용되어야 한다는 것을 의미한다. 형식 문자열은 아래에서 설명된다. 이 값을 `None`으로 설정하는 것은 파이썬 `time` 객체가 `to_representation`에 의해 반환되어야 한다는 것을 의미한다. 이 경우 시간 인코딩은 렌더러에 의해 결정된다.
- `input_formats`<br>
  시간를 파싱하기 위해 사용되는 입력 형식을 나타내는 문자열의 리스트. 주어지지 않는다면 `['iso-8601']`을 기본값으로 가지는 `DATE_INPUT_FORMATS` 설정이 사용된다.

### `TimeField` format strings
형식 문자열은 형식을 명시적으로 구체화하는 [파이썬 strftime formats](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior)이나 [ISO 8601](https://www.w3.org/TR/NOTE-datetime) 형식 시간(예: `'12:34:56.000000'`)이 사용되어야 함을 가리키는 특수 문자열 `'iso-8601'`이 될 수 있다.

## DurationField
기간 표현. `django.db.models.fields.DurationField`에 대응된다.

이 필드를 위한 `validated_data`는 `datetime.timedelta` 인스턴스를 포함한다. `'[DD] [HH:[MM:]]ss[.uuuuuu]'`과 같은 형식을 가지는 문자열 표현이다.

**Signature**: `DurationField(max_value=None, min_value=None)`

- `max_value`: 주어진 기간이 이 값보다 길지 않은지 검증한다.
- `min_value`: 주어진 기간이 이 값보다 짧지 않은지 검증한다.

# Choice selection fields
## ChoiceField
한정된 선택 모음의 값만 허용하는 필드

대응되는 모델 필드가 `choices=...` 인자를 가지는 경우 자동으로 필드를 생성하기 위해 `ModelSerializer`에 의해 사용된다.

**Signature**: `ChoiceField(choices)`

- `choices`<br>
  유효한 값 또는 `(key, display_name)` 튜플의 리스트
- `allow_blank`<br>
  `True`로 설정된다면 빈 문자열이 유효한 값으로 간주된다. `False`로 설정된다면 빈 문자열이 유효하지 않은 값으로 간주되며 유효성 검증 오류를 일으킨다. 기본값은 `False`.
- `html_cutoff`<br>
  설정된다면 HTML 선택 드롭다운에서 보여지는 선택지의 최대 숫자가 된다. 자동으로 생성된 매우 많은 선택지를 가진 ChoiceField가 템플릿 폼 렌더링을 방해하지 않는 것을 보장하기 위해 사용될 수 있다. 기본값은 `None`.
- `html_cutoff_text`<br>
  설정된다면 HTML 선택 드롭다운에서 최대 숫자를 넘겨 생략된 아이템이 있을 때 텍스트 설명을 보여준다. 기본값은 `"More than {count} items..."`

둘 모두를 사용하기 보다 하나만 사용하는 것이 강력히 권장되지만, `allow_blank`와 `allow_null` 모두 `ChoiceField`에서 유효한 옵션이다. `allow_blank`는 문자 선택지, `allow_null`은 숫자 또는 문자가 아닌 다른 선택지에 선호된다.

## MultipleChoiceField
한정된 선택지에서 선택된 빈 값, 하나 혹은 여러 개의 값 모음을 허용하는 필드. 하나의 필수 인자를 가진다. `to_internal_value`는 선택된 값을 포함하는 `set`를 반환한다.

**Signature**: `MultipleChoiceField(choices)`

- `choices`<br>
  유효한 값 또는 `(key, display_name)` 튜플의 리스트
- `allow_blank`<br>
  `True`로 설정된다면 빈 문자열이 유효한 값으로 간주된다. `False`로 설정된다면 빈 문자열이 유효하지 않은 값으로 간주되며 유효성 검증 오류를 일으킨다. 기본값은 `False`.
- `html_cutoff`<br>
  설정된다면 HTML 선택 드롭다운에서 보여지는 선택지의 최대 숫자가 된다. 자동으로 생성된 매우 많은 선택지를 가진 ChoiceField가 템플릿 폼 렌더링을 방해하지 않는 것을 보장하기 위해 사용될 수 있다. 기본값은 `None`.
- `html_cutoff_text`<br>
  설정된다면 HTML 선택 드롭다운에서 최대 숫자를 넘겨 생략된 아이템이 있을 때 텍스트 설명을 보여준다. 기본값은 `"More than {count} items..."`

`ChoiceField`에서처럼, 둘 모두를 사용하기 보다 하나만 사용하는 것이 강력히 권장되지만 `allow_blank`와 `allow_null` 모두 `ChoiceField`에서 유효한 옵션이다. `allow_blank`는 문자 선택지, `allow_null`은 숫자 또는 문자가 아닌 다른 선택지에 선호된다.

# File upload fields
### Parsers and file uploads
`FileField`와 `ImageField` 클래스는 오직 `MultiPartParser` 또는 `FileUploadParser`와 함께 사용할 수 있다. JSON과 같은 대부분의 parser는 파일 업로드를 지원하지 않는다. Django의 표준 [FILE_UPLOAD_HANDERS](https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-FILE_UPLOAD_HANDLERS)가 파일 업로드를 다루기 위해 사용된다.

## FileField
파일 표현. Django의 표준 FileField 유효성 검증을 수행한다.

`django.forms.fields.FileField`에 대응된다.

**Signature**: `FileField(max_length=None, allow_empty_file=False, use_url=UPLOADED_FILES_USE_URL)`

- `max_length`<br>
  파일 이름의 최대 길이를 지정한다.
- `allow_empty_file`<br>
  빈 파일 허용 여부를 지정한다.
- `use_url`<br>
  `True`로 설정되면 출력 표현에 URL 문자열 값이 사용된다. `False`로 설정되면 출력 표현에 파일 이름 문자열 값이 사용된다. 다르게 설정되지 않았다면 `True`인 `UPLOADED_FILE_USE_URL` 설정 키 값을 기본값으로 가진다.

## ImageField
이미지 표현. 업로드된 파일이 알려진 이미지 포맷에 맞는지 유효성을 검증한다.

`django.forms.fields.ImageField`에 대응된다.

**Signature**: `ImageField(max_length=None, allow_empty_file=False, use_url=UPLOADED_FILES_USE_URL)`

- `max_length`<br>
  파일 이름의 최대 길이를 지정한다.
- `allow_empty_file`<br>
  빈 파일 허용 여부를 지정한다.
- `use_url`<br>
  `True`로 설정되면 출력 표현에 URL 문자열 값이 사용된다. `False`로 설정되면 출력 표현에 파일 이름 문자열 값이 사용된다. 다르게 설정되지 않았다면 `True`인 `UPLOADED_FILE_USE_URL` 설정 키 값을 기본값으로 가진다.

`Pillow` 또는 `PIL` 패키지를 필요로 한다. `PIL`이 오랫동안 관리되지 않았기 때문에 `Pillow` 패키지가 권장된다.

# Composite fields
## ListField
객체 리스트의 유효성을 검사하는 필드 클래스

**Signature**: `ListField(child=<A_FILED_INSTANCE>, allow_empty=True, min_length=None, max_length=None)`

- `child`<br>
  리스트 내부의 객체의 유효성을 검사하기 위해 사용되는 필드 인스턴스. 이 인자가 제공되지 않는다면 리스트 내부의 객체의 유효성이 검사되지 않는다.
- `allow_empty`<br>
  빈 리스트 허용 여부를 지정한다.
- `min_length`<br>
  리스트가 이 숫자보다 적은 개수의 원소를 가지지 않았는지 검증한다.
- `max_length`<br>
  리스트가 이 숫자보다 많은 개수의 원소를 가지지 않았는지 검증한다.

예를 들어, 정수 리스트의 유효성을 검사하려면 다음과 같은 코드를 작성한다.

```python
scores = serializers.ListField(
    child=serializers.IntegerField(min_value=0, max_value=100)
)
```

`ListField` 클래스는 재사용 가능한 리스트 필드 클래스를 작성하도록 허용하는 선언 형식을 지원한다.

```python
class StringListField(serializers.ListField):
    child = serializers.CharField()
```

`child` 인자를 제공할 필요 없이, 애플리케이션에서 사용자 정의 `StringListField` 클래스를 재사용할 수 있게 된다.

## DictField
객체 딕셔너리의 유효성을 검사하는 필드 클래스. `DictField` 내의 키는 언제나 문자열 값으로 간주된다.

**Signature**: `DictField(child=<A_FIELD_INSTANCE>, allow_empty=True)`

- `child`<br>
  딕셔너리 내의 값의 유효성을 검사하기 위해 사용되는 필드 인스턴스. 이 인자가 주어지지 않는다면 매핑된 값의 유효성이 검사되지 않는다.
- `allow_empty`<br>
  빈 딕셔너리 허용 여부를 지정한다.

예를 들어, 문자열에 문자열을 매핑한 것의 유효성을 검사하는 필드를 생성하려면 다음과 같은 코드를 작성한다.

```python
document = DictField(child=CharField())
```

`ListField`에서 그러하듯이 선언 형식을 사용할 수도 있다. 예를 들면:

```python
class DocumentField(DictField):
    child = CharField()
```

## HStoreField
Django의 postgres `HStoreField`와 호환되는 미리 설정된 `DictField`.

**Signature**: `HStoreField(child=<A_FIELD_INSTANCE>, allow_empty=True)`

- `child`<br>
  딕셔너리 내의 값의 유효성을 검사하기 위해 사용되는 필드 인스턴스. 기본 child 필드는 빈 문자열과 null 값을 모두 허용한다.
- `allow_empty`<br>
  빈 딕셔너리 허용 여부를 지정한다.

hstore 확장이 값을 문자열로 저장하기 때문에 child 필드는 **반드시** `CharField`의 인스턴스여야 한다는 점에 주의한다.

## JSONField
들어오는 자료 구조가 유효한 JSON 원시 요소로 구성되어 있는지 검증하는 필드 클래스. 대체 이진 모드에서는 JSON 인코딩 이진 문자열을 표현하고 그 유효성을 검사한다.

**Signature**: `JSONField(binary, encoder)`

- `binary`<br>
  `True`로 설정되어 있다면 필드는 원시적인 자료 구조 대신 JSON 인코딩 문자열을 출력하고 그 유효성을 검사한다. 기본값은 `False`.
- `encoder`<br>
  입력 객체를 serialize하기 위한 JSON 인코더. 기본값은 `None`.

# Miscellaneous fields
## ReadOnlyField
필드의 값을 수정하지 않고 단순히 반환하는 필드 클래스

이 필드는 모델 필드 대신 속성에 관련된 필드 이름을 포함할 때 `ModelSerializer`와 함께 기본값으로 사용된다.

**Signature**: `ReadOnlyField()`

예를 들어 `has_expired`가 `Account` 모델의 속성이었다면, 다음의 시리얼라이저는 이를 `ReadOnlyField`로 자동으로 생성한다.

```python
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'has_expired']
```

## HiddenField
사용자 입력에 기반한 값을 가지지 않고 기본값이나 호출 가능한 것으로부터 값을 가져오는 필드 클래스

**Signature**: `HiddenField()`

예를 들어, 시리얼라이저의 유효한 값의 일부로 언제나 현재 시간을 제공하는 필드를 포함시키려면 다음과 같이 작성한다.

```python
modified = serializers.HiddenField(default=timezone.now)
```

`HiddenField` 클래스는 대개 미리 제공된 필드 값에 기반하여 유효성 검사를 해야하지만 최종 사용자에게 모든 필드를 노출하고 싶지 않을 때에만 필요하다.

`HiddenField`에 관한 더 많은 예시는 [validators](https://www.django-rest-framework.org/api-guide/validators/) 문서에서 확인할 수 있다.

## ModelField
임의의 모델 필드에 묶일 수 있는 제네릭 필드. `ModelField` 클래스는 serialization/deserialzation 작업을 연결된 모델 필드에 위임한다. 이 필드는 새로운 사용자 정의 시리얼라이저 필드를 생성할 필요 없이 사용자 정의 모델 필드를 위해 시리얼라이저 필드를 생성하기 위해 사용될 수 있다.

이 필드는 `ModelSerializer`에 의해 사용자 정의 필드 클래스에 대응하기 위해 사용된다.

**Signature**: `ModelField(model_field=<Django ModelField instance>)`

`ModelField` 클래스는 일반적으로 내부 사용을 목적으로 하지만 필요 시에는 API에 의해 사용될 수 있다. `ModelField`를 적절하게 인스턴스화하기 위해서, 인스턴스화된 모델에 속한 필드를 전달해야 한다. 예를 들면: `ModelField(model_field=MyModel()._meta.get_field('custom_field'))`

## SerializerMethodField
읽기 전용 필드이다. 속해있는 시리얼라이저 클래스에 있는 메서드를 호출해 값을 불러온다. 객체의 serialize된 표현에 아무 종류의 데이터를 추가하기 위해 사용될 수 있다.

**Signature**: `SerializerMethodField(method_name=None)`

- `method_name`: 시리얼라이저에 있는 호출될 메서드의 이름. 주어지지 않는다면 기본값은 `get_<field_name>`로 정해진다.

`method_name` 인자에 의해 참조되는 시리얼라이저 메서드는 serialize되는 객체인 하나의 인자(`self`에 더해)를 수용해야 한다. 객체의 serialize된 표현에 포함되기를 바라는 것이라면 무엇이든 반환해야 한다. 예를 들면:

```python
from django.contrib.auth.models import User
from django.utils.timezone import now
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    days_since_joined = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_days_since_joined(self, obj):
        return (now() - obj.date_joined).days
```