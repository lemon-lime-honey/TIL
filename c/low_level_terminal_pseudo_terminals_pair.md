# Allocating Pseudo-Terminals

- 이 하위 섹션은 가상 터미널을 할당하고 이 가상 터미널을 실제로 사용할 수 있게 만드는 함수를 설명함
- 함수는 헤더 파일 `stdlib.h`에 선언됨

## Function: `int posix_openpt(int flags)`

- Preliminary: | MT-Safe | AS-Safe | AC-Safe fd | [POSIX Safety Concepts](https://sourceware.org/glibc/manual/2.40/html_node/POSIX-Safety-Concepts.html) 참조
- `posix_openpt`는 다음 사용 가능한 마스터 가상 터미널을 위한 새로운 파일 기술자를 반환함
- 오류가 발생한 경우 -1을 대신 반환하고, 오류를 표현하기 위해 `errno`를 설정함
  - `errno`에 사용 가능한 값은 [Opening and Closing Files](https://sourceware.org/glibc/manual/2.40/html_node/Opening-and-Closing-Files.html)에서 확인 가능
- `flags`는 0개 이상의 다음 플래그의 비트연산 OR 값으로부터 생성된 비트 마스크
  - `O_RDWR`
    - 읽기와 쓰기 모두를 위해 디바이스 열기
    - 이 플래그를 명시하는 것은 일반적임
  - `O_NOCTTY`
    - 디바이스를 프로세스 제어 터미널로 만들지 않기
  - 이 플래그들은 `fcntl.h`에서 정의됨
    - [File Access Modes](https://sourceware.org/glibc/manual/2.40/html_node/Access-Modes.html) 참조
- 이 함수를 사용하려면, `_XOPEN_SOURCE`가 `'600'`보다 큰 값으로 정의되어야 함
  - [Feature Test Macros](https://sourceware.org/glibc/manual/2.40/html_node/Feature-Test-Macros.html) 참조

## Function: `int getpt(void)`

- Preliminary: | MT-Safe | AS-Safe | AC-Safe fd | [POSIX Safety Concepts](https://sourceware.org/glibc/manual/2.40/html_node/POSIX-Safety-Concepts.html) 참조
- `posix_openpt`와 유사함
- GNU 확장이며, portable 프로그램에서는 사용하면 안됨
- 다음 사용 가능한 마스터 가상 터미널을 위한 새로운 파일 기술자 반환
  - 일반적인 반환값은 음수가 아닌 정수 파일 기술자
- 오류가 발생한 경우 -1을 대신 반환함
  - 이 함수를 위해 다음 `errno` 조건이 정의됨
    - `ENOENT`: 사용 가능한 연결되지 않은 마스터 가상 터미널이 없음

## Function: `int grantpt(int filedes)`

- Preliminary: | MT-Safe locale | AS-Unsafe dlopen plugin heap lock | AC-Unsafe corrupt lock fd mem | [POSIX Safety Concepts](https://sourceware.org/glibc/manual/2.40/html_node/POSIX-Safety-Concepts.html) 참조
- 파일 기술자 `filedes`에 연결된 마스터 가상 터미널 디바이스에 대응하는 슬레이브 가상 터미널 디바이스의 소유권과 접근 권한을 변경함
  - 소유자는 호출 프로세스의 실제 사용자 ID로부터 설정되며([The Persona of a Process](https://sourceware.org/glibc/manual/2.40/html_node/Process-Persona.html) 참조), 그룹은 특수 그룹(보통 _tty_) 또는 호출 프로세스의 실제 그룹 ID로부터 설정됨
  - 접근 권한은 소유자는 읽기와 쓰기, 그룹은 쓰기만 가능하도록 설정됨
- 일부 운영 체제에서 이 함수는 특수한 `setuid` 루트 프로그램을 호출하여 구현됨([How an Application Can Change Persona](https://sourceware.org/glibc/manual/2.40/html_node/How-Change-Persona.html) 참조)
  - 그 결과로, `SIGCHLD` 신호([Job Control Signals](https://sourceware.org/glibc/manual/2.40/html_node/Job-Control-Signals.html) 참조)에 대한 신호 핸들러를 설치하는 것은 `grantpt` 호출에 간섭할 수 있음
- 일반적인 반환값은 0
- 실패한 경우 -1 반환
  - 이 함수를 위해 다음 `errno` 조건이 정의됨
    - `EBADF`: `filedes` 인자가 유효한 파일 기술자가 아님
    - `EINVAL`: `filedes` 인자가 마스터 가상 터미널 디바이스와 연결되지 않음
    - `EACCES`: `filedes`에 연결된 마스터에 대응하는 슬레이브 가상 터미널 디바이스에 접근 불가

## Function: `int unlockpt(int filedes)`

Preliminary: | MT-Safe | AS-Unsafe heap/bsd | AC-Unsafe mem fd | [POSIX Safety Concepts](https://sourceware.org/glibc/manual/2.40/html_node/POSIX-Safety-Concepts.html) 참조

- 파일 기술자 `filedes`에 연결된 마스터 가상 터미널 디바이스에 대응하는 슬레이브 가상 터미널 디바이스를 해제함
- 많은 운영체제에서 슬레이브는 해제된 후에만 열 수 있으므로 portable 애플리케이션은 슬레이브를 열기 전에 언제나 `unlockpt`를 호출해야 함
- 일반적인 반환값은 0
- 실패한 경우 -1 반환
  - 이 함수를 위해 다음 `errno` 조건이 정의됨
    - `EBADF`: `filedes` 인자가 유효한 파일 기술자가 아님
    - `EINVAL`: `filedes` 인자가 마스터 가상 터미널 디바이스와 연결되지 않음

## Function: `char *ptsname(int filedes)`

- Preliminary: | MT-Unsafe race:ptsname | AS-Unsafe heap/bsd | AC-Unsafe mem fd | [POSIX Safety Concepts](https://sourceware.org/glibc/manual/2.40/html_node/POSIX-Safety-Concepts.html) 참조
- 파일 기술자 `filedes`가 마스터 가상 터미널 디바이스에 연결되어 있다면, 연결된 슬레이브 가상 터미널 파일의 파일명을 포함하는 정적 할당된, null 종단 문자열을 가리키는 포인터를 반환함
  - 이 문자열은 `ptsname`의 후속 호출에 의해 덮어써질 수 있음

## Function: `int ptsname_r(int filedes, char *buf, size_t len)`

- Preliminary: | MT-Safe | AS-Unsafe heap/bsd | AC-Unsafe mem fd | [POSIX Safety Concepts](https://sourceware.org/glibc/manual/2.40/html_node/POSIX-Safety-Concepts.html) 참조
- `ptsname` 함수와 유사하나 결과를 사용자가 명시한 `buf`에서 시작하는 길이 `len`의 버퍼에 저장함
- GNU 확장

<br />

이 함수들의 일반적인 사용법은 다음 예제에서 확인 가능

```C
int open_pty_pair(int *amaster, int *aslave) {
  int master, slave;
  char *name;

  master = posix_openpt(O_RDWR | O_NOCTTY);
  if (master < 0) return 0;

  if (grantpt(master) < 0 || unlockpt(master) < 0) goto close_master;
  name = ptsname(master);
  if (name == NULL) goto close_master;

  slave = open(name, O_RDWR);
  if (slave == -1) goto close_master;

  *amaster = master;
  *aslave = slave;
  return 1;

close_slave:
  close(slave);

close_master:
  close(master);
  return 0;
}
```
