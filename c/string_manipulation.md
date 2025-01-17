# String Manipulation

<details>

<summary><h2><code>strcpy, strcpy_s</code></h2></summary>

헤더 <string.h>에서 정의

- `char* strcpy(char* dest, const char* src);` (1) (C99 이전)
- `char* strcpy(char* restrict dest, const char* restrict src);` (1) (C99부터)
  - `src`가 가리키는 null 종단 문자열을 null 문자를 포함해 `dest`가 가리키는 문자 배열에 복사
  - `dest` 배열이 충분히 크지 않거나 문자열이 겹치거나(overlap) `dest`가 문자 배열을 가리키는 포인터가 아니거나 `src`가 null 종단 문자열을 가리키지 않는다면 undefined
- `errno_t strcpy_s(char* restrict dest, rsize_t destsz, const char* restrict src);` (2) (C11부터)
  - 다음을 제외하면 (1)과 같음
    - 지정되지 않은 값으로 `dest` 배열을 덮어쓰고 아래의 오류가 런타임에서 감지되어 현재 설치된 제약조건 핸들러 함수를 호출할 수 있음:
      - `src` 또는 `dest`가 null 포인터
      - `destsz`가 0이거나 `RSIZE_MAX`보다 큼
      - `destsz`가 `strnlen_s(src, destsz)`보다 작거나 같음: 즉, 문자열이 잘림
      - 원 문자열과 목적지 문자열에 겹침이 발생한 경우
  - (`dest`가 가리키는 문자 배열의 크기) <= `strnlen_s(src, destsz) < `destsz` 일 때 undefined
    - `destsz`가 잘못된 값을 가지더라도 버퍼 오버플로우 발생을 일으키지 않음
  - 모든 bounds-checked 함수처럼, `strlen` 는 구현에 의해 `__STDC_LIB_EXT1__`이 정의되어 있거나 사용자가 `<string.h>` 을 include하기 전에 `__STDC_WANT_LIB_EXT1__` 을 1로 정의할 때 동작함

### 파라미터

- `dest`: 복사할 문자열을 저장할 문자 배열을 가리키는 포인터
- `src`: 저장할 null 종단 문자열을 가리키는 포인터
- `destsz`: 저장할 문자의 최대 수. 일반적으로 목적지 버퍼의 크기

### 반환값

1. `dest`의 사본 반환
2. 성공일 때 0, 오류 발생시 0이 아닌 수
   - 오류가 발생했을 때, `dest[0]`에 0 저장 (`dest`가 null 포인터이거나 `destsz`가 0이거나 `RSIZE_MAX`보다 큰 경우가 아니라면)

### 참고

- `strcpy_s`는 효율성 증대를 위해 마지막으로 저장된 문자부터 `destsz`까지 목적지 배열을 덮어쓸 수 있게 허용됨
  - 멀티바이트 블록을 복사하고 난 후 null 바이트를 확인할 수 있음
- `strcpy_s`는 다음을 제외하면 BSD 함수 `strlcpy`와 유사함
  - `strlcpy`는 원 문자열을 목적지에 맞게 자름(보안 이슈)
  - `strlcpy`는 `strcpy_s`가 하는 모든 런타임 체크를 수행하지 않음
  - `strlcpy`는 호출이 실패했을 때 목적지를 null 문자열로 설정하거나 핸들러를 호출하는 등의 동작으로 실패를 명확히 나타내는 동작을 수행하지 않음
- `strcpy_s`가 발생 가능한 보안 문제 때문에 문자열 잘림을 방지함에도 불구하고 bounds-checked 함수인 `strncpy_s`를 대신 사용해 문자열을 자르는 것이 가능함

### 예제

```c
#define __STDC_WANT_LIB_EXT1__ 1
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
  const char *src = "Take the test.";
  //  src[0] = 'M' ; // this would be undefined behavior
  char dst[strlen(src) + 1];  // +1 to accommodate for the null terminator
  strcpy(dst, src);
  dst[0] = 'M';  // OK
  printf("src = %s\ndst = %s\n", src, dst);

#ifdef __STDC_LIB_EXT1__
  set_constraint_handler_s(ignore_handler_s);
  int r = strcpy_s(dst, sizeof dst, src);
  printf("dst = \"%s\", r = %d\n", dst, r);
  r = strcpy_s(dst, sizeof dst, "Take even more tests.");
  printf("dst = \"%s\", r = %d\n", dst, r);
