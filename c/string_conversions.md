# Conversions to and from numeric formats

<details>

<summary><h2><code>atof</code></h2></summary>

헤더 <stdlib.h>에서 정의

- `double atof(const char* str);`
  - `str`가 가리키는 바이트 문자열의 부동소수점 값 변환
  - 이 함수는 공백이 아닌 문자가 처음으로 발견될 때까지 모든 공백 문자(`isspace`로 결정됨)를 제거함
  - 유효한 부동소수점 표현을 형성할 수 있는 가장 많은 문자를 가지고 부동소수점 값으로 변환함
  - 유효한 부동소수점 값은 다음 중 하나
    - 십진법 부동소수점 표현. 다음으로 구성됨:
      - (선택) 양수 또는 음수 부호
      - 소수점 문자(현재 C 로케일이 결정)를 포함하거나 포함하지 않는 비어있지 않은 십진법 숫자의 시퀀스(유효숫자를 결정함)
      - (선택) 선택적인 양수 또는 음수 부호와 비어있지 않은 십진법 숫자 시퀀스가 뒤에 붙은 **e** 또는 **E** (밑이 10인 지수 정의)
    - 십육진법 부동소수점 표현. 다음으로 구성됨:
      - (선택) 양수 또는 음수 부호
      - **`0x`** 또는 **`0X`**
      - 소수점 문자(현재 C 로케일이 결정)를 포함하거나 포함하지 않는 비어있지 않은 십진법 숫자의 시퀀스(유효숫자를 결정함)
      - (선택) 선택적인 양수 또는 음수 부호와 비어있지 않은 십진법 숫자 시퀀스가 뒤에 붙은 **`p`** 또는 **`P`** (밑이 2인 지수 정의)
    - 무한 표현. 다음으로 구성됨:
      - (선택) 양수 또는 음수 부호
      - **`INF`** 또는 **`INFINITY`**, 대소문자 구분 안함
    - not-a-number 표현. 다음으로 구성됨:
      - (선택) 양수 또는 음수 부호
      - **`NAN`** 또는 <code><b>NAN</b>(char_sequence)</code> (대소문자 구분 안함)
        - *char_sequence*는 숫자, 라틴 문자, 언더스코어만 포함함
      - 결과: NaN 부동소수점 값
  - 현재 설치된 C 로케일에 따라 다른 표현을 적용할 수 있음

### 파라미터

- `str`: 변환할 null 종단 바이트 문자열을 가리키는 포인터

### 반환값

- 성공: `str` 내용에 대응하는 `double` 값
- 변환된 값이 반환 타입의 범위 바깥이라면 반환값 undefined
- 변환할 수 없다면 `0.0` 반환

### 참고

"ASCII to float"의 약자

### 예제

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
  printf("%g\n", atof("   -0.0000000123junk"));
  printf("%g\n", atof("0.012"));
  printf("%g\n", atof("15e16"));
  printf("%g\n", atof("-0xlafp-2"));
  printf("%g\n", atof("inF"));
  printf("%g\n", atof("Nan"));
  printf("%g\n", atof("1.0e+309"));  // UB: out of range of double
  printf("%g\n", atof("0.0"));
  printf("%g\n", atof("junk"));
}
```

가능한 출력:

```text
-1.23e-08
0.012
1.5e+17
-107.75
inf
nan
inf
0
0
```

</details>

<details>

<summary><h2><code>atoi, atol, atoll</code></h2></summary>

헤더 <stdlib.h>에서 정의

- `int atoi(const char* str);`
- `long atol(const char* str);`
- `long long atoll(const char* str);` (C99부터)

  - `str`가 가리키는 바이트 문자열의 정수 값 변환
  - 암시된 밑은 언제나 10
  - 이 함수는 공백이 아닌 문자가 처음으로 발견될 때까지 모든 공백 문자를 제거하고, 유효한 정수 숫자 표현을 형성 가능한 최대한 많은 문자를 찾아 정수 값으로 변환함
  - 유효한 정수 값은 다음으로 구성됨:
    - (선택) 양수 또는 음수 부호
    - 십진법 숫자
  - 결과 값을 표현할 수 없다면(예: 변환 값이 대응하는 반환 타입 범위 밖이라면) 동작 결과를 예측할 수 없음

### 파라미터

`str`: 변환되어야 하는 null 종단 바이트 문자열을 가리키는 포인터

### 반환값

- 성공: `str` 내용에 해당하는 정수 값
- 변환할 수 없으면 `0`

### 참고

"ASCII to integer"의 약자

### 예제

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
  printf("%i\n", atoi("  -123junk"));
  printf("%i\n", atoi("  +321dust"));
  printf("%i\n", atoi("0"));
  printf("%i\n",
         atoi("0042"));  // treated as a decimal number with leading zeros
  printf("%i\n",
         atoi("0x2A"));  // only leading zero is converted discarding "x2A"
  printf("%i\n", atoi("junk"));        // no conversion can be performed
  printf("%i\n", atoi("2147483648"));  // UB: out of range of int
}
```

