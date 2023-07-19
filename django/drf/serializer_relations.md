# [Serializer relations](https://www.django-rest-framework.org/api-guide/relations/)
```
알고리즘이 아닌 자료구조가 프로그래밍의 중심이다.
- Rob Pike
```

관계 필드는 모델 관계를 나타내기 위해 사용된다. `ForeignKey`, `ManyToManyField`, `OneToOneField` 관계 뿐만 아니라 역관계, `GenericForeignKey`와 같은 사용자 정의 관계에 적용될 수 있다.

- **Note**:<br>
  관계 필드는 `relations.py`에서 선언되지만 관습적으로는 `from rest_framework import serializer`를 사용해 `serializers` 모듈에서 불러온 후 `serializers.<FieldName>`으로 참조한다.

- **Note**: <br>
  REST Framework는 지나치게 마법 같을 것이므로 시리얼라이저로 전달된 queryset을 `selected_related`와 `prefetch_related`로 자동으로 최적화하려 하지 않는다. 원본 속성을 통해 orm 관계를 확장하는 필드를 가진 시리얼라이저는 데이터베이스로부터 관련 객체를 가져오기 위해 추가적인 데이터베이스 히트를 필요로 할 수 있다. 이러한 시리얼라이저를 사용하는 도중 발생할 수 있는 추가적인 데이터베이스 히트를 피하기 위해 쿼리를 최적화하는 것은 프로그래머의 책임이다.

  예를 들어, 다음의 시리얼라이저는 tracks 필드가 prefetch되지 않았다면 필드를 산출할 때마다 매번 데이터베이스 히트를 할 것이다.

  ```python
  class AlbumSerializer(serializers.ModelSerializer):
      tracks = serializers.SlugRelatedField(
          many=True,
          read_only=True,
          slug_field='title'
      )

      class Meta:
          model = Album
          fields = ['album_name', 'artist', 'tracks']

  # For each album object, tracks should be fetched from database
  qs = Album.objects.all()
  print(AlbumSerializer(qs, many=True).data)
  ```

  `AlbumSerializer`가 `many=True`를 가지고 있어 상당히 큰 queryset을 serialize하는데 사용된다면 심각한 성능 문제가 될 수 있다. `AlbumSeiralizer`로 전달되는 queryset을 다음과 같이 최적화하면 문제를 해결할 수 있다.

  ```python
  qs = Album.objects.prefetch_related('tracks')
  # No additional database hits required
  print(AlbumSerializer(qs, many=True).data)
  ```

### Inspecting relationships
`ModelSerializer` 클래스를 사용할 때 시리얼라이저 필드와 관계가 자동으로 생성된다. 이 자동생성된 필드를 살펴보는 것은 관계 스타일을 어떻게 커스터마이즈할 것인지 정하기 위한 유용한 도구가 될 수 있다.

그렇게 하려면 `python manage.py shell`을 사용해 Django shell을 열고 시리얼라이저를 불러온 후 인스턴스화하고 객체 표현을 출력한다.

```python
>>> from myapp.serializers import AccountSerializer
>>> serializer = AccountSerializer()
>>> print(repr(serializer))
AccountSerializer():
    id = IntegerField(label='ID', read_only=True)
    name = CharField(allow_blank=True, max_length=100, required=False)
    owner = PrimaryKeyRelatedField(queryset=User.objects.all())
```

# API Reference
관계 필드의 다양한 타입을 설명하기 위해 예시에서 여러 단순한 모델을 사용할 것이다. 모델은 음악 앨범과 각 앨범에 수록된 트랙들이다.

```python
class Album(models.Model):
    album_name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)


class Track(models.Model):
    album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    order = models.IntegerField()
    title = models.CharField(max_length=100)
    duration = models.IntegerField()

    class Meta:
        unique_together = ['album', 'order']
        ordering = ['order']

    def __str__(self):
        return '%d: %s' % (self.order, self.title)
```

## StringRelatedField
`StringRelatedField`는 `__str__` 메서드를 사용해 관계의 타겟을 나타내기 위해 사용된다.

예를 들어, 다음의 시리얼라이저는

