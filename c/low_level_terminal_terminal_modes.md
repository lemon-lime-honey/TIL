# Terminal Modes

- 이 섹션은 입력과 출력이 어떻게 되는지 제어하는 다양한 터미널 속성을 설명함
  - 함수, 자료 구조, 기호 상수는 모두 헤더 `termios.h`에서 선언됨
- 터미널 속성은 파일 속성과 다름
  - [File Attributes](https://sourceware.org/glibc/manual/2.40/html_node/File-Attributes.html)에서 설명하듯이, 터미널에 연결된 장치 파일(특수 파일)이 파일 속성을 가짐
  - 이는 이 섹션에서 논의하는 터미널 디바이스 자체의 속성과는 관련이 없음

- [Terminal Mode Data Types](./low_level_terminal_terminal_mode_data_types.md)
- [Terminal Mode Functions](./low_level_terminal_terminal_mode_functions.md)
- [Setting Terminal Modes Properly](./low_level_terminal_terminal_mode_setting.md)
- [Input Modes](./low_level_terminal_terminal_mode_input_modes.md)
- [Output Modes](./low_level_terminal_terminal_mode_output_modes.md)
- [Control Modes](./low_level_terminal_terminal_mode_control_modes.md)
- [Local Modes](./low_level_terminal_terminal_mode_local_modes.md)
- [Line Speed](./low_level_terminal_terminal_mode_line_speed.md)
- [Special Characters](./low_level_terminal_terminal_mode_special_characters.md)
- [Noncanonical Input](./low_level_terminal_terminal_mode_noncanonical_input.md)