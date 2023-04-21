# 비동기 요청
## Ajax
- 비동기적인 웹 애플리케이션 개발을 위한 프로그래밍 기술
- 사용자의 요청에 대한 즉각적인 반응을 제공하면서 페이지 전체를 다시 로드하지 않고 필요한 부분만 업데이트 하는 것을 목표로 한다.

## XMLHTTPRequest
- 클라이언트와 서버 간에 데이터를 비동기적으로 주고받을 수 있도록 해주는 JavaScript 객체
- JavaScript 코드에서 서버에 요청을 보내고 서버로부터 응답을 받을 수 있다.

## Axios
- JavaScript에서 HTTP 요청을 보내는 라이브러리
- 주로 프론트엔드 프레임워크에서 사용한다.

### Axios 기본 문법
```javascript
axios({
  method: 'HTTP 메서드',
  url: '요청 URL',
})
  .then(/* 성공하면 수행할 콜백함수 */)
  .catch(/* 실패하면 수행할 콜백함수 */)
```
- `get`, `post` 등 여러 메서드 사용가능
- `then`을 이용해 성공하면 수행할 로직을 작성한다.
- `catch`를 이용해 실패하면 수행할 로직을 작성한다.
<br><br>

# Follow with Ajax
```html
<!-- accounts/profile.html -->

<div>
  팔로잉 : <span id="followings-count">{{ person.followings.all|length }}</span> / 
  팔로워 : <span id="followers-count">{{ person.followers.all|length }}</span>
</div>

{% if request.user != person %}
  <div>
    <form id="follow-form" data-user-id="{{ person.pk }}">
      {% csrf_token %}
      {% if request.user in person.followers.all %}
        <input type="submit" value="언팔로우">
      {% else %}
        <input type="submit" value="팔로우">
      {% endif %}
    </form>
  </div>
{% endif %}
```
```javascript
// JS
// html body 하단에 axios CDN 작성

const form = document.querySelector('#follow-form')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

form.addEventListener('submit', function (event) {
  event.preventDefault()
  const userId = event.target.dataset.userId
  
  axios({
    method: 'post',
    url: `/accounts/${userId}/follow/`,
    headers: {'X-CSRFToken': csrftoken},
  })
    .then((response) => {
      const isFollowed = response.data.is_followed
      const followBtn = document.querySelector('#follow-form > input[type=submit]')

      if (isFollowed === true) {
        followBtn.value = '언팔로우'
      } else {
        followBtn.value = '팔로우'
      }

      const followingCountTag = document.querySelector('#followings-count')
      const followerCountTag = document.querySelector('#followers-count')

      const followingsCountData = response.data.followings_count
      const followersCountData = response.data.followers_count

      followingCountTag.textContent = followingsCountData
      followerCountTag.textContent = followersCountData
    })
})
```
```python
# accounts/views.py

from django.http import JsonResponse

@login_required
def follow(request, user_pk):
    User = get_user_model()
    you = User.objects.get(pk=user_pk)
    me = request.user

    if you != me:
        if me in you.followers.all():
            you.followers.remove(me)
            is_followed = False
        else:
            you.followers.add(me)
            is_followed = True
        context = {
            'is_followed': is_followed,
            'followings_count': you.followings.count(),
            'followers_count': you.followers.count(),
        }
        return JsonResponse(context)
    return redirect('accounts:profile', you.username)
```
<br><br>

# Like with Ajax
```html
<!-- articles/index.html -->

<form class="like-forms" data-article-id="{{ article.pk }}">
  {% csrf_token %}
  {% if request.user in article.like_users.all %}
    <input type="submit" value="좋아요 취소" id="like-{{ article.pk }}">
  {% else %}
    <input type="submit" value="좋아요" id="like-{{ article.pk }}">
  {% endif %}
</form>
```
```javascript
// JS

const forms = document.querySelectorAll('.like-forms')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

forms.forEach((form) => {
  form.addEventListener('submit', function (event) {
    event.preventDefault()    
    const articleId = event.target.dataset.articleId
    axios({
      method: 'post',
      url: `/articles/${articleId}/likes/`,
      headers: {'X-CSRFToken': csrftoken},
    })
      .then((response) => {        
        const isLiked = response.data.is_liked        
        const likeBtn = document.querySelector(`#like-${articleId}`)
        if (isLiked === true) {
          likeBtn.value = '좋아요 취소'
        } else {
          likeBtn.value = '좋아요'
        }
      })
      .catch((error) => {
        console.log(error.response)
      })
  })
})
```
```python
# articles/views.py

from django.http import JsonResponse

@login_required
def likes(request, article_pk):
    article = Article.objects.get(pk=article_pk)

    if request.user in article.like_users.all():
        article.like_users.remove(request.user)
        is_liked = False
    else:
        article.like_users.add(request.user)
        is_liked = True
    context = {
        'is_liked': is_liked,
    }
    return JsonResponse(context)
```