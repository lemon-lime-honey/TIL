# Noncanonical Input

- 비정규 입력 모드에서 ERASE와 KILL과 같은 특수 수정 문자는 무시됨
  - 입력 수정을 위한 시스템 편의 기능은 비정규 입력 모드에서는 비활성화되기 때문에 (신호 또는 흐름 제어 목적이 아니라면) 모든 입력 문자는 입력된 그대로 애플리케이션 프로그램에 전달됨
  - 적절하다면, 사용자에게 입력을 수정하는 방법을 제공하는 것은 애플리케이션 프로그램에 달림
- 비정규 모드는 유효한 입력을 받을 수 있는지 여부와 얼마나 오래 기다릴 것인지를 제어하기 위해 MIN과 TIME이라는 특수 파라미터를 제공함
  - 대기를 피하기 위해, 입력이 유효하다면 즉시 반환하기 위해, 또는 입력이 없는 상태로 반환하기 위해 이를 사용할 수 있음
- MIN과 TIME은 `struct termios` 구조체의 멤버인 `c_cc` 배열의 원소로 저장됨
  - 이 배열의 각 원소는 특정한 역할을 가지며, 각 원소는 그 원소의 인덱스를 나타내는 기호 상수를 가짐
  - `VMIN`과 `VTIME`은 MIN과 TIME 슬롯의 배열에서의 인덱스를 나타내는 이름

## Macro: `int VMIN`

- `c_cc` 배열의 MIN 슬롯을 위한 서브스크립트
  - `termios.c_cc[VMIN]`은 값 그 자체
- MIN 슬롯은 비정규 입력 모드에서만 유효함
  - `read`가 반환하기 위해 입력 큐에 사용 가능한 바이트의 최소 수를 명시함

## Macro: `int VTIME`

- `c_cc` 배열의 TIME 슬롯을 위한 서브스크립트
  - `termios.c_cc[VTIME]`은 값 그 자체
- TIME 슬롯은 비정규 입력 모드에서만 유의미함
  - 반환 전에 입력을 얼마나 오래 기다릴지 0.1초 단위로 명시함

<br />

MIN과 TIME 값은 `read`가 언제 반환되어야 하는가에 관한 기준을 결정하기 위해 상호작용함

- 그 중 어느 것이 0이 아닌 값인지에 따라 정확한 의미가 달라짐
- 가능한 네 가지 경우가 존재
  - TIME, MIN 모두 0이 아님
    - TIME은 더 많은 입력이 도착할지 확인하기 위해 각 문자를 입력한 이후 얼마나 오래 기다려야 할지 명시함
    - 첫 번째 문자를 받은 후, `read`는 MIN 바이트가 도착하거나 추가적인 입력 없이 TIME이 지났을 때까지 기다림
    - `read`는 TIME이 먼저 지나더라도 언제나 첫 번째 문자가 도착할 때까지 정지시킴
    - `read`는 큐에 MIN보다 많은 문자가 있다면 MIN보다 많은 문자를 반환할 수 있음
  - TIME, MIN 모두 0
    - `read`는 요청된 숫자까지 가능한 한 많은 문자를 즉시 반환함
    - 즉시 반환 가능한 입력이 없다면 0 반환
  - MIN은 0, TIME은 0이 아님
    - `read`는 입력이 사용 가능할 때까지 TIME 동안 기다림
      - 단일 바이트의 사용 가능성은 `read` 요청을 만족시키고 `read`가 반환하게 하는데 충분함
    - 반환할 때, 요청된 숫자까지 가능한 한 많은 문자를 즉시 반환함
    - 타이머가 끝나기 전에 사용 가능한 입력이 없다면, `read`는 0 반환
  - MIN은 0이 아님, TIME은 0
    - `read`는 큐에 최소한 MIN 바이트의 사용 가능한 문자가 존재할 때까지 대기
      - 그때 `read`는 요청된 숫자까지 가능한 한 많은 문자를 즉시 반환함
      - 큐에 MIN보다 많은 문자가 있다면 MIN보다 많은 문자를 반환할 수 있음

<br />

MIN이 50인데 10 바이트만 읽으라고 요청하면 어떻게 될까?

- 보통 `read`는 버퍼에 50 바이트가 저장될 때까지 기다림(또는, 더 일반적으로는, 위에서 설명한 대기 조건이 만족될 때까지)
- 그리고 10을 읽고, 나머지 40바이트는 운영 체제에서 버퍼링되어 나중에 읽기 위해 남겨짐

### Portability Note

- 어떤 시스템에서는 MIN과 TIME 슬롯은 사실상 EOF과 EOL 슬롯과 같음
- 이는 MIN과 TIME이 비정규 입력에서만 사용되고, EOF와 EOL 슬롯이 정규 입력에서만 사용되기 때문에 심각한 문제를 일으키지는 않지만, 깔끔하진 않음
- GNU C 라이브러리는 이러한 용도로 별도의 슬롯을 할당함

#### Function: `void cfmakeraw(struct termios *termios-p)`

- Preliminary: | MT-Safe | AS-Safe | AC-Safe | [POSIX Safety Concepts](https://sourceware.org/glibc/manual/2.40/html_node/POSIX-Safety-Concepts.html)
- 이 함수는 전통적으로 BSD에서 "raw mode"라고 불린 `*termios-p`를 설정하는 쉬운 방법을 제공함
- 비정규 입력 사용
- 수정되지 않은 채널을 터미널에 제공하기 위해 대부분의 처리를 끔
- 정확히 이를 수행함:
  ```C
  termios-p->c_iflag &= ~(IGNBRK|BRKINT|PARMRK|ISTRIP|INLCR|IGNCR|ICRNL|IXON);
  termios-p->c_oflag &= ~OPOST:
  termios-p->c_lflag &= ~(ECHO|ECHONL|ICANON|ISI|IEXTEN);
  termios-p->c_cflag &= ~(CSIZE|PARENB);
  termios-p->c_cflag |= CS8;
  ```