#endif
}
```

가능한 출력:

```text
src = Take the test.
dst = Make the test.
dst = "Take the test.", r = 0
dst = "", r = 22
```

</details>

<details>

<summary><h2><code>strncpy, strncpy_s</code></h2></summary>

헤더 <string.h>에서 정의

- `char* strncpy(char* dest, const char* src, size_t count);` (1) (C99 이전)
- `char* strncpy(char* restrict dest, const char* restrict src, size_t count);` (1) (C99부터)
  - `src`가 가리키는 문자 배열 중 최대 `count`개의 문자(null 종단 문자 포함, 그러나 null 문자 이후의 문자는 불포함)를 `dest`가 가리키는 문자 배열에 복사
  - `src` 전체가 복사되기 전에 `count`에 도달한다면 결과 문자 배열은 null 종단이 아니게 됨
  - `src`에서 null 종단 문자를 복사한 후에도 `count`에 도달하지 않았다면 전체 `count`개의 문자가 복사될 때까지 추가적으로 null 문자를 `dest`에 복사함
  - 두 문자 배열이 겹치거나 `dest` 또는 `src`가 문자 배열을 가리키는 포인터가 아니거나(둘 중 하나가 null 포인터인 경우 포함) `dest`가 가리키는 배열의 크기가 `count`보다 작거나 `src`가 가리키는 배열이 크기는 `count`보다 작고 null 문자를 포함하지 않는다면 undefined
- `errno_t strncpy_s(char* restrict dest, rsize_t destsz, const char* restrict src, rsize_t count);` (2) (C11부터)
  - 다음을 제외하면 (1)과 같음
    - `count`가 될 때까지 목적지 배열에 null 문자를 `dest`에 채워넣지 않음
    - null 종단 문자 입력 후 멈춤(null이 원 배열에 없다면 dest[count]에 null 문자를 쓰고 멈춤)
    - 런타임에서 아래의 오류가 감지되면 현재 설치된 제약조건 핸들러 함수를 호출함:
      - `src` 또는 `dest`가 null 포인터
      - `destsz`가 0이거나 `RSIZE_MAX`보다 큼
      - `count`가 `RSIZE_MAX`보다 큼
      - `count`가 `destsz`보다 크거나 같은데 `destsz`가 `strnlen_s(src, count)`보다 작거나 같음. 즉, 문자열이 잘릴 때
      - 원 문자열과 목적지 문자열에 겹침이 발생할 때
  - 다음의 경우 undefined
    - (`dest`가 가리키는 문자 배열의 크기) <= `strnlen_s(src, destsz) < `destsz`, 즉 `destsz`가 잘못된 값을 가지더라도 버퍼 오버플로우 발생을 일으키지 않음
    - (`src`가 가리키는 문자 배열의 크기) <= `strnlen_s(src, destsz) < `destsz`, 즉 `destsz`가 잘못된 값을 가지더라도 버퍼 오버플로우 발생을 일으키지 않음
  - 모든 bounds-checked 함수처럼, `strlen` 는 구현에 의해 `__STDC_LIB_EXT1__`이 정의되어 있거나 사용자가 `<string.h>` 을 include하기 전에 `__STDC_WANT_LIB_EXT1__` 을 1로 정의할 때 동작함

### 파라미터

- `dest`: 복사할 문자열을 저장할 문자 배열을 가리키는 포인터
- `src`: 저장할 문자 배열을 가리키는 포인터
- `count`: 저장할 문자의 최대 수
- `destsz`: 목적지 버퍼의 크기

### 반환값

1. `dest`의 사본 반환
2. 성공시 0 반환, 오류 발생시 0이 아닌 값 반환
   - 오류가 발생했을 때, `dest[0]`에 0 저장 (`dest`가 null 포인터이거나 `destsz`가 0이거나 `RSIZE_MAX`보다 큰 경우가 아니라면)
   - 목적지 배열의 나머지를 정해지지 않은 값으로 덮어쓸 수 있음

### 참고

- post-C11 DR 468에서 정정되었듯이, `strcpy_s`와는 달리 오류가 발생했을 때 목적지 배열의 남은 부분만 덮어쓰도록 제한됨
- `strncpy`와는 다르게 `strncpy_s`는 목적지 배열을 0으로 채우지 않음
  - 존재하는 코드를 bounds-checked 버전으로 변환할 때 오류를 일으키는 흔한 원인
- 목적지 배열에 맞추기 위해 문자열을 자르는 것은 보안 상의 문제를 일으킬 수 있고, `strncpy_s`에 대한 런타임 제약사항 위반이지만 목적지 배열의 크기에서 1을 뺀 값과 같은 값으로 `count`를 명시해 문자열 자르기 동작을 구현할 수 있음
  - 늘 그렇듯이 첫 `count` 바이트를 복사한 후 null 종단 문자를 뒤에 추가함:
    - `strncpy_s(dst, sizeof dst, src, (sizeof dst) - 1);`

### 예제

```c
#define __STDC_WANT_LIB_EXT1__ 1
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
  char src[] = "hi";
  char dest[6] = "abcdef";  // no null terminator
  // writes five characters 'h', 'i', '\0', '\0', '\0' to dest
  strncpy(dest, src, 5);
  printf("strncpy(dest, src, 5) to a 6-byte dest gives : ");
  for (size_t n = 0; n < sizeof dest; ++n) {
    char c = dest[n];
    c ? printf("'%c' ", c) : printf("'\\0' ");
  }

  printf("\nstrncpy(dest2, src2) to a 2-byte dst gives : ");
  char dest2[2];
  // truncation: writes two characters 'h', 'i', to dest2
  strncpy(dest2, src, 2);
  for (size_t n = 0; n < sizeof dest2; ++n) {
    char c = dest2[n];
    c ? printf("'%c' ", c) : printf("'\\0' ");
  }
  printf("\n");

