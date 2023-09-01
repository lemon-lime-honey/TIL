# [Internationalization](https://www.django-rest-framework.org/topics/internationalization/)
```
국제화 지원은 선택이 아니다. 주요 특징이어야 한다.
- Jannis Leidel, speaking at Django Under the Hood, 2015
```

REST framework는 번역 가능한 오류 메시지를 제공한다. [Django의 표준 번역 메커니즘](https://docs.djangoproject.com/en/stable/topics/i18n/translation) 사용을 설정하여 영어 이외의 언어로 나타나게 할 수 있다.

이렇게 하면:

- Django 설정의 표준 `LANGUAGE_CODE`를 사용하여 영어 이외의 다른 언어를 기본으로 선택할 수 있다.
- Django에 포함된 `LocaleMiddleware`를 사용하여 클라이언트가 언어를 선택할 수 있게 한다. API 클라이언트를 위한 일반적인 사용법은 `Accept-Language` 요청 헤더를 포함하는 것이다.

## Enabling internationalized APIs
표준 Django `LANGUAGE_CODE` 설정을 사용하여 기본 언어를 변경할 수 있다:

```python
LANGUAGE_CODE = "ko-kr"
```

`MIDDLEWARE` 설정에 `LocalMiddleware`을 추가하여 요청별 언어 요청을 설정할 수 있다:

```python
MIDDLEWARE = [
    ...
    'django.middleware.locale.LocaleMiddleware'
]
```

요청별 국제화가 설정될 경우, 클라이언트 요청은 가능한 경우 `Accept-Language` 헤더를 존중한다. 예를 들어: 지원되지 않는 미디어 타입에 대한 요청을 생성해보자:

**Request**
```
GET /api/users HTTP/1.1
Accept: application/xml
Accept-Language: ko-kr
Host: example.org
```

**Response**
```
HTTP/1.0 406 NOT ACCEPTABLE

{"detail": "Accept header 요청을 만족할 수 없습니다."}
```

REST framework는 표준 예외 케이스와 시리얼라이저 유효성 검사 오류를 위해 이러한 빌트인 번역을 포함한다.

번역이 오류 문자열 자체에만 적용된다는 점에 유의한다. 오류 메시지의 포맷과 필드 이름 키는 그대로 유지된다. 다음은 `400 Bad Request` 응답 바디의 예시이다:

```
{"detail": {"username": ["이 필드는 반드시 고유(unique)해야 합니다."]}}
```

`detail`과 `non_field_errors`와 같은 응답의 일부에 다른 문자열을 사용하고 싶다면 [사용자 정의 예외 처리](../api-guide/exceptions.md/#custom-exception-handling)를 사용하여 이 동작을 변경할 수 있다.

### Specifying the set of supported languages
기본적으로 모든 사용 가능한 언어가 지원된다.

Django의 표준 `LANGUAGE` 설정을 사용하여 사용 가능한 언어 중 일부만 지원하게 할 수도 있다:

```python
LANGUAGES = [
    ('ko', _('Korean')),
    ('en', _('English')),
]
```

## Adding new translations
REST framework 번역은 [Transifex](https://www.transifex.com/projects/p/django-rest-framework/)를 사용하여 온라인으로 관리된다. 새로운 언어 번역을 추가하기 위해 Transifex 서비스를 이용할 수 있다. 그러면 정비 팀이 이러한 번역 문자열이 REST framework 패키지에 포함되도록 할 것이다.

때로 프로젝트에 번역 문자열을 로컬로 추가해야 하는 경우가 있다. 이런 경우 그렇게 해야 한다:

- Transifex에서 번역되지 않은 언어로 REST framework를 사용하고 싶은 경우
- 프로젝트가 REST framework의 기본 번역 문자열에 포함되지 않은 사용자 정의 오류 메시지를 포함하는 경우

### Translating a new language locally
이 가이드는 사용자가 이미 Django 애플리케이션을 번역하는데 익숙하다고 간주한다. 그렇지 않다면 [Django의 번역 문서](https://docs.djangoproject.com/en/stable/topics/i18n/translation)를 먼저 본다.

새로운 언어로 번역한다면 이미 존재하는 REST framework 오류 메시지를 번역해야 한다:

1. 국제화 리소스를 저장하고 싶은 곳에 새 폴더를 생성한다. 이 경로를 `LOCALE_PATHS` 설정에 추가한다.
2. 번역하려는 언어를 위한 하위 폴더를 생성한다. 이 폴더는 [로케일 이름](https://docs.djangoproject.com/en/stable/topics/i18n/#term-locale-name) 규칙을 사용해 명명되어야 한다. 예를 들어: `de`, `pt_BR`, `es_AR`
3. REST framework 소스 코드에서 [기본 번역 파일](https://raw.githubusercontent.com/encode/django-rest-framework/master/rest_framework/locale/en_US/LC_MESSAGES/django.po)을 번역 폴더로 복사한다.
4. 복사한 `django.po` 파일을 수정해 모든 오류 메시지를 번역한다.
5. Django가 사용할 수 있는 번역을 생성하기 위해 `manage.py compilemessages -l ko_KR`을 실행한다. `processing file django.po in <...>/locale/ko_KR/LC_MESSAGES`와 같은 메시지가 나타나야 한다.
6. 변경사항을 반영하기 위해 개발 서버를 재시작한다.

프로젝트 코드베이스에 존재하는 사용자 정의 오류 메시지를 번역한다면 REST framework 소스 `django.po` 파일을 `LOCALE_PATHS` 폴더에 복사하는 대신 단순히 Django의 표준 `makemessages` 프로세스를 실행한다.

### How the language is determined
요청별 언어 선택을 허용하고 싶다면 `MIDDLEWARE` 설정에 `django.middleware.locale.LocaleMiddleware`를 포함해야 한다.

[Django 문서](https://docs.djangoproject.com/en/stable/topics/i18n/translation/#how-django-discovers-language-preference)에서 언어 선택이 어떻게 결정되는지에 대한 더 많은 정보를 확인할 수 있다. 참고로, 방법은 다음과 같다:

1. 먼저 요청된 URL에서 언어 접두사를 찾는다.
2. 실패하면 현재 사용자의 세션에서 `LANGUAGE_SESSION_KEY`를 찾는다.
3. 실패하면 쿠키를 찾는다.
4. 실패하면 `Accept-Language` HTTP 헤더를 확인한다.
5. 실패하면 전역 `LANGUAGE_CODE` 설정을 사용한다.

API 클라이언트의 경우 일반적으로 `Accept-Language` 헤더를 사용하는 것이 가장 적절하다. 세션과 쿠키는 세션 인증을 사용하지 않는 한 사용할 수 없으며, 일반적으로 언어 URL 접두사를 사용하는 것보다 `Accept-Language` 헤더를 선호하는 것이 더 좋은 관습이다.