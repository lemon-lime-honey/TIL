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