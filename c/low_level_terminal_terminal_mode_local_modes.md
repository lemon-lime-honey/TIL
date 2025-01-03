# Local Modes

- 이 섹션은 `struct termios` 구조체의 `c_lflag` 멤버의 플래그를 설명함
  - 이러한 플래그는 일반적으로 [Input Modes](https://sourceware.org/glibc/manual/2.40/html_node/Input-Modes.html)에서 설명한 입력 모드 플래그보다 더 고수준 측면의 입력 처리(에코, 신호, 정규 또는 비정규 입력 선택 등)를 제어함
- `c_lflag` 멤버 자체는 정수이고 연산자 `&`, `|`, `^`로 플래그와 필드 변경 가능
  - `c_lflag` 전체 값을 특정하려 하지 말 것
  - 대신 특정한 플래그만 변경해 나머지를 변경되지 않은 상태로 유지
  - [Setting Terminal Modes Properly](https://sourceware.org/glibc/manual/2.40/html_node/Setting-Modes.html) 참조

## Macro: `tcflag_t ICANON`

- 이 비트가 설정되면 정규 입력 처리 모드가 활성화됨
- 설정되지 않으면 비정규 모드로 입력이 처리됨
- [Two Styles of Input: Canonical or Not](https://sourceware.org/glibc/manual/2.40/html_node/Canonical-or-Not.html) 참조

## Macro: `tcflag_t ECHO`

이 비트가 설정되면 터미널로 입력 문자가 에코되는 것이 활성화됨

## Macro: `tcflag_t ECHOE`

- 이 비트가 설정되면, 에코는 스크린의 현재 행의 마지막 문자를 지워 ERASE 문자로 입력을 삭제하는 것을 지시함
- 설정되지 않으면 지워진 문자는 무엇이 일어났는지 보여주기 위해 다시 에코됨(출력 터미널에 적합함)
- 이 비트는 표현 동작만 제어함
  - `ICANON` 비트는 실제로 ERASE 문자 인식과 입력 삭제를 제어함
  - 이 비트가 없으면 `ECHOE`는 단순히 무의미해짐

## Macro: `tcflag_t ECHOPRT`

- `ECHOE`처럼 이 비트는 하드카피 터미널에 맞춘 ERASE 문자 표시를 활성화함
  - ERASE 문자를 입력할 때, `\` 문자가 지워진 첫 문자 앞에 출력됨
  - ERASE 문자를 다시 입력하면 지워진 다음 문자가 출력됨
  - 그 다음, 일반적인 문자를 입력하면 문자가 에코되기 전에 `/` 문자가 출력됨
- BSD 확장: BSD, GNU/LINUX, GNU/Hurd 체제에만 존재

## Macro: `tcflag_t ECHOK`

- 이 비트는 KILL 문자를 정상적으로 에코한 후 개행해 KILL 문자를 특별하게 표시하는 것을 활성화함
  - `ECHOKE`의 동작이 보기에는 더 나음
- 이 비트가 설정되지 않으면 KILL 문자는 KILL 문자가 아닌 것처럼 에코됨
  - KILL 문자가 앞선 입력을 지운 것을 기억하는 건 사용자에게 달린 일
  - 스크린에는 이것이 나타나지 않음
- 이 비트는 표시 동작만 제어함
  - `ICANON` 비트는 실제로 KILL 문자의 인식과 입력 삭제를 제어함
  - 이 비트가 없으면 `ECHOK`는 단순히 무의미해짐

## Macro: `tcflag_t ECHOKE`

- 이 비트는 `ECHOK`와 유사함
  - 제거된 전체 행을 화면에서 지워 KILL 문자를 특별하게 표시하는 것을 활성화함
- BSD 확장: BSD, GNU/Linux, GNU/Hurd 체제에서만 존재

## Macro: `tcflag_t ECHONL`

이 비트가 설정되고 `ICANON` 또한 설정되었다면 `ECHO` 비트가 설정되지 않았더라도 개행(`\n`) 문자가 에코됨

## Macro: `tcflag_t ECHOCTL`

- 이 비트가 설정되고 `ECHO` 비트 또한 설정되었다면, 대응하는 텍스트 문자 앞에 `^`가 추가된 제어 문자를 에코함
  - control-A는 `^A`로 에코됨
  - 이는 보통 상호적 입력에서 선호되는 모드인데, 제어 문자를 터미널에 다시 에코하는 것이 터미널에 원치 않는 영향을 줄 수 있기 때문임
- BSD 확장: BSD, GNU/Linux, GNU/Hurd 체제에만 존재

## Macro: `tcflag_t ISIG`

- 이 비트는 INTR, QUIT, SUSP 문자 인식 여부를 제어함
  - 이 문자와 연관된 함수는 이 비트가 설정되었을 때에만 동작함
  - 정규 또는 비정규 입력 모드에 있는 것이 이러한 문자를 해석하는 것에 영향을 주지 않음
- 이러한 문자 인식을 비활성화할 때에는 주의해야 함
  - 상호적으로 중단될 수 없는 프로그램은 매우 비-사용자 친화적임
  - 만약 이 비트를 ㅌ지우면, 프로그램은 이러한 문자들에 연관된 신호를 상호적으로 보낼 수 있도록 하거나 프로그램에서 벗어나는 대체 방법을 제공함
- [Characters that Cause Signals](https://sourceware.org/glibc/manual/2.40/html_node/Signal-Characters.html) 참조

## Macro: `tcflag_t IEXTEN`

- POSIX.1은 `IEXTEN`에 구현에 의해 정의된 의미를 부여하므로 모든 체제에서 이 해석을 의존할 수는 없음
- BSD, GNU/Linux, GNU/Hurd 체제에서 이는 LNEXT와 DISCARD 문자를 활성화함
- [Other Special Characters](https://sourceware.org/glibc/manual/2.40/html_node/Other-Special.html) 참조

## Macro: `tcflag_t NOFLSH`

- 일반적으로 INTR, QUIT, SUSP 문자는 터미널의 입력과 출력 큐를 비우게 함
- 이 비트가 설정되면 큐가 비워지지 않음

## Macro: `tcflag_t TOSTOP`

- 이 비트가 설정되고 시스템이 작업 제어를 지원하면, 터미널에 쓰려고 시도하는 백그라운드 프로세스에 의해 `SIGTTOU` 신호가 생성됨
- [Access to the Controlling Terminal](https://sourceware.org/glibc/manual/2.40/html_node/Access-to-the-Terminal.html) 참조

<br />

다음 비트들은 BSD 확장: BSD, GNU/Hurd 체제에만 존재

## Macro: `tcflag_t ALTWERASE`

- 이 비트는 WERASE 문자가 얼마나 많이 지울지 결정함
  - WERASE 문자는 문자의 시작점까지 지움
  - 문자는 어디서부터 시작하는가?
- 이 비트가 설정되지 않으면, 단어의 시작점은 공백문자 뒤의 공백이 아닌 문자가 됨
- 설정되면 단어의 시작점은 alphanumeric 문자 또는 alphanumeric 또는 언더스코어(\_)가 아닌 문자 앞의 언더스코어가 됨
- WERASE 문자에 대한 더 많은 정보를 확인하려면 [Characters for Input Editing](https://sourceware.org/glibc/manual/2.40/html_node/Editing-Characters.html) 참조

## Macro: `tcflag_t FLUSHO`

- 사용자가 DISCARD 문자를 입력했을 때 토글되는 비트
- 이 비트가 설정되면 모든 출력이 버려짐
- [Other Special Characters](https://sourceware.org/glibc/manual/2.40/html_node/Other-Special.html) 참조

## Macro: `tcflag_t NOKERNINFO`

- 이 비트를 설정하면 STATUS 문자를 다루는 것이 비활성화됨
- [Other Special Characters](https://sourceware.org/glibc/manual/2.40/html_node/Other-Special.html) 참조

## Macro: `tcflag_t PENDIN`

- 이 비트가 설정되면 재출력되어야 하는 입력 행이 있다는 것을 나타냄
- REPRINT 문자를 타이핑하면 이 비트가 설정됨
- 재출력이 끝날 때까지 비트는 설정된 상태로 머무름
- [Characters for Input Editing](https://sourceware.org/glibc/manual/2.40/html_node/Editing-Characters.html) 참조