#ifdef __STDC_LIB_EXT1__
  set_constraint_handler_s(ignore_handler_s);
  char dst1[6], src1[100] = "hello";
  // writes 0 to r1, 6 characters to dst1
  errno_t r1 = strncpy_s(dst1, 6, src1, 100);
  // 'h','e','l','l','o','\0' to dst1
  printf("dst1 = \"%s\", r1 = %d\n", dst1, r1);

  char dst2[5], src2[7] = {'g', 'o', 'o', 'd', 'b', 'y', 'e'};
  // copy overflows the destination array
  errno_t r2 = strncpy_s(dst2, 5, src2, 7);
  // writes nonzero to r2,'\0' to dst2[0]
  printf("dst2 = \"%s\", r2 = %d\n", dst2, r2);

  char dst3[5];
  // writes 0 to r3, 5 characters to dst3
  errno_t r3 = strncpy_s(dst3, 5, src2, 4);
  // 'g', 'o', 'o', 'd', '\0' to dst3
  printf("dst3 = \"%s\", r3 = %d\n", dst3, r3);
#endif
}
```

가능한 출력:

```text
strncpy(dest, src, 5) to a 6-byte dst gives : 'h' 'i' '\0' '\0' '\0' 'f'
strncpy(dest2, src, 2) to a 2-byte dst gives : 'h' 'i'
dst1 = "hello", r1 = 0
dst2 = "", r2 = 22
dst3 = "good", r3 = 0
```

</details>

<details>

<summary><h2><code>strcat, strcat_s</code></h2></summary>

헤더 <string.h>에서 정의

- `char* strcat(char* dest, const char* src);` (1) (C99 이전)
- `char* strcat(char* restrict dest, const char* restrict src);` (1) (C99부터)
  - `dest`가 가리키는 null 종단 문자열 뒤에 `src`가 가리키는 null 종단 문자열의 사본을 추가
    - 문자 `src[0]`이 `dest` 마지막의 null 문자를 대체함
    - 결과 바이트 문자열은 null로 끝남
  - 목적지 배열이 `src`와 `dest`의 내용과 null 문자를 모두 포함할 만큼 크지 않거나 문자열들이 겹치거나 `dest` 또는 `src`가 null 종단 바이트 문자열을 가리키는 포인터가 아닐 때 undefined
- `errno_t strcat_s(char* restrict dest, rsize_t destsz, const char* restrict src);` (2) (C11부터)
  - 다음을 제외하고 (1)과 같음
    - 목적지 배열의 나머지(마지막으로 저장한 문자부터 `destsz`까지)를 정해지지 않은 값으로 덮어쓸 수 있음
    - 런타임에서 아래의 오류가 감지되면 현재 설치된 제약조건 핸들러 함수를 호출함:
      - `src` 또는 `dest`가 null 포인터
      - `destsz`가 0이거나 `RSIZE_MAX`보다 큼
      - `dest`의 처음 `destsz` 바이트 안에 null 문자가 없음
      - 문자열이 잘림 (`dest` 끝의 가용공간이 null 문자를 포함한 `src`의 모든 문자를 담기에는 적음)
      - `src`와 `dest`가 가리키는 문자열들이 겹침
  - 다음의 경우 undefined
    - (`dest`가 가리키는 문자 배열의 크기) <= `strnlen_s(src, destsz) < `destsz`, 즉 `destsz`가 잘못된 값을 가지더라도 버퍼 오버플로우 발생을 일으키지 않음
    - (`src`가 가리키는 문자 배열의 크기) <= `strnlen_s(src, destsz) < `destsz`, 즉 `destsz`가 잘못된 값을 가지더라도 버퍼 오버플로우 발생을 일으키지 않음
  - 모든 bounds-checked 함수처럼, `strlen` 는 구현에 의해 `__STDC_LIB_EXT1__`이 정의되어 있거나 사용자가 `<string.h>` 을 include하기 전에 `__STDC_WANT_LIB_EXT1__` 을 1로 정의할 때 동작함

### 파라미터

- `dest`: 문자열이 추가될 null 종단 바이트 문자열을 가리키는 포인터
- `src`: 복사될 null 종단 바이트 문자열을 가리키는 포인터
- `destsz`: 저장할 문자의 최대 수. 일반적으로 목적지 버퍼의 크기

### 반환값

1. `dest`의 사본 반환
2. 성공시 0, 오류 발생시 0이 아닌 값 반환

- 오류 발생 시 `dest[0]`에 0 저장 (`dest`가 null 포인터이거나 `destsz`가 0 또는 `RSIZE_MAX`보다 큰 경우 제외)

### 참고

- `strcat`은 호출될 때마다 `dest`의 마지막 부분을 찾아야 하므로 `strcat`을 이용해 여러 개의 문자열을 하나로 합치는 것은 비효율적임
- `strcat_s`는 효율성을 높이기 위해 마지막으로 저장된 문자부터 `destsz`까지의 목적지 배열을 덮어쓸 수 있음
  - 멀티바이트 블록을 복사한 후 null 바이트를 검색함
- 함수 `strcat_s`는 다음을 제외하고 BSD 함수 `strlcat`과 유사함
  - `strlcat`은 `dest`에 맞도록 `src` 문자열을 자름
  - `strlcat`은 `strcat_s`가 수행하는 모든 런타임 검사를 수행하지 않음
  - `strlcat`은 호출이 실패했을 때 목적지를 null 문자열로 설정하거나 핸들러를 호출하는 등의 동작으로 실패를 명확히 나타내는 동작을 수행하지 않음
- `strcat_s`가 발생 가능한 보안 문제 때문에 문자열 잘림을 방지함에도 불구하고 bounds-checked 함수인 `strncat_s`를 대신 사용해 문자열을 자르는 것이 가능함

### 예제

```c
#define __STDC_WANT_LIB_EXT1__ 1
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
  char str[50] = "Hello ";
  char str2[50] = "World!";
  strcat(str, str2);
  strcat(str, " ...");
  strcat(str, " Goodbye World!");
  puts(str);

#ifdef __STDC_LIB_EXT1__
  set_constraint_handler_s(ignore_handler_s);
  int r = strcat_s(str, sizeof str, " ... ");
  printf("str = \"%s\", r = %d\n", str, r);
  r = strcat_s(str, sizeof str, " and this is too much");
  printf("str = \"%s\", r = %d\n", str, r);
#endif
}
```

가능한 출력:

```text
Hello World! ... Goodbye World!
str = "Hello World! ... Goodbye World! ... ", r = 0
str = "", r = 22
```

</details>

<details>

<summary><h2><code>strncat, strncat_s</code></h2></summary>

</details>

<details>

<summary><h2><code>strxfrm</code></h2></summary>

</details>

<details>

<summary><h2><code>strdup</code></h2></summary>

</details>

<details>

<summary><h2><code>strndup</code></h2></summary>

</details>
