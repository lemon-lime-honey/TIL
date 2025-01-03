# Opening a Pseudo-Terminal Pair

BSD에서 유래된 다음 함수는 `pty.h`에서 선언되어 별개의 `libutil` 라이브러리에서 사용 가능

## Function: `int openpty(int *amaster, int *aslave, char *name, const struct termios *termp, const struct winsizwe *winp)`

- Preliminary: | MT-Safe locale | AS-Unsafe dlopen plugin heap lock | AC-Unsafe corrupt lock fd mem | [POSIX Safety Concepts](https://sourceware.org/glibc/manual/2.40/html_node/POSIX-Safety-Concepts.html) 참조
- 가상 터미널 한 쌍을 할당하고 연 후 마스터의 파일 기술자는 `*amaster`에, 슬레이브의 파일 기술자는 `*aslave`에 반환함
  - 인자 `name`이 null 포인터가 아니라면, 슬레이브 가상 터미널 디바이스의 이름이 `*name`에 저장됨
  - `temp`가 null 포인터가 아니라면, 슬레이브의 터미널 속성이 `temp`가 가리키는 구조체 내에 명시된 것으로 설정됨([Terminal Modes](https://sourceware.org/glibc/manual/2.40/html_node/Terminal-Modes.html) 참조)
  - `winp`가 null 포인터가 아니라면, 슬레이브의 스크린 크기는 `winp`가 가리키는 구조체에서 명시된 값으로 설정됨
- 일반적인 반환값은 0
- 실패 시 -1 반환
  - 이 함수를 위해 다음 `errno` 조건이 정의됨
    -  `ENOENT`: 사용 가능한 연결되지 않은 가상 터미널 쌍이 없음

### 주의

- `name`을 `NULL`로 설정하지 않고 `openpty` 함수를 사용하는 것은 **매우 위험**
  - 문자열 `name`이 오버플로우 되는 것을 방지할 방법이 주어지지 않음
- 슬레이브 가상 터미널 디바이스의 파일명을 찾기 위해 `*slave`에 반환된 파일 기술자에 `ttyname` 함수를 사용해야 함

## Function: `int forkpty(int *amaster, char *name, const struct termios *termp, const struct winsize *winp)`

- Preliminary: | MT-Safe locale | AS-Unsafe dlopen plugin heap lock | AC-Unsafe corrupt lock fd mem | [POSIX Safety Concepts](https://sourceware.org/glibc/manual/2.40/html_node/POSIX-Safety-Concepts.html) 참조
- `openpty` 함수와 유사
  - 새 프로세스를 포크하고([Creating a Process](https://sourceware.org/glibc/manual/2.40/html_node/Creating-a-Process.html) 참조) 새로 연 슬레이브 가상 터미널 디바이스를 자식 프로세스를 위한 제어 터미널([Controlling Terminal of a Process](https://sourceware.org/glibc/manual/2.40/html_node/Controlling-Terminal.html) 참조)로 만듦
- 동작이 성공적이었다면 자식과 부모 프로세스가 존재하게 되며, 둘 다 `forkpty` 반환을 확인할 수 있으나 값이 다름
  - 자식 프로세스에서는 0을 반환하고, 부모 프로세스에서는 자식 프로세스의 ID를 반환함
- 가상 터미널 쌍 할당이나 프로세스 생성에 실패했다면 부모 프로세스에서 -1을 반환함

### 주의

`forkpty` 함수는 `openpty`에서의 `name` 인자에 관한 동일한 문제점을 가짐