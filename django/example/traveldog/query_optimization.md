# app 'accounts'
```python
# function profile

# 회원정보 상세페이지의 회원 정보 가져오기
# 회원정보 상세페이지는 세 탭, '사용자 작성 리뷰'/'북마크'/'좋아요를 누른 리뷰'를 가진다
person = get_user_model().objects.prefetch_related('bookmarked_places', 'user_reviews', 'like_reviews').get(username=username)

# 사용자 작성 리뷰
# 장소와 일대다 관계인 사진까지 가져와야 한다
# place__photos
my_reviews = Review.objects.filter(user=person).prefetch_related('place', 'place__photos', 'like')

# 북마크
bookmark_places = Place.objects.prefetch_related('bookmark', 'photos', 'place_reviews').filter(bookmark=person)

# 좋아요를 누른 리뷰
# 리뷰에 해당하는 장소와 그 장소의 사진도 가져와야 한다
reviews_like = Review.objects.filter(like=person).prefetch_related('place', 'user', 'like', 'place__photos')

# 북마크 탭에서 표시되는 장소별 별점 평균
raw_star = bookmark_places.annotate(avg_star=Avg('place_reviews__star'))
stars = raw_star.values('id').annotate(avg_star=Avg('place_reviews__star'))
```

# app 'places'
## function index
```python
# 장소와 사진, 장소별 리뷰, 북마크
places = Place.objects.prefetch_related('photos', 'place_reviews', 'bookmark').all()

# 장소별 별점
raw_star = Review.objects.annotate(avg_star=Avg('star'))
stars = raw_star.values('place').annotate(avg_star=Avg('star'))
```

## function detail
```python
# 장소의 사진과 북마크
place = Place.objects.prefetch_related('photos', 'bookmark').get(pk=place_pk)

# 리뷰 좋아요와 리뷰 작성자
reviews = Review.objects.prefetch_related('like', 'user').filter(place=place).order_by('-pk')
```