# Character Manipulation

<details>

  <summary><h2><code>tolower</code></h2></summary>

  `int tolower(int ch);`

  - 주어진 문자를 현재 C 로케일에 의해 정의된 문자 변환 규칙에 따라 소문자로 변환함
  - 기본 "C" 로케일에서는 다음 대문자 `ABCDEFGHIJKLMNOPQRSTUVWXYZ`가 대응하는 소문자 `abcdefghijklmnopqrstuvwxyz`로 교체됨

  ### 파라미터

  - `ch`
    - 변환될 문자
    - `ch`의 값이 `unsigned char`로 나타낼 수 없으며 `EOF`와 같지 않다면 동작을 예측할 수 없음

  ### 반환값

  `ch`의 소문자 버전 또는 현재 C 로케일에 소문자 버전이 없다면 수정되지 않은 `ch`

  ### 예제

  ```C
  #include <ctype.h>
  #include <limits.h>
  #include <locale.h>
  #include <stdio.h>

  int main(void) {
    /* In the default locale: */
    for (unsigned char u = 0; u < UCHAR_MAX; u++) {
      unsigned char l = tolower(u);
      if (l != u) printf("%c%c ", u, l);
    }
    printf("\n\n");

    unsigned char c = '\xb4';  // the character Ž in ISO-8859-15
                              // but ´ (acute accent) in ISO-8859-1
    setlocale(LC_ALL, "en_US.iso88591");
    printf("in iso8859-1, tolower('0x%x') gives 0x%x\n", c, tolower(c));
    setlocale(LC_ALL, "en_US.iso885915");
    printf("in iso8859-15, tolower('0x%x') gives 0x%x\n", c, tolower(c));
  }
  ```

  출력:

  ```text
  Aa Bb Cc Dd Ee Ff Gg Hh Ii Jj Kk Ll Mm Nn Oo Pp Qq Rr Ss Tt Uu Vv Ww Xx Yy Zz
 
  in iso8859-1, tolower('0xb4') gives 0xb4
  in iso8859-15, tolower('0xb4') gives 0xb8
  ```

</details>

<details>

  <summary><h2><code>toupper</code></h2></summary>

  `int toupper(int ch);`

  - 주어진 문자를 현재 C 로케일에 의해 정의된 문자 변환 규칙에 따라 대문자로 변환함
  - 기본 "C" 로케일에서는 다음 소문자가 `abcdefghijklmnopqrstuvwxyz` 대응하는 대문자 `ABCDEFGHIJKLMNOPQRSTUVWXYZ`로 교체됨

  ### 파라미터

  - `ch`
    - 변환될 문자
    - `ch`의 값이 `unsigned char`로 나타낼 수 없으며 `EOF`와 같지 않다면 동작을 예측할 수 없음

  ### 반환값

  `ch`의 대문자 버전 또는 현재 C 로케일에 대문자 버전이 없다면 수정되지 않은 `ch`

  ### 예제

  ```C
  #include <ctype.h>
  #include <limits.h>
  #include <locale.h>
  #include <stdio.h>

  int main(void) {
    // in the default locale:
    for (unsigned char l = 0, u; l != UCHAR_MAX; ++l)
      if ((u = toupper(l)) != l) printf("%c%c ", l, u);
    printf("\n\n");

    unsigned char c = '\xb8';  // the character ž in ISO-8859-15
                              // but ¸ (cedilla) in ISO-8859-1
    setlocale(LC_ALL, "en_US.iso88591");
    printf("in iso8859-1, toupper('0x%x') gives 0x%x\n", c, toupper(c));
    setlocale(LC_ALL, "en_US.iso885915");
    printf("in iso8859-15, toupper('0x%x') gives 0x%x\n", c, toupper(c));
  }
  ```

  출력:

  ```text
  aA bB cC dD eE fF gG hH iI jJ kK lL mM nN oO pP qQ rR sS tT uU vV wW xX yY zZ
  
  in iso8859-1, toupper('0xb8') gives 0xb8
  in iso8859-15, toupper('0xb8') gives 0xb4
  ```

</details>
