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

## Accessing the initial data and instance
초기 객체나 queryset을 시리얼라이저 인스턴스로 전달할 때 객체는 `.instance`로 사용 가능하게 된다. 초기 객체가 전달되지 않았다면 `.instance` 속성은 `None`이 된다.

시리얼라이저 인스턴스로 데이터를 전달할 때, 수정되지 않은 데이터는 `.initial_data`로 사용 가능하게 된다. `data` 키워드 인자가 전달되지 않았다면 `initial_data` 속성이 존재하지 않게 된다.


## Partial updates
기본적으로 시리얼라이저에는 모든 필수 필드를 위한 값이 전달되어야 하며, 그렇지 않을 경우 유효성 검사 오류가 발생한다. 부분 갱신을 하려면 `partial` 인자를 사용하면 된다.

```python
# Update `comment` with partial data
serializer = CommentSerializer(comment, data={'content': 'foo bar'}, partial=True)
```

## Dealing with nested objects
이전 예시는 단순한 데이터 타입만을 가지는 객체를 다루는 데에는 괜찮았지만 때로 객체의 속성이 문자열, 날짜 또는 정수와 같은 단순한 데이터 타입이 아닌 좀 더 복잡한 객체를 나타낼 수 있어야 한다.

`Serializer` 클래스는 그 스스로 `Field`의 유형이며, 하나의 객체 유형이 다른 객체 안에 중첩된 관계를 나타내는데 사용될 수 있다.

```python
class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)

class CommentSerializer(serializers.Serializer):
    user = UserSerializer()
    conent = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
```

중첩된 표현이 부분적으로 `None` 값을 수용한다면, 중첩된 시리얼라이저에 `required=False` 플래그를 전달해야 한다.

```python
class CommentSerializer(serializers.Serializer):
    user = UserSerializer(required=False) # May be an anonymous user.
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
```

유사하게, 중첩된 표현이 아이템의 리스트가 되어야 한다면 중첩된 시리얼라이저에 `many=True` 플래그를 전달해야 한다.

```python
class CommentSerializer(serializers.Serializer):
    user = UserSerializer(required=False)
    edits = EditItemSerializer(many=True) # A nested list of 'edit' items.
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
```

## Writable nested representations
데이터 deserialize를 지원하는 중첩된 표현을 다룰 때, 중첩된 객체에 관한 어느 오류라도 중첩된 객체의 필드명 아래 중첩될 것이다.

```python
serializer = CommentSerializer(data={'user': {'email': 'foobar', 'username': 'doe'}, 'content': 'baz'})
serializer.is_valid()
# False
serializer.errors
# {'user': {'email': ['Enter a valid e-mail address']}, 'created': ['This field is required.']}
```

이와 유사하게, `.validated_data`속성이 중첩된 자료 구조에 포함될 것이다.

### Writing `.create()` methods for nested representations
작성 가능한 중첩된 표현을 지원해야 한다면, 복수 객체 저장을 다루는 `.create()` 혹은 `.update()` 메서드를 작성해야 한다.

다음 예시는 중첩된 프로필 객체를 동반한 사용자 생성을 다루는 방법을 보여준다.

```python

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user
```

### Writing `.update()` methods for nested representations
관계 갱신을 어떻게 다루어야 할지에 관해 고려해보자. 예를 들어 관계의 데이터가 `None`이거나 제공되지 않았다면 다음 중 어느 것이 일어나야 할까?

- 데이터베이스에서 관계를 `NULL`로 설정하기
- 연관된 인스턴스 삭제하기
- 데이터를 무시하고 인스턴스를 그대로 두기
- 유효성 검증 오류를 발생시키기

다음은 이전의 `UserSerializer` 클래스의 `.update()` 메서드 예시이다.

```python
def update(self, instance, validated_data):
    profile_data = validated_data.pop('profile')
    # Unless the application properly enforces that this field is
    # always set, the following could raise a `DoesNotExist`, which would need to be handled.
    profile = instance.profile

    instance.username = validated_data.get('username', instance.username)
    instance.email = validated_data.get('email', instance.email)
    instance.save()

    profile.is_premium_member = profile_data.get(
        'is_premium_member',
        profile.is_premium_member
    )
    profile.has_support_contract = profile_data.get(
        'has_support_contract',
        profile.has_support_contract
    )
    profile.save()

    return instance
```

