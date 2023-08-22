# [Validators](https://www.django-rest-framework.org/api-guide/validators/)
```
유효성 검사기는 서로 다른 타입의 필드 사이에서 유효성 검사 로직을 재사용하는데 유용할 수 있다.
- Django 공식문서
```

REST framework에서 유효성 검사를 다루는 대부분의 시간동안 단순히 기본 필드 유효성 검사에 의존하거나 혹은 시리얼라이저나 필드 클래스의 명시적인 유효성 검사 메서드를 작성할 것이다.

그러나 가끔 유효성 검사 로직을 재사용 가능한 요소에 배치해 코드베이스를 통틀어 쉽게 재사용될 수 있게 하고 싶을 수 있다. 이는 유효성 검사 함수와 유효성 검사기 클래스를 사용해 달성할 수 있다.

## Validation in REST framework
Django REST framework 시리얼라이저에서의 유효성 검사는 Django의 `ModelForm` 클래스에서 유효성 검사가 동작하는 것과 조금 다르게 다루어진다.

`ModelForm`에서는 유효성 검사가 폼에서 부분적으로, 모델 인스턴스에서 부분적으로 실행된다. REST framework의 유효성 검사는 완전히 시리얼라이저 클래스에서만 실행된다. 이는 다음의 이유에서 유리하다.

- 문제를 적절히 분리해 코드 동작을 더 명확하게 한다.
- 지름길 `ModelSerializer` 클래스를 사용하는 것과 명시된 `Serializer` 클래스를 사용하는 것을 전환하기 쉽다. `ModelSerializer`에 사용되는 유효성 검사 동작은 복제하기 단순하다.
- 시리얼라이저 인스턴스의 `repr`를 출력하는 것은 그것이 어떤 유효성 검사 규칙을 적용하는지 보여주게 된다. 모델 인스턴스에 의해 호출되는 추가적인 숨겨진 유효성 검사 동작이 없다.

`ModelSerializer`를 사용할 때 이 모든 것은 자동으로 다루어진다. 대신 `Serializer` 클래스를 사용하고 싶다면 유효성 검사 규칙을 명시적으로 정의해야 한다.

### Example
REST framework가 어떻게 명시적 유효성 검사를 사용하는지의 예시로 유일성 제한이 있는 필드를 가지는 단순한 모델 클래스를 사용한다.

```python
class CustomerReportRecord(models.Model):
    time_raised = models.DateTimeField(default=timezone.now, editable=False)
    reference = models.CharField(unique=True, max_length=20)
    description = models.TextField()
```

다음은 `CustomerReportRecord`의 인스턴스를 생성하거나 갱신하기 위해 사용할 수 있는 기본 `ModelSerializer`이다.

```python
class CustomerReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerReportRecord
```

`manage.py shell`을 사용해 Django 셸을 연다.

```python
>>> from project.example.serializers import CustomerReportSerializer
>>> serializer = CustomerReportSerializer()
>>> print(repr(serializer))
CustomerReportSerializer():
    id = IntegerField(label='ID', read_only=True)
    time_raised = DateTimeField(read_only=True)
    reference = CharField(max_length=20, validators=[<UniqueValidator(queryset=CustomerReportRecord.objects.all())>])
    description = CharField(style={'type': 'textarea'})
```
여기서 눈 여겨볼 만한 것은 `reference` 필드이다. 시리얼라이저 필드의 유효성 검사기에 의해 유일성 제한이 명시적으로 강제되는 것을 확인할 수 있다.

이러한 더 명시적인 형식 때문에 REST framework는 core Django에서는 사용할 수 없는 몇 개의 유효성 검사기 클래스를 가진다. 아래에서 기술한다.

## UniqueValidator
이 유효성 검사기는 모델 필드에 `unique=True` 제한을 강제하는데 사용할 수 있다. 하나의 필수 인자와 선택 인자 `messages`를 가진다.

- `queryset` *필수*<br>
  유일성이 강제되어야 하는 queryset이다.
- `message`<br>
  유효성 검사에 실패했을 때 사용되는 오류 메시지이다.
- `lookup`<br>
  값의 유효성이 검사될 때 존재하는 인스턴스를 찾기 위해 사용되는 lookup이다. 기본값은 `exact`.

이 유효성 검사지는 다음과 같이 *시리얼라이저 필드*에 적용되어야 한다.

```python
from rest_framework.validators import UniqueValidator

slug = SlugField(
    max_field=100,
    validators=[UniqueValidator(queryset=BlogPost.objects.all())]
)
```

## UniqueTogetherValidator
이 유효성 검사기는 모델 인스턴스에 `unique_together` 제한을 강제하는데 사용할 수 있다. 두 개의 필수 인자와 하나의 선택인자 `messages`를 가진다.

- `queryset` *필수*<br>
  유일성이 강제되어야 하는 queryset이다.
- `fields` *필수*<br>
  유일한 세트가 되어야 하는 필드 이름의 리스트 또는 튜플. 시리얼라이저 클래스에 필드로 존재해야 한다.
- `message`<br>
  유효성 검사에 실패했을 때 사용되는 오류 메시지이다.

