# Terminal Mode Data Types

- 터미널의 모든 속성 모음은 타입 `struct termios`의 구조체에 저장됨
  - 이 구조체는 속성을 읽고 설정하기 위해 함수 `tcgetattr`와 `tcsetattr`와 함께 사용됨

## Data Type: `struct termios`

- `struct termios`는 터미널의 모든 I/O 속성을 기록함
- 이 구조체는 최소 다음을 포함함
  - `tcflag_t c_iflag`
    - 입력 모드 플래그를 명시하는 비트 마스크
    - [Input Modes](https://sourceware.org/glibc/manual/2.40/html_node/Input-Modes.html) 참조
  - `tcflag_t c_oflag`
    - 출력 모드 플래그를 명시하는 비트 마스크
    - [Output Modes](https://sourceware.org/glibc/manual/2.40/html_node/Output-Modes.html) 참조
  - `tcflag_t c_cflag`
    - 제어 모드 플래그를 명시하는 비트 마스크
    - [Control Modes](https://sourceware.org/glibc/manual/2.40/html_node/Control-Modes.html) 참조
  - `tcflag_t c_lflag`
    - 로컬 모드 플래그를 명시하는 비트 마스크
    - [Local Modes](https://sourceware.org/glibc/manual/2.40/html_node/Local-Modes.html) 참조
  - `cc_t c_cc[NCCS]`
    - 다양한 제어 함수와 연결된 문자를 명시하는 배열
    - [Special Characters](https://sourceware.org/glibc/manual/2.40/html_node/Special-Characters.html) 참조
- `struct termios` 구조체는 입력과 출력 전송 속도를 인코딩하는 멤버를 포함하지만, 표현이 구체화되지는 않음
  - 속도 값을 어떻게 확인하고 저장하는가: [Line Speed](https://sourceware.org/glibc/manual/2.40/html_node/Line-Speed.html) 참조

다음에서 `struct termios` 구조체 멤버의 상세를 설명함

## Data Type: `tcflag_t`

터미널 플래그를 위한 다양한 비트마스크를 표현하기 위해 사용하는 부호 없는 정수형

## Data Type: `cc_t`

다양한 터미널 제어 함수와 연결된 문자를 나타내기 위해 사용하는 부호 없는 정수형

## Macro: `int NCCS`

이 매크로의 값은 `c_cc` 배열의 원소 개수