가능한 출력:

```text
-123
321
0
42
0
0
-2147483648
```

</details>

<details>

<summary><h2><code>strtol, strtoll</code></h2></summary>

헤더 <stdlib.h>에서 정의

- `long strtol(const char* str, char** str_end, int base);` (until C99)
- `long strtol(const char* restrict str, char** restrict str_end, int base);` (since C99)
- `long long strtoll(const char* restrict str, char** restrict str_end, int base);` (since C99)
  - `str`가 가리키는 바이트 문자열의 정수 값 변환
  - 이 함수는 공백이 아닌 문자가 처음으로 발견될 때까지 모든 공백 문자(`isspace`로 결정됨)를 제거함
  - 유효한 n진수 (`n=base`) 정수 숫자 표현이 형성될 수 있는 가장 많은 문자열을 가지고 정수 값으로 변환함
  - 유효한 정수값은 다음으로 구성됨:
    - (선택) 양수 또는 음수 부호
    - (선택) 8진수를 가리키는 접두사 `0` (`base`가 `8` 또는 `0`일 때에만 적용)
    - (선택) 16진수를 가리키는 접두사 `0x` 또는 `0X` (`base`가 `16` 또는 `0`일 때에만 적용)
    - 숫자 시퀀스
  - `base`에 사용 가능한 숫자: {0, 2, 3, ..., 36}
    - 2진수 정수에 사용 가능한 숫자는 {0, 1}
    - 3진수 정수에 사용 가능한 숫자는 {0, 1, 2}
    - 10보다 큰 `base`의 경우 유효한 숫자에 로마자(11진수 정수를 위한 Aa에서 36진수 정수를 위한 Zz까지)도 포함됨
      - 문자의 대소문자는 무시됨
  - 현재 설치된 C 로케일에 의해 추가적인 숫자 포맷이 허용될 수 있음
  - 만약 `base`가 `0`이라면, 진법은 자동으로 감지됨
    - 접두사가 `0`이라면 8진법, `0x` 또는 `0X`라면 16진법, 그 외에는 10진법
    - 입력 시퀀스에 음수 부호가 포함된다면, 숫자 시퀀스에서 계산되는 숫자값은 결과 타입에서의 단항 연산자 마이너스처럼 음수가 됨
  - 함수는 `str_end`가 마지막으로 변환된 숫자 문자 다음 문자를 가리키도록 설정함
    - `str_end`가 null 포인터라면 무시됨
  - `str`가 비었거나 예상된 형식을 가지지 않는다면 변환이 수행되지 않으며, (`str_end`가 null 포인터가 아니라면) `str_end`는 객체에 저장된 `str`의 값을 가리킴

### 파라미터

- `str`: 변환되어야 할 null 종단 바이트 문자열을 가리키는 포인터
- `str_end`: 문자를 가리키는 포인터를 가리키는 포인터
- `base`: 변환된 정수 값의 진법

### 반환값

