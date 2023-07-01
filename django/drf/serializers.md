# [Serializers](https://www.django-rest-framework.org/api-guide/serializers/)
```
우리는 시리얼라이저의 유용함을 확장하는 것에 관해 다루고자 한다.
하지만 이것은 사소한 문제가 아니며, 심도 있는 디자인 작업을 필요로 한다.
- Russell Keith-Magee, Django users group
```

시리얼라이저는 queryset과 모델 인스턴스와 같은 복잡한 데이터를 `JSON`이나 `XML` 또는 다른 컨텐츠 유형으로 쉽게 렌더링할 수 있는 네이티브 파이썬 자료형으로 변환할 수 있게 한다. 시리얼라이저는 들어오는 데이터가 처음 유효성 검증이 된 후 파싱된 데이터를 다시 복잡한 유형으로 변환하게 해주는 deserialization 또한 제공한다.

REST framework의 시리얼라이저는 Django의 `Form`과 `ModelForm` 클래스와 매우 유사하게 동작한다. 모델 인스턴스와 queryset을 다루는 시리얼라이저를 생성하는 유용한 지름길을 제공하는 `ModelSerializer` 뿐만 아니라 응답 결과를 제어하는 강력하고 generic한 방법을 제공하는 `Serializer` 클래스가 제공된다.

## Declaring Serializers
예시 목적으로 사용할 만한 단순한 객체를 만드는 것부터 시작한다.

```python
from datetime import datetime

class Comment:
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = created of datetime.now()

comment = Comment(email='example@example.com', content='foo bar')
```

`Comment` 객체에 대응하는 데이터를 serialize하고 deserialize 할 때 사용할 수 있는 시리얼라이저를 선언한다.

시리얼라이저 선언은 폼 선언과 매우 유사하다.

```python
from rest_framework import serializers

class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content - serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
```

## Serializing objects
이제 댓글이나 댓글 목록을 serialize하기 위해 `CommentSerializer`를 사용할 수 있다. 다시 언급하지만, `Serializer` 클래스를 사용하는 것은 `Form` 클래스를 사용하는 것과 많이 유사하다.

```python
serializer = CommentSerializer(comment)
serializer.data
# {'email': 'example@example.com', 'content': 'foo bar', 'created': '2023-06-29 20:11:22.458258'}
```

이 지점에서 모델 인스턴스를 파이썬 네이티브 자료형으로 번역했다. Serialization 과정을 마치려면 데이터를 `json`으로 렌더링 해야 한다.

```python
from rest_framework.renderers import JSONRenderer

json = JSONRenderer().render(serializer.data)
json
# b'{"email":"example@example.com", "content":"foo bar", "created":"2023-06-29 20:11:22.458258"}'
```

## Deserializing objects
Deserialization 또한 유사하다. 먼저 스트림을 파이썬 네이티브 자료형으로 파싱한다.

```python
import io
from rest_framework.parsers import JSONParser

stream = io.BytesIO(json)
data = JSONParser().parse(stream)
```

그 다음 네이티브 자료형을 유효성 검사된 데이터의 딕셔너리로 복구한다.

```python
serializer = CommentSerializer(data=data)
serializer.is_valid()
# True
serializer.validated_data
# {'content': 'foo bar', 'email': 'example@example.com'. 'created': datetime.datetime(2023, 6, 29, 20, 11, 22, 458258)}
```

## Saving instances
유효성이 검증된 데이터에 기반한 온전한 객체 인스턴스를 반환하게 하고 싶다면 `.create()`와 `.update()` 메서드 중 하나 이상을 구현해야 한다. 예를 들면:

```python
class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

    def create(self, validated_data):
        return Comment(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        return instance
```

객체 인스턴스가 Django 모델에 대응된다면, 다음의 메서드가 데이터베이스에 객체를 저장하게 할 수 있다. 예를 들어 `Comment`가 Django 모델이라면, 메서드는 아래와 같이 작성될 것이다.

```python
def create(self, validated_data):
    return Comment.objects.create(**validated_data)

def update(self, instance, validated_data):
    instance.email = validated_data.get('email', instance.email)
    instance.content = validated_data.get('content', instance.content)
    instance.created = validated_data.get('created', instance.created)
    return instance
```

이제 데이터를 deserialize할 때 유효성이 검증된 데이터에 기반한 객체 인스턴스를 반환하기 위해 `.save()`를 호출할 수 있다.

```python
comment = serializer.save()
```

`.save()`를 호출하면 시리얼라이저 클래스를 초기화할 때 존재하는 인스턴스를 전달했는지의 여부에 따라 새로운 인스턴스를 생성하거나 이미 존재하는 인스턴스를 갱신한다.

```python
# .save() will create a new instance.
serializer = CommentSerializer(data=data)

# .save() will update the existing `comment` instance.
serializer = CommentSerializer(comment, data=data)
```

`.create()` 와 `.update()`는 모두 선택적인 메서드이다. 시리얼라이저 클래스의 용도에 따라 전부 다, 혹은 하나만 구현하거나 아무것도 구현하지 않을 수 있다.

### Passing additional attributes to `.save()`
인스턴스를 저장하는 시점에 추가 데이터를 삽입할 수 있도록 뷰 코드를 작성할 수 있다. 이 추가 데이터는 현재 사용자, 현재 시각, 또는 요청 데이터에 포함되지 않은 어떤 내용과 같은 정보를 포함할 수 있다.

`.save()`를 호출할 때 추가적인 키워드 인자를 포함하면 그렇게 할 수 있다. 예를 들면:

