# [Serializers](https://www.django-rest-framework.org/api-guide/serializers/)
```
시리얼라이저의 유용함을 확장하는 것에 관해 다루고자 한다.
그런데 이것은 쉬운 문제가 아니며, 심도 깊은 설계 작업을 요구한다.

- Russell Keith-Magee, Django users group
```

시리얼라이저는 queryset과 모델 인스턴스와 같은 복잡한 데이터를 `JSON`이나 `XML` 또는 다른 컨텐츠 타입으로 쉽게 렌더링할 수 있는 파이썬 네이티브 자료형으로 변환할 수 있게 한다. 시리얼라이저는 들어오는 데이터가 처음으로 유효성 검증이 된 후 파싱된 데이터를 다시 복잡한 유형으로 변환하게 해주는 역직렬화 또한 제공한다.

REST framework의 시리얼라이저는 Django의 `Form`과 `ModelForm` 클래스와 매우 유사하게 동작한다. 모델 인스턴스와 queryset을 다루는 시리얼라이저를 생성하는 유용하지만 쉽고 빠른 방법을 제공하는 `ModelSerializer` 뿐만 아니라 응답 결과물을 제어하는 강력하고 제네릭한 방법을 제공하는 `Serializer` 클래스가 제공된다.

## Declaring Serializers
예시 목적으로 사용할 만한 단순한 객체를 만드는 것부터 시작한다:

```python
from datetime import datetime

class Comment:
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()

comment = Comment(email='example@example.com', content='foo bar')
```

`Comment` 객체에 대응하는 데이터를 직렬화, 역직렬화 할 때 사용할 수 있는 시리얼라이저를 선언한다.

시리얼라이저 선언은 폼 선언과 매우 유사하다:

```python
from rest_framework import serializers

class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content - serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
```

## Serializing objects
이제 댓글이나 댓글 목록을 직렬화하기 위해 `CommentSerializer`를 사용할 수 있다. 다시 언급하지만, `Serializer` 클래스를 사용하는 것은 `Form` 클래스를 사용하는 것과 많이 유사하다.

```python
serializer = CommentSerializer(comment)
serializer.data
# {'email': 'example@example.com', 'content': 'foo bar', 'created': '2023-06-29 20:11:22.458258'}
```

이 지점에서 모델 인스턴스를 파이썬 네이티브 자료형으로 변환했다. 직렬화 과정을 마치려면 데이터를 `json`으로 렌더링 해야 한다.

```python
from rest_framework.renderers import JSONRenderer

json = JSONRenderer().render(serializer.data)
json
# b'{"email":"example@example.com", "content":"foo bar", "created":"2023-06-29 20:11:22.458258"}'
```

## Deserializing objects
역직렬화 또한 유사하다. 먼저 스트림을 파이썬 네이티브 자료형으로 파싱한다.

```python
import io
from rest_framework.parsers import JSONParser

stream = io.BytesIO(json)
data = JSONParser().parse(stream)
```

그 다음 네이티브 자료형을 유효성을 검증한 데이터의 딕셔너리로 복구한다.

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

이제 데이터를 역직렬화할 때 유효성을 검증한 데이터에 기반한 객체 인스턴스를 반환하기 위해 `.save()`를 호출할 수 있다.

```python
comment = serializer.save()
```

`.save()`를 호출하면 시리얼라이저 클래스를 초기화할 때 존재하는 인스턴스를 전달했는지 여부에 따라 새로운 인스턴스를 생성하거나 이미 존재하는 인스턴스를 갱신한다.

```python
# .save()가 새 인스턴스를 생성한다.
serializer = CommentSerializer(data=data)

# .save()가 존재하는 `comment` 인스턴스를 생신한다.
serializer = CommentSerializer(comment, data=data)
```

`.create()` 와 `.update()`는 모두 선택 메서드이다. 시리얼라이저 클래스의 용도에 따라 전부 다, 혹은 하나만 구현하거나 아무것도 구현하지 않을 수 있다.

### Passing additional attributes to `.save()`
인스턴스를 저장하는 시점에 추가 데이터를 삽입할 수 있도록 뷰 코드를 작성할 수 있다. 이 추가 데이터는 현재 사용자, 현재 시각, 또는 요청 데이터에 포함되지 않은 어떤 내용 같은 정보를 포함할 수 있다.

`.save()`를 호출할 때 추가 키워드 인자를 포함하면 그렇게 할 수 있다. 예를 들면:

