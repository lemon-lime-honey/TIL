# Characters that Cause Signals

- 다음의 특수 문자들은 정규 또는 비정규 입력 모드에서 `ISIG` 플래그가 설정되었을 때에만 사용 가능
- [Local Modes](https://sourceware.org/glibc/manual/2.40/html_node/Local-Modes.html) 참조

## Macro: `int VINTR`

- 특수 제어 문자 배열의 INTR 문자를 위한 서브스크립트
  - `termios.c_cc[VINTR]`은 문자 그 자체
- INTR(interrupt) 문자는 터미널에 연결된 forground 작업의 모든 프로세스에 `SIGINT` 신호를 전송함
  - INTR 문자 자체는 그 다음 제거됨
  - 신호에 관한 더 많은 정보는 [Signal Handling](https://sourceware.org/glibc/manual/2.40/html_node/Signal-Handling.html)에서 확인
- 보통 INTR 문자는 `C-c`

## Macro: `int VQUIT`

- 특수 제어 문자 배열의 QUIT 문자를 위한 서브스크립트
  - `termios.c_cc[VQUIT]`은 문자 그 자체
- QUIT 문자는 터미널에 연결된 forground 작업의 모든 프로세스에 `SIGQUIT` 신호를 전송함
  - QUIT 문자 자체는 그 다음 제거됨
  - 신호에 관한 더 많은 정보는 [Signal Handling](https://sourceware.org/glibc/manual/2.40/html_node/Signal-Handling.html)에서 확인
- 보통 QUIT 문자는 `C-\`

## Macro: `int VSUSP`

- 특수 제어 문자 배열의 SUSP 문자를 위한 서브스크립트
  - `termios.c_cc[VSUSP]`은 문자 그 자체
- SUSP(suspend) 문자는 구현이 작업 제어([Job Control](https://sourceware.org/glibc/manual/2.40/html_node/Job-Control.html) 참조)를 지원할 때에만 인식됨
  - 터미널에 연결된 forground 작업의 모든 프로세스에 `SIGTSTP` 신호를 전송함
  - SUSP 문자 자체는 그 다음 제거됨
  - 신호에 관한 더 많은 정보는 [Signal Handling](https://sourceware.org/glibc/manual/2.40/html_node/Signal-Handling.html)에서 확인
- 보통 SUSP 문자는 `C-z`

<br />

어떤 애플리케이션은 SUSP 문자의 일반적인 해석을 비활성화함
  - 이러한 경우 사용자가 작업을 중단시킬 수 있는 다른 메커니즘을 제공해야 함
  - 사용자가 이 메커니즘을 호출했을 때, 프로그램은 프로세스 그 자체 뿐만 아니라 프로세스의 프로세스 그룹에도 `SIGTSTP` 신호를 보내야 함
  - [Signaling Another Process](https://sourceware.org/glibc/manual/2.40/html_node/Signaling-Another-Process.html) 참조

## Macro: `int VDSUSP`

- 특수 제어 문자 배열의 DSUSP 문자를 위한 서브스크립트
  - `termios.c_cc[VDSUSP]`은 문자 그 자체
- DSUSP(suspend) 문자는 구현이 작업 제어([Job Control](https://sourceware.org/glibc/manual/2.40/html_node/Job-Control.html) 참조)를 지원할 때에만 인식됨
  - SUSP 문자처럼 터미널에 연결된 forground 작업의 모든 프로세스에 `SIGTSTP` 신호를 전송하지만 바로 전송하는 것은 아님
    - 프로그램이 입력으로 이를 읽으려고 할 때만 전송
  - 신호에 관한 더 많은 정보는 [Signal Handling](https://sourceware.org/glibc/manual/2.40/html_node/Signal-Handling.html)에서 확인
- 보통 DSUSP 문자는 `C-y`
- 작업 제어가 가능한 모든 체제가 DSUSP를 지원하는 건 아님
  - BSD 호환 체제 한정(GNU/Hurd 체제 포함)