- 성공: `str`에 대응되는 정수 값
- 변환된 값이 해당하는 반환 타입의 범위를 벗어난 값이라면 범위 오류 발생(`ERANGE`에 `errno` 설정), `LONG_MAX`, `LONG_MIN`, `LLONG_MAX` 또는 `LLONG_MIN`이 반환됨
- 변환할 수 없다면 `0` 반환

### 예제

```c
#include <errno.h>
#include <limits.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

int main(void) {
  // parsing with error handling
  const char* p = "10 200000000000000000000000000000 30 -40 junk";
  printf("Parsing '%s':\n", p);

  for (;;) {
    // errno can be set to any non-zero value by a library function call
    // regardless of whether there was an error, so it needs to be cleared
    // in order to check the error set by strtol
    errno = 0;
    char* end;
    const long i = strtol(p, &end, 10);
    if (p == end) break;

    const bool range_error = errno == ERANGE;
    printf("Extracted '%.*s', strtol returned %ld.", (int)(end - p), p, i);
    p = end;

    if (range_error) printf("\n --> Range error occurred.");

    putchar('\n');
  }

  printf("Unextracted leftover: '%s'\n\n", p);

  // parsing without error handling
  printf("\"1010\" in binary  --> %ld\n", strtol("1010", NULL, 2));
  printf("\"12\"   in octal   --> %ld\n", strtol("12", NULL, 8));
  printf("\"A\"    in hex     --> %ld\n", strtol("A", NULL, 16));
  printf("\"junk\" in base-36 --> %ld\n", strtol("junk", NULL, 36));
  printf("\"012\"  in auto-detected base --> %ld\n", strtol("012", NULL, 0));
  printf("\"0xA\"  in auto-detected base --> %ld\n", strtol("0xA", NULL, 0));
  printf("\"junk\" in auto-detected base --> %ld\n", strtol("junk", NULL, 0));
}
```

가능한 출력:

```text
Parsing '10 200000000000000000000000000000 30 -40 junk':
Extracted '10', strtol returned 10.
Extracted ' 200000000000000000000000000000', strtol returned 9223372036854775807.
 --> Range error occurred.
Extracted ' 30', strtol returned 30.
Extracted ' -40', strtol returned -40.
Unextracted leftover: ' junk'

"1010" in binary  --> 10
"12"   in octal   --> 10
"A"    in hex     --> 10
"junk" in base-36 --> 926192
"012"  in auto-detected base --> 10
"0xA"  in auto-detected base --> 10
"junk" in auto-detected base --> 0
```

</details>

<details>

<summary><h2><code>strtoul, strtoull</code></h2></summary>

헤더 <stdlib.h>에서 정의

- `unsigned long strtoul(const char* str, char** str_end, int base);` (C99 이전)
- `unsigned long strtoul(const char* restrict str, char** restrict str_end, int base)` (C99부터)
- `unsigned long long strtoull(const char* restrict str, char** restrict str_end, int base)` (C99부터)
  - `str`이 가리키는 바이트 문자열의 부호가 없는 정수 값 변환
  - 이 함수는 공백이 아닌 문자가 처음으로 발견될 때까지 모든 공백 문자(`isspace`로 결정됨)를 제거함
  - 유효한 n진수 (`n=base`) 부호가 없는 정수 숫자 표현이 형성될 수 있는 가장 많은 문자열을 가지고 정수 값으로 변환함
  - 유효한 부호가 없는 정수값은 다음으로 구성됨:
    - (선택) 양수 또는 음수 부호
    - (선택) 8진수를 가리키는 접두사 `0` (`base`가 `8` 또는 `0`일 때에만 적용)
    - (선택) 16진수를 가리키는 접두사 `0x` 또는 `0X` (`base`가 `16` 또는 `0`일 때에만 적용)
    - 숫자 시퀀스
  - `base`에 사용 가능한 숫자: {0, 2, 3, ..., 36}
    - 2진수 정수에 사용 가능한 숫자는 {0, 1}
    - 3진수 정수에 사용 가능한 숫자는 {0, 1, 2}
    - 10보다 큰 `base`의 경우 유효한 숫자에 로마자(11진수 정수를 위한 Aa에서 36진수 정수를 위한 Zz까지)도 포함됨
      - 문자의 대소문자는 무시됨
  - 현재 설치된 C 로케일에 의해 추가적인 숫자 포맷이 허용될 수 있음
  - 만약 `base`가 `0`이라면, 진법은 자동으로 감지됨
    - 접두사가 `0`이라면 8진법, `0x` 또는 `0X`라면 16진법, 그 외에는 10진법
    - 입력 시퀀스에 음수 부호가 포함된다면, 숫자 시퀀스에서 계산되는 숫자값은 결과 타입에서의 단항 연산자 마이너스처럼 음수로 계산되나, 부호 반전 후에는 부호 없는 정수의 오버플로우 규칙이 적용됨
  - 함수는 `str_end`가 마지막으로 변환된 숫자 문자 다음 문자를 가리키도록 설정함
    - `str_end`가 null 포인터라면 무시됨

