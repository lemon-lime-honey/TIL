# Character Classification

<details>

  <summary><h2><code>isalnum</code></h2></summary>
  
  `int isalnum(int ch);`

  - 주어진 문자가 현재 C 로케일 상에서 alphanumeric 문자로 분류되는지 확인함
  - 기본 로케일에서는 다음 문자가 alphanumeric 문자임
    - 숫자(`0123456789`)
    - 로마자 대문자(`ABCDEFGHIJKLMNOPQRSTUVWXYZ`)
    - 로마자 소문자(`abcdefghijklmnopqrstuvwxyz`)
  - `ch`의 값이 `unsigned char`로 나타낼 수 없고 `EOF`와 같지 않다면 동작을 예측할 수 없음

  ### 파라미터

  - `ch`: 분류할 문자

  ### 반환값

  문자가 alphanumeric이라면 0이 아닌 값, 그렇지 않다면 `0`

  ### 예제

  다른 로케일에 따른 `isalnum` 사용을 증명함(OS-specific)

  ```C
  #include <ctype.h>
  #include <locale.h>
  #include <stdio.h>

  int main(void) {
    unsigned char c = '\xdf';  // German letter ß in ISO-8859-1

    printf("isalnum('\\xdf') in default C locale returned %d\n", !!isalnum(c));

    if (setlocale(LC_CTYPE, "de_DE.iso88591")) {
      printf("isalnum('\\xdf') in ISO-8859-1 locale returned %d\n", !!isalnum(c));
    }

    return 0;
  }
  ```

  출력:

  ```text
  isalnum('\xdf') in default C locale returned 0
  isalnum('\xdf') in ISO-8859-1 locale returned 1
  ```

</details>

<details>

  <summary><h2><code>isalpha</code></h2></summary>

  `int isaplha(int ch);`

  - 주어진 문자가 alphabetic 문자인지 확인함
    - 대문자, 소문자 가리지 않음
  - "C" 이외의 로케일에서, alphabetic 문자는 `isupper()` 또는 `islower()`가 `true`를 반환하거나 로케일에 의해 alphabetic하다고 간주되는 문자
    - 어떤 경우에서든, `iscntrl()`, `isdigit()`, `ispunct()`, `isspace()`는 이 문자에서는 `false`를 반환함
  - `ch`의 값이 `unsigned char`로 표현될 수 없으며 `EOF`와 같지 않은 경우 동작을 예측할 수 없음

  ### 파라미터

  - `ch`: 분류할 문자

  ### 반환값

  문자가 alphabetic이면 0이 아닌 값, 그렇지 않다면 `0`

  ### 예제

  다른 로케일에 따른 `isalnum` 사용을 증명함(OS-specific)

  ```C
  #include <ctype.h>
  #include <locale.h>
  #include <stdio.h>
  
  int main(void) {
    unsigned char c = '\xdf'; // German letter ß in ISO-8859-1

    printf("isalpha('\\xdf') in default C locale returned %d\n", !!isalpha(c));

    setlocale(LC_CTYPE, "de_DE.iso88591");
    printf("isalpha('\\xdf') in ISO-8859-1 locale returned %d\n", !!isalpha(c));
  }
  ```

  출력:

  ```text
  isalpha('\xdf') in default C locale returned 0
  isalpha('\xdf') in ISO-8859-1 locale returned 1
  ```

</details>

<details>

  <summary><h2><code>islower</code></h2></summary>

  `int islower(int ch);`

  - 주어진 문자가 현재 C 로케일에서 소문자로 분류되는지 확인함
  - 기본 "C" 로케일에서, `islower`는 소문자(`abcdefghijklmnopqrstuvwxyz`)에서만 `true`를 반환함
  - `islower`가 `true`를 반환하면, 동일한 C 로케일에서 `iscntrl()`, `isdigit()`, `ispunct()`, `isspace()`가 이 문자에서는 `false`를 반환하는 것이 보장됨
  - `ch`의 값이 `unsigned char`로 표현될 수 없으며 `EOF`와 같지 않은 경우 동작을 예측할 수 없음

  ### 파라미터

  - `ch`: 분류할 문자

  ### 반환값

  문자가 소문자라면 0이 아닌 값, 그렇지 않다면 `0`

  ### 예제

  ```C
  #include <ctype.h>
  #include <locale.h>
  #include <stdio.h>

  int main(void) {
    unsigned char c = '\xe5';  // letter å in ISO-8859-1
    printf("In the default C locale, \\xe5 is %slowercase\n",
          islower(c) ? "" : "not ");
    setlocale(LC_ALL, "en_GB.iso88591");
    printf("In ISO-8859-1 locale, \\xe5 is %slowercase\n",
          islower(c) ? "" : "not ");
  }
  ```

  출력:

  ```text
  In the default C locale, \xe5 is not lowercase
  In ISO-8859-1 locale, \xe5 is lowercase
  ```