```python
class AlbumSerializer(serializers.ModelSerializer):
    tracks = serializers.StringRelatedField(many=True)

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']
```

다음 표현으로 serialize된다.

```
{
    'album_name': 'Kid A',
    'artist': 'Radiohead',
    'tracks': [
        '1: Everything in its Right Place',
        '2: Kid A',
        '3: The National Anthem',
        ...
    ]
}
```

이 필드는 읽기 전용이다.

**Arguments**:
- `many`: ~대 다 관계에 적용된다면 이 인자를 `True`로 설정해야 한다.

## PrimaryKeyRelatedField
`PrimaryKeyRelatedField`는 기본키를 사용해 관계의 타겟을 표현하기 위해 사용된다.

예를 들어, 다음의 시리얼라이저는

```python
class AlbumSerializer(serializers.ModelSerializer):
    tracks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']
```

다음 표현으로 serialize된다.

```
{
    'album_name': 'This Is Acting',
    'artist': 'Sia',
    'tracks': [
        1,
        2,
        3,
        ...
    ]
}
```

`read_only` 플래그를 사용해 동작을 변경할 수 있지만, 기본적으로 이 필드는 읽기와 쓰기 전용이다.

**Arguments**:
- `queryset`<br>
  필드 입력의 유효성을 검사할 때 모델 인스턴스 검색을 위해 사용되는 queryset. 관계는 queryset을 명시적으로 설정하거나 `read_only=True`를 설정해야 한다.
- `many`<br>
  ~ 대 다 관계에 적용하려면 이 인자를 `True`로 설정해야 한다.
- `allow_null`<br>
  `True`로 설정하면 필드가 null값을 가질 수 있는 관계를 위해 `None`이나 빈 문자열을 허용하게 된다. 기본값은 `False`.
- `pk_field`<br>
  기본키 값의 serialization/deserialization을 제어하기 위해 필드를 설정한다. 예를 들어, `pk_field=UUIDField(format='hex')`는 UUID 기본키를 압축된 16진법 표현으로 serialize한다.

## HyperlinkedRelatedField
`HyperlinkedRelatedField`는 하이퍼링크를 이용해 관계의 타겟을 나타내기 위해 사용된다.

예를 들어, 다음의 시리얼라이저는

```python
class AlbumSerializer(serializers.ModelSerializer):
    tracks = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='track-detail'
    )

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']
```

다음 표현으로 serialize된다.

```
{
    'album_name': 'Born to Die',
    'artist': 'Lana Del Rey',
    'tracks': [
        'http://www.example.com/api/tracks/45/',
        'http://www.example.com/api/tracks/46/',
        'http://www.example.com/api/tracks/47/',
        ...
    ]
}
```

`read_only` 플래그를 사용해 동작을 변경할 수 있지만 기본적으로 이 필드는 읽기와 쓰기 전용이다.