### 파라미터

- `str`: 변환할 null 종단 바이트 문자열을 가리키는 포인터
- `str_end`: 문자를 가리키는 포인터를 가리키는 포인터. 마지막으로 변환된 문자 직후를 가리킬 수 있음
- `base`: 변환된 정수 값의 진법

### 반환값

- 성공: `str` 내용에 대응하는 정수 값 반환
- 변환된 값이 반환 타입의 범위를 벗어나면 범위 오류 발생(`ERANGE`에 `errno` 설정), `ULONG_MAX` 또는 `ULLONG_MAX` 반환
- 변환 불가: `0` 반환

### 예제

```c
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>

int main(void) {
  const char* p = "10 200000000000000000000000000000 30 -40 - 42";

  printf("Parsing '%s':\n", p);

  char* end = NULL;

  for (unsigned long i = strtoul(p, &end, 10); p != end;
       i = strtoul(p, &end, 10)) {
    printf("'%.*s' -> ", (int)(end - p), p);
    p = end;
    if (errno == ERANGE) {
      errno = 0;
      printf("range error, got ");
    }
    printf("%lu\n", i);
  }
  printf("After the loop p prints to '%s'\n", p);
}
```

출력:

```text
Parsing '10 200000000000000000000000000000 30 -40 - 42':
'10' -> 10
' 200000000000000000000000000000' -> range error, got 18446744073709551615
' 30' -> 30
' -40' -> 18446744073709551576
After the loop p points to ' - 42'
```

</details>

<details>

<summary><h2><code>strtof, strtod, strtold</code></h2></summary>

헤더 <stdlib.h>에서 정의

- `float strtof(const char* restrict str, char** restrict str_end);` (1) (C99부터)
- `double strtod(const char* str, char** str_end);` (2) (C99 이전)
- `double strtod(const char* restrict str, char** restrict str_end);` (2) (C99부터)
- `long double strtold(const char* restrict str, char** restrict str_end);` (3) (C99부터)
  - `str`이 가리키는 바이트 문자열의 부동소수점 값 변환
  - 이 함수는 공백이 아닌 문자가 처음으로 발견될 때까지 모든 공백 문자(`isspace`로 결정됨)를 제거함
  - 부동소수점 숫자 표현이 형성될 수 있는 가장 많은 문자열을 가지고 부동소수점 값으로 변환함
  - 유효한 십진법 부동소수점 값은 다음으로 구성됨:
    - (선택) 양수 또는 음수 부호
    - 소수점 문자(현재 C 로케일이 결정)를 포함하거나 포함하지 않는 비어있지 않은 십진법 숫자의 시퀀스(유효숫자를 결정함)
      - (선택) 선택적인 양수 또는 음수 부호와 비어있지 않은 십진법 숫자 시퀀스가 뒤에 붙은 **e** 또는 **E** (밑이 10인 지수 정의)
    - 십육진법 부동소수점 표현. 다음으로 구성됨:
      - (선택) 양수 또는 음수 부호
      - **`0x`** 또는 **`0X`**
      - 소수점 문자(현재 C 로케일이 결정)를 포함하거나 포함하지 않는 비어있지 않은 십진법 숫자의 시퀀스(유효숫자를 결정함)
      - (선택) 선택적인 양수 또는 음수 부호와 비어있지 않은 십진법 숫자 시퀀스가 뒤에 붙은 **`p`** 또는 **`P`** (밑이 2인 지수 정의)
    - 무한 표현. 다음으로 구성됨:
      - (선택) 양수 또는 음수 부호
      - **`INF`** 또는 **`INFINITY`**, 대소문자 구분 안함
    - not-a-number 표현. 다음으로 구성됨:
      - (선택) 양수 또는 음수 부호
      - **`NAN`** 또는 <code><b>NAN</b>(char_sequence)</code> (대소문자 구분 안함)
        - *char_sequence*는 숫자, 라틴 문자, 언더스코어만 포함함
      - 결과: NaN 부동소수점 값
  - 현재 설치된 C 로케일에 따라 다른 표현을 적용할 수 있음
  - 함수는 `str_end`가 마지막으로 변환된 숫자 문자 다음 문자를 가리키도록 설정함
    - `str_end`가 null 포인터라면 무시됨