</details>

<details>

  <summary><h2><code>isupper</code></h2></summary>

  `int isupper(int ch);`

  - 주어진 문자가 현재 C 로케일에서 대문자로 분류되는지 확인함
  - 기본 "C" 로케일에서, `isupper`는 대문자(`ABCDEFGHIJKLMNOPQRSTUVWXYZ`)에서만 `true`를 반환함
  - `isupper`가 `true`를 반환하면, 동일한 C 로케일에서 `iscntrl()`, `isdigit()`, `ispunct()`, `isspace()`가 이 문자에서는 `false`를 반환하는 것이 보장됨
  - `ch`의 값이 `unsigned char`로 표현될 수 없으며 `EOF`와 같지 않은 경우 동작을 예측할 수 없음

  ### 파라미터

  - `ch`: 분류할 문자

  ### 반환값

  문자가 대문자라면 0이 아닌 값, 그렇지 않다면 `0`

  ### 예제

  ```C
  #include <ctype.h>
  #include <locale.h>
  #include <stdio.h>

  int main(void) {
    unsigned char c = '\xc6'; // letter Æ in ISO-8859-1
    printf("In the default C locale, \\xc6 is %suppercase\n",
          isupper(c) ? "" : "not " );
    setlocale(LC_ALL, "en_GB.iso88591");
    printf("In ISO-8859-1 locale, \\xc6 is %suppercase\n",
          isupper(c) ? "" : "not " );
  }
  ```

  출력:

  ```text
  In the default C locale, \xc6 is not uppercase
  In ISO-8859-1 locale, \xc6 is uppercase
  ```

</details>

<details>

  <summary><h2><code>isdigit</code></h2></summary>

  `int isdigit(int ch);`

  - 주어진 문자가 숫자인지 확인함(`0123456789`)
  - `ch`의 값이 `unsigned char`로 표현될 수 없으며 `EOF`와 같지 않은 경우 동작을 예측할 수 없음

  ### 파라미터

  - `ch`: 분류할 문자

  ### 반환값

  문자가 숫자라면 0이 아닌 값, 그렇지 않다면 `0`

  ### 참고

  `isdigit`과 `isxdigit`은 현재 설치된 C 로케일에 영향을 받지 않는 유일한 표준 반각 문자 분류 함수임
  - 일부 구현(예: 마이크로소프트 1252 코드 페이지)에서는 추가적인 1바이트 문자를 숫자로 분류하기도 함

  ### 예제

  ```C
  #include <ctype.h>
  #include <limits.h>
  #include <stdio.h>

  int main(void) {
    for (int ndx = 0; ndx <= UCHAR_MAX; ++ndx) {
      if (isdigit(ndx)) {
        printf("%c", ndx);
      }
    }
    printf("\n");
  }
  ```

  출력:

  ```text
  0123456789
  ```

</details>

<details>

  <summary><h2><code>isxdigit</code></h2></summary>

  `int isxdigit(int ch);`

  - 주어진 문자가 16진수 숫자(`0123456789abcdefABCDEF`) 또는 16지수 문자로 분류되는지 확인함
  - `ch`의 값이 `unsigned char`로 표현될 수 없으며 `EOF`와 같지 않은 경우 동작을 예측할 수 없음

  ### 파라미터

  - `ch`: 분류할 문자

  ### 반환값

  문자가 16진수 숫자라면 0이 아닌 값, 그렇지 않다면 `0`

  ### 참고

  `isdigit`과 `isxdigit`은 현재 설치된 C 로케일에 영향을 받지 않는 유일한 표준 반각 문자 분류 함수임
  - 일부 구현(예: 마이크로소프트 1252 코드 페이지)에서는 추가적인 1바이트 문자를 숫자로 분류하기도 함

  ### 예제

  ```C
  #include <ctype.h>
  #include <limits.h>
  #include <stdio.h>

  int main(void) {
    for (int ndx = 0; ndx <= UCHAR_MAX; ++ndx) {
      if (isxdigit(ndx)) {
        printf("%c", ndx);
      }
    }
    printf("\n");
  }
  ```

  출력:

  ```text
  0123456789ABCDEFabcdef
  ```

