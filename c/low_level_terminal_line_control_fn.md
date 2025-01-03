# Line Control Functions

- 다음의 함수는 터미널 디바이스에 여러 종류의 제어 동작을 수행함
- 터미널 접근에 관해, 출력하는 것과 같이 취급됨
  - 다음 함수 중 어떤 것이라도 제어 중인 터미널의 백그라운드 프로세스에서 사용된다면, 보통은 프로세스 그룹 내의 모든 프로세스가 `SIGTTOU` 신호를 수신함
  - 예외: 호출 프로세스 자체가 `SIGTTOU` 신호를 무시하거나 막아 동작은 수행되었으나 신호가 송신되지 않은 경우
  - [Job Control](https://sourceware.org/glibc/manual/2.40/html_node/Job-Control.html) 참조

## Function: `int tcsendbreak(int filedes, int duration)`

- Preliminary: | MT-Unsafe race:tcattr(filedes)/bsd | AS-Unsafe | AC-Unsafe corrupt/bsd | [POSIX Safety Concepts](https://sourceware.org/glibc/manual/2.40/html_node/POSIX-Safety-Concepts.html) 참조
- 파일 기술자 `filedes`와 연결된 터미널에 0 비트로 이루어진 스트림을 전송해 브레이크 조건을 생성함
- 브레이크의 지속 시간은 `duration` 인자에 의해 제어됨
  - 0이라면 지속 시간은 0.25초에서 0.5초 사이
  - 0이 아닌 값은 운영체제에 따라 의미가 다름
- 터미널이 비동기 시리얼 데이터 포트가 아니라면 아무 동작도 수행하지 않음
- 반환값
  - 일반적으로 `0`
  - 오류가 발생했을 때 `-1`
  - 이 함수를 위해 다음의 `errno` 오류 조건이 정의됨
    - `EBADF`: `filedes`가 유효한 파일 기술자가 아님
    - `ENOTTY`: `filedes`가 터미널 디바이스와 연결되지 않음

## Function: `int tcdrain(int filedes)`

- Preliminary: | MT-Safe | AS-Safe | AC-Safe | [POSIX Safety Concepts](https://sourceware.org/glibc/manual/2.40/html_node/POSIX-Safety-Concepts.html) 참조
- 모든 대기열 출력이 터미널 `filedes`로 전송될 때까지 대기
- 이 함수는 멀티스레드 프로그램의 취소 지점임
  - `tcdrain`이 호출된 시점에 스레드가 어떤 자원들(메모리, 파일 기술자, 세마포어 등)을 할당하면 문제가 발생함
  - 스레드가 취소되면, 이 자원들은 프로그램이 종료될 때까지 할당된 상태로 머무름
  - 이를 방지하려면 `tcdrain` 호출은 취소 핸들러를 사용해 보호되어야 함
- 반환값
  - 일반적으로 `0`
  - 오류가 발생했을 때 `-1`
  - 이 함수를 위해 다음의 `errno` 오류 조건이 정의됨
    - `EBADF`: `filedes`가 유효한 파일 기술자가 아님
    - `ENOTTY`: `filedes`가 터미널 디바이스와 연결되지 않음
    - `EINTR`
      - 신호 전달로 동작이 방해를 받은 경우
      - [Primitives Interrupted by Signals](https://sourceware.org/glibc/manual/2.40/html_node/Interrupted-Primitives.html) 참조

## Function `int tcflush(int filedes, int queue)`

- Preliminary: | MT-Safe | AS-Safe | AC-Safe | [POSIX Safety Concepts](https://sourceware.org/glibc/manual/2.40/html_node/POSIX-Safety-Concepts.html) 참조
- 터미널 파일 `filedes`와 연결된 입력 그리고/또는 출력 대기열을 비우기 위해 사용됨
  - `queue` 인자는 어느 대기열을 비울지 명시하며, 다음 값 중 하나
    - `TCIFLUSH`: 아직 읽지는 않았으나 받은 모든 입력 데이터 비우기
    - `TCOFLUSH`: 아직 전송되지 않았으나 쓰인 모든 출력 데이터 비우기
    - `TCIOFLUSH`: 입력과 출력 대기열 모두 비우기
- 반환값
  - 일반적으로 `0`
  - 오류가 발생했을 때 `-1`
  - 이 함수를 위해 다음의 `errno` 오류 조건이 정의됨
    - `EBADF`: `filedes`가 유효한 파일 기술자가 아님
    - `ENOTTY`: `filedes`가 터미널 디바이스와 연결되지 않음
    - `EINVAL`: `queue` 인자에 나쁜 값이 제공됨
- 이 함수의 이름이 `tcflush`인 것은 유감스러운 일임
  - "flush"라는 표현이 보통 꽤 다른 동작, 모든 출력이 전송될 때까지 기다리는 동작에 주로 사용되기 때문
  - 입력이나 출력을 버리는데 사용하는 것은 혼란스러울 수 있음
  - 불행히도, `tcflush`라는 이름은 POSIX에서 유래하기 때문에 변경할 수 없음

## Function `int tcflow(int filedes, int action)`

- Preliminary: | MT-Unsafe race:tcattr(filedes)/bsd | AS-Unsafe | AC-Safe | [POSIX Safety Concepts](https://sourceware.org/glibc/manual/2.40/html_node/POSIX-Safety-Concepts.html) 참조
- `filedes`가 명시한 터미널 파일에 대한 XON/XOFF 흐름 제어에 관한 동작을 수행하기 위해 사용됨
- `action` 인자는 어떤 동작을 수행할지 명시하며, 다음 중 하나의 값일 수 있음
  - `TCOOFF`: 출력 전송 중단
  - `TCOON`: 출력 전송 재개
  - `TCIOFF`: STOP 문자 전송
  - `TCION`: START 문자 전송
  - STOP과 START 문자에 대해서는 [Special Characters](https://sourceware.org/glibc/manual/2.40/html_node/Special-Characters.html) 참조
- 반환값
  - 일반적으로 `0`
  - 오류가 발생했을 때 `-1`
  - 이 함수를 위해 다음의 `errno` 오류 조건이 정의됨
    - `EBADF`: `filedes`가 유효한 파일 기술자가 아님
    - `ENOTTY`: `filedes`가 터미널 디바이스와 연결되지 않음
    - `EINVAL`: `action` 인자에 나쁜 값이 제공됨