### 파라미터

- `str`: 변환할 null 종단 바이트 문자열을 가리키는 포인터
- `str_end`: 문자를 가리키는 포인터를 가리키는 포인터

### 반환값

- 성공: `str`의 내용에 해당하는 부동소수점 값 반환
- 변환된 값이 반환값의 범위를 벗어난 경우 범위 오류 발생(`ERANGE`에 `errno` 설정), `HUGE_VAL`, `HUGE_VALF` 또는 `HUGE_VALL`이 반환됨
- 변환을 수행할 수 없다면 `0` 반환

### 예제

```c
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>

int main(void) {
  // parsing with error handling
  const char* p =
      "111.11 -2.22 Nan nan(2) inF 0X1.BC70A3D70A3D7P+6  1.18973e+4932zzz";

  printf("Parsing '%s':\n", p);

  char* end = NULL;

  for (double f = strtod(p, &end); p != end; f = strtod(p, &end)) {
    printf("'%.*s' -> ", (int)(end - p), p);
    p = end;

    if (errno == ERANGE) {
      printf("range error, got ");
      errno = 0;
    }
    printf("%f\n", f);
  }

  // parsing without error handling
  printf("\"  -0.0000000123junk\"  -->  %g\n",
         strtod("  -0.0000000123junk", NULL));
  printf("\"junk\"                 -->  %g\n", strtod("junk", NULL));
}
```

가능한 출력:

```text
Parsing '111.11 -2.22 Nan nan(2) inF 0X1.BC70A3D70A3D7P+6  1.18973e+4932zzz':
'111.11' -> 111.110000
' -2.22' -> -2.220000
' Nan' -> nan
' nan(2)' -> nan
' inF' -> inf
' 0X1.BC70A3D70A3D7P+6' -> 111.110000
'  1.18973e+4932' -> range error, got inf
"  -0.0000000123junk"  -->  -1.23e-08
"junk"                 -->  0
```

</details>

<details>

<summary><h2><code>strfromf, strfromd, strfroml</code></h2></summary>

헤더 <stdlib.h>에서 정의

- `int strfromf(char* restrict s, sizt_t n, const char* restrict format, float fp);` (C23부터)
- `int strfromd(char* restrict s, sizt_t n, const char* restrict format, double fp);` (C23부터)
- `int strfroml(char* restrict s, sizt_t n, const char* restrict format, long double fp);` (C23부터)
  - 부동소수점 값을 바이트 문자열로 변환
  - 다음 특징을 제외하면 `snprintf(s, n, format, fp)`와 동일함
    - 포맷 문자열은 문자 `%`만을 포함해야 함,
    - 포맷 문자열의 정밀도(선택)는 애스터리스크(`*`)을 포함하지 말아야 함
    - 변환 지정어(`double`, `float`, `long double`을 가리키는 a, A, e, E, f, F, g, G)는 함수 접미사에 의해 지시됨 (길이 수식어보다)
    - 다른 포맷 문자열을 가지고 이 함수들을 사용하면 동작의 결과를 예측할 수 없게 됨

