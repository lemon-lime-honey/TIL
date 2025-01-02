# String Examination

<details>

<summary><h2><code>strlen</code>, <code>strlen_s</code></h2></summary>

</details>

<details>

<summary><h2><code>strcmp</code></h2></summary>

</details>

<details>

<summary><h2><code>strncmp</code></h2></summary>

</details>

<details>

<summary><h2><code>strcoll</code></h2></summary>

</details>

<details>

<summary><h2><code>strchr</code></h2></summary>

</details>

<details>

<summary><h2><code>strrchr</code></h2></summary>

</details>

<details>

<summary><h2><code>strspn</code></h2></summary>

</details>

<details>

<summary><h2><code>strcspn</code></h2></summary>

</details>

<details>

<summary><h2><code>strpbrk</code></h2></summary>

</details>

<details>

<summary><h2><code>strstr</code></h2></summary>

</details>

<details>

<summary><h2><code>strtok</code>, <code>strtok_s</code></h2></summary>

  헤더 `<string.h>`에서 정의

  - `char *strtok(char *str, const char *delim);` (C99 전까지)
  - `char *strtok(char *restrict str, const char *restrict delim);` (C99부터)

    - `str`이 가리키는 null 종단 바이트 문자열의 다음 토큰을 찾음
    - 구분자 문자(복수 가능)는 `delim`이 가리키는 null 종단 바이트 문자열에 의해 식별됨
    - 이 함수는 동일한 문자열에서 연속적인 토큰들을 찾기 위해 여러 번 호출되도록 고안됨
    - `str`이 null 포인터가 아니라면, 함수 호출은 이 특정 문자열에 `strtok`을 처음으로 호출하는 것으로 간주됨
      - 함수는 `delim`에 포함되지 *않은* 첫 번째 문자를 찾음
        - 그러한 문자를 찾지 못했다면 `str`에는 토큰이 존재하지 않는 것이므로 함수는 null 포인터를 반환함
        - 그러한 문자를 찾았다면, 이는 *토큰의 시작점* 임. 함수는 그 다음으로 그 지점부터 `delim`에 *포함된* 첫 번째 문자를 찾음
          - 그러한 문자를 찾지 못했다면, `str`은 단 하나의 토큰을 가진 것이므로 이후의 `strtok` 호출은 null 포인터를 반환함
          - 그러한 문자를 찾았다면, 그 문자는 null 문자 `\0`으로 *대체되고*, 그 다음 문자를 가리키는 포인터는 다음 호출을 위해 정적 위치에 저장됨
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