</details>

<details>

  <summary><h2><code>iscntrl</code></h2></summary>

  `int iscntrl(int ch);`

  - 주어진 문자가 제어문자(0x00 - 0x1F 그리고 0x7F)인지 확인함
  - `ch`의 값이 `unsigned char`로 표현될 수 없으며 `EOF`와 같지 않은 경우 동작을 예측할 수 없음

  ### 파라미터

  - `ch`: 분류할 문자

  ### 반환값

  문자가 제어문자라면 0이 아닌 값, 그렇지 않다면 `0`

  ### 예제

  ```C
  #include <ctype.h>
  #include <locale.h>
  #include <stdio.h>

  int main(void) {
    unsigned char c = '\x94';  // the control code CCH in ISO-8859-1
    printf("In the default C locale, \\x94 is %sa control character\n",
          iscntrl(c) ? "" : "not ");
    setlocale(LC_ALL, "en_GB.iso88591");
    printf("In ISO-8859-1 locale, \\x94 is %sa control character\n",
          iscntrl(c) ? "" : "not ");
  }
  ```

  출력:

  ```text
  In the default C locale, \x94 is not a control character
  In ISO-8859-1 locale, \x94 is a control character
  ```

</details>

<details>

  <summary><h2><code>isgraph</code></h2></summary>

  `int isgraph(int ch);`

  - 주어진 문자가 인쇄 표현을 가지는지 확인함
    - 숫자(`0123456789`)
    - 대문자(`ABCDEFGHIJKLMNOPQRSTUVWXYZ`)
    - 소문자(`abcdefghijklmnopqrstuvwxyz`)
    - 구두점(`!"#$%&'()*+,-./:;<=>?@[\]^_\`{|}~`)
    - 현재 C 로케일 상에서 위의 문자 이외의 문자 중 인쇄 문자로 간주되는 문자
  - `ch`의 값이 `unsigned char`로 표현될 수 없으며 `EOF`와 같지 않은 경우 동작을 예측할 수 없음

  ### 파라미터

  - `ch`: 분류할 문자

  ### 반환값

  문자가 인쇄 표현을 가지는 문자라면 0이 아닌 값, 그렇지 않다면 `0`

  ### 예제

  ```C
  #include <ctype.h>
  #include <locale.h>
  #include <stdio.h>

  int main(void) {
    unsigned char c = '\xb6';  // the character ¶ in ISO-8859-1
    printf("In the default C locale, \\xb6 is %sgraphical\n",
          isgraph(c) ? "" : "not ");
    setlocale(LC_ALL, "en_GB.iso88591");
    printf("In ISO-8859-1 locale, \\xb6 is %sgraphical\n",
          isgraph(c) ? "" : "not ");
  }
  ```

  출력:

  ```text
  In the default C locale, \xb6 is not graphical
  In ISO-8859-1 locale, \xb6 is graphical
  ```

</details>

<details>

  <summary><h2><code>isspace</code></h2></summary>

  `int isspace(int ch);`

  - 주어진 문자가 다음에 해당하는지 확인함
    - 표준 공백 문자
      - 공백(0x20, `' '`)
      - 폼 피드(0x0C, `'\f'`)
      - 라인 피드(0x0A, `'\n'`)
      - 캐리지 리턴(0x0D, `'\r'`)
      - 수평 탭(0x09, `'\t'`)
      - 수직 탭(0x0B, `'\v'`)
    - 또는 로케일에 따라 공백으로 간주되는 문자
  - `ch`의 값이 `unsigned char`로 표현될 수 없으며 `EOF`와 같지 않은 경우 동작을 예측할 수 없음

  ### 파라미터

  - `ch`: 분류할 문자

  ### 반환값

  문자가 공백 문자라면 0이 아닌 값, 그렇지 않다면 `0`.

  ### 예제

  ```C
  #include <ctype.h>
  #include <limits.h>
  #include <stdio.h>

  int main(void) {
    for (int ndx = 0; ndx <= UCHAR_MAX; ++ndx) {
      if (isspace(ndx)) {
        printf("0x%02x ", ndx);
      }
    }
  }
  ```

  출력:

  ```text
  0x09 0x0a 0x0b 0x0c 0x0d 0x20
  ```

