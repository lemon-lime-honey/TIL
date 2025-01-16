# String Examination

<details>

<summary><h2><code>strlen</code>, <code>strlen_s</code></h2></summary>

- `size_t strlen(const char* str);`
  - 주어진 null 종결 바이트 문자열의 길이를 반환함
  - 길이는 문자 배열에서 `str`가 가리키는 첫 원소부터 처음으로 등장하는 null 문자 직전까지의 문자 개수를 의미함
  - `str`이 null 종결 바이트 문자열을 가리키지 않는다면 동작의 결과를 예측할 수 없음
- `size_t strlen_s(const char* str, size_t strsz);` (C11부터)
  - `str`이 null 포인터일 때 0을 반환, `str`의 첫 `strsz` 바이트에서 null 문자를 발견하지 못했을 때 `strsz`를 반환한다는 점을 제외하면 `strlen`과 같음
  - `str`이 null 종결 문자열을 가리키지 않거나 `strsz`가 문자 배열의 크기보다 크다면 동작의 결과를 예측할 수 없음
  - 모든 bounds-checked 함수처럼, `strlen` 는 구현에 의해 `__STDC_LIB_EXT1__`이 정의되어 있거나 사용자가 `<string.h>` 을 include하기 전에 `__STDC_WANT_LIB_EXT1__` 을 1로 정의할 때 동작함

### 파라미터

- `str`: 검사할 null 종결 문자열을 가리키는 포인터
- `strsz`: 검사할 문자의 최대 개수

### 반환값

1. null 종결 문자열 `str`의 길이
2. 성공했을 때 null 종결 문자열 `str`의 길이, `str`이 null 포인터일 때 0, null 문자를 발견하지 못했을 때 `strsz`

### 참고