이 유효성 검사기는 다음과 같이 *시리얼라이저 클래스*에 적용되어야 한다.

```python
from rest_framework.validators import UniqueTogetherValidator

class ExampleSerializer(serializers.Serializer):
    # ...
    class Meta:
        # ToDo items belong to a parent list, and have an ordering defined
        # by the 'position' field. No two items in a given list may share
        # the same position.
        validators = [
            UniqueTogetherValidator(
                queryset=ToDoItem.objects.all(),
                fields=['list', 'position']
            )
        ]
```

- **Note**:<br>
  `UniqueTogetherValidator` 클래스는 항상 적용되는 필드가 언제나 필수로 다루어지게 하는 암묵적인 제한을 둔다. `default` 값을 가지는 필드는 사용자 입력에서 생략되어도 언제나 값을 제공하기 때문에 예외이다.

## UniqueForDateValidator
## UniqueForMonthValidator
## UniqueForYearValidator
이 유효성 검사기들은 모델 인스턴스에 `unique_for_date`, `unique_for_month`, `unique_for_year` 제한을 강제하기 위해 사용한다. 다음의 인자를 가진다.

- `queryset` *필수*<br>
  유일성이 강제되어야 하는 queryset이다.
- `field` *필수*<br>
  주어진 날짜 범위에서 유일성에 관한 유효성이 검증될 필드 이름이다. 시리얼라이저 클래스에 필드로 존재해야 한다.
- `date_field` *필수*<br>
  유일성 제한을 위한 날짜 범위를 결정하는데 사용되는 필드 이름이다. 시리얼라이저 클래스에 필드로 존재해야 한다.
- `message`<br>
  유효성 검사에 실패했을 때 사용되는 오류 메시지이다.

이 유효성 검사기는 다음과 같이 *시리얼라이저 클래스*에 적용되어야 한다.

```python
from rest_framework.validators import UniqueForYearValidator

class ExampleSerializer(serializers.Serializer):
    # ...
    class Meta:
        # Blog posts should have a slug that is unique for the current year.
        validators = [
            UniqueForYearValidator(
                queryset=BlogPostItem.objects.all(),
                field='slug',
                date_field='published'
            )
        ]
```

유효성 검사에 사용되는 날짜 필드는 언제나 시리얼라이저 클래스에 존재해야 한다. 단순히 모델 클래스의 `default=...`에 의존할 수는 없는데, 왜냐하면 기본값에 사용되는 값이 유요성 검사를 실행하기 전까지는 생성되지 않기 때문이다.

API 동작에 따라 이것을 사용할 수 있는 스타일이 여러 가지 있다. `ModelSerializer`를 사용한다면 단순히 REST framework가 생성하는 기본 검사기에 의존할 수 있지만 `Serializer`를 사용하거나 그저 더 명시적인 제어를 원한다면 아래의 스타일을 사용한다.

### Using with a writable date field.
날짜 필드가 쓰기 가능이라면 `default` 인자 설정에 의해, 혹은 `required=True` 설정에 의해 입력 데이터에서 언제나 사용 가능하다는 것을 보장해야 한다.

```
published = serializers.DateTimeField(required=True)
```

### Using with a read-only date field.
날짜 필드가 보이지만 사용자에 의해 수정될 수 없는 것을 원한다면 `read_only=True`를 설정하고 추가적으로 `default=...` 인자를 설정한다.

```python
published = serializers.DateTimeField(read_only=True, default=timezone.now)
```

### Using with a hidden date field.
날짜 필드를 사용자가 볼 수 없게 하고 싶다면 `HiddenField`를 사용한다. 이 필드 타입은 사용자 입력을 허용하지 않지만 언제나 시리얼라이저의 `validated_data`에 기본값을 반환한다.

```python
published = serializers.HiddenField(default=timezone.now)
```

- **Note**:<br>
  `UniqueFor<Range>Validator` 클래스는 항상 적용되는 필드가 언제나 필수로 다루어지게 하는 암묵적인 제한을 둔다. `default` 값을 가지는 필드는 사용자 입력에서 생략되어도 언제나 값을 제공하기 때문에 예외이다.

# Advanced field defaults
시리얼라이저에서 복수의 필드에 적용되는 유효성 검사기는 때로 API 클라이언트에 의해 제공되지 않아야 하지만 유효성 검사기의 입력으로는 사용 가능한 필드 입력을 필요로 한다.

이러한 종류의 유효성 검사를 위해 사용할 수 있는 두 가지 패턴은 다음과 같다.

- `HiddenField` 사용. 이 필드는 `validated_data`에는 존재하지만 시리얼라이저 출력 표현에는 사용되지 *않을* 것이다.
- `read_only=True` 뿐만 아니라 `default=...` 인자 또한 가진 표준 필드 사용. 이 필드는 시리얼라이저 출력 표현에 사용 *될* 것이지만, 사용자가 직접 설정할 수는 없다.

REST framework는 이 맥락에서 유용할 두 개의 기본값을 가진다.