### 파라미터

- `s`: 결과를 저장할 문자열을 가리키는 포인터
- `n`: 최대 `n - 1` 개의 문자 저장 가능(1: null 문자)
- `format`: 데이터를 어떻게 변환할지 명시하는 null 종단 바이트 문자열을 가리키는 포인터
- `fp`: 변환할 부동소수점 값

### 반환값

- `n`이 충분히 클 때, 종결 null 문자를 제외한 저장된 문자들의 수
- 반환값이 `n` 보다 작은 음수가 아닌 수일 때 null 종결 출력이 온전히 저장됨 / null 종결 출력이 온전히 저장되면 `n`보다 작은 음수가 아닌 수 반환

### 예제

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
  char buffer[32];
  int written;
  const char* format[] = {"%a", "%A", "%e", "%E", "%f", "%F", "%g", "%G"};

  for (size_t fmt = 0; fmt != sizeof format / sizeof format[0]; ++fmt) {
    written = strfromf(buffer, sizeof buffer, format[fmt], 3.1415f);
    printf("strfromf(... %s ...) = %2i, buffer: \"%s\"\n", format[fmt], written,
           buffer);
  }
  puts("");

  for (size_t fmt = 0; fmt != sizeof format / sizeof format[0]; ++fmt) {
    written = strfromd(buffer, sizeof buffer, format[fmt], 3.1415);
    printf("strfromd(... %s ...) = %2i, buffer: \"%s\"\n", format[fmt], written,
           buffer);
  }
  puts("");

  for (size_t fmt = 0; fmt != sizeof format / sizeof format[0]; ++fmt) {
    written = strfroml(buffer, sizeof buffer, format[fmt], 3.1415);
    printf("strfroml(... %s ...) = %2i, buffer: \"%s\"\n", format[fmt], written,
           buffer);
  }
}
```

출력:

```text
strfromf(... %a ...) = 13, buffer: "0x1.921cacp+1"
strfromf(... %A ...) = 13, buffer: "0X1.921CACP+1"
strfromf(... %e ...) = 12, buffer: "3.141500e+00"
strfromf(... %E ...) = 12, buffer: "3.141500E+00"
strfromf(... %f ...) =  8, buffer: "3.141500"
strfromf(... %F ...) =  8, buffer: "3.141500"
strfromf(... %g ...) =  6, buffer: "3.1415"
strfromf(... %G ...) =  6, buffer: "3.1415"

strfromd(... %a ...) = 20, buffer: "0x1.921cac083126fp+1"
strfromd(... %A ...) = 20, buffer: "0X1.921CAC083126FP+1"
strfromd(... %e ...) = 12, buffer: "3.141500e+00"
strfromd(... %E ...) = 12, buffer: "3.141500E+00"
strfromd(... %f ...) =  8, buffer: "3.141500"
strfromd(... %F ...) =  8, buffer: "3.141500"
strfromd(... %g ...) =  6, buffer: "3.1415"
strfromd(... %G ...) =  6, buffer: "3.1415"