- `strnlen_s`와 `wcsnlen_s`는 runtime contraint 핸들러를 호출하지 않는 유이한 [bounds checked 함수](https://en.cppreference.com/w/c/error)
- null 종결이 아닌 문자열을 위한 제한적인 지원을 제공하는데 사용되는 순수한 유틸리티 함수들

### 예시

```c
#define __STDC_WANT_LIB_EXT1__ 1
#include <stdio.h>
#include <string.h>

int main(void) {
  const char str[] = "How many characters does this string contain?";

  printf("without null character: %zu\n", strlen(str));
  printf("with null character:    %zu\n", sizeof(str));

#ifdef __STDC_LIB_EXT1__
  printf("without null character: %zu\n", strnlen_s(str, sizeof str));
#endif
}
```

출력:

```text
without null character: 45
with null character:    46
without null character: 45
```

</details>

<details>

<summary><h2><code>strcmp</code></h2></summary>

- `int strcpm(const char* lhs, const char* rhs);`
  - 두 개의 null 종결 바이트 문자열을 사전순으로 비교
  - 결과의 부호는 비교하는 두 문자열에서 처음으로 차이가 발생하는 쌍(둘 모두 `unsigned char`형으로 간주)의 값 차이의 부호와 같음
  - `lhs` 또는 `rhs`가 null 종결 바이트 문자열을 가리키는 포인터가 아니라면 결과를 예측할 수 없음

### 파라미터

`lhs`, `rhs`: 비교할 null 종결 바이트 문자열을 가리키는 포인터

### 반환값

- 사전순으로 `lhs` 가 `rhs` 보다 먼저 등장할 때 음수
- `lhs` 와 `rhs` 가 같으면 0
- 사전순으로 `lhs` 가 `rhs` 보다 늦게 등장할 때 양수

### 참고

이 함수는 [`strcoll`](https://en.cppreference.com/w/c/string/byte/strcoll)과 [`strxfrm`](https://en.cppreference.com/w/c/string/byte/strxfrm)과는 달리 로케일을 구분하지 않음

### 예시

```c
#include <stdio.h>
#include <string.h>

void demo(const char* lhs, const char* rhs) {
  const int rc = strcmp(lhs, rhs);
  const char* rel = rc < 0 ? "precedes" : rc > 0 ? "follows" : "equals";
  printf("[%s] %s [%s]\n", lhs, rel, rhs);
}

int main(void) {
  const char* string = "Hello World!";
  demo(string, "Hello!");
  demo(string, "Hello");
  demo(string, "Hello there");
  demo("Hello, everybody!" + 12, "Hello, somebody" + 11);
}
```

출력:

```text
[Hello World!] precedes [Hello!]
[Hello World!] follows [Hello]
[Hello World!] precedes [Hello there]
[body!] equals [body!]
```

</details>

<details>

<summary><h2><code>strncmp</code></h2></summary>

- `int strncmp(const char* lhs, const char* rhs, size_t count);`
  - 두 개의 null 종결일 수 있는 배열의 최대 `count` 개의 문자 비교
  - 비교는 사전순으로 이루어짐
  - null 문자열 이후의 문자는 비교되지 않음
  - 결과의 부호는 비교하는 두 문자열에서 처음으로 차이가 발생하는 쌍(둘 모두 `unsigned char`형으로 간주)의 값 차이의 부호와 같음
  - `lhs` 또는 `rhs` 배열 마지막을 지나 접근이 발생하거나 `lhs` 또는 `rhs`가 null 종결 바이트 문자열을 가리키는 포인터가 아니라면 결과를 예측할 수 없음

### 파라미터

- `lhs`, `rhs`: 비교할 null 종결일 수도 있는 배열을 가리키는 포인터
- `count`: 비교할 최대 문자 수

### 반환값

- 사전순으로 `lhs` 가 `rhs` 보다 먼저 등장할 때 음수
- `lhs` 와 `rhs` 가 같으면 0
- 사전순으로 `lhs` 가 `rhs` 보다 늦게 등장할 때 양수

### 참고

이 함수는 [`strcoll`](https://en.cppreference.com/w/c/string/byte/strcoll)과 [`strxfrm`](https://en.cppreference.com/w/c/string/byte/strxfrm)과는 달리 로케일을 구분하지 않음

### 예시

```c
#include <stdio.h>
#include <string.h>

void demo(const char* lhs, const char* rhs, int sz) {
  const int rc = strncmp(lhs, rhs, sz);
  if (rc < 0)
    printf("First %d chars of [%s] precede [%s]\n", sz, lhs, rhs);
  else if (rc > 0)
    printf("First %d chars of [%s] follow [%s]\n", sz, lhs, rhs);
  else
    printf("First %d chars of [%s] equal [%s]\n", sz, lhs, rhs);
}

int main(void) {
  const char* string = "Hello World!";
  demo(string, "Hello!", 5);
  demo(string, "Hello", 10);
  demo(string, "Hello there", 10);
  demo("Hello, everybody!" + 12, "Hello, somebody!" + 11, 5);
}
```

출력:

```text
First 5 chars of [Hello World!] equal [Hello!]
First 10 chars of [Hello World!] follow [Hello]
First 10 chars of [Hello World!] precede [Hello there]
First 5 chars of [body!] equal [body!]
```

</details>

<details>

<summary><h2><code>strcoll</code></h2></summary>

- `int strcoll(const char* lhs, const char* rhs);`
  - [`LC_COLLATE`](https://en.cppreference.com/w/c/locale/LC_categories) 카테고리에서 정의된 현재 로케일에 따라 두 개의 null 종결 바이트 문자열 비교

### 파라미터

`lhs`, `rhs`: 비교할 null 종결 바이트 문자열을 가리키는 포인터

### 반환값

- `lhs` 가 `rhs` 보다 _작으면_ (앞서면) 음수
- `lhs` 와 `rhs` 가 같으면 0
- `lhs` 가 `rhs` 보다 _크면_ (늦으면) 양수

### 참고

- 대조 순서는 사전 순
- 현재 로케일의 알파벳(그와 _동등한 클래스_ )에서의 문자의 위치가 case(대문자/소문자의 case)나 변형보다 높은 우선순위를 가짐
- 동등한 클래스 안에서, 소문자 문자는 대응하는 대문자보다 앞서며, 분음 기호를 가지는 문자에는 로케일에 따른 순서가 적용될 수 있음
- 어떤 로케일에서는, 문자 모음을 하나의 _대조 단위_ 로 간주함
  - 체코어에서는 `"ch"`가 `"h"` 뒤, `"i"` 앞
  - 헝가리어에서는 `"dzs"`가 `"dz"` 뒤, `"g"` 앞

### 예시

```c
#include <locale.h>
#include <stdio.h>
#include <string.h>

int main(void) {
  setlocale(LC_COLLATE, "cs_CZ.utf8");
  // Alternatively, ISO-8859-2 (a.k.a. Latin-2)
  // may also work on some OS:
  // setlocale(LC_COLLATE, "cs_CZ.iso88592");

  const char* s1 = "hrnec";
  const char* s2 = "chrt";

  printf("In the Czech locale: ");
  if (strcoll(s1, s2) < 0)
    printf("%s before %s\n", s1, s2);
  else
    printf("%s before %s\n", s2, s1);

  printf("In lexicographical comparison: ");
  if (strcmp(s1, s2) < 0)
    printf("%s before %s\n", s1, s2);
  else
    printf("%s before %s\n", s2, s1);
}
```

출력:

```text
In the Czech locale: hrnec before chrt
In lexicographical comparison: chrt before hrnec
```

</details>

<details>

<summary><h2><code>strchr</code></h2></summary>

헤더 `<string.h>`에서 정의

- `char* strchr(const char* str, int ch);` (1)

  - `str`가 가리키는 null 종단 바이트 문자열 (각 문자는 `unsigned char`로 해석됨) 안에서의 `ch` (`(char)ch`를 통해 `char`로 변환한 후) 의 첫 등장
  - 종결하는 null 문자는 문자열의 일부로 간주되며, `\0`을 검색할 때 찾을 수 있음

- `/*QChar*/ *strchr(/*QChar*/ *str, int ch);` (2) (C23부터)

  - (1)과 동등한 제네릭 함수
  - `T`를 임의의 문자 객체 타입이라고 하면
    - `str`이 `const T*` 타입일 때, 반환값은 `const char*`
    - 만약 `str`이 `T*` 타입일 때, 반환값은 `char*`
    - 그 외의 경우 동작의 결과를 예측할 수 없음
  - 만약 이러한 제네릭 함수의 거시적인 정의가 실제 함수에 접근하기 위해 제한된다면 (e.g. 만약 `(strchr)` 또는 함수 포인터가 사용된 경우), 실제 함수 선언 (1)이 표시됨

- `str`이 null 종단 바이트 문자열을 가리키는 포인터가 아닐 때 동작의 결과를 예측할 수 없음

### 파라미터

- `str`: 분석할 null 종단 문자열을 가리키는 포인터
- `ch`: 찾을 문자

### 반환값

- 문자를 찾은 경우 `str`에서 찾은 문자를 가리키는 포인터
- 찾지 못한 경우 null 포인터

### 예시

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    const char *str = "Try not. Do, or do not. There is no try.";
    char target = 'T';
    const char* result = str;

    while ((result = strchr(result, target)) != NULL) {
        printf("Found '%c' starting at '%s'\n", target, result);
        ++result; // Increment result, otherwise we'll find target at the same location
    }
}
```

결과:

```text
Found 'T' starting at 'Try not. Do, or do not. There is no try.'
Found 'T' starting at 'There is not try.'
```

</details>

<details>

<summary><h2><code>strrchr</code></h2></summary>

헤더 `<string.h>`에서 정의

- `char* strrchr(const char* str, int ch);` (1)

  - `str`가 가리키는 null 종단 바이트 문자열 (각 문자는 `unsigned char`로 해석됨) 안에서의 `ch` (`(char)ch`를 통해 `char`로 변환한 후) 의 마지막 등장
  - 종결하는 null 문자는 문자열의 일부로 간주되며, `\0`을 검색할 때 찾을 수 있음

- `/*QChar*/ *strrchr(/*QChar*/ *str, int ch);` (2) (C23부터)

  - (1)과 동등한 제네릭 함수
  - `T`를 임의의 문자 객체 타입이라고 하면
    - `str`이 `const T*` 타입일 때, 반환값은 `const char*`
    - 만약 `str`이 `T*` 타입일 때, 반환값은 `char*`
    - 그 외의 경우 동작의 결과를 예측할 수 없음
  - 만약 이러한 제네릭 함수의 거시적인 정의가 실제 함수에 접근하기 위해 제한된다면 (e.g. 만약 `(strchr)` 또는 함수 포인터가 사용된 경우), 실제 함수 선언 (1)이 표시됨

- `str`이 null 종단 바이트 문자열을 가리키는 포인터가 아닐 때 동작의 결과를 예측할 수 없음

### 파라미터

- `str`: 분석할 null 종단 문자열을 가리키는 포인터
- `ch`: 찾을 문자

### 반환값

- 문자를 찾은 경우 `str`에서 찾은 문자를 가리키는 포인터
- 찾지 못한 경우 null 포인터

### 예시

```c
#include <stdio.h>
#include <string.h>

int main(void) {
  char szSomeFileName[] = "foo/bar/foobar.txt";
  char* pLastSlash = strrchr(szSomeFileName, '/');
  char* pszBaseName = pLastSlash ? pLastSlash + 1 : szSomeFileName;
  printf("Base Name: %s\n", pszBaseName);
}
```

결과:

```text
Base Name: foobar.txt
```

</details>

<details>

<summary><h2><code>strspn</code></h2></summary>

- `size_t strspn(const char* dest, const char* src);`
  - `src`가 가리키는 null 종단 바이트 문자열에서 찾을 수 있는 문자로만 이루어진 `dest`가 가리키는 null 종단 바이트 문자열의 초기 segment(span)의 최대 길이 반환
- `dest` 또는 `src`가 null 종단 바이트 문자열을 가리키는 포인터가 아닐 때 동작의 결과를 예측할 수 없음

### 파라미터

- `dest`: 분석할 null 종단 바이트 문자열을 가리키는 포인터
- `src`: 검색할 문자로 구성된 null 종단 바이트 문자열을 가리키는 포인터

### 반환값

`src`가 가리키는 null 종단 바이트 문자열이 포함하는 문자만을 가지는 최장 초기 segment의 길이

### 예제

```c
#include <stdio.h>
#include <string.h>

int main(void) {
  const char* string = "abcde312$#@";
  const char* low_alpha = "qwertyuiopasdfghjklzxcvbnm";

  size_t spnsz = strspn(string, low_alpha);
  printf(
      "After skipping initial lowercase letters from '%s'\n"
      "The remainder is '%s'\n",
      string, string + spnsz);
}
```

출력:

```text
After skipping initial lowercase letters from 'abcde312$#@'
The remainder is '312$#@'
```

</details>

<details>

<summary><h2><code>strcspn</code></h2></summary>

헤더 <string.h>에서 정의

- `size_t strcspn(const char* dest, const char* src);`
  - `src`가 가리키는 null 종단 바이트 문자열에 포함되지 _않은_ 문자만으로 구성된 `dest`가 가리키는 null 종단 바이트 문자열의 최장 초기 segment의 길이 반환
  - `dest` 또는 `src`가 null 종단 바이트 문자열을 가리키는 포인터가 아니라면 동작의 결과를 예측할 수 없음

### 파라미터

- `dest`: 분석할 null 종단 바이트 문자열을 가리키는 포인터
- `src`: 제외할 문자로 구성된 null 종단 바이트 문자열을 가리키는 포인터

### 반환값

`src`가 가리키는 null 종단 바이트 문자열에서 찾을 수 없는 문자만 포함하는 최장 초기 segment의 길이

### 참조

이 함수의 이름은 "complementary span"의 약자인데, `src`에서 찾을 수 없는 문자, 즉 `src`의 complement를 찾는 함수이기 때문

### 예제

```c
#include <stdio.h>
#include <string.h>

int main(void) {
  const char* string = "abcde312$#@";
  const char* invalid = "*$#";

  size_t valid_len = strcspn(string, invalid);
  if (valid_len != strlen(string))
    printf("'%s' contains invalid chars starting at position %zu\n", string,
           valid_len);
}
```

출력:

```text
'abcde312$#@' contains invalid chars starting at position 8
```

</details>

<details>

<summary><h2><code>strpbrk</code></h2></summary>

- `char *strpbrk(const char* dest, const char* breakset);` (1)

  - `dest`가 가리키는 null 종단 바이트 문자열을 탐색해 `breakset`가 가리키는 null 종단 바이트 문자열 내의 문자를 찾으면 그 문자를 가리키는 포인터를 반환함

- `/*QChar*/ *strpbrk(/*QChar*/ *dest, const char* breakset);` (2) (C23부터)

  - (1)과 동등한 제네릭 함수
  - `T`를 임의의 문자 객체 타입이라고 하면
    - `str`이 `const T*` 타입일 때, 반환값은 `const char*`
    - 만약 `str`이 `T*` 타입일 때, 반환값은 `char*`
    - 그 외의 경우 동작의 결과를 예측할 수 없음
  - 만약 이러한 제네릭 함수의 거시적인 정의가 실제 함수에 접근하기 위해 제한된다면 (e.g. 만약 `(strpbrk)` 또는 함수 포인터가 사용된 경우), 실제 함수 선언 (1)이 표시됨

- `str` 또는 `breakset`이 null 종단 바이트 문자열을 가리키는 포인터가 아닐 때 동작의 결과를 예측할 수 없음

### 파라미터

- `dest`: 분석할 null 종단 바이트 문자열을 가리키는 포인터
- `breakset`: 찾을 문자를 포함하는 null 종단 바이트 문자열을 가리키는 포인터

### 반환값

- `breakset`에 포함된 문자가 `dest`에서 처음으로 나타날 때 그 문자의 포인터
- 그런 문자가 없으면 null 포인터

### 참조

첫 번째 분리자("break") 문자를 가리키는 포인터를 반환하기 때문에 "string pointer break"의 약자

### 예제

```c
#include <stdio.h>
#include <string.h>

int main(void) {
  const char* str = "hello world, friend of mine!";
  const char* sep = " ,!";

  unsigned int cnt = 0;
  do {
    str = strpbrk(str, sep);           // find separator
    if (str) str += strspn(str, sep);  // skip separator
    ++cnt;                             // increment word count
  } while (str && *str);

  printf("There are %u words\n", cnt);
}
```

출력:

```text
There are 5 words
```

</details>

<details>

<summary><h2><code>strstr</code></h2></summary>

</details>

헤더 <string.h>에서 정의
- `char* strstr(const char* str, const char* substr);` (1)
  - `str`가 가리키는 null 종단 바이트 문자열에서 `substr`가 가리키는 null 종단 바이트 문자열의 첫 등장을 찾음
  - 문자열 종단 null 문자는 비교되지 않음
- `/*QChar*/ *strstr(/*QChar*/ *str, const char* substr);` (2) (C23부터)
  - (1)과 동등한 제네릭 함수
  - `T`를 임의의 문자 객체 타입이라고 하면
    - `str`이 `const T*` 타입일 때, 반환값은 `const char*`
    - 만약 `str`이 `T*` 타입일 때, 반환값은 `char*`
    - 그 외의 경우 동작의 결과를 예측할 수 없음
  - 만약 이러한 제네릭 함수의 거시적인 정의가 실제 함수에 접근하기 위해 제한된다면 (e.g. 만약 `(strstr)` 또는 함수 포인터가 사용된 경우), 실제 함수 선언 (1)이 표시됨

- `str` 또는 `substr`이 null 종단 바이트 문자열을 가리키는 포인터가 아닐 때 동작의 결과를 예측할 수 없음

### 파라미터

- `str`: 조사할 null 종단 바이트 문자열을 가리키는 포인터
- `substr`: 찾을 null 종단 바이트 문자열을 가리키는 포인터

### 반환값

- `str`에서 찾은 부분 문자열의 첫 문자를 가리키는 포인터
- 그러한 부분 문자열을 찾지 못한 경우 null 보인터
- `substr`이 빈 문자열이라면 `str`

### 예제

```c
#include <stdio.h>
#include <string.h>

void find_str(char const* str, char const* substr) {
  char const* pos = strstr(str, substr);
  if (pos) {
    printf("Found the string [%s] in [%s] at position %td\n", substr, str,
           pos - str);
  } else {
    printf("The string [%s] was not found in [%s]\n", substr, str);
  }
}

int main(void) {
  char const* str = "one two three";
  find_str(str, "two");
  find_str(str, "");
  find_str(str, "nine");
  find_str(str, "n");

  return 0;
}
```

출력:

```text
Found the string [two] in [one two three] at position 4
Found the string [] in [one two three] at position 0
The string [nine] was not found in [one two three]
Found the string [n] in [one two three] at position 1
```

<details>

<summary><h2><code>strtok</code>, <code>strtok_s</code></h2></summary>

헤더 `<string.h>`에서 정의

- `char *strtok(char *str, const char *delim);` (C99 전까지)
- `char *strtok(char *restrict str, const char *restrict delim);` (C99부터)

  - `str`이 가리키는 null 종단 바이트 문자열의 다음 토큰을 찾음
  - 구분자 문자(복수 가능)는 `delim`이 가리키는 null 종단 바이트 문자열에 의해 식별됨
  - 이 함수는 동일한 문자열에서 연속적인 토큰들을 찾기 위해 여러 번 호출되도록 고안됨
  - `str`이 null 포인터가 아니라면, 함수 호출은 이 특정 문자열에 `strtok`을 처음으로 호출하는 것으로 간주됨
    - 함수는 `delim`에 포함되지 _않은_ 첫 번째 문자를 찾음
      - 그러한 문자를 찾지 못했다면 `str`에는 토큰이 존재하지 않는 것이므로 함수는 null 포인터를 반환함
      - 그러한 문자를 찾았다면, 이는 _토큰의 시작점_ 임. 함수는 그 다음으로 그 지점부터 `delim`에 _포함된_ 첫 번째 문자를 찾음
        - 그러한 문자를 찾지 못했다면, `str`은 단 하나의 토큰을 가진 것이므로 이후의 `strtok` 호출은 null 포인터를 반환함
        - 그러한 문자를 찾았다면, 그 문자는 null 문자 `\0`으로 _대체되고_, 그 다음 문자를 가리키는 포인터는 다음 호출을 위해 정적 위치에 저장됨
      - 함수는 토큰의 시작점을 가리키는 포인터를 반환함
  - `str`가 null 포인터라면, 호출은 `strtok`의 후속 호출로 취급됨
    - 함수는 이전 호출에서 저장된 위치에서 재개됨
    - 이 동작은 이전에 저장된 포인터가 `str`로 넘겨졌을 때와 같이 동작함
  - `str` 또는 `delim`이 null 종단 바이트 문자열을 가리키는 포인터가 아닐 때에는 동작의 결과를 예측할 수 없음

- `char *strtok_s(char *restrict str, rsize_t *restrict strmax, const char *restrict delim, char **restrict ptr);` (C11부터)

  - 모든 단계에서 `*strmax`에 확인해야 할 잔여 문자의 수를, `*ptr`에 토크나이저의 내부 상태를 저장함
  - (null `str`을 가지는) 반복된 호출에서는 이전 호출에서 저장된 `strmax`와 `ptr` 값을 반드시 같이 넘겨야 함
  - `ptr`가 가리키는 객체에 아무것도 저장하지 않는다면 런타임에 다음 오류가 감지되며, [constraint 핸들러 함수](https://en.cppreference.com/w/c/error/set_constraint_handler_s)를 호출함
    - `strmax`, `delim`, 또는 `ptr`이 null 포인터
    - 초기 호출이 아닐 때(null `str`을 가짐), `*ptr`이 null 포인터
    - 초기 호출에서 `*strmax`가 0이거나 `RSIZE_MAX`보다 큼
    - 토큰의 종결점 탐색이 null 종결문자를 발견하지 않은 채 원 문자열의 끝(`*strmax`의 초기값에 의해 측정됨)에 도달함
  - `str`이 null 문자를 가지지 않은 문자열을 가리키고 `strmax`가 그 문자열의 크기보다 큰 값일 때 동작의 결과를 예측할 수 없음
  - 모든 경계 검사 함수들을 사용하는 경우와 같이, `strtok_s`는 구현에 의해 `__STDC_LIB_EXT1__`이 정의되었으며, [`<string.h>`](https://en.cppreference.com/w/c/string/byte)을 포함하기 전에 사용자가 `__STDC_WANT_LIB_EXT1__`을 정수 상수 `1`로 정의할 때에만 사용 가능성이 보장됨

### 파라미터

- `str`: 토큰화할 null 종단 바이트 문자열을 가리키는 포인터
- `delim`: 구분자들을 식별하는 null 종단 바이트 문자열을 가리키는 포인터
- `strmax`
  - 초기에 `str`의 크기를 저장하는 객체를 가리키는 포인터
  - `strtok_s`는 확인해야 할 남은 문자의 수를 저장함
- `ptr`: `strtok_s`가 내부 상태를 저장하기 위해 사용하는 `char*` 타입의 객체를 가리키는 포인터

### 반환값

다음 토큰의 시작점을 가리키는 포인터 또는 더 이상 토큰이 남아있지 않은 경우 null 포인터 반환

### 참고

- 이 함수는 파괴적임
  - `str` 문자열의 원소에 `\0` 문자를 저장함
  - 특히, 문자열 리터럴은 `strtok`의 첫 번째 인자로 사용될 수 없음
- `strtok`을 호출할 때마다 정적 변수가 변경됨: 스레드 안전하지 않음
- 다른 대부분의 토크나이저와 다르게, `strtok`의 구분자는 각각의 연속되는 토큰에서 다를 수 있으며, 이전 토큰의 내용물에 의존할 수도 있음
- `strtok_s` 함수는 POSIX [`strtok_r`](http://pubs.opengroup.org/onlinepubs/9699919799/functions/strtok.html) 함수와 다름
  - 토큰화되는 문자열 바깥에 저장되는 것을 방지함
  - 런타임 제약 조건을 확인함
- 마이크로소프트 CRT `strtok_s`는 C11 `strtok_s`가 아닌 POSIX `strtok_r` 정의와 일치함
  - `char *__cdecl strtok_s(char *_String, const char *_Delimiter, char **_Context)`

### 예제

```c
#define __STDC_WANT_LIB_EXT1__ 1
#include <stdio.h>
#include <string.h>

int main(void) {
  char input[] = "A bird came down the walk";
  printf("Parsing the input string '%s'\n", input);
  char *token = strtok(input, " ");
  while (token) {
    puts(token);
    token = strtok(NULL, " ");
  }

  printf("Contents of the input string now: '");
  for (size_t n = 0; n < sizeof input; ++n)
    input[n] ? putchar(input[n]) : fputs("\\0", stdout);
  puts("'");

  /* cpp reference의 예제
      char str[] = "A bird came down the walk";
      rsize_t strmax = sizeof str;
      const char *delim = " ";
      char *next_token;
      printf("Parsing the input string '%s'\n", str);
      token = strtok_r(str, &strmax, delim, &next_token);
      while (token) {
        puts(token);
        token = strtok_s(NULL, &strmax, delim, &next_token);
      }

      printf("Contents of the input string now: '");
      for (size_t n = 0; n < sizeof str; ++n)
        str[n] ? putchar(str[n]) : fputs("\\0", stdout);
      puts("'");
  */

#ifdef __STDC_WANT_LIB_EXT1__
  char str[] = "A bird came down the walk";
  int *strmax = (int *)sizeof str;
  const char *delim = " ";
  char *next_token;
  printf("Parsing the input string '%s'\n", str);
  token = strtok_r(str, delim, &next_token);
  while (token) {
    puts(token);
    token = strtok_r(NULL, delim, &next_token);
  }

  printf("Contents of the input string now: '");
  for (size_t n = 0; n < sizeof str; ++n)
    str[n] ? putchar(str[n]) : fputs("\\0", stdout);
  puts("'");
#endif
}
```

출력:

```text
Parsing the input string 'A bird came down the walk'
A
bird
came
down
the
walk
Contents of the input string now: 'A\0bird\0came\0down\0the\0walk\0'
Parsing the input string 'A bird came down the walk'
A
bird
came
down
the
walk
Contents of the input string now: 'A\0bird\0came\0down\0the\0walk\0'
```

</details>