```python
serializer.save(owner=request.user)`
```

모든 추가적인 키워드 인자는 `.create()` 혹은 `.update()`가 호출되었을 때 `validated_data` 인자에 포함된다.

### Overriding `.save()` directly.
`.create()`와 `.update()`라는 이름이 의미있지 않은 경우가 있다. 예를 들어 연락 폼으로 새 인스턴스를 생성하는 대신 이메일이나 다른 메시지를 송신할 것이다.

이런 경우 좀 더 가독성 있고 의미를 가지도록 `.save()`를 직접 override할 수 있다.

예를 들면:

```python
class ContactForm(serializers.Serializer):
    email = serializers.EmailField()
    message = serializers.CharField()

    def save(self):
        email = self.validated_data['email']
        message = self.validated_data['message']
        send_email(form=email, message=message)
```

위의 경우 시리얼라이저의 `.validated_data` 속성에 직접 접근해야 한다는 점에 유의한다.

## Validation
데이터를 deserialize할 때, 유효성이 검증된 데이터에 접근하려 하거나 객체 인스턴스를 저장하기 전에 꼭 `is_calid()`를 호출해야 한다. 유효성 오류가 발생하면 `.errors` 속성이 에러 메시지를 표현하는 딕셔너리를 포함하게 된다. 예를 들어:

```python
serializer = CommentSerializer(data={'email': 'foobar', 'content': 'baz'})
serializer.is_valid()
# False
serializer.errors
# {'email': ['Enter a valid e-mail address.'], 'created': ['This Field is required.']}
```

딕셔너리 안의 각각의 키는 필드명이 되고, 그 값은 해당하는 필드에 대응하는 에러 메시지 문자열의 리스트가 된다. `non_field_errors` 키 또한 존재할 수 있으며, 일반적인 유효성 오류를 나열할 것이다. REST framework 설정에서 `NON_FIELD_ERRORS_KEY`를 사용해 `non_field_errors` 키의 이름을 변경할 수 있다.

아이템 리스트를 deserialize할 때에는 각각의 deserialize된 아이템을 나타내는 딕셔너리의 리스트로 에러가 반환된다.

### Raising an exception on invalid data
`.is_valid()` 메서드는 유효성 오류가 있을 때 `serializers.ValidationError` 예외를 발생시키기 위한 선택적인 `raise_exception` 플래그를 가진다.

이러한 예외들은 REST framework가 제공하는 기본 예외 핸들러에 의해 자동으로 다루어지며, 기본으로 `HTTP 400 Bad Request` 응답을 반환한다.

```python
# Return a 400 response if the data was invalid.
serializer.is_valid(raise_exception=True)
```

### Field-level validation
`Serializer` 서브클래스에 `.validate_<field_name>` 메서드를 추가해 사용자 정의 필드 수준 유효성 검사를 명시할 수 있다. 이는 Django 폼의 `.clean_<field_name>` 메서드와 유사하다.

이러한 메서드들은 유효성 검사를 필요로 하는 필드 값인 하나의 인자를 가진다.

`validate_<field_name>` 메서드는 유효성이 검증된 값을 반환하거나 `serializers.ValidationError`를 발생시켜야 한다. 예를 들면:

```python
from rest_framework import serializers

class BlogPostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField()

    def validate_title(self, value):
        """
        Check that the blog post is about Django.
        """
        if 'django' not in value.lower():
            raise serializers.ValidationError("Blog post is not about Django")
        return value
```

- **Note**<br>
  만약 `<field_name>`이 `required=False` 인자와 함께 시리얼라이저에서 선언되었다면 해당 필드가 포함되지 않았을 때 이 유효성 검증 단계는 생략될 것이다.

### Object-level validation
유효성 검사가 복수의 필드에 접근하는 것을 요구한다면, `Serializer` 서브클래스에 `.validate()` 메서드를 추가한다. 이 메서드는 필드 값의 딕셔너리인 하나의 인자를 가진다. 필요하다면 `serializers.ValidationError`를 발생시키거나 유효성이 검증된 값을 반환한다. 예를 들면:

```python
from rest_framework import serializers

class EventSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=100)
    start = serializers.DateTimeField()
    finish = serializers.DateTimeField()

    def validate(self, data):
        """
        Check that start is before finish.
        """
        if data['start'] > data['finish']:
            raise serializers.ValidationError("finish must occur after start")
        return data
```

### Validators
시리얼라이저에 있는 각각의 필드는 다음과 같이 필드 인스턴스에서 validator를 선언해 포함할 수 있다.

```python
def multiple_of_ten(value):
    if value % 10 != 0:
        raise serializers.ValidationError('Not a multiple of ten')

class GameRecord(serializers.Serializer):
    score = IntegerField(validators=[multiple_of_ten])
    ...
```

시리얼라이저 클래스는 필드 테이터의 온전한 세트에 적용되는 재사용 가능한 validator를 포함할 수 있다. 이러한 validator는 다음과 같이 내부의 `Meta` 클래스에서 선언하여 포함될 수 있다.

```python
class EventSerializer(serializers.Serializer):
    name = serializers.CharField()
    room_number = serializers.IntegerField(choices=[101, 102, 103, 201])
    date = serializers.DateField()

    class Meta:
        # Each room only has one event per day.
        validators = [
            UniqueTogetherValidator(
                queryset=Event.objects.all(),
                fields=['room_number', 'date']
            )
        ]
```

더 많은 정보는 [validators 문서](https://www.django-rest-framework.org/api-guide/validators/)에서 확인할 수 있다.