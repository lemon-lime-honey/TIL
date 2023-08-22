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

  만약 더 복잡한 하이퍼링크 표현을 필요로 한다면 아래의 [custom hyperlinked fields](serializer_relations.md/#custom-hyperlinked-fields) 섹션에서 설명되어 있듯이 필드를 커스터마이즈해야 한다.

**Arguments**:
- `view_name`<br>
  관계 타겟으로 사용되는 뷰의 이름. [표준 라우터 클래스](routers.md/#defaultrouter)를 사용하고 있다면 `<modelname>-detail` 형식의 문자열이 된다. **필수**.
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
  관계 타겟으로 사용되는 뷰의 이름. [표준 라우터 클래스](routers.md/#defaultrouter)를 사용하고 있다면 `<modelname>-detail` 형식의 문자열이 된다. **필수**.
- `lookup_field`<br>
  검색에 사용되어야 할 타겟이 있는 필드. 참조된 뷰의 URL 키워드 인자에 대응되어야 한다. 기본값은 `pk`.
- `lookup_url_kwarg`<br>
  검색 필드에 대응되는 URL 설정에서 정의된 키워드 인자의 이름. 기본값은 `lookup_field`와 같은 값을 사용하는 것이다.
- `format`<br>
  포맷 접미사를 사용하면 `format` 인자를 사용해 override 되지 않는 한 하이퍼링크된 필드가 타켓에 같은 포맷 접미사를 사용한다.

# Nested relationships
이전에 논의한 다른 엔터티에 관한 *참조*와는 달리, 참조된 엔터티는 그 엔터티를 참조하는 객체 표현에 포함되거나 *중첩*될 수 있다. 그러한 중첩된 관계는 필드로 시리얼라이저를 사용하여 표현될 수 있다.

필드가 ~ 대 다 관계를 표현하기 위해 사용된다면 시리얼라이저 필드에 `many=True` 플래그를 추가해야 한다.

## Example
예를 들어, 다음의 시리얼라이저는

```python
class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['order', 'title', 'duration']

class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']
```

다음의 중첩된 표현으로 serialize될 수 있다.

```python
>>> album = Album.objects.create(album_name='In Rainbows', artist='Radiohead')
>>> Track.objects.create(album=album, order=1, title='15 Step', duration=238)
<Track: Track object>
>>> Track.objects.create(album=album, order=2, title='Bodysnatchers', duration=242)
<Track: Track object>
>>> Track.objects.create(album=album, order=3, title='Nude', duration=255)
<Track: Track object>
>>> serializer = AlbumSerializer(instance=album)
>>> serializer.data
{
    'album_name': 'In Rainbows',
    'artist': 'Radiohead',
    'tracks': [
        {'order': 1, 'title': '15 Step', 'duration': 238},
        {'order': 2, 'title': 'Bodysnatchers', 'duration': 242},
        {'order': 3, 'title': 'Nude', 'duration': 255},
        ...
    ]
}
```

## Writable nested serializers
기본적으로 중첩된 시리얼라이저는 읽기 전용이다. 중첩된 시리얼라이저 필드에 쓰기 연산을 지원하고 싶다면 어떻게 자식 관계가 저장되는지를 명시적으로 구체화하기 위해 `create()` 그리고/또는 `update()` 메서드를 생성해야 한다.

```python
class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['order', 'title', 'duration']


class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True)

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']

    def create(self, validated_data):
        track_data = validated_data.pop('tracks')
        album = Album.objects.create(**validated_data)
        for track_data in tracks_data:
            Track.objects.create(album=album, **track_data)
        return album

>>> data = {
    'album_name': 'In Rainbows',
    'artist': 'Radiohead',
    'tracks': [
        {'order': 1, 'title': '15 Step', 'duration': 238},
        {'order': 2, 'title': 'Bodysnatchers', 'duration': 242},
        {'order': 3, 'title': 'Nude', 'duration': 255},
        ...
    ]
}
>>> serializer = AlbumSerializer(data=data)
>>> serializer.is_valid()
True
>>> serializer.save()
<Album: Album object>
```

# Custom relational fields
이미 존재하는 관계 스타일 중 필요로 하는 표현에 맞는 것이 없는 경우 모델 인스턴스로부터 출력 표현이 정확히 어떻게 생성되는지를 설명하는 사용자 정의 관계 필드를 구현할 수 있다.

사용자 정의 필드를 구현하기 위해서는 `RelatedField`를 override해야 하고, `.to_representation(self, value)` 메서드를 구현해야 한다. 이 메서드는 필드의 타겟을 `value` 인자로 가지고, 타겟을 serialize하기 위해 사용되어야 할 표현을 반환한다. `value` 인자는 보통 모델 인스턴스이다.

읽기-쓰기 관계 필드를 구현해야 한다면 [`.to_internal_value(self, data)` 메서드](serializers.md/#to_internal_valueself-data)를 구현해야 한다.

`context`에 기반한 동적 queryset을 제공하려면 클래스에서 혹은 필드를 초기화할 때 `.queryset`을 구체화하는 대신 `.get_queryset(self)`를 override하면 된다.

## Example
예를 들어, 트랙을 그 순서, 제목, 그리고 시간을 사용한 사용자 정의 문자열 표현으로 serialize하기 위한 관계 필드를 정의할 수 있다.

```python
import time

class TrackListingField(serializers.RelatedField):
    def to_representation(self, value):
        duration = time.strftime('%M:%S', time.gmtime(value.duration))
        return 'Track %d: %s (%s)' % (value.order, value.name, duration)

class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackListingField(many=True)

    class Meta:
        model = Album
        fields = ['album_name', 'artist', 'tracks']
```

이 사용자 정의 필드는 다음 표현으로 serialize된다.

```
{
    'album_name': 'In Rainbows',
    'artist': 'Radiohead',
    'tracks': [
        'Track 1: 15 Step (3:58)',
        'Track 2: Bodysnatchers (4:02)',
        'Track 3: Nude (4:15)',
        ...
    ]
}
```

# Custom hyperlinked fields
하나보다 많은 탐색 필드를 필요로 하는 URL을 표현하기 위해 하이퍼링크된 필드의 동작을 커스터마이즈해야 하는 경우가 있다.

`HyperlinkedRelatedField`를 override하여 구현할 수 있다. 다음은 Override해야 할 두 메서드이다.

#### get_url(self, obj, view_name, request, format)
`get_url` 메서드는 객체 인스턴스를 URL 표현으로 매핑하는데 사용된다.

`view_name`과 `lookup_field` 속성이 URL 설정에 정확히 맞지 않게 제공된다면 `NoReverseMatch`를 발생시킨다.

#### get_object(self, view_name, view_args, view_kwargs)
쓰기 가능한 하이퍼링크된 필드를 지원하고 싶다면 들어오는 URL을 대표하는 객체로 다시 매핑하기 위해 `get_object`를 override한다. 읽기 전용인 하이퍼링크된 필드는 이 메서드를 override할 필요가 없다.

이 메서드의 반환값은 매치된 URL 설정 인자에 대응되는 객체이다.

`ObjectDoesNotExist` 예외를 발생시킬 수 있다.

## Example
다음과 같이 두 개의 키워드 인자를 가지는 고객 객체를 위한 URL이 있다고 하자.

```
/api/<organization_slug>/customers/<customer_pk>/
```

이것은 하나의 검색 필드만을 수용하는 기본 구현으로는 표현될 수 없다.

이 경우 원하는 동작을 얻기 위해 `HyperlinkedRelatedField`를 override해야 한다.

```python
from rest_framework import serializers
from rest_framework.reverse import reverse

class CustomerHyperlink(serializers.HyperlinkedRelatedField):
    # We define these as class attributes, so we don't need to pass them as arguments.
    view_name = 'customer-detail'
    queryset = Customer.objects.all()

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'organization_slug': obj.organization.slug,
            'customer_pk': obj.pk
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
            'organization__slug': view_kwargs['organization_slug'],
            'pk': view_kwargs['customer_pk']
        }
        return self.get_queryset().get(**lookup_kwargs)
```

이 스타일을 제네릭 뷰와 함께 사용하고 싶다면 탐색이 올바르게 동작하도록 뷰의 `.get_object`를 override해야 한다.

보통 가능하면 API 표현에 납작한 스타일을 권장하지만, 적절히 사용된다면 중첩된 URL 스타일 또한 타당하다.

# Further notes
## The `queryset` argument
`queryset` 인자는 *쓰기 가능한* 관계 필드에서만 필요로 하는데, 이 경우 가공되지 않은 사용자 입력을 모델 인스턴스로 매핑하는 모델 인스턴스 탐색을 수행하는데 사용된다.

버전 2.x에서는 `ModelSerializer` 클래스가 사용되는 *경우* *간혹* 시리얼라이저 클래스가 자동으로 `queryset` 인자를 결정했다.

이 동작은 이제 쓰기 가능한 관계 필드에서 명시적인 `queryset` 인자를 *언제나* 사용하는 것으로 대체되었다.

그렇게 하면 `ModelSerializer`가 제공하는 숨겨진 '마법'의 양이 줄어들어 필드의 동작을 더 투명하게 되고, `ModelSerializer` 지름길을 사용하거나 완전히 명시적인 `Serializer` 클래스를 사용하는 것은 사소한 일이라는 걸 보장한다.

## Customizing the HTML display
모델의 빌트인 `__str__` 메서드는 `choices` 속성을 채우기 위해 사용되는 객체의 문자열 표현을 생성하는데 사용된다. 이 선택지는 브라우징 가능한 API의 select HTML 입력을 채우는데 사용된다.

그런 입력에 사용자 정의 표현을 제공하려면, `RelatedField` 서브클래스의 `display_value()`를 override한다. 이 메서드는 모델 객체를 받아 그것을 표현하기에 적절한 문자열을 반환한다. 예를 들면:

```python
class TrackPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def display_value(self, instance):
        return 'Track %s' % (instance.title)
```

## Select field cutoffs
브라우징 가능한 API에서 렌더링될 때, 관계 필드는 최대 1000개까지의 선택지를 표시한다. 만약 더 많은 선택지가 있다면 "More than 1000 items..."인 선택 불가능한 옵션이 나타날 것이다.

이 동작은 템플릿이 매우 큰 양의 관계가 보이는 것 때문에 수용 가능한 시간 내에 렌더링하는 것이 불가능해지는 것을 방지하는 것을 의도한다.

이 동작을 제어하기 위해 사용할 수 있는 두 개의 키워드 인자가 있다.

- `html_cutoff`<br>
  설정하면 HTML select 드롭다운에 표시되는 선택지의 최대 개수가 된다. 제한을 없애려면 `None`으로 설정한다. 기본값은 `1000`.
- `html_cutoff_text`<br>
  설정하면 HTML select 드롭다운에서 최대 개수보다 많은 선택지가 있어 생략되는 경우 텍스트 알림이 된다. 기본값은 `"More than {count} items..."`.

전역적으로 `HTML_SELECT_CUTOFF`와 `HTML_SELECT_CUTOFF_TEXT` 설정을 사용해 제어할 수도 있다.

생략이 강제되는 경우 HTML 폼에서 단순한 입력 필드를 대신 사용할 수 있다. `style` 키워드 인자를 사용하면 된다. 예를 들어:

```python
assigned_to = serializers.SlugRelatedField(
    queryset=User.objects.all(),
    slug_field='username',
    style={'base_template': 'input.html'}
)
```

## Reverse relations
역관계는 `ModelSerializer`와 `HyperlinkedModelSerializer`에 의해 자동으로 유도되지 않는다는 점에 유의한다. 역관계를 포함하려면 필드 목록에 명시적으로 추가해야 한다. 예를 들어:

```python
class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['tracks', ...]
```

보통 관계에 적절한 `related_name`을 설정하는 것을 보장하기 위해 필드 이름을 사용한다. 예를 들어:

```python
class Track(models.Model):
    album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    ...
```

역관계에 관계명을 설정하지 않으면 `fields` 인자에 있는 자동으로 생성된 관계명을 사용해야 한다. 예를 들면:

```python
class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['track_set', ...]
```

더 많은 정보는 [역관계](https://docs.djangoproject.com/en/stable/topics/db/queries/#following-relationships-backward)에 관한 Django 공식문서에서 확인할 수 있다.

## Generic relationships
제네릭 외래키를 serialize하고 싶다면 관계의 타겟을 어떻게 serialize하는지 명시적으로 결정하기 위해 사용자 정의 필드를 정의해야 한다.

다음은 다른 임의의 모델과 제네릭한 관계를 가진 태그를 위한 모델의 예시이다.

```python
class TaggedItem(models.Model):
    """
    Tags arbitrary model instances using a generic relation.

    See: https://docs.djangoproject.com/en/stable/ref/contrib/contenttypes/
    """
    tag_name = models.SlugField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    tagged_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.tag_name
```

그리고 다음은 연관된 태그를 가지는 두 모델이다.

```python
class Bookmark(models.Model):
    """
    A bookmark consists of a URL, and 0 or more descriptive tags.
    """
    url = models.URLField()
    tags = GenericRelation(TaggedItem)


class Note(models.Model):
    """
    A note consists of some text, and 0 or more descriptive tags.
    """
    text = models.CharField(max_length=1000)
    tags = GenericRelation(TaggedItem)
```

어떻게 serialize될 것인지를 결정하기 위해 각 인스턴스의 타입을 사용해 태그된 인스턴스를 serialize하기 위해 사용되는 사용자 정의 필드를 정의한다.

```python
class TaggedObjectRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `tagged_object` generic relationship.
    """

    def to_representation(self, value):
        """
        Serialize tagged objects to a simple textual representation.
        """
        if isinstance(value, Bookmark):
            return 'Bookmark: ' + value.url
        elif isinstance(value, Note):
            return 'Note: ' + value.text
        raise Exception('Unexpected type of tagged object')
```

관계의 타겟이 중첩된 표현을 가진다면 `.to_representation` 메서드 안에서 필요한 시리얼라이저를 사용한다.

```python
def to_representation(self, value):
    """
    Serialize bookmark instances using a bookmark serializer,
    and note instances using a note serializer.
    """
    if isinstance(value, Bookmark):
        serializer = BookmarkSerializer(value)
    elif isinstance(value, Note):
        serializer = NoteSerializer(value)
    else:
        raise Exception('Unexpected type of tagged object')
    return serializer.data
```

관계 안의 타겟의 타입이 언제나 알려져 있기 때문에 `GenericRelation` 필드를 사용해 표현되는 역 제네릭 키가 일반적인 관계 필드 타입을 사용해 serialize될 수 있다는 점에 유의한다.

더 많은 정보는 [제네릭한 관계에 관한 Django 공식문서](https://docs.djangoproject.com/en/stable/ref/contrib/contenttypes/#id1)에서 확인한다.

## ManyToManyFields with a Through Model
기본적으로, `through` 모델로 구체화된 `ManyToManyField`를 목적으로 하는 관계 필드는 읽기 전용으로 설정된다.

through 모델을 사용한 `ManyToManyField`를 가리키는 관계 필드를 명시적으로 구체화하고 싶다면 `read_only`를 `True`로 설정해야 한다.

[through 모델인 추가 필드](https://docs.djangoproject.com/en/stable/topics/db/models/#intermediary-manytomany)를 표현하고 싶다면 through 모델을 [중첩된 객체](serializers.md/#dealing-with-nested-objects)로 serialize한다.

# Third Party Packages
다음의 서드파티 패키지를 사용할 수 있다.

## DRF Nested Routers
[drf-nested-routers](https://github.com/alanjds/drf-nested-routers) 패키지는 중첩된 요소를 다루기 위한 라우터와 관계 필드를 제공한다.

# Rest Framework Generic Relations
[rest-framework-generic-relations](https://github.com/Ian-Foote/rest-framework-generic-relations) 라이브러리는 제네릭한 외래키를 위한 읽기/쓰기 serialization을 제공한다.