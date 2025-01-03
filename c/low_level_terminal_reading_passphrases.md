# Reading Passphrases

- 비밀 구절(passphrase)를 읽을 때, 비밀을 지키기 위해 스크린에 표시하는 것을 피하는 것이 바람직함
- 다음 함수는 이를 편리한 방식으로 다룸

## Function: `char *getpass(const char *prompt)`

- Preliminary: | MT-Unsafe term | AS-Unsafe heap lock corrupt | AC-Unsafe term lock corrupt | [POSIX Safety Concepts](https://sourceware.org/glibc/manual/2.40/html_node/POSIX-Safety-Concepts.html) 참조
- `prompt`를 출력하고, 터미널에서 문자열을 에코 없이 읽음
  - 가능하다면 실제 터미널, `/dev/tty`를 연결해 사용자가 파일에 일반 텍스트 암호를 넣지 않도록 유도함
  - 그렇지 않은 경우 `stdin`과 `stderr`를 사용함
- `ISIG` 터미널 속성([Local Modes](https://sourceware.org/glibc/manual/2.40/html_node/Local-Modes.html) 참조)을 사용해 INTR, QUIT, SUSP 문자를 터미널에서 비활성화함
- `getpass` 호출 이전과 이후에 터미널이 초기화되어 잘못 입력된 암호의 문자가 우연히 보이지 않도록 함
- 다른 C 라이브러리에서는 `getpass`는 암호의 첫 `PASS_MAX` 바이트만을 반환할 수 있음
  - GNU C 라이브러리는 제한이 없기 때문에 `PASS_MAX`가 정의되지 않음
- 이 함수의 프로토타입은 `unistd.h`에 있으며, `PASS_MAX`는 `limits.h`에서 정의될 것

<br />

이 정확한 연산 모음은 모든 가능한 상황에 맞지 않을 수 있음

- 그런 경우, 사용자가 직접 `getpass` 대체 함수를 작성하는 것이 추천됨
- 예를 들어, 다음과 같은 매우 단순한 대체 함수를 작성할 수 있음

  ```C
  #include <stdio.h>
  #include <termios.h>
  #include <unistd.h>

  ssize_t my_getpass(char **lineptr, size_t *n, FILE *stream) {
    struct termios old, new;
    int nread;

    // 에코 끄기
    if (tcgetattr(fileno(stream), &old) != 0) return -1;
    new = old;
    new.c_lflag &= ~ECHO;
    if (tcsetattr(fileno(stream), TCSAFLUSH, &new) != 0) return -1;

    // 암호 읽기
    nread = getline(lineptr, n, stream);

    // 터미널 복원
    (void)tcsetattr(fileno(stream), TCSAFLUSH, &old);

    return nread;
  }
  ```

- 대체 함수는 `getline`([Line-Orientedc Input](https://sourceware.org/glibc/manual/2.40/html_node/Line-Input.html) 참조)와 같은 파라미터를 가짐
  - 사용자는 원하는 모든 프롬프트를 출력해야 함