중첩된 생성과 갱신의 동작이 모호할 수 있고, 연관된 모델 사이에 복잡한 의존성이 요구될 수 있으므로 REST framework 3은 이러한 메서드를 명시적으로 작성할 것을 요구한다. 기본 `ModelSerializer`의 `.create()`와 `.update()` 메서드는 작성 가능한 중첩된 표현에 관한 지원을 포함하지 않는다.

그러나 자동으로 작성 가능한 중첩된 표현을 지원하는 [DRF Writable Nested](https://www.django-rest-framework.org/api-guide/serializers/#drf-writable-nested)와 같은 서드파티 패키지를 사용할 수 있다.

### Handling saving related instances in model manager classes
시리얼라이저에서 복수의 연관된 인스턴스를 저장하는 다른 방법은 정확한 인스턴스 생성을 다루는 사용자 정의 모델 매니저 클래스를 작성하는 것이다.

예를 들어 `User` 인스턴스와 `Profile` 인스턴스가 언제나 한 쌍으로 같이 생성되게 해야 한다고 해보자. 다음과 같은 사용자 정의 클래스를 작성할 수 있다.

```python
class UserManager(models.Manager):
    ...

    def create(self, username, email, is_premium_member=False, has_support_contract=False):
        user = User(username=username, email=email)
        user.save()
        profile = Profile(
            user=user,
            is_premium_member=is_premium_member,
            has_support_contract=has_support_contract
        )
        profile.save()
        return user
```

이제 매니저 클래스는 사용자 인스턴스와 프로필 인스턴스가 언제나 같은 시간에 생성하는 것을 더 멋지게 캡슐화한다. 이제 새 매니저 메서드를 사용하기 위해 시리얼라이저의 `.create()` 메서드를 재작성한다.

```python
def create(self, validated_data):
    return User.objects.create(
        username=validated_data['username'],
        email=validated_data['email'],
        is_premium_member=validated_data['profile']['is_premium_member'],
        has_support_contract=validated_data['profile']['has_support_contract']
    )
```

이 접근에 관한 자세한 사항은 [모델 매니저에 관한 Django 문서](https://docs.djangoproject.com/en/stable/topics/db/managers/)와 [모델과 매니저 클래스를 사용하는 법에 관한 블로그](https://www.dabapps.com/blog/django-models-and-encapsulation/)에서 확인할 수 있다.

## Dealing with multiple objects
`Serializer` 클래스는 객체 리스트의 serialization이나 deserialization 또한 다룰 수 있다.

### Serializing multiple objects
하나의 객체 인스턴스 대신 queryset이나 객체 리스트를 serialize하려면 시리얼라이저를 초기화할 때 `many=True` 플래그를 전달해야 한다. 그 다음 serialize 되어야 할 queryset이나 객체 리스트를 전달할 수 있다.

```python
queryset = Book.objects.all()
serializer = BookSerializer(queryset, many=True)
serializer.data
# [
#    {'id': 0, 'title': 'Children of the Rune: Blooded 5', 'author': 'Jeon Min-Hee'},
#    {'id': 1, 'title': 'The Handmaid's Tale', 'author': 'Margaret Atwood'},
#    {'id': 2, 'title': 'Harry Potter and the Deathly Hallows', 'author': 'J. K. Rowling'}
# ]
```

### Deseiralizing multiple objects
복수의 개체를 deserialize하는 기본 동작은 복수의 개체 생성을 지원하지만 복수의 개체 갱신은 지원하지 않는 것이다. 이런 경우를 어떻게 지원할지, 혹은 어떻게 커스터마이즈를 할지에 관한 정보는 아래의 [ListSerializer](https://www.django-rest-framework.org/api-guide/serializers/#listserializer) 문서에서 확인할 수 있다.

## Including extra context
Serialize 되는 객체에 더해 추가적인 컨텍스트를 시리얼라이저에 제공해야 하는 경우가 있다. 흔한 경우 중 하나는 적절하게 온전히 작동하는 URL을 생성할 수 있도록 시리얼라이저가 현재 요청에 접근하게 하는 것을 필요로 하는 하이퍼링크된 관계를 포함하는 시리얼라이저를 사용할 때이다.

시리얼라이저를 초기화할 때 `context` 인자를 전달해 임의의 추가적인 컨텍스트를 제공할 수 있다. 예를 들면:

```python
serializer = AccountSerializer(account, context={'request': request})
serializer.data
# {'id': 6, 'owner': 'lemon-lime-honey', 'created': datetime.datetime(2023, 7, 3, 21, 35, 47, 413287), 'details': 'https://github.com/lemon-lime-honey'}
```

컨텍스트 딕셔너리는 `self.context` 속성에 접근해 사용자 정의 `.to_representation()` 메서드와 같은 어느 시리얼라이저 필드 로직에서도 사용될 수 있다.

# ModelSerializer
Django 모델 정의와 유사한 시리얼라이저 클래스를 작성할 수도 있다.

`ModelSerializer` 클래스는 모델 필드에 대응되는 필드를 동반하는 `Serializer` 클래스를 자동으로 생성할 수 있게 한다.

**`ModelSerializer` 클래스는 다음 특징을 제외하면 일반적인 `Serializer` 클래스와 같다.**

- 모델에 기반해 자동으로 필드 세트를 생성한다.
- unique_together 유효성 검사기와 같은 시리얼라이저를 위한 유효성 검사기를 자동으로 생성한다.
- 기본으로 `.create()`와 `.update()`의 단순한 구현을 포함한다.

`ModelSerializer`를 선언하는 것은 이렇다.

```python
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'users', 'created']
```

기본적으로 클래스 안의 모든 모델 필드는 대응되는 시리얼라이저 필드에 매핑될 것이다.

외래키와 같은 모델의 관계는 `PrimaryKeyRelatedField`에 매핑될 것이다. 역관계는 [시리얼라이저 관계](https://www.django-rest-framework.org/api-guide/relations/) 문서에서 기술된 것처럼 명시적으로 포함된 것이 아니라면 기본으로 포함되지는 않는다.

### Inspecting a `ModelSerializer`
시리얼라이저 클래스는 필드 상태를 온전히 점검할 수 있게 해주는 도움말 문자열을 생성한다. 이는 어떤 필드와 유효성 검사기 세트가 자동으로 생성되는지 결정하기 위해 `ModelSerializers`를 다룰 때 특히 유용하다.

그렇게 하려면 `python manage.py shell`을 사용해 Django 셸을 열고 시리얼라이저 클래스를 불러온 다음 초기화를 시킨 후 객체 표현을 출력한다.

```python
>>> from myapp.serializers import AccountSerializer
>>> serializer = AccountSerializer()
>>> print(repr(serializer))
AccountSerializer():
    id = IntegerField(label='ID', read_only=True)
    name = CharField(allow_blank=True, max_length=100, required=False)
    owner = PrimaryKeyRelatedField(queryset=User.objects.all())
```

## Specifying which fields to include
모델 시리얼라이저에 사용될 기본 필드의 일부 만을 사용하고 싶다면, `ModelForm`에서 했던 것처럼 `fields`나 `exclude` 옵션을 사용하면 된다. `fields` 속성을 사용해 serialize되어야 할 모든 필드를 명시적으로 설정하는 것을 강력히 권고한다. 이는 모델이 변경되었을 때 의도치 않게 데이터가 노출될 확률을 줄일 수 있다.

예를 들면:

```python
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'users', 'created']
```

`fields` 속성에 모델의 모든 필드가 사용되어야 한다는 것을 표시하기 위한 특별 값 `'__all__'`을 설정해도 된다.

예를 들면:

```python
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
```

`exclude` 속성에 시리얼라이저에서 제외되어야 할 필드의 리스트를 설정할 수도 있다.

예를 들면:

```python
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ['users']
```

위의 예시에서 `Account` 모델이 `account_name`, `users`, `created`라는 세 개의 필드를 가진다면 필드 `account_name`과 `created`가 serialize되는 결과가 나올 것이다.

`fields`와 `excludes` 속성 안의 이름은 보통 모델 클래스의 모델 필드에 매핑된다.

그 대신에 `fields` 옵션 안의 이름은 모델 클래스에 존재하는 인자를 가지지 않는 속성이나 메서드에 매핑될 수도 있다.

버전 3.0.0부터 `fields` 혹은 `exclude` 중 하나를 제공하는 것이 **강제**된다.

## Specifying nested serialization
기본 `ModelSerializer`는 관계를 위해 기본키를 사용하지만, `depth` 옵션을 사용한 중첩 표현을 쉽게 생성할 수 있다.

```python
class AccountSerializer(serializers.ModelSerialzer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'users', 'created']
        depth = 1
```

`depth` 옵션은 납작한 표현으로 되돌아 가기 전에 지나야 할 관계의 깊이를 나타내는 정수 값으로 설정되어야 한다.

Serialization이 되는 방식을 커스터마이즈하고 싶다 해도 필드를 직접 정의할 필요는 없다.

## Specifying fields explicitly
`ModelSerializer`에 추가 필드를 더하거나, `Serializer` 클래스에서처럼 클래스 내의 필드를 선언해 기본 필드를 override할 수 있다.

```python
class AccountSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    groups = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = Account
        fields = ['url', 'groups']
```

추가 필드는 모델에 있는 속성이나 호출 가능한 것에 대응될 수 있다.

## Specifying read only fields
복수의 필드를 읽기전용으로 명시할 수 있다. 각 필드에 `read_only=True` 속성을 명시하는 대신 Meta 옵션인 `read_only_fields`를 사용하면 된다.

이 옵션은 필드 이름의 리스트 혹은 튜플이어야 하며, 다음과 같이 선언되어야 한다.

```python
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'users', 'created']
        read_only_fields = ['account_name']
```

`editable=False` 설정을 가진 모델 필드나 `AutoField` 필드는 기본적으로 읽기 전용으로 설정될 것이며, `read_only_fields` 옵션에 추가될 필요가 없다.

- **Note**: <br>
  읽기 전용 필드가 모델 수준에서 `unique_together` 제한의 일부인 특수한 경우가 있다. 이 경우, 제한 조건을 충족시키기 위해 해당 필드가 시리얼라이저 클래스에서 요구되지만, 동시에 사용자에 의해 수정되어서는 안 된다.

  이를 다루는 방법은 시리얼라이저에서 `read_only=True`와 `default=...` 키워드 인자를 제공하며 필드를 명시하는 것이다.

  한 가지 예시는 다른 식별자와 `unique_together`인 현재 인증된 `User`의 읽기 전용 관계이다. 이 경우 사용자 필드를 다음과 같이 선언한다.

  ```python
  user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
  ```

  [UniqueTogetherValidator](https://www.django-rest-framework.org/api-guide/validators/#uniquetogethervalidator)와 [CurrentUserDefault](https://www.django-rest-framework.org/api-guide/validators/#currentuserdefault) 클래스에 관한 자세한 내용은 [Validators 문서](https://www.django-rest-framework.org/api-guide/validators/)에서 확인할 수 있다.

## Additional keyword arguments
`extra_kwargs` 옵션을 사용해 필드의 임의의 키워드 인자를 명시할 수 있는 방법이 있다. `read_only_fields`의 경우처럼 이는 시리얼라이저에 필드를 명시적으로 선언하지 않아도 된다는 것을 의미한다.

이 옵션은 필드 이름을 키워드 인자의 딕셔너리로 매핑하는 딕셔너리이다. 예를 들면:

```python
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
```

필드가 이미 시리얼라이저 클래스에서 명시적으로 선언되었다면 `extra_kwargs` 옵션이 무시된다는 점을 유의한다.