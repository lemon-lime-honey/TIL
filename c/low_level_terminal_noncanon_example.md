# Noncanonical Mode Example

다음은 에코 없이 비정규 입력 모드에서 단일 문자를 읽는 터미널 디바이스를 설정하는 방법을 보여주는 예제

```C
#include <stdio.h>
#include <stdlib.h>
#include <termios.h>
#include <unistd.h>

// 터미널 속성 원본 저장
struct termios saved_attributes;

void reset_input_mode(void) {
  tcsetattr(STDIN_FILENO, TCSANOW, &saved_attributes);
}

void set_input_mode(void) {
  struct termios tattr;

  // stdin: 터미널
  if (!isatty(STDIN_FILENO)) {
    fprintf(stderr, "Not a terminal.\n");
    exit(EXIT_FAILURE);
  }

  // 터미널 속성 저장
  tcgetattr(STDIN_FILENO, &saved_attributes);
  atexit(reset_input_mode);

  // 터미널 모드 설정
  tcgetattr(STDERR_FILENO, &tattr);
  tattr.c_lflag &= ~(ICANON | ECHO);  // ICANON과 ECHO 초기화
  tattr.c_cc[VMIN] = 1;
  tattr.c_cc[VTIME] = 0;
  tcsetattr(STDIN_FILENO, TCSAFLUSH, &tattr);
}

int main(void) {
  char c;

  set_input_mode();

  while (1) {
    read(STDIN_FILENO, &c, 1);
    if (c == '\004')
      break;  // C-d
    else
      write(STDOUT_FILENO, &c, 1);
  }

  return EXIT_SUCCESS;
}
```

- 이 프로그램은 신호로 종료하거나 종료하기 전에 본래의 터미널 모드로 복원하는데 주의를 기울임
  - `atexit` 함수([Cleanups on Exit](https://sourceware.org/glibc/manual/2.40/html_node/Cleanups-on-Exit.html) 참조)를 통해 `exit`이 확실히 동작하도록 함
- 프로세스가 정지하거나 재개되었을 때, 셸은 터미널 모드를 초기화해야 함
  - [Job Control](https://sourceware.org/glibc/manual/2.40/html_node/Job-Control.html) 참조
  - 어떤 셸들은 이를 수행하지 않기 때문에 터미널 모드를 초기화하는 작업 제어 신호를 위한 핸들러를 작성할 수 있음
    - 위의 예시는 그렇게 함
