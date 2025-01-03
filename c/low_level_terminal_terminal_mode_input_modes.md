# Input Modes

- 이 섹션은 입력 처리의 상당히 저수준인 측면을 제어하는 터미널 속성 플래그에 관해 설명함
  - 패리티 오류, 브레이크 신호, 흐름 제어, `RET`, `LFD` 문자
- 이러한 모든 플래그는 `struct termios` 구조체의 `c_iflag` 멤버 내의 비트
  - 멤버는 정수이고, 연산자 `&`, `|`, `^`를 사용해 플래그 변경 가능
  - `c_iflag` 전체 값을 특정하려 하지 말고, 특정한 플래그들만 변경해 나머지는 변경하지 않도록 함
  - [Setting Terminal Modes Properly](https://sourceware.org/glibc/manual/2.40/html_node/Setting-Modes.html) 참조

## Macro: `tcflag_t INPCK`

- 이 비트가 설정되면 입력 패리티 체크가 활성화됨
- 설정되지 않으면, 입력에 대한 체크가 수행되지 않음
  - 응용 프로그램에 문자가 단순히 넘어감
- 입력 처리에서의 패리티 체크는 패리티 감지와 기저에 있는 터미널 하드웨어 생성이 활성화 되었는가와는 독립적임
  - [Control Modes](https://sourceware.org/glibc/manual/2.40/html_node/Control-Modes.html) 참조
  - 예를 들어, `INPCK` 입력 모드 플래그를 해제하고 입력의 패리티 오류를 무시하기 위해 `PARENB` 제어 모드 플래그를 설정해도 출력에서는 패리티가 생성됨
- 이 비트가 설정된다면 `IGNPAR` 또는 `PARMRK` 비트 설정 여부에 따라 패리티 오류가 감지되었을 때의 동작이 달라짐
  - 두 비트 모두 설정되지 않았다면 패리티 오류를 가지는 바이트는 응용 프로그램에 `\0` 문자로 전달됨

## Macro: `tcflag_t IGNPAR`

- 이 비트가 설정되면 프레이밍이나 패리티 오류를 가진 바이트는 무시됨
- `INPCK`이 설정되었을 때에만 유용함

## Macro: `tcflag_t PARMRK`

- 이 비트가 설정되면 패리티 또는 프레이밍 오류를 가진 입력 바이트가 프로그램에 전달될 때 마킹됨
- `INPCK`은 설정, `IGNPAR`은 설정되지 않았을 때에만 의미가 있음
- 두 개의 선행 바이트, `377`과 `0`으로 에러가 존재하는 바이트를 마킹함
  - 프로그램은 실제로 터미널에서 받은 하나의 오류가 존재하는 바이트를 위해 3바이트를 읽음
- 유효한 바이트가 `0377` 값을 가지고, `ISTRIP`이 설정되지 않았다면, 프로그램은 이를 패리티 오류를 마킹하는 접두사로 혼동할 수 있음
  - 유효한 바이트 `0377`은 이런 경우 프로그램에 `0377 0377`, 2바이트로 전송됨

## Macro: `tcflag_t ISTRIP`

- 이 비트가 설정되면 유효한 입력 바이트는 7비트로 줄어듦
- 설정되지 않으면 프로그램은 모든 8비트를 읽을 수 있게 됨

## Macro: `tcflag_t IGNBRK`

- 이 비트가 설정되면 브레이크 조건이 무시됨
- *브레이크 조건* 은 비동기 시리얼 데이터 전송 컨텍스트에서 하나의 바이트보다 긴 일련의 0 값을 가진 비트들로 정의됨

## Macro: `tcflag_t BRKINT`

- 이 비트가 설정되고 `IGNBRK`가 설정되지 않으면, 브레이크 조건은 터미널 입력과 출력 큐를 비우고 터미널과 연결된 foreground 프로세스 그룹에 `SIGINT` 신호를 보냄
- `BRKINT`와 `IGNBRK` 모두 설정되지 않았을 때
  - `PARMRK`가 설정되지 않았다면 브레이크 조건은 프로그램에 단일 `\0` 문자로 전달됨
  - 설정되었다면 세 문자 시퀀스 `\377`, `\0`, `\0`으로 전달됨

## Macro: `tcflag_t IGNCR`

- 이 비트가 설정되었다면 캐리지 리턴 문자(`\r`)는 입력에서 버려짐
- 캐리지 리턴을 버리는 것은 `RET` 키를 입력했을 때 캐리지 리턴과 라인 피드를 전부 보내는 터미널에서 유용할 수 있음

## Macro: `tcflag_t ICRNL`

이 비트가 설정되고 `IGNCR`이 설정되지 않으면, 입력으로 들어온 캐리지 리턴 문자(`\r`)가 프로그램에 개행 문자(`\n`)로 전달됨

## Macro: `tcflag_t INLCR`

이 비트가 설정되면 입력으로 들어온 개행 문자(`\n`)가 프로그램에 캐리지 리턴 문자(`\r`)로 전달됨

## Macro: `tcflag_t IXOFF`

- 이 비트가 설정되면 입력에 대한 시작/중단 제어가 활성화됨
- 컴퓨터가 프로그램이 읽는 것보다 더 빨리 입력이 들어오는 것을 방지하기 위해 필요에 따라 STOP과 START 문자를 전송할 수 있게 됨
- 입력 데이터를 생성하는 실제 터미널 하드웨어가 전송을 중단하는 것으로 STOP 문자에 응답하고, 전송을 재개하는 것으로 START 문자에 응답함
- [Special Characters for Flow Control](https://sourceware.org/glibc/manual/2.40/html_node/Start_002fStop-Characters.html) 참조

## Macro: `tcflag_t IXON`

- 이 비트가 설정되면 출력에 대한 시작/중단 제어가 활성화됨
- 컴퓨터가 STOP 문자을 받으면, START 문자를 받기 전까지 출력을 중단함
  - 이 경우, 응용 프로그램에는 STOP과 START 문자가 전달되지 않음
- 이 비트가 설정되지 않으면 START와 STOP은 일반적인 문자로 읽힘
- [Special Characters for Flow Control](https://sourceware.org/glibc/manual/2.40/html_node/Start_002fStop-Characters.html)

## Macro: `tcflag_t IXANY`

- 이 비트가 설정되면 출력이 STOP 문자에 의해 중단되었을 때 어떤 입력 문자로도 출력이 재개됨
- 설정되지 않으면 START 문자만이 출력을 재개함
- BSD 확장: BSD, GNU/Linux, GNU/Hurd 체제에만 존재

## Macro: `tcflag_t IMAXBEL`

- 이 비트가 설정되면 터미널 입력 버퍼를 채우는 것이 터미널에 BEL 문자(코드 `007`)을 전송해 벨을 울리게 함
- BSD 확장