### CurrentUserDefault
현재 사용자를 나타내기 위해 사용할 수 있는 기본값 클래스. 이것을 사용하려면 시리얼라이저를 인스턴스화할 때 컨텍스트 딕셔너리에 'request'가 반드시 들어가야 한다.

```python
owner = serializers.HiddenField(
    default=serializers.CurrentUserDefault()
)
```

### CreateOnlyDefault
*생성 작업 중에만 설정할 수 있는 기본값 인자*에 사용할 수 있는 기본값 클래스. 이 필드는 갱신 중에는 생략된다.

기본값 또는 생성 작업 중에 사용되어야 할 호출 가능한 것인 하나의 인자를 가진다.

```python
created_at = serializers.DateTimeField(
    default=serializers.CreateOnlyDefault(timezone.now)
)
```

# Limitations of validators
`ModelSerializer`가 생성하는 기본 시리얼라이저 클래스에 의존하기보다 명시적으로 유효성 검사를 다루어야 하는 모호한 경우가 있다.

이러한 경우 시리얼라이저의 `Meta.validators` 속성에 빈 리스트를 명시해 자동으로 생성된 유효성 검사기를 비활성화 할 수 있다.

## Optional fields
기본적으로 "unique together" 유효성 검사는 모든 필드가 `required=True`가 되도록 강제한다. 몇 가지 경우, 요구되는 유효성 검사의 동작이 모호한 필드에 명시적으로 `required=False`를 적용하기를 원할 수 있다.

이러한 경우 보통 시리얼라이저에서 유효성 검사기를 제외하고 `.validate()` 메서드나 뷰에서 유효성 검사 로직을 명시적으로 작성할 필요가 있다.

예를 들면:

```python
class BillingRecordSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        # Apply custom validation either here, or in the view.

        class Meta:
            fields = ['client', 'date', 'amount']
            extra_kwargs = {'client': {'required': False}}
            validators = [] # Remove a default "unique together" constraint.
```

## Updating nested serializers
이미 존재하는 인스턴스를 갱신할 때, 유일성 유효성 검사기는 유일성 검사에서 현재 인스턴스를 제외한다. 현재 인스턴스는 유일성 검사 컨텍스트에서 사용할 수 있는데, 왜냐하면 시리얼라이저를 초기화할 때 `instance=...`를 통해 초기에 전달되기 때문에 시리얼라이저의 속성으로 존재하기 때문이다.

*중첩된* 시리얼라이저에서의 갱신 동작의 경우 인스턴스를 사용할 수 없기 때문에 이러한 예외를 적용할 방법이 없다.

다시 말하자면, 시리얼라이저에서 유효성 검사기를 명시적으로 제외하고 `.validate()` 메서드나 뷰에서 유효성 검사 로직을 명시적으로 작성할 수 있다.

## Debugging complex cases
`ModelSerializer` 클래스가 생성하는 동작이 정확히 어떤 것인지 확실하지 않다면 `manage.py shell`을 실행한 후 시리얼라이저의 인스턴스를 출력해 자동으로 생성되는 필드와 유효성 검사기를 확인하는 것이 좋다.

```python
>>> serializer = MyComplexModelSerializer()
>>> print(serializer)
class MyComplexModelSerializer:
    my_fields = ...
```

복잡한 경우 기본 `ModelSerializer` 동작에 의존하기 보다는 명시적으로 시리얼라이저 클래스를 정의하는 것이 낫다는 점에 유의한다. 좀 더 많은 코드를 필요로 하지만 결과 동작이 좀 더 투명하게 된다.

# Writing custom validators
이미 존재하는 Django의 유효성 검사기를 사용하거나 사용자 정의 유효성 검사기를 작성할 수 있다.

## Function based
유효성 검사기는 실패시 `serializers.ValidationError`를 발생시키는 호출 가능한 것이다.

```python
def even_number(value):
    if value % 2 != 0:
        raise serializers.ValidationError('This field must be an even number.')
```

### Field-level validation
`Serializer` 서브클래스에 `.validate_<field_name>`  메서드를 추가해 사용자 정의 필드 수준 유효성 검사를 명시할 수 있다. [시리얼라이저 문서](serializers.md/#field-level-validation)에 기술되어 있다.

## Class-based
클래스 기반 유효성 검사기를 작성하려면 `__call__` 메서드를 사용한다. 클래스 기반 유효성 검사기는 매개변수화와 재사용 동작을 허용하기 때문에 유용하다.

```python
class MultipleOf:
    def __init__(self, base):
        self.base = base

    def __call__(self, value):
        if value % self.base != 0:
            message = 'This field must be a multiple of %d.' % self.base
            raise serializers.ValidationError(message)
```

### Accessing the context
좀 더 발전한 경우 추가 컨텍스트로 사용되는 시리얼라이저 필드로 전달되는 유효성 검사기를 원할 수 있다. 유효성 검사기에 `required_context = True` 속성을 설정하면 된다. `__call__` 메서드는 추가 인자로 `serializer_field` 또는 `serializer`와 함께 호출될 것이다.

```python
requires_context = True

def __call__(self, value, serializer_field):
    ...
```