strfroml(... %a ...) = 20, buffer: "0xc.90e5604189378p-2"
strfroml(... %A ...) = 20, buffer: "0XC.90E5604189378P-2"
strfroml(... %e ...) = 12, buffer: "3.141500e+00"
strfroml(... %E ...) = 12, buffer: "3.141500E+00"
strfroml(... %f ...) =  8, buffer: "3.141500"
strfroml(... %F ...) =  8, buffer: "3.141500"
strfroml(... %g ...) =  6, buffer: "3.1415"
strfroml(... %G ...) =  6, buffer: "3.1415"
```

</details>

<details>

<summary><h2><code>strtoimax, strtoumax</code></h2></summary>

헤더 <inttypes.h>에서 정의

- `intmax_t strtoimax(const char* restrict nptr, char** restrict endptr, int base);` (1) (C99부터)
- `uintmax_t strtoumax(const char* restrict nptr, char** restrict endptr, int base);` (2) (C99부터)
  - `nptr`이 가리키는 바이트 문자열의 정수 값 변환
  - 이 함수는 공백이 아닌 문자가 처음으로 발견될 때까지 모든 공백문자(`isspace`로 결정됨)를 제거함
  - 유효한 n진수 (`n=base`) 정수 숫자 표현이 형성될 수 있는 가장 긴 문자열을 정수 값으로 변환
  - 유효한 정수 값은 다음으로 구성됨:
    - (선택) 양수 또는 음수 부호
    - (선택) 8진수를 가리키는 접두사 `0` (`base`가 `8` 또는 `0`일 때에만 적용)
    - (선택) 16진수를 가리키는 접두사 `0x` 또는 `0X` (`base`가 `16` 또는 `0`일 때에만 적용)
    - 숫자 시퀀스
  - `base`에 사용 가능한 숫자: {0, 2, 3, ..., 36}
    - 2진수 정수에 사용 가능한 숫자는 {0, 1}
    - 3진수 정수에 사용 가능한 숫자는 {0, 1, 2}
    - 10보다 큰 `base`의 경우 유효한 숫자에 로마자(11진수 정수를 위한 Aa에서 36진수 정수를 위한 Zz까지)도 포함됨
      - 문자의 대소문자는 무시됨
  - 현재 설치된 C 로케일에 의해 추가적인 숫자 포맷이 허용될 수 있음
  - 만약 `base`가 `0`이라면, 진법은 자동으로 감지됨
    - 접두사가 `0`이라면 8진법, `0x` 또는 `0X`라면 16진법, 그 외에는 10진법
  - 입력 시퀀스에 음수 부호가 포함된다면, 숫자 시퀀스에서 계산되는 숫자값은 결과 타입에서의 단항 연산자 마이너스처럼 음수로 계산됨
  - 함수는 `endptr`가 가리키는 포인터를 마지막으로 변환된 숫자 문자 다음 문자를 가리키도록 설정함
    - `endptr`가 null 포인터라면 무시됨
  - `nptr`이 빈 값이거나 요구된 형식이 아니라면 변환이 수행되지 않으며 (만약 `endptr`가 null 포인터가 아니라면) `nptr`의 값은 `endptr`이 가리키는 객체에 저장됨

### 파라미터

- `nptr`: 변환될 null 종단 문자열을 가리키는 포인터
- `endptr`: 문자를 가리키는 포인터를 가리키는 포인터
- `base`: 변환된 정수 값의 진법

### 반환값

- 성공: `str` 내용에 해당하는 정수 값 반환
- 변환된 값이 반환 타입의 범위를 벗어났다면 범위 오류가 발생하며(`ERANGE`에 `errno` 설정) 적절히 `INTMAX_MAX`, `INTMAX_MIN`, `UINTMAX_MAX` 또는 `0`이 반환됨
- 변환을 수행할 수 없다면 `0` 반환

### 예제

```c
#include <errno.h>
#include <inttypes.h>
#include <stdio.h>
#include <string.h>

int main(void) {
  char* endptr = NULL;

  printf("%ld\n", strtoimax(" -123junk", &endptr, 10));  // base 10
  printf("%ld\n", strtoimax("11111111", &endptr, 2));    // base 2
  printf("%ld\n", strtoimax("XyZ", &endptr, 36));        // base 36
  printf("%ld\n", strtoimax("010", &endptr, 0));         // octal auto-detection
  printf("%ld\n", strtoimax("10", &endptr, 0));    // decimal auto-detection
  printf("%ld\n", strtoimax("0x10", &endptr, 0));  // hexadecimal auto-detection

  // range error: LONG_MAX+1 --> LONG_MAX
  errno = 0;
  printf("%ld\n", strtoimax("9223372036854775808", &endptr, 10));
  printf("%s\n", strerror(errno));
}
```

출력:

```text
-123
255
44027
8
10
16
9223372036854775807
Numerical result out of range
```

</details>
