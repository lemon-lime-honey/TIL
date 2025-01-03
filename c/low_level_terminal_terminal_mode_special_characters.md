# Special Characters

- 정규 입력에서 터미널 드라이버는 다양한 제어 기능을 수행하는 여러 특수한 문자를 인식함
  - 이 중에는 입력을 수정하기 위한 ERASE 문자(대개는 `DEL`)도 있으며, 다른 수정 문자 또한 포함함
  - `SIGINT` 신호를 보내기 위한 INTR 문자(대개는 `C-c`), 그리고 다른 신호를 보내는 문자들은 정규 또는 비정규 입력 모드에서 사용 가능할 수 있음
  - 이러한 모든 문자를 이 섹션에서 설명함
- 사용되는 특정 문자들은 `struct termios` 구조체의 `c_cc` 멤버에 명시되어 있음
  - 이 멤버는 배열: 각 원소는 특정 역할을 위한 문자를 명시함
  - 각 원소는 그 원소의 인덱스를 나타내는 기호 상수를 가짐
    - `VINTR`는 `INTR` 문자를 명시하는 원소의 인덱스이므로 `termios.c_cc[VINTR]`에 `'='`를 저장하는 것은 `'='`을 INTR 문자로 명시하는 것
- 어떤 체제에서는 역할에 `_POSIX_VDISABLE` 값을 명시하여 특정 특수 문자 기능을 비활성화 할 수 있음
  - 이 값은 다른 어떤 가능한 문자 코드와도 같지 않음
  - 사용하는 운영체제가 `_POSIX_VDISABLE`을 지원하는지 확인하는 방법에 대해서는 [Optional Features in File Support](https://sourceware.org/glibc/manual/2.40/html_node/Options-for-Files.html) 참조

<br />

- [Characters for Input Editing](./low_level_terminal_editing_characters.md)
- [Characters that Cause Signals](./low_level_terminal_signal_characters.md)
- [Special Characters for Flow Control](./low_level_terminal_start_stop_characters.md)
- [Other Special Characters](./low_level_terminal_other_special_characters.md)
