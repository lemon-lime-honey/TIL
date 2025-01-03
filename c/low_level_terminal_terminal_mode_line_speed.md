# Line Speed

- 터미널 회선 속도는 컴퓨터에게 터미널에서 얼마나 빨리 데이터를 읽고 써야 하는지 알려줌
- 터미널이 실제 시리얼 회선과 연결되었다면, 명시한 터미널 속도는 실제로 회선을 제어함
  - 터미널의 속도 개념과 일치하지 않는다면 통신이 동작하지 않음
  - 실제 시리얼 포트는 특정한 표준 속도만을 허용함
  - 또한, 특정 하드웨어는 모든 표준 속도를 지원하지 않을 수도 있음
  - 속도를 0으로 명시하는 것은 dial up 연결이 끊어지게 하고, 모뎀 제어 신호를 끔
- 터미널이 실제 시리얼 회선이 아니라면(예를 들어 네트워크 연결이라면), 회선 속도는 데이터 전송 속도에 영향을 미치지 않을 것이지만, 어떤 프로그램들은 이를 필요한 패딩의 양을 결정하는데 사용함
  - 실제 터미널의 실제 속도와 일치하는 회선 속도로 명시하는 것이 최선이지만, 패딩의 양을 다양하게 하기 위해 서로 다른 여러 값을 가지고 안전히 실험할 수도 있음
- 사실 각 터미널에는 두 개의 회선속도가 존재함
  - 입력, 출력
  - 두 값을 독립적으로 설정할 수 있지만, 대부분의 터미널은 양방향에 같은 속도를 사용함
- 속도 값은 `struct termios` 구조체에 저장되지만 `struct termios` 구조체 내의 값에 직접 접근하지 말 것
  - 대신, 다음의 함수를 이용해 값을 읽고 저장

## Function: `speed_t cfgetospeed(const struct termios *termios-p)`

- Preliminary: | MT-Safe | AS-Safe | AC-Safe | [POSIX Safety Concepts](https://sourceware.org/glibc/manual/2.40/html_node/POSIX-Safety-Concepts.html) 참조
- 구조체 `*termios-p`에 저장된 출력 회선 속도 반환

## Function: `speed_t cfgetispeed(const struct termios *termios-p)`

- Preliminary: | MT-Safe | AS-Safe | AC-Safe | [POSIX Safety Concepts](https://sourceware.org/glibc/manual/2.40/html_node/POSIX-Safety-Concepts.html) 참조
- 구조체 `*termios-p`에 저장된 입력 회선 속도 반환

## Function: `int cfsetospeed(const struct termios *termios-p, speed_t speed)`

- Preliminary: | MT-Safe | AS-Safe | AC-Safe | [POSIX Safety Concepts](https://sourceware.org/glibc/manual/2.40/html_node/POSIX-Safety-Concepts.html) 참조
- `speed`를 구조체 `*termios-p`에 출력 속도로 저장
- 일반적인 반환값 `0`
- 오류 발생 시 `-1` 반환
  - `speed`가 속도가 아닌 경우 `cfsetospeed`는 `-1` 반환

## Function: `int cfgetispeed(const struct termios *termios-p, speed_t speed)`

- Preliminary: | MT-Safe | AS-Safe | AC-Safe | [POSIX Safety Concepts](https://sourceware.org/glibc/manual/2.40/html_node/POSIX-Safety-Concepts.html) 참조
- `speed`를 구조체 `*termios-p`에 입력 속도로 저장
- 일반적인 반환값 `0`
- 오류 발생 시 `-1` 반환
  - `speed`가 속도가 아닌 경우 `cfsetispeed`는 `-1` 반환

## Function: `int cfsetspeed(const struct termios *termios-p, speed_t speed)`

- Preliminary: | MT-Safe | AS-Safe | AC-Safe | [POSIX Safety Concepts](https://sourceware.org/glibc/manual/2.40/html_node/POSIX-Safety-Concepts.html) 참조
- `speed`를 구조체 `*termios-p`에 입력과 출력 속도로 저장
- 일반적인 반환값 `0`
- 오류 발생 시 `-1` 반환
  - `speed`가 속도가 아닌 경우 `cfsetspeed`는 `-1` 반환
- 4.4 BSD의 확장 함수

## Data Type: `speed_t`

회선 속도를 표현하기 위해 사용되는 부호 없는 정수 데이터형

<br />

- 함수 `cfsetospeed`와 `cfsetispeed`는 시스템이 단순히 다룰 수 없는 속도값에 대해서만 오류로 보고함
  - 기본적으로 수용 가능한 속도 값을 명시했다면 이 함수들은 정상적으로 동작함
  - 그러나 위 함수들은 특정한 하드웨어 디바이스가 명시된 속도를 실제로 지원하는지는 확인하지 않음
    - 정확히는, 속도를 설정할 디바이스가 어떤 것인지 모름
  - `tcsetattr`을 특정 기기가 다룰 수 없는 값으로 설정하기 위해 사용한다면 `tcsetattr`은 `-1`을 반환함

### Portability Note

- GNU C 라이브러리에서는, 위의 함수들은 입력으로 초당 비트로 측정된 속도를 받고, 초당 비트로 측정된 속도를 반환함
- 다른 라이브러리는 특수한 코드로 지시되는 코드를 필요로 함
  - POSIX.1 이식성을 가지려면 속도를 나타내기 위해 다음 기호 중 하나를 사용해야 함
    - 정밀한 숫자값은 시스템에 따라 다르지만, 각각의 이름은 고정된 의미를 가짐
    - 예: `B110`은 110bps, `B300`은 300bps
    - 다음이 아닌 속도를 나타내는 이식성 있는 방법은 없는데, 다음 속도들은 일반적인 시리얼 회선이 지원할 수 있는 속도
      - `B0` `B50` `B75` `B110` `B134` `B150` `B200` `B300` `B600` `B1200` `B1800`  
        `B2400` `B4800` `B9600` `B19200` `B38400` `B57600` `B115200` `B230400` `B460800`
- BSD는 두 개의 추가적인 속도 기호를 별칭으로 정의함
  - EXTA는 `B19200`
  - EXTB는 `B38400`
  - 이 별칭들은 사용되지 않음
