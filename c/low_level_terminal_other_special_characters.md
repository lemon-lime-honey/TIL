# Other Special Characters

## Macro: `int VLNEXT`

- 특수 제어 문자 배열의 LNEXT 문자를 위한 서브스크립트
  - `termios.c_cc[VLNEXT]`은 문자 그 자체
- LNEXT 문자는 `IEXTEN`이 설정되었을 때에만 인식됨
  - 정규 모드, 비정규 모드 둘 다 가능
  - 사용자가 입력하는 다음 문자의 특수한 의미를 비활성화 함
  - 보통의 경우 수정 기능을 수행하거나 신호를 생성하는 문자더라도, 평범한 문자로 읽힘
  - Emacs의 `C-q` 명령과 유사함
- LNEXT는 literal next를 의미함
- LNEXT 문자는 일반적으로 `C-v`
- 이 문자는 BSD, GNU/Linux, GNU/Hurd 체제에서 사용 가능

## Macro: `int VDISCARD`

- 특수 제어 문자 배열의 DISCARD 문자를 위한 서브스크립트
  - `termios.c_cc[VDISCARD]`은 문자 그 자체
- DISCARD 문자는 `IEXTEN`이 설정되었을 때에만 인식됨
  - 정규 모드, 비정규 모드 둘 다 가능
  - 출력 제거 플래그 토글 효과
  - 이 플래그가 설정되면 모든 프로그램 출력이 제거됨
  - 또한 플래그를 설정하면 현재 출력 버퍼에 존재하는 모든 출력을 제거함
  - 다른 문자를 입력하면 플래그가 초기화됨
- 이 문자는 BSD, GNU/Linux, GNU/Hurd 체제에서 사용 가능

## Macro: `int VSTATUS`

- 특수 제어 문자 배열의 STATUS 문자를 위한 서브스크립트
  - `termios.c_cc[VSTATUS]`은 문자 그 자체
- STATUS 문자의 효과는 현재 프로세스가 어떻게 동작 중인지에 관한 상태 메시지를 출력하는 것
- STATUS 문자는 정규 모드에서 `NOKERNINFO`가 설정되지 않았을 때에만 인식됨
- 이 문자는 BSD, GNU/Linux, GNU/Hurd 체제에서 사용 가능
