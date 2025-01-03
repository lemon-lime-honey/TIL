# Output Modes

- 이 섹션은 출력 문자가 표현되기 위해 어떻게 번역되고 패딩이 추가되는지 제어하는 터미널 플래그와 필드를 설명함
  - 이 모든 것은 `struct termios` 구조체의 `c_oflag` 멤버에 포함됨
- `c_oflag` 멤버 자체는 정수이므로 `&`, `|`, `^` 연산자를 이용해 플래그와 필드 변경 가능
  - `c_oflag`의 전체 값을 특정하려 하지 말 것
  - 대신 특정한 플래그만 변경해 나머지 값들을 보존
  - [Setting Terminal Modes Properly](https://sourceware.org/glibc/manual/2.40/html_node/Setting-Modes.html) 참조

## Macro: `tcflag_t OPOST`

- 이 비트가 설정되면 출력 데이터가 터미널 디바이스에 적절히 표현되도록 특정되지 않은 어떤 방법으로 처리됨
  - 이는 보통 개행 문자(`\n`)를 캐리지 리턴과 라인 피드 쌍으로 매핑하는 것을 포함함
- 설정되지 않는다면 문자가 그대로 전송됨

## Macro: `tcflag_t ONLCR`

이 비트가 설정되면 출력의 개행문자를 캐리지 리턴과 그 다음으로 라인 피트 문자의 한 쌍으로 변환함

## Macro: `tcflag_t OXTABS`

- 이 비트가 설정되면 탭이 모든 여덟번째 열마다 멈추도록 하기 위해 출력의 탭 문자를 적절한 수의 공백으로 변환함
- 이 비트는 BSD 체제와 GNU/Hurd 체제에만 존재함
  - GNU/Linux 체제에서는 `XTABS`로 사용 가능

## Macro: `tcflag_t ONOEOT`

- 이 비트가 설정되면 출력의 `C-d` 문자(코드 `004`)를 버림
- 이 문자는 많은 전화 접속(dial-up) 터미널의 연결이 끊어지는 원인이 됨
- 이 비트는 BSD 체제와 GNU/Hurd 체제에만 존재함