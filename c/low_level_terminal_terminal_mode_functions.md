# Terminal Mode Functions

## Function: `int tcgetattr(int filedes, struct termios *termios-p)`

- Preliminary: | MT-Safe | AS-Safe | AC-Safe | [POSIX Safety Concepts](https://sourceware.org/glibc/manual/2.40/html_node/POSIX-Safety-Concepts.html) 참조
- 이 함수는 파일 기술자 `filedes`를 이용해 터미널 디바이스의 속성을 확인하기 위해 사용됨
  - 속성은 `termios-p`가 가리키는 구조체 내로 반환됨
- 반환값
  - 성공: `0`
  - 실패: `-1`
    - 이 함수에 대해 다음의 `errno` 에러 조건이 정의됨
      - `EBADF`: `filedes` 인자가 유효한 파일 기술자가 아님
      - `ENOTTY`: `filedes`가 터미널과 연결되어 있지 않음

## Function: `int tcsetattr(int filedes, int when, struct termios *termios-p)`

- Preliminary: | MT-Safe | AS-Safe | AC-Safe | [POSIX Safety Concepts](https://sourceware.org/glibc/manual/2.40/html_node/POSIX-Safety-Concepts.html) 참조
- 이 함수는 파일 기술자 `filedes`를 이용해 터미널 디바이스의 속성을 설정하기 위해 사용됨
  - 새로운 속성은 `termios-p`가 가리키는 구조체에서 가져옴
  - `when` 인수는 이미 큐에 저장된 입력과 출력을 어떻게 다룰 것인지 명시하며, 다음 값 중 하나를 가짐
    - `TCSANOW`: 즉시 바꿈
    - `TCSADRAIN`
      - 큐에 존재하는 모든 출력 값이 출력될 때까지 기다린 후 바꿈
      - 파라미터 변경이 출력에 영향을 줄 때 보통 이 옵션을 사용함
    - `TCSAFLUSH`: `TCSADRAIN`과 유사하나 큐에 존재하는 입력을 버림
    - `TCSASOFT`
      - 위의 값들에 더할 수 있는 플래그 비트
        - 터미널 하드웨어의 상태 변화 방지
      - BSD 확장: BSD, GNU/Hurd 체제에서만 지원함
      - `termios-p`가 가리키는 구조체의 `c_cflag` 멤버에 `CIGNORE` 비트를 설정하는 것과 동일함
        - `CIGNORE`에 관한 설명은 [Control Modes](https://sourceware.org/glibc/manual/2.40/html_node/Control-Modes.html)에서 확인 가능
- 이 함수가 백그라운드 프로세스를 제어하는 터미널에서 호출되었다면, 프로세스가 터미널에 입력을 시도하는 것과 같은 방식으로 보통은 프로세스 그룹 내의 모든 프로세스에 `SIGTTOU` 신호가 송신됨
  - 만약 호출 프로세스 자체가 `SIGTTOU` 신호를 무시하거나 막아 동작이 수행되었으나 신호가 송신되지 않은 경우가 예외
  - [Job Control](https://sourceware.org/glibc/manual/2.40/html_node/Job-Control.html) 참조
- 반환값
  - 성공: `0`
  - 실패: `-1`
    - 이 함수에 대해 다음의 `errno` 에러 조건이 정의됨
      - `EBADF`: `filedes` 인자가 유효한 파일 기술자가 아님
      - `ENOTTY`: `filedes`가 터미널과 연결되어 있지 않음
      - `EINVAL`: `when` 인수의 값이 유효하지 않거나 `termios-p` 인수 내의 데이터에 문제가 있는 경우

<br />

- `tcgetattr`와 `tcsetattr`가 파일 기술자로 터미널 디바이스를 명시함에도 불구하고, 속성은 터미널 디바이스 자체의 속성이지 파일 기술자의 속성이 아님
  - 이는 터미널 속성을 변경하는 것의 효과가 영속적이라는 것을 의미함
  - 다른 프로세스가 이후에 터미널 파일을 연다면, 원래 명시한 파일 기술자의 속성을 변경하지 않았더라도 변경된 속성을 보게 될 것
- 비슷하게, 만약 하나의 프로세스가 동일한 터미널 디바이스에 대한 복수의, 또는 복제된 파일 기술자를 가지고 있다면 터미널 속성을 변경하는 것은 이러한 파일 기술자 모두의 입력과 출력에 영향을 미침
  - 이는, 예를 들어 하나의 터미널로부터 읽기 위해 일반적인 라인 버퍼링, 에코 모드 파일 기술자나 스트림을 여는 동시에 동일한 터미널로부터 읽기 위해 또 다른 단일 문자 버퍼링, 논에코 모드 파일 기술자나 스트림을 열 수 없다는 것을 의미함
  - 그 대신 명시적으로 터미널을 한 모드에서 다른 모드로 변경해야 함