</details>

<details>

  <summary><h2><code>isblank</code></h2></summary>

  `int isblank(int ch);` (C99부터)

  - 주어진 문자가 현재 C 로케일에서 공백문자로 간주되는지 확인
    - 기본 C 로케일에서는 오직 공백(0x20)과 수평 탭(0x09)만이 공백으로 분류됨
  - `ch`의 값이 `unsigned char`로 표현될 수 없으며 `EOF`와 같지 않은 경우 동작을 예측할 수 없음

  ### 파라미터

  - `ch`: 분류할 문자

  ### 반환값

  문자가 공백 문자라면 0이 아닌 값, 그렇지 않다면 `0`.

  ### 예제

  ```C
  #include <ctype.h>
  #include <limits.h>
  #include <stdio.h>

  int main(void) {
    for (int ndx = 0; ndx <= UCHAR_MAX; ndx++)
      if (isblank(ndx)) printf("0x%02x\n", ndx);
  }
  ```

  출력:

  ```text
  0x09
  0x20
  ```

</details>

<details>

  <summary><h2><code>isprint</code></h2></summary>

  `int isprint(int ch);`

  - 주어진 문자가 출력 가능한지 확인함
    - 숫자(`0123456789`)
    - 대문자(`ABCDEFGHIJKLMNOPQRSTUVWXYZ`)
    - 소문자(`abcdefghijklmnopqrstuvwxyz`)
    - 구두점(`!"#$%&'()*+,-./:;<=>?@[\]^_\`{|}~`)
    - 공백
    - 또는 로케일에 따라 출력 가능하다고 간주되는 문자
  - `ch`의 값이 `unsigned char`로 표현될 수 없으며 `EOF`와 같지 않은 경우 동작을 예측할 수 없음

  ### 파라미터

  - `ch`: 분류할 문자

  ### 반환값

  문자가 출력 가능한 문자라면 0이 아닌 값, 그렇지 않다면 0

  ### 예제

  ```C
  #include <ctype.h>
  #include <locale.h>
  #include <stdio.h>

  int main(void) {
    unsigned char c = '\xa0';  // the non-breaking space in ISO-8859-1
    printf("In the default C locale, \\xa0 is %sprintable\n",
          isprint(c) ? "" : "not ");
    setlocale(LC_ALL, "en_GB.iso88591");
    printf("In ISO-8859-1 locale, \\xa0 is %sprintable\n",
          isprint(c) ? "" : "not ");
  }
  ```

  출력:

  ```text
  In the default C locale, \xa0 is not printable
  In ISO-8859-1 locale, \xa0 is printable
  ```

</details>

<details>

  <summary><h2><code>ispunct</code></h2></summary>

  `int ispunct(int ch);`

  - 주어진 문자가 현재 C 로케일에서 구두점 문자인지 확인함
    - 기본 C 로케일에서는 `!"#$%&'()*+,-./:;<=>?@[\]^_\`{|}~`을 구두점으로 분류함
  - `ch`의 값이 `unsigned char`로 표현될 수 없으며 `EOF`와 같지 않은 경우 동작을 예측할 수 없음

  ### 파라미터

  - `ch`: 분류할 문자

  ### 반환값

  문자가 구두점 문자라면 0이 아닌 값, 그렇지 않다면 0

  ### 예제

  ```C
  #include <ctype.h>
  #include <locale.h>
  #include <stdio.h>

  int main(void) {
    unsigned char c =
        '\xd7';  // the character × (multiplication sign) in ISO-8859-1
    printf("In the default C locale, \\xd7 is %spunctuation\n",
          ispunct(c) ? "" : "not ");
    setlocale(LC_ALL, "en_GB.iso88591");
    printf("In ISO-8859-1 locale, \\xd7 is %spunctuation\n",
          ispunct(c) ? "" : "not ");
  }
  ```

  출력:

  ```text
  In the default C locale, \xd7 is not punctuation
  In ISO-8859-1 locale, \xd7 is punctuation
  ```

</details>