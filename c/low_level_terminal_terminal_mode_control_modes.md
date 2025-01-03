# Control Modes

- 이 섹션은 보통 비동기 시리얼 데이터 전송과 연관된 파라미터를 제어하는 터미널 플래그와 필드에 관해 설명함
  - 이러한 플래그는 다른 종류의 터미널 포트(예를 들어 네트워크 연결 가상 터미널)에는 적용이 되지 않을 수 있음
  - 이 모든 것은 `struct termios` 구조체의 `c_cflag` 멤버에 포함됨
- `c_cflag` 멤버 자체는 정수이고, 연산지 `&`, `|`, `^`를 사용해 플래그와 필드 변경 가능
  - `c_cflag` 전체 값을 특정하려고 하지 말 것
  - 대신, 특정 플래그만 변경해 나머지는 변경되지 않도록 함
  - [Setting Terminal Modes Properly](https://sourceware.org/glibc/manual/2.40/html_node/Setting-Modes.html) 참조

## Macro: `tcflag_t CLOCAL`

- 이 비트가 설정되면 터미널이 "로컬"로 연결되어 (캐리어 탐지와 같은) 모뎀 상태 명령이 무시되는 것을 나타냄
- 많은 체제에서 이 비트가 설정되지 않고 `O_NONBLOCK` 플래그가 설정되지 않은 채 `open`을 호출하면, `open`은 모뎀 연결이 체결될 때까지 중단됨
- 이 비트가 설정되지 않고 모뎀이 연결되지 않은 것이 감지되면, 터미널(하나 존재할 때) 제어 프로세스 그룹에 `SIGHUP` 신호가 전송됨
  - 일반적으로 이는 프로세스가 종료되도록 함
  - [Signal Handling](https://sourceware.org/glibc/manual/2.40/html_node/Signal-Handling.html) 참조
  - 연결이 종료된 후 터미널로부터 읽는 것은 end-of-file 조건을 야기하며, 쓰는 것은 `EIO` 에러가 반환되도록 함
  - 터미널 디바이스는 이런 조건을 제거하기 위해 닫혔다 다시 열려야 함

## Macro: `tcflag_t HUPCL`

이 비트가 설정되면 열린 터미널 디바이스를 가진 모든 프로세스가 파일이 닫혔거나 종료되었을 때 모뎀 연결 해제가 되도록 함

## Macro: `tcflag_t CREAD`

- 이 비트가 설정되면 터미널로부터 입력을 읽을 수 있게 됨
- 설정되지 않으면 입력이 도착했을 때 버려짐

## Macro: `tcflag_t CSTOPB`

- 이 비트가 설정되면 두 개의 stop 비트가 사용됨
- 설정되지 않으면 한 개의 stop 비트가 사용됨

## Macro: `tcflag_t PARENB`

- 이 비트가 설정되면 패리티 비트의 생성과 감지가 활성화됨
  - 입력 패리티 오류가 어떻게 다루어지는지 확인하려면 [Input Modes](https://sourceware.org/glibc/manual/2.40/html_node/Input-Modes.html) 참조
- 설정되지 않으면 출력 문자에 패리티 비트가 추가되지 않으며, 입력 문자가 정확한 패리티를 가지는지 확인하지 않음

## Macro: `tcflag_t PARODD`

- 이 비트는 `PARENB`가 설정되었을 때에만 유용함
  - `PARODD`가 설정되었다면 홀수 패리티가 사용됨
  - `PARODD`가 설정되지 않았다면 짝수 패리티가 사용됨

또한 제어 모드 플래그는 문자 당 비트의 숫자를 위한 필드를 포함함. 해당 값을 추출하기 위해 다음과 같이 `CSIZE` 매크로를 마스크로 사용할 수 있음: `settings.c_cflag & CSIZE`

## Macro: `tcflag_t CSIZE`

문자 당 비트의 수를 위한 마스크

## Macro: `tcflag_t CS5`

바이트 당 5 비트를 명시함

## Macro: `tcflag_t CS6`

바이트 당 6 비트를 명시함

## Macro: `tcflag_t CS7`

바이트 당 7 비트를 명시함

## Macro: `tcflag_t CS8`

바이트 당 8 비트를 명시함

<br />

다음의 네 비트는 BSD 확장: BSD 체제와 GNU/Hurd 체제에만 존재함

## Macro: `tcflag_t CCTS_OFLOW`

이 비트가 설정되면 CTS 전선에 기반한 출력 흐름 제어를 활성화함(RS232 프로토콜)

## Macro: `tcflag_t CCTS_IFLOW`

이 비트가 설정되면 RTS 전선에 기반한 입력 흐름 제어를 활성화함(RS232 프로토콜)

## Macro: `tcflag_t MDMBUF`

이 비트가 설정되면 출력의 캐리어 기반 흐름 제어를 활성화함

## Macro: `tcflag_t CIGNORE`

- 이 비트가 설정되면 제어 모드와 라인 속도 값을 전부 무시함
  - `tcsetattr` 호출에서만 유의미함
- `cfgetispeed`와 `cfgetospeed`에 의해 반환되는 `c_cflag` 멤버와 라인 속도 값은 호출에 영향을 받지 않음
- `CIGNORE`는 모든 멤버에 있는 소프트웨어 모드를 전부 설정하지만 `c_cflag`의 하드웨어 상세는 바뀌지 않은 상태로 두고 싶을 때 유용함
  - `tcsetattr`의 `TCSASOFT` 플래그가 동작하는 방법임
- 이 비트는 `tcgetattr`에 의해 채워진 구조체에서는 설정되지 않음
