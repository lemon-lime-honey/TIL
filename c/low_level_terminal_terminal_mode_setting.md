# Setting Terminal Modes Properly

- 터미널 모드를 설정할 때, 변경해야 할 모드만을 변경하기 위해 특정 터미널 디바이스의 현재 모드를 구하기 위해 우선 `tcgetattr`를 호출하고 `tcsetattr`로 결과를 저장함
- 단순히 `struct termios`를 선택한 속성 값으로 초기화하고 직접 `tcsetattr`로 전달하는 것은 좋은 방법이 아님
  - 프로그램은 앞으로 몇 년 동안, 이 매뉴얼에서 언급되지 않는 멤버를 지원하는 체제에서 동작할 수도 있음
  - 이러한 멤버들이 비합리적인 값으로 설정되는 것을 피하려면 그 멤버들을 변경하는 것을 피하면 됨
- 또한 서로 다른 터미널 디바이스는 적절히 동작하기 위해 서로 다른 모드 설정을 필요로 할 수도 있음
  - 아무 생각 없이 하나의 터미널 디바이스의 속성을 복사해 다른 터미널 디바이스에 적용하는 것을 피해야 함
- 멤버가 `c_iflag`, `c_oflag`, `c_cflag`와 같은 독립적인 플래그의 모음을 포함한다면 특정 운영체제들은 자체적인 플래그를 가지기 때문에 전체 멤버를 설정하는 것 또한 나쁜 방법일 수 있음
  - 대신, 멤버의 현재 값을 가지고 시작해 다른 플래그가 변경되지 않도록 프로그램과 상관있는 플래그의 값만 변경함
- 다음은 `struct termios` 구조체의 다른 데이터를 적절히 보존하면서 하나의 플래그(`ISTRIP`)을 설정하는 예제

  ```C
  int set_istrp(int desc, int value) {
    struct termios settings;
    int result;

    result = tcgetattr(desc, &settings);

    if (result < 0) {
      perror("error in tcgetattr");
      return 0;
    }

    settings.c_iflag &= ~ISTRIP;

    if (value) {
      settings.c_iflag |= ISTRIP;
    }

    result = tcsetattr(desc, TCSANOW, &settings);

    if (result < 0) {
      perror("error in tcsetattr");
      return 0;
    }

    return 1;
  }
  ```