```python
serializer.save(owner=request.user)`
```

모든 추가 키워드 인자는 `.create()` 혹은 `.update()`가 호출되었을 때 `validated_data` 인자에 포함된다.

### Overriding `.save()` directly.
`.create()`와 `.update()`라는 이름이 의미 없는 경우가 있다. 예를 들어 연락 폼에서 새로운 인스턴스를 생성하지 않는 대신 이메일이나 다른 메시지를 보낼 수 있다.

이런 경우 좀 더 가독성이 좋고 의미를 가지도록 `.save()`를 직접 재정의할 수 있다.

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
데이터를 역직렬화할 때, 유효성을 검증한 데이터에 접근하려 하거나 객체 인스턴스를 저장하기 전에 꼭 `is_valid()`를 호출해야 한다. 유효성 오류가 발생하면 `.errors` 속성이 에러 메시지를 표현하는 딕셔너리를 포함하게 된다. 예를 들어:

```python
serializer = CommentSerializer(data={'email': 'foobar', 'content': 'baz'})
serializer.is_valid()
# False
serializer.errors
# {'email': ['Enter a valid e-mail address.'], 'created': ['This Field is required.']}
```

딕셔너리 안의 각각의 키는 필드명이 되고, 그 값은 해당하는 필드에 대응하는 에러 메시지 문자열의 리스트가 된다. `non_field_errors` 키 또한 존재할 수 있으며, 일반적인 유효성 오류를 나열할 것이다. REST framework 설정에서 `NON_FIELD_ERRORS_KEY`를 사용해 `non_field_errors` 키의 이름을 변경할 수 있다.

아이템 리스트를 역직렬화할 때에는 각각의 역직렬화된 아이템을 나타내는 딕셔너리의 리스트로 에러가 반환된다.

### Raising an exception on invalid data
`.is_valid()` 메서드는 유효성 오류가 있을 때 `serializers.ValidationError` 예외를 발생시키기 위한 선택적인 `raise_exception` 플래그를 가진다.

이러한 예외들은 REST framework가 제공하는 기본 예외 처리기에 의해 자동으로 다루어지며, 기본적으로 `HTTP 400 Bad Request` 응답을 반환한다.

```python
# 데이터가 유효하지 않은 경우 400 응답을 반환한다.
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
        블로그 게시글이 Django에 관한 것인지 확인한다.
        """
        if 'django' not in value.lower():
            raise serializers.ValidationError("Blog post is not about Django")
        return value
```

---

**Note**: 만약 `<field_name>`이 `required=False` 인자가 있는 상태로 시리얼라이저에서 선언되었다면 해당 필드가 포함되지 않았을 때 이 유효성 검증 단계는 생략될 것이다.

---

### Object-level validation
유효성 검사가 복수의 필드에 접근해야 한다면 `Serializer` 서브클래스에 `.validate()` 메서드를 추가한다. 이 메서드는 필드 값의 딕셔너리인 하나의 인자를 가진다. 필요하다면 `serializers.ValidationError`를 발생시키거나 유효한 값을 반환한다. 예를 들어:

```python
from rest_framework import serializers

class EventSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=100)
    start = serializers.DateTimeField()
    finish = serializers.DateTimeField()

    def validate(self, data):
        """
        `start`가 `finish` 이전인지 확인한다.
        """
        if data['start'] > data['finish']:
            raise serializers.ValidationError("finish must occur after start")
        return data
```

### Validators
시리얼라이저에 있는 각각의 필드는 다음과 같이 필드 인스턴스에서 유효성 검사기를 선언해 포함할 수 있다.

```python
def multiple_of_ten(value):
    if value % 10 != 0:
        raise serializers.ValidationError('Not a multiple of ten')

class GameRecord(serializers.Serializer):
    score = IntegerField(validators=[multiple_of_ten])
    ...
```

시리얼라이저 클래스는 필드 테이터의 완전한 집합에 적용되는 재사용 가능한 유효성 검사기를 포함할 수 있다. 이러한 유효성 검사기는 다음과 같이 내부의 `Meta` 클래스에서 선언하여 포함될 수 있다.

```python
class EventSerializer(serializers.Serializer):
    name = serializers.CharField()
    room_number = serializers.IntegerField(choices=[101, 102, 103, 201])
    date = serializers.DateField()

    class Meta:
        # 각 방은 하루에 단 하나의 이벤트를 가질 수 있다.
        validators = [
            UniqueTogetherValidator(
                queryset=Event.objects.all(),
                fields=['room_number', 'date']
            )
        ]
```

더 많은 정보는 [유효성 검사기 문서](validators.md)에서 확인할 수 있다.

## Accessing the initial data and instance
초기 객체나 queryset을 시리얼라이저 인스턴스로 전달할 때 객체는 `.instance`로 사용 가능하게 된다. 초기 객체가 전달되지 않았다면 `.instance` 속성은 `None`이 된다.

시리얼라이저 인스턴스로 데이터를 전달할 때, 수정되지 않은 데이터는 `.initial_data`로 사용 가능하게 된다. `data` 키워드 인자가 전달되지 않았다면 `initial_data` 속성이 존재하지 않게 된다.


## Partial updates
기본적으로 시리얼라이저에는 모든 필수 필드를 위한 값이 전달되어야 하며, 그렇지 않을 경우 유효성 검사 오류가 발생한다. 부분 갱신을 하려면 `partial` 인자를 사용하면 된다.

```python
# 일부 데이터로 `comment` 갱신하기
serializer = CommentSerializer(comment, data={'content': 'foo bar'}, partial=True)
```

## Dealing with nested objects
이전 예시는 단순한 데이터 타입만을 가지는 객체를 다루는 데에는 괜찮았지만 때로 객체의 속성이 문자열, 날짜 또는 정수와 같은 단순한 데이터 타입이 아닌 좀 더 복잡한 객체를 나타낼 수 있어야 한다.

`Serializer` 클래스는 그 스스로 `Field`의 유형이며, 하나의 객체 타입이 다른 객체 안에 중첩된 관계를 나타내는데 사용될 수 있다.

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
    user = UserSerializer(required=False) # 익명의 사용자일 수도 있다.
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
```

유사하게, 중첩된 표현이 아이템의 리스트가 되어야 한다면 중첩된 시리얼라이저에 `many=True` 플래그를 전달해야 한다.

```python
class CommentSerializer(serializers.Serializer):
    user = UserSerializer(required=False)
    edits = EditItemSerializer(many=True) # 'edit' 항목의 중첩된 리스트
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
```

## Writable nested representations
데이터 역직렬화를 지원하는 중첩된 표현을 다룰 때, 중첩된 객체에 관한 모든 오류는 중첩된 객체의 필드명 아래 중첩된다.

```python
serializer = CommentSerializer(data={'user': {'email': 'foobar', 'username': 'doe'}, 'content': 'baz'})
serializer.is_valid()
# False
serializer.errors
# {'user': {'email': ['Enter a valid e-mail address']}, 'created': ['This field is required.']}
```

이와 유사하게, `.validated_data`속성이 중첩된 자료 구조에 포함된다.

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
    # 애플리케이션이 이 필드가 언제나 설정되어 있다는 것을 적절히 보장하지 않는다면
    # 다음은 `DoesNotExist`를 발생시켜야 하며, 이는 처리될 필요가 있다.
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

그러나 자동으로 작성 가능한 중첩된 표현을 지원하는 [DRF Writable Nested](serializers.md/#drf-writable-nested)와 같은 서드파티 패키지를 사용할 수 있다.

### Handling saving related instances in model manager classes
시리얼라이저에서 복수의 연관된 인스턴스를 저장하는 다른 방법은 올바른 인스턴스 생성을 다루는 사용자 정의 모델 매니저 클래스를 작성하는 것이다.

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

이제 매니저 클래스는 사용자 인스턴스와 프로필 인스턴스가 항상 같이 생성되는 것을 더 좋게 캡슐화한다. 이제 새 매니저 메서드를 사용하기 위해 시리얼라이저의 `.create()` 메서드를 재작성한다.

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
복수의 개체를 deserialize하는 기본 동작은 복수의 개체 생성을 지원하지만 복수의 개체 갱신은 지원하지 않는 것이다. 이런 경우를 어떻게 지원할지, 혹은 어떻게 커스터마이즈를 할지에 관한 정보는 아래의 [ListSerializer](serializers.md/#listserializer) 문서에서 확인할 수 있다.

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

외래키와 같은 모델의 관계는 `PrimaryKeyRelatedField`에 매핑될 것이다. 역관계는 [시리얼라이저 관계](serializer_relations.md) 문서에서 기술된 것처럼 명시적으로 포함된 것이 아니라면 기본으로 포함되지는 않는다.

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

  [UniqueTogetherValidator](validators.md/#uniquetogethervalidator)와 [CurrentUserDefault](validators.md/#currentuserdefault) 클래스에 관한 자세한 내용은 [Validators 문서](validators.md)에서 확인할 수 있다.

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

## Relational fields
모델 인스턴스를 serialize할 때 관계를 나타내는 여러 다른 방법이 있다. `ModelSerializer`의 기본 표현은 연관된 인스턴스의 기본키를 사용하는 것이다.

다른 표현 방식에는 하이퍼링크를 이용한 serialize, 중첩된 표현을 온전히 serialize하는 것 또는 사용자 정의 표현을 serialize하는 것이 있다.

[serializer relations](serializer_relations.md)문서에서 더 많은 정보를 확인할 수 있다.

## Customizing field mappings
ModelSerializer 클래스는 시리얼라이저를 초기화할 때 어떻게 자동으로 시리얼라이저 필드가 결정되리 정하기 위해 override할 수 있는 API를 노출시킨다.

보통 `ModelSerializer`는 필요로 하는 필드를 기본으로 생성하지는 않기 때문에 클래스에 필드를 명시적으로 추가하거나 대신 일반적인 `Serializer` 클래스를 사용해야 한다. 한편, 주어진 모델을 위해 시리얼라이저 필드가 어떻게 생성되어야 할지를 정의하는 새로운 베이스 클래스를 작성할 수 있다.

#### `.serializer_field_mapping`
Django 모델 필드를 REST framework 시리얼라이저 필드로 매핑하는 것. 이 매핑을 각 모델 필드에 사용할 기본 시리얼라이저 필드로 바꾸기 위해 override할 수 있다.

#### `.serializer_related_field`
이 속성은 기본적으로 과계 필드에 사용되는 시리얼라이저 필드 클래스가 되어야 한다.

`ModelSerializer`의 경우 기본 값은 `serializers.PrimaryKeyRelatedField`<br>
`HyperlinkedModelSerializer`의 경우 기본 값은 `serializers.HyperlinkedRelatedField`

#### `.serializer_url_field`
시리얼라이저에 있는 `url` 필드에 사용되는 시리얼라이저 필드 클래스.

기본값: `serializers.HyperlinkedIdentityField`

#### `.serializer_choice_field`
시리얼라이저에 있는 초이스 필드에 사용되는 시리얼라이저 필드 클래스.

기본값: `serializers.ChoiceField`

### The field_class and field_kwargs API
다음의 메서드는 자동으로 시리얼라이저에 포함될 각 필드를 위한 클래스와 키워드 인자를 결정하기 위해 호출된다. 각 메서드는 튜플 `(field_class, field_kwargs)`를 반환한다.

#### `.build_standard_field(self, field_name, model_field)`
일반적인 모델 필드로 매핑되는 시리얼라이저 필드를 생성하기 위해 호출된다.

기본 구현은 `serializer_field_mapping` 속성에 기반한 시리얼라이저 클래스를 반환한다.

#### `.build_relational_field(self, field_name, relation_info)`
관계 모델 필드로 매핑되는 시리얼라이저 필드를 생성하기 위해 호출된다.

기본 구현은 `serializer_related_field` 속성에 기반한 시리얼라이저 클래스를 반환한다.

`related_info` 인자는 속성 `model_field`, `related_model`, `to_many`, `has_through_model`을 포함하는 named 튜플이다.

#### `.build_nested_field(self, field_name, relation_info, nested_depth)`
`depth` 옵션이 설정되었을 때, 관계 모델 필드로 매핑되는 시리얼라이저 필드를 생성하기 위해 호출된다.

기본 구현은 `ModelSerializer` 또는 `HyperlinkedModelSerializer`에 기반한 중첩된 시리얼라이저 클래스를 동적으로 생성한다.

`nested_depth`는 `depth` 옵션의 값에서 1을 뺀 값이다.

`relation_info` 인자는 속성 `model_field`, `related_model`, `to_many`, `has_through_model`을 포함하는 named 튜플이다.

#### `.build_property_field(self, field_name, model_class)`
모델 클래스의 속성이나 인자 없는 메서드로 매핑되는 시리얼라이저 필드를 생성하기 위해 호출된다.

기본 구현은 `ReadOnlyField` 클래스를 반환한다.

#### `.build_url_field(self, field_name, model_class)`
시리얼라이저 자체 `url` 필드를 위한 시리얼라이저 필드를 생성하기 위해 호출된다. 기본 구현은 `HyperlinkedIdentityField` 클래스를 반환한다.

#### `.build_unknown_field(self, field_name, model_class)`
필드 이름이 어느 모델 필드나 모델 속성에도 매핑되지 않을 때 호출된다. 기본 구현은 서브클래스가 이런 동작을 커스터마이즈할 수 있지만 에러를 발생시킨다.

# HyperlinkedModelSerializer
`HyperlinkedModelSerializer` 클래스는 관계를 표현하기 위해 기본키가 아닌 하이퍼링크를 사용한다는 점을 제외하면 `ModelSerializer` 클래스와 유사하다.

기본적으로, 시리얼라이저는 기본키 필드 대신 `url` 필드를 포함하게 된다.

url 필드는 `HyperlinkedIdentityField` 시리얼라이저 필드를 사용해 표현될 것이며, 모델에 있는 모든 관계는 `HyperlinkedRelatedField` 시리얼라이저 필드를 사용해 표현된다.

다음과 같이 `fields` 옵션에 기본키를 명시해 추가할 수도 있다.

```python
class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ['url', 'id', 'account_name', 'users', 'created']
```

## Absolute and relative URLs
다음과 같이 `HyperlinkedModelSerializer`를 초기화할 때에는 시리얼라이저 컨텍스트에 현재 `request`를 포함시켜야 한다.

```
serializer = AccountSerializer(queryset, context={'request': request})
```

이렇게 하면 하이퍼링크가 적절한 호스트 네임을 포함하는 것을 보장할 수 있으며 그러면 다음과 같이 표현되는 정규화된 URL을 결과물로 사용하게 된다.

```
http://api.example.com/accounts/1
```

다음과 같은 상대 경로 대신.

```
/accounts/1/
```

상대 경로를 *사용하고 싶다*면, 시리얼라이저 컨텍스트에 `{'request': None}`을 명시적으로 전달해야 한다.

## How hyperlinked views are determined
모델 인스턴스에 하이퍼링크되는데 사용하는 뷰를 결정하는 방법이 필요하다.

기본적으로 하이퍼링크는 `'{model_name}-detail'` 형식의 이름을 가지는 뷰에 대응되고, `pk` 키워드 인자로 인스턴스를 찾는다.

다음과 같이 `extra_kwargs` 설정에서 `view_name`과 `lookup_field` 옵션 중 하나 혹은 둘 모두를 사용해 URL 필드 뷰 이름과 탐색 필드를 override할 수 있다.

```python
class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ['account_url', 'account_name', 'users', 'created']
        extra_kwargs = {
            'url': {'view_name': 'accounts', 'lookup_field': 'account_name'},
            'users': {'lookup_field': 'username'}
        }
```

시리얼라이저의 필드를 명시적으로 설정할 수도 있다. 예를 들면:

```python
class AccountSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='accounts',
        lookup_field='slug'
    )
    users = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        lookup_field='username',
        many=True,
        read_only=True
    )

    class Meta:
        model = Account
        fields = ['url', 'account_name', 'users', 'created']
```

- **Tip**:<br>
  하이퍼링크된 표현과 URL 설정을 적절하게 일치시키는 것은 간혹 성가시다. `HyperlinkedModelSerializer` 인스턴스의 `repr`를 출력하는 것이 관계를 매핑하기 위해 어느 뷰 이름과 검색 필드를 찾을 때에도 특히 유용한 방법이다.

## Changing the URL field name
URL 필드의 기본 이름은 `url`이다. `URL_FIELD_NAME` 설정을 사용해 전역적으로 override할 수 있다.

# ListSerializer
`ListSerializer` 클래스는 복수의 개체를 한 번에 serialize하고 유효성을 확인하기 위한 동작을 제공한다. 보통은 `ListSerializer`를 직접 사용할 일이 없고, 대신 단순히 시리얼라이저를 초기화할 때 `many=True`를 전달한다.

시리얼라이저가 초기화되고 `many=True`가 전달될 때, `ListSerializer` 인스턴스가 생성된다. 시리얼라이저 클래스는 그 다음에 부모 `ListSerializer`의 자신이 된다.

다음의 인자는 `ListSerializer` 필드나 `many=True`가 전달된 시리얼라이저에 전달될 수 있다.

#### `allow_empty`
기본적으로 `True`이지만 빈 리스트를 유효한 입력으로 허용하고 싶지 않다면 `False`로 설정한다.

#### `max_length`
기본적으로 `None`이지만 리스트의 최대 길이에 제한을 두고 싶다면 양의 정수로 설정한다.

#### `min_length`
기본적으로 `None`이지만 리스트의 최소 길이에 제한을 두고 싶다면 양의 정수로 설정한다.

## Customizing `ListSerializer` behavior
`ListSerializer`의 동작을 수정하게 되는 몇 가지 경우가 있다. 예를 들면:

- 리스트 내의 한 원소가 다른 원소와 충돌을 일으키지 않는지 확인하는 등의 리스트에 특정한 유효성 검사를 제공하는 경우
- 복수의 객체를 생성하거나 갱신하는 동작을 수정하는 경우

이러한 경우, 시리얼라이저의 `Meta` 클래스의 `list_serializer_class` 옵션을 사용해 `many=True`가 전달되었을 때 사용될 클래스를 수정한다.

예를 들어:

```python
class CustomListSerializer(serializers.ListSerializer):
    ...


class CustomSerializer(serializers.Serializer):
    ...
    class Meta:
        list_serializer_class = CustomListSerializer
```

### Customizing multiple create
복수의 개체를 생성하는 기본 구현은 단순히 리스트에 있는 각각의 아이템에 대해 `.create()`를 호출하는 것이다. 이 동작을 수정하려면, `many=True`가 전달되었을 때 사용되는 `ListSerializer` 클래스의 `.create()` 메서드를 커스터마이즈해야 한다.

예를 들면:

```python
class BookListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        books = [Book(**item) for item in validated_data]
        return Book.objects.bulk_create(books)


class BookSerializer(serializers.Serializer):
    ...
    class Meta:
        list_serializer_class = BookListSerializer
```

### Customizing multiple update
`ListSerializer` 클래스는 기본적으로 다중 갱신을 지원하지 않는다. 왜냐하면 삽입과 삭제에 관해 예상되는 동작이 모호하기 때문이다.

다중 갱신을 지원하려면 명시적으로 해야 한다. 다음을 염두에 두고 다중 갱신 코드를 작성해야 한다.

- 데이터 리스트의 아이템 중 어느 인스턴스가 갱신되어야할지 어떻게 결정할 수 있을까?
- 삽입은 어떻게 다루어져야 하는가? 유효하지 않은 것인가, 아니면 새 객체를 생성하게 되는가?
- 삭제는 어떻게 다루어져야 하는가? 객체 삭제를 의미하는가, 혹은 관계 삭제를 의미하는가? 조용히 무시되어야 하는 것인가 혹은 유효하지 않은 것인가?
- 순서는 어떻게 다루어져야 하는가? 두 아이템의 위치를 바꾸는 것이 어떤 상태의 변화를 의미하는가 혹은 무시되는가?

인스턴스 시리얼라이저에 명시적인 `id` 필드를 추가해야 한다. 암묵적으로 생성되는 기본 `id` 필드는 `read_only`로 표시된다. 이는 갱신될 때 삭제된다. 한 번 명시적으로 선언하면 리스트 시리얼라이저의 `update` 메서드에서 사용할 수 있다.

다음은 다중 갱신을 구현하는 한 가지 방법이다.

```python
class BookListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        # Maps for id -> instance and id -> data item.
        book_mapping = {book.id: book for book in instance}
        data_mapping = {item['id']: item for item in validated_data}

        # Perform creations and updates.
        ret = []
        for book_id, data in data_mapping.items():
            book = book_mapping.get(book_id, None)
            if book is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(book, data))

        # Perform deletions.
        for book_id, book in book_mapping.items():
            if book_id not in data_mapping:
                book.delete()

        return ret


class BookSerializer(serializers.Serializer):
    # We need to identify elements in the list using their primay key,
    # so use a writable field here, rather than the default which would be read-only.
    id = serializers.IntegerField()
    ...

    class Meta:
        list_serializer_class = BookListSerializer
```

REST framework 2에 존재했던 `allow_add_remove` 동작과 유사한, 다중 갱신 연산 자동 지원을 제공하는 서드파티 패키지를 3.1 버전과 함께 사용할 수도 있다.

### Customizing ListSerializer initialization
`many=True`인 시리얼라이저를 인스턴스화할 때 어느 인자와 키워드 인자가 자식 `Serializer` 클래스와 부모 `ListSerializer` 클래스의 `.__init__()` 메서드에 전달되어야 하는지 결정해야 한다.

기본 구현은 자식 시리얼라이저 클래스를 대상으로 하는 것으로 간주되는 `validator`와 사용자 정의 키워드 인자를 제외한 모든 인자를 두 클래스에 전달하는 것이다.

때때로 `many=True`가 전달될 때 자식과 부모 클래스가 어떻게 인스턴스화되어야 하는지 명시적으로 구체화해야 하는 경우가 있다. `many_init` 클래스 메서드를 사용하면 된다.

```python
@classmethod
def many_init(cls, *args, **kwargs):
    # Instantiate the child serializer.
    kwargs['child'] = cls()
    # Instantiate the parent list serializer.
    return CustomListSerializer(*args, **kwargs)
```

# BaseSerializer
`BaseSerializer` 클래스는 또 다른 serialization과 deserialization 방식을 쉽게 지원하기 위해 사용된다.

이 클래스는 `Serializer` 클래스와 같은 기본 API를 구현한다.

- `.data`: 가공되지 않은 출력 표현을 반환한다.
- `.is_valid()`: 들어오는 데이터를 deserialize하고 그 유효성을 검사한다.
- `.validated_data`: 들어온 유효한 데이터를 반환한다.
- `.errors`: 유효성 검사 중 발생한 에러를 반환한다.
-`.save()`: 유효한 데이터를 객체 인스턴스로 남긴다.

시리얼라이저 클래스가 지원하기를 바라는 기능에 따라 override될 수 있는 네 개의 메서드가 있다.

- `.to_representation()`: 읽기 연산에 serialization을 지원하기 위해 override한다.
- `.to_internal_value()`: 쓰기 연산에 deserialization을 지원하기 위해 override한다.
- `.create`, `.update()`: 인스턴스 저장을 지원하기 위해 둘 중 하나 이상을 override한다.

이 클래스가 `Serializer` 클래스와 동일한 인터페이스를 제공하기 때문에 일반적인 `Serializer`나 `ModelSerializer`의 경우에서 그러하듯이 존재하는 generic 클래스 기반 뷰와 함께 사용할 수 있다.

그럴 때의 유일한 차이점은 `BaseSerializer` 클래스가 브라우징 가능한 API를 HTML 폼으로 생성하지 않을 것이라는 점이다. 왜냐하면 반환하는 데이터가 각 필드를 적절한 HTML 입력으로 렌더링할 수 있도록 해주는 필드 정보를 포함하고 있지 않기 때문이다.

## Read-only `BaseSerializer` classes
`BaseSerializer`를 사용해 읽기 전용 시리얼라이저를 구현하려면 `.to_representation()` 메서드를 override한다. 다음은 간단한 Django 모델을 사용한 예시이다.

```python
class HighScore(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    player_name = models.CharField(max_length=10)
    score = models.IntegerField()
```

`HighScore` 인스턴스를 원시 데이터형으로 변환하는 읽기 전용 시리얼라이저를 생성하는 것은 간단하다.

```python
class HighScoreSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'score': instance.score,
            'player_name': instance.player_name
        }
```

이제 이 클래스를 하나의 `HighScore` 인스턴스를 serialize하는데 사용할 수 있다.

```python
@api_view(['GET'])
def high_score(request, pk):
    instance = HighScore.objects.get(pk=pk)
    serializer = HighScoreSerializer(instance)
    return Response(serializer.data)
```

혹은 복수의 인스턴스를 serialize하기 위해 사용할 수 있다.

```python
@api_view(['GET'])
def all_high_scores(request):
    queryset = HighScore.objects.order_by('-score')
    serializer = HighScoreSerializer(queryset, many=True)
    return Response(serializer.data)
```

## Read-write `BaseSerializer` classes
읽기-쓰기 시리얼라이저를 생성하려면 우선 `.to_internal_value` 메서드를 구현할 필요가 있다. 이 메서드는 객체 인스턴스를 생성하기 위해 사용되는 유효한 값을 반환하며, 제공된 데이터가 정확하지 않은 형식이라면 `serializers.ValidationError`를 발생시킨다.

`.to_internal_value()`를 구현하면 시리얼라이저에서 기본 유효성 검사 API를 사용할 수 있게 되며 `.is_valid()`, `.validated_data`, `.errors`를 사용할 수 있게 된다.

`.save()`를 지원하려면 `.create()`나 `.update()` 메서드 중 하나 혹은 둘 모두를 구현하면 된다.

다음은 읽기와 쓰기 연산을 둘 다 지원하도록 갱신된 `HighScoreSerializer`의 완성된 예시이다.

```python
class HighScoreSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data):
        score = data.get('score')
        player_name = data.get('player_name')

        # Perform the data validation.
        if not score:
            raise serializers.ValidationError({
                'score': 'This field is required.'
            })
        if not player_name:
            raise serializers.ValidationError({
                'player_name': 'This field is required.'
            })
        if len(player_name) > 10:
            raise serializers.ValidationError({
                'player_name': 'May not be more than 10 characters.'
            })

        # Return the validation values. This will be available as
        # the `.validated_data` property.
        return {
            'score': int(score),
            'player_name': player_name
        }

    def to_representation(self, instance):
        return {
            'score': instance.score,
            'player_name': instance.player_name
        }

    def create(self, validated_data):
        return HighScore.objects.create(**validated_data)
```

## Creating new base classes
`BaseSerializer` 클래스는 특정한 serialization 형식을 다루기 위해, 혹은 대체 스토리지 백엔드와 통합하기 위해 새로운 generic 시리얼라이저 클래스를 구현할 때에도 유용하다.

다음의 클래스는 임의의 복잡한 객체를 원시 표현으로 강제하는 것을 다루는 generic 시리얼라이저의 예시이다.

```python
class ObjectSerializer(serializers.BaseSerializer):
    """
    A read-only serializer that coerces arbitrary complex objects
    into primitive representations.
    """
    def to_representation(self, instance):
        output = {}
        for attribute_name in dir(instance):
            attribute = getattr(instance, attribute_name)
            if attribute_name.startswith('_'):
                # Ignore private attributes.
                pass
            elif hasattr(attribute, '__call__'):
                # Ignore methods and other callables.
                pass
            elif isinstance(attribute, (str, int, bool, float, type(None))):
                # Primitive types can be passed through unmodified.
                output[attribute_name] = attribute
            elif isinstance(attribute, list):
                # Recursively deal with items in lists.
                output[attribute_name] = [
                    self.to_representation(item) for item in attribute
                ]
            elif isinstance(attribute, dict):
                # Recursively deal with items in dictionaries.
                output[attribute_name] = {
                  str(key): self.to_representation(value)
                  for key, value in attribute.items()
                }
            else:
                # Force anything else to its string representation.
                output[attribute_name] = str(attribute)
        return output
```

# Advanced serializer usage
## Overriding serialization and deserialization behavior
시리얼라이저 클래스의 serialize나 deserialize 동작을 변경해야 한다면 `.to_representation()`이나 `.to_internal_value()` 메서드를 override하면 된다.

이것이 유용한 이유는...

- 새로운 시리얼라이저 베이스 클래스를 위한 새로운 동작을 추가한다.
- 이미 존재하는 클래스의 동작을 약간 변경한다.
- 많은 데이터를 반환하는 접근이 잦은 API 엔드포인트의 serialization 퍼포먼스를 향상시킨다.

이 메서드의 특징은 다음과 같다.

### `.to_representation(self, instance)`
Serialize가 필요한 객체 인스턴스를 전달받아 원시적인 표현을 반환한다. 보통 이는 빌트인 파이썬 데이터형 구조로 반환하는 것을 의미한다. 다루게 되는 정확한 데이터형은 API를 위해 설정된 렌더 클래스에 따라 다르다.

표현 양식을 변경하기 위해 override될 수 있다. 예를 들면:

```python
def to_representation(self, instance):
    # Convert `username` to lowercase.
    ret = super().to_representation(instance)
    ret['username'] = ret['username'].lower()
    return ret
```

### `.to_internal_value(self, data)`
유효성 검증이 되지 않은 들어오는 데이터를 입력으로 받아 `serializer.validated_data`로 사용가능하게 되는 유효한 데이터를 반환한다. 반환값은 시리얼라이저 클래스에서 `.save()`가 반환되었을 때 `.create()` 또는 `.update()` 메서드로 전달된다.

유효성 검증에 실패한다면 메서드는 `serializers.ValidationError(errors)`를 발생시킨다. `errors` 인자는 필드 이름(또는 `settings.NON_FIELD_ERRORS_KEY`)을 오류 메시지의 리스트로 매핑하는 딕셔너리여야 한다. Deserialization 동작을 바꾸지 않는 대신 객체 수준의 유효성 검사를 제공하고 싶다면 `.validate()` 메서드를 override하는 것을 권장한다.

이 메서드로 전달되는 `data` 인자는 보통 `request.data`의 값이므로 이것이 제공하는 데이터형은 API를 위해 설정한 parser 클래스에 따라 다르다.

## Serializer Inheritance
Django 폼과 유사하게, 상속을 통해 시리얼라이저를 확장하고 재사용할 수 있다. 이는 여러 시리얼라이저에서 사용할 수 있는 필드나 메서드의 공통적인 세트를 부모 클래스에 선언할 수 있게 한다.

```python
class MyBaseSerializer(Serializer):
    my_field = serializers.CharField()

    def validate_my_field(self, value):
        ...

class MySerializer(MyBaseSerializer):
    ...
```

Django의 `Model`과 `ModelForm` 클래스처럼, 시리얼라이저 내부의 `Meta` 클래스는 부모 내부의 `Meta` 클래스를 반드시 상속받지는 않는다. 부모 클래스로부터 `Meta` 클래스를 상속받고 싶다면 명시적으로 해야 한다. 예를 들어:

```python
class AccountSerializer(MyBaseSerializer):
    class Meta(MyBaseSerializer.Meta):
        model = Account
```

보통 내부 Meta 클래스를 상속받는 것을 권장하지 *않는* 대신, 모든 옵션을 명시적으로 선언하는 것을 권장한다.

추가적으로, 시리얼라이저 상속에 적용되는 주의사항은 다음과 같다.

- 일반적인 파이썬 이름 확인 규칙이 적용된다. 내부 `Meta` 클래스를 선언하는 복수의 베이스 클래스가 있다면 오직 첫번째 것이 사용된다. 이는 존재한다면 자식의 `Meta`, 그렇지 않다면 첫번째 부모의 `Meta`를 의미한다.
- 서브클래스에서 이름이 `None`이 되도록 설정해 부모 클래스에서 상속받은 `Field`를 선언하듯이 제거할 수 있다.
  ```python
  class MyBaseSerializer(ModelSerializer):
      my_field = serializers.CharField()
  
  class MySerializer(MyBaseSerializer):
      my_field = None
  ```
  그러나 이 방법은 부모 클래스에 의해 선언하듯이 정의된 필드를 없앨 때에만 사용할 수 있다. 이것은 `ModelSerializer`가 기본 필드를 생성하는 것을 방지하지 못한다. 기본 필드를 사용하지 않으려면 [어느 필드를 포함할지 구체화하기](serializers.md/#specifying-which-fields-to-include) 문서를 확인한다.

## Dynamically modifying fields
일단 시리얼라이저가 초기화되면, `.fields` 속성을 사용해 시리얼라이저에 설정된 필드 딕셔너리에 접근할 수 있다. 이 속성에 접근하는 것과 이 속성을 수정하는 것은 시리얼라이저를 동적으로 수정할 수 있게 한다.

`fields` 인자를 직접 수정하면 시리얼라이저를 선언하는 순간이 아니라 동작 중 시리얼라이저 필드의 인자를 변경하는 등의 흥미로운 일을 할 수 있게 된다.

### Example
예를 들어, 시리얼라이저를 초기화하는 시점에 어느 필드를 시리얼라이저에서 사용할지 정하게 하고 싶다면 시리얼라이저 클래스를 다음과 같이 작성하면 된다.

```python
class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
```

이는 다음을 가능하게 한다.

```python
>>> class UserSerializer(DynamicFieldsModelSerializer):
>>>     class Meta:
>>>         model = User
>>>         fields = ['id', 'username', 'email']
>>>
>>> print(UserSerializer(user))
{'id': 2, 'username': 'lime', 'email': 'lime@example.com'}
>>>
>>> print(UserSerializer(user, fields=('id', 'email')))
{'id': 2, 'email': 'lime@example.com'}
```

## Customizing the default fields
REST framework 2는 개발자가 `ModelSerializer` 클래스가 어떻게 필드의 기본 세트를 자동으로 생성할지 override할 수 있게 해주는 API를 제공했다.

이 API는 `.get_field()`, `.get_pk_field()`와 다른 메서드를 포함했다.

3.0에서 시리얼라이저가 근본적으로 재설계되었기 때문에 이 API는 더이상 존재하지 않는다. 여전히 생성되는 필드를 수정할 수 있지만 소스 코드를 참조해야 하며, API의 private bit에 반하는 변경사항이 발생하는 경우 이 또한 변경될 수 있다는 점에 유의해야 한다.

# Third party packages
다음의 서드파티 패키지를 사용할 수 있다.

## Django REST marshmallow
[django-rest-marshmallow](https://marshmallow-code.github.io/django-rest-marshmallow/) 패키지는 파이썬 [marshmallow](https://marshmallow.readthedocs.io/en/latest/) 라이브러리를 사용해 시리얼라이저의 대체 구현을 제공한다. REST framework 시리얼라이저와 같은 API를 제공하며 일부 사용 예시에서 드롭 인 대체로 사용될 수 있다.

## Serpy
[serpy](https://github.com/clarkduvall/serpy) 패키지는 속도를 위해 빌드된 시리얼라이저를 위한 대체 구현이다. Serpy는 복잡한 데이터형을 단순한 네이티브 형으로 serialize한다. 네이티브 형은 JSON이나 다른 필요로 하는 포맷으로 쉽게 변환될 수 있다.

## MongoengineModelSerializer
[django-rest-framework-mongoengine](https://github.com/umutbozkurt/django-rest-framework-mongoengine) 패키지는 Django REST framework를 위한 스토리지 레이어로 MongoDB를 사용할 수 있게 지원하는 `MongoEngineModelSerializer` 시리얼라이저 클래스를 제공한다.

## GeoFeatureModelSerializer
[django-rest-framework-gis](https://github.com/djangonauts/django-rest-framework-gis) 패키지는 읽기와 쓰기 연산을 위한 GeoJSON을 지원하는 `GeoFeatureModelSerializer` 시리얼라이저 클래스를 제공한다.

## HStoreSerializer
[django-rest-framework-hstore](https://github.com/djangonauts/django-rest-framework-hstore)는 [django-hstore](https://github.com/djangonauts/django-hstore)의 `DictionaryField` 모델 필드와 `schema-mode` 기능을 지원하는 `HStoreSerializer`를 제공한다.

## Dynamic REST
[dynamic-rest](https://github.com/AltSchool/dynamic-rest) 패키지는 ModelSerializer와 ModelViewSet 인터페이스를 확장해 시리얼라이저에 의해 정의된 모든 필드와 관계를 필터링, 정렬, 그리고 포함/제외하는 API 쿼리 인자를 추가한다.

## Dynamic Fields Mixin
[drf-dynamic-fields](https://github.com/dbrgn/drf-dynamic-fields) 패키지는 URL 인자에 의해 구체화된 서브셋으로 시리얼라이저 당 필드를 동적으로 제한하는 mixin을 제공한다.

## DRF FlexFields
[drf-flex-fields](https://github.com/rsinger86/drf-flex-fields)는 URL 인자와 시리얼라이저 클래스 정의로부터 동적으로 정해지는 필드와 원시 필드를 중첩된 모델로 확장하는 자주 사용되는 기능을 제공하기 위해 ModelSerializer와 ModelViewSet을 확장한다.

## Serializer Extensions
[django-rest-framework-serializer-extensions](https://github.com/evenicoulddoit/django-rest-framework-serializer-extensions) 패키지는 필드를 뷰당/요청 기준에 따라 정의되도록 허용하는 것으로 시리얼라이저를 DRY(Don't Repeat Yourself)하기 위한 도구 모음을 제공한다. 필드를 화이트리스트나 블랙리스트에 올릴 수 있고 자식 시리얼라이저는 선택적으로 확장될 수 있다.

## HTML JSON Forms
[html-json-forms](https://github.com/wq/html-json-forms) 패키지는 `<form>` 제출을 (비활성화된)[HTML JSON FORM specification](https://www.w3.org/TR/html-json-forms/)에 따라 가공하기 위한 알고리즘과 시리얼라이저를 제공한다. 시리얼라이저는 HTML 내의 임의의 중첩된 JSON 구조를 가공하는 것을 용이하게 한다. 예를 들어 `<input name="items[0][id]" value="5">`는 `{"items": [{"id": "5"}]}`로 해석된다.

## DRF-Base64
[DRF-Base64](https://bitbucket.org/levit_scs/drf_base64)는 base64 인코딩된 파일 업로드를 다루는 필드의 세트와 모델 시리얼라이저를 제공한다.

## QueryFields
[djangorestframework-queryfields](https://djangorestframework-queryfields.readthedocs.io/)는 쿼리 인자 포함/제외를 통해 API 클라이언트가 어느 필드를 응답에 포함시킬 것인지 구체화하도록 한다.

## DRF Writable Nested
[drf-writable-nested](https://github.com/beda-software/drf-writable-nested) 패키지는 중첩된 연관 데이터로 모델을 생성/갱신할 수 있게 해주는 쓰기 가능한 중첩된 모델 시리얼라이저를 제공한다.

## DRF Encrypt Content
[drf-encrypt-content](https://github.com/oguzhancelikarslan/drf-encrypt-content) 패키지는 ModelSerializer를 통해 serialize된 데이터를 암호화하는 것을 도화준다. 데이터를 암호화하는데 도움을 주는 몇 가지 도우미 함수 또한 포함하고 있다.