# Special Characters for Flow Control

- 다음의 특수 문자들은 정규 또는 비정규 입력 모드에서 사용 가능하지만 `IXON`과 `IXOFF` 플래그에 의해 사용이 제어됨
- [Input Modes](https://sourceware.org/glibc/manual/2.40/html_node/Input-Modes.html) 참조

## Macro: `int VSTART`

- 특수 제어 문자 배열의 START 문자를 위한 서브스크립트
  - `termios.c_cc[VSTART]`은 문자 그 자체
- START 문자는 `IXON`과 `IXOFF` 입력 모드를 지원하기 위해 사용됨
  - `IXON`이 설정되었을 때 START 문자를 받으면 중단된 출력을 재개함
    - START 문자 자체는 제거됨
  - `IXANY`가 설정되었을 때 아무 문자나 받으면 중단된 출력을 재개함
    - START 문자가 아니라면 제거되지 않음
  - `IXOFF`가 설정되었다면 시스템 또한 터미널에 START 문자를 전송할 수 있음
- 보통 START 문자는 `C-q`
  - 이 값을 변경하지 못할 수 있음
  - 명시된 값과 무관하게 하드웨어가 `C-q` 사용을 강제할 수 있음

## Macro: `int VSTOP`

- 특수 제어 문자 배열의 STOP 문자를 위한 서브스크립트
  - `termios.c_cc[VSTOP]`은 문자 그 자체
- STOP 문자는 `IXON`과 `IXOFF` 입력 모드를 지원하기 위해 사용됨
  - `IXON`이 설정되었을 때 STOP 문자를 받으면 출력을 중단함
    - STOP 문자 자체는 제거됨
  - `IXOFF`가 설정되었다면 입력 큐가 오버플로우 되는 것을 방지하기 위해 시스템 또한 터미널에 STOP 문자를 전송할 수 있음
- 보통 STOP 문자는 `C-s`
  - 이 값을 변경하지 못할 수 있음
  - 명시된 값과 무관하게 하드웨어가 `C-s` 사용을 강제할 수 있음
