# Characters for Input Editing

- 다음 특수 문자들은 정규 입력 모드에서만 활성화됨
- [Two Styles of Input: Canonical or Not](https://sourceware.org/glibc/manual/2.40/html_node/Editing-Characters.html) 참조

## Macro: `int VEOF`

- 특수 제어 문자 배열의 EOF 문자를 위한 서브스크립트
  - `termios.c_cc[VEOF]`는 문자 그 자체
- EOF 문자는 정규 입력 모드에서만 인식됨
  - 개행 문자와 같은 방식으로 문장의 종단 역할을 하지만 EOF 문자가 행 시작점에 입력되면 end-of-file을 지시하게 되어 `read`가 바이트 집계를 0으로 반환함
  - EOF 문자 자체는 제거됨
- 보통 EOF 문자는 `C-d`

## Macro: `int VEOL`

- 특수 제어 문자 배열의 EOL 문자를 위한 서브스크립트
  - `termios.c_cc[VEOL]`는 문자 그 자체
- EOL 문자는 정규 입력 모드에서만 인식됨
  - 개행 문자와 같은 방식으로 문장의 종단 역할을 함
  - EOF 문자는 버려지지 않음: 입력 파일의 마지막 문자로 읽힘
- `RET`가 행을 끝낼 수 있게 하기 위해 EOL 문자를 사용할 필요는 없음
  - ICRNL 플래그를 설정하면 됨
  - 사실 이것이 기본 상태임

## Macro: `int VEOL2`

- 특수 제어 문자 배열의 EOL2 문자를 위한 서브스크립트
  - `termios.c_cc[VEOL2]`는 문자 그 자체
- EOL2 문자는 EOL 문자처럼 동작하지만 다른 문자가 될 수 있음
  - EOL을 종료 문자로, EOL2를 또 다른 종료 문자로 설정해 입력행을 종료하기 위한 두 개의 문자를 명시할 수 있음
- BSD 확장: BSD, GNU/Linux, GNU/Hurd 체제에서만 존재

## Macro: `int VERASE`

- 특수 제어 문자 배열의 ERASE 문자를 위한 서브스크립트
  - `termios.c_cc[VERASE]`는 문자 그 자체
- ERASE 문자는 정규 입력 모드에서만 인식됨
  - 사용자가 ERASE 문자를 입력하면 이전에 입력된 문자는 버려짐
    - 터미널이 멀티바이트 문자 시퀀스를 생성한다면, 이는 단일 바이트보다 더 많은 바이트의 입력을 제거할 수 있음
  - 텍스트의 현재 행의 시작점 이전을 지우는데 사용할 수 없음
  - ERASE 문자 자체는 제거됨
- 일반적으로 ERASE 문자는 `DEL`

## Macro: `int VWERASE`

- 특수 제어 문자 배열의 WERASE 문자를 위한 서브스크립트
  - `termios.c_cc[VWERASE]`는 문자 그 자체
- WERASE 문자는 정규 입력모드에서만 인식됨
  - 이전 입력의 단어 전체와 그 후의 모든 공백을 제거함
  - 단어 이전의 공백은 제거되지 않음
- "단어"의 정의는 `ALTWERASE` 모드의 설정에 따라 다름: [Local Modes](https://sourceware.org/glibc/manual/2.40/html_node/Local-Modes.html) 참조
  - `ALTWERASE`가 설정되지 않았다면 단어는 공백 또는 탭을 제외한 모든 문자의 시퀀스로 정의됨
  - `ALTWERASE`가 설정되었다면 단어는 문자, 숫자, 그리고 문자 또는 숫자, 언더스코어(\_)가 아닌 하나의 문자가 뒤에 오는 언더스코어()를 포함한 문자의 시퀀스로 정의됨
- WERASE 문자는 보통 `C-w`
- BSD 확장

## Macro: `int VKILL`

- 특수 제어 문자 배열의 KILL 문자를 위한 서브스크립트
  - `termios.c_cc[KILL]`는 문자 그 자체
- KILL 문자는 정규 입력모드에서만 인식됨
  - 사용자가 KILL 문자를 입력하면 입력의 현재 행의 모든 내용이 제거됨
  - KILL 문자 또한 제거됨
- KILL 문자는 보통 `C-u`

## Macro: `int VREPRINT`

- 특수 제어 문자 배열의 REPRINT 문자를 위한 서브스크립트
  - `termios.c_cc[REPRINT]`는 문자 그 자체
- REPRINT 문자는 정규 입력모드에서만 인식됨
  - 현재 입력 행을 재출력함
  - 입력 중 어떤 비동기 출력이 도착했을 때 입력 중인 행을 다시 선명하게 볼 수 있게 함
- REPRINT 문자는 보통 `C-r`
- BSD 확장
