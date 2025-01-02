# Identifying Terminals

- 이 챕터에서 설명하는 함수는 터미널 디바이스에 대응하는 파일에서만 동작함
- `isatty` 함수를 이용하여 파일 기술자가 터미널과 연결되었는지 확인 가능
- 이 섹션 내의 함수의 프로토타입은 헤더 `unistd.h`에 선언되어 있음

## `int isatty(int filedes)`

- Preliminary: | MT-Safe | AS-Safe | AC-Safe | [POSIX Safety Concepts](https://sourceware.org/glibc/manual/2.40/html_node/POSIX-Safety-Concepts.html) 확인
- 이 함수는 `filedes`가 열려 있는 터미널 디바이스와 연결된 파일 기술자라면 `1`을, 아니라면 `0`을 반환함
- 파일 기술자가 터미널과 연결되어 있다면, `ttyname` 함수를 이용해 연결된 이름을 구할 수 있음
- [제어 터미널 식별](https://sourceware.org/glibc/manual/2.40/html_node/Identifying-the-Terminal.html)에서 설명한 `ctermid` 함수 참조

## `char *ttyname(int filedes)`

- Preliminary: | MT-Unsafe race:ttyname | AS-Unsafe heap lock | AC-Unsafe lock fd mem | [POSIX Safety Concepts](https://sourceware.org/glibc/manual/2.40/html_node/POSIX-Safety-Concepts.html) 확인
- 파일 기술자 `filesdes`가 터미널 디바이스와 연결되어 있다면 `ttyname` 함수는 터미널 파일의 파일명을 포함한 정적 할당된, null 종단 문자열을 가리키는 포인터를 반환함
- 파일 기술자가 터미널과 연결되어 있지 않거나 파일명이 결정될 수 없다면 null 포인터 반환

## `int ttyname_r(int filedes, char *buf, size_t len)`

- Preliminary: | MT-Safe | AS-Unsafe heap | AC-Unsafe mem fd | [POSIX Safety Concepts](https://sourceware.org/glibc/manual/2.40/html_node/POSIX-Safety-Concepts.html) 확인
- `ttyname_r` 함수는 `buf`에서 시작해 길이 `len`을 가지는 사용자 정의 버퍼에 결과를 저장하는 것을 제외하면 `ttyname` 함수와 유사함
- `ttyname_r`의 일반적인 반환값은 `0`
  - 그렇지 않은 경우 오류를 나타내는 오류 코드가 반환됨
  - 다음은 이 함수에 대한 `errno` 오류 조건
    - `EBADF`: `filedes` 인자가 유효한 파일 기술자가 아님
    - `ENOTTY`: `filedes`가 터미널과 연결되어 있지 않음
    - `ERANGE`: 버퍼 길이 `len`이 반환되는 문자열을 저장하기에는 너무 작음
    - `ENODEV`
      - `filedes`가 슬레이브 유사 터미널을 가지는 터미널 디바이스와 연결되어 있으나 그 디바이스와 연결된 파일명을 결정할 수 없음
      - GNU 확장