- **Note**:<br>
  이 필드는 `lookup_field`와 `lookup_url_kwarg` 인자를 사용해 설정된 하나의 URL 키워드 인자를 수용하는 URL에 매핑되는 객체를 위해 설계되었다.

  URL의 일부로 하나의 기본키 또는 슬러그 인자를 포함하는 URL에 적합하다.

  만약 더 복잡한 하이퍼링크 표현을 필요로 한다면 아래의 [custom hyperlinked fields](https://github.com/lemon-lime-honey/TIL/blob/main/django/drf/serializer_relations.md#custom-hyperlinked-fields) 섹션에서 설명되어 있듯이 필드를 커스터마이즈해야 한다.

**Arguments**:
- `view_name`<br>
  관계 타겟으로 사용되는 뷰의 이름. [표준 라우터 클래스](https://www.django-rest-framework.org/api-guide/routers#defaultrouter)를 사용하고 있다면 `<modelname>-detail` 형식의 문자열이 된다. **필수**.
- `queryset`<br>
  필드 입력의 유효성을 검사할 때 모델 인스턴스 검색을 위해 사용되는 queryset. 관계는 queryset을 명시적으로 설정하거나 `read_only=True`를 설정해야 한다.
- `many`<br>
  ~ 대 다 관계에 적용하려면 이 인자를 `True`로 설정해야 한다.
- `allow_null`<br>
  `True`로 설정하면 필드가 null값을 가질 수 있는 관계를 위해 `None`이나 빈 문자열을 허용하게 된다. 기본값은 `False`.
- `lookup_field`<br>
  검색에 사용되어야 할 타겟이 있는 필드. 참조된 뷰의 URL 키워드 인자에 대응되어야 한다. 기본값은 `pk`.
- `lookup_url_kwarg`<br>
  검색 필드에 대응되는 URL 설정에서 정의된 키워드 인자의 이름. 기본값은 `lookup_field`와 같은 값을 사용하는 것이다.
- `format`<br>
  포맷 접미사를 사용하면 `format` 인자를 사용해 override 되지 않는 한 하이퍼링크된 필드가 타켓에 같은 포맷 접미사를 사용한다.

## SlugRelatedField
`SlugRelatedField`는 타겟의 필드를 이용해 관계의 타겟을 나타내는데 사용된다.

예를 들어, 다음의 시리얼라이저는

```python
class AlbumSerializer(serializers.ModelSerializer):
    tracks = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
    )

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']
```

다음 표현으로 serialize된다.

```
{
    'album_name': 'Tidal',
    'artist': 'Fiona Apple',
    'tracks': [
        'Sleep to Dream',
        'Sullen Girl',
        'Shadowboxer',
        ...
    ]
}
```

`read_only` 플래그를 사용해 동작을 변경할 수 있지만 기본적으로 이 필드는 읽기와 쓰기 전용이다.

`SlugRelatedField`를 읽기-쓰기 필드로 사용할 때 보통은 슬러그 필드가 `unique=True`로 모델 필드와 대응되는 것을 확실하게 한다.

**Arguments**:
- `slug_field`<br>
  타겟을 나타내기 위해 사용되는 타겟의 필드. 주어진 인스턴스를 개별적으로 식별할 수 있는 필드여야 한다. 예를 들면 `username`. **필수**.
- `queryset`<br>
  필드 입력의 유효성을 검사할 때 모델 인스턴스 검색을 위해 사용되는 queryset. 관계는 queryset을 명시적으로 설정하거나 `read_only=True`를 설정해야 한다.
- `many`<br>
  ~ 대 다 관계에 적용하려면 이 인자를 `True`로 설정해야 한다.
- `allow_null`<br>
  `True`로 설정하면 필드가 null값을 가질 수 있는 관계를 위해 `None`이나 빈 문자열을 허용하게 된다. 기본값은 `False`.

## HyperlinkedIdentityField
이 필드는 HyperlinkedModelSerializer의 `'url'`필드와 같이 identity 관계로 적용될 수 있다. 객체의 속성을 위해 사용될 수도 있다. 예를 들어, 다음의 시리얼라이저는

```python
class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    track_listing = serializers.HyperlinkedIdentityField(view_name='track-list')

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'track_listing']
```

다음 표현으로 serialize된다.

```
{
    'album_name': 'Eat to the Beat',
    'artist': 'Blondie',
    'track_listing': 'http://www.example.com/api/track_list/12/',
}
```

이 필드는 언제나 읽기 전용이다.

**Arguments**:
- `view_name`<br>
  관계 타겟으로 사용되는 뷰의 이름. [표준 라우터 클래스](https://www.django-rest-framework.org/api-guide/routers#defaultrouter)를 사용하고 있다면 `<modelname>-detail` 형식의 문자열이 된다. **필수**.
- `lookup_field`<br>
  검색에 사용되어야 할 타겟이 있는 필드. 참조된 뷰의 URL 키워드 인자에 대응되어야 한다. 기본값은 `pk`.
- `lookup_url_kwarg`<br>
  검색 필드에 대응되는 URL 설정에서 정의된 키워드 인자의 이름. 기본값은 `lookup_field`와 같은 값을 사용하는 것이다.
- `format`<br>
  포맷 접미사를 사용하면 `format` 인자를 사용해 override 되지 않는 한 하이퍼링크된 필드가 타켓에 같은 포맷 접미사를 사용한다.