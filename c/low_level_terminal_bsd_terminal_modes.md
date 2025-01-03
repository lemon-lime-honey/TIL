# BSD Terminal Modes

- 터미널 모드를 확인하고 설정하는 일반적인 방법은 [Terminal Modes](https://sourceware.org/glibc/manual/2.40/html_node/Terminal-Modes.html)에서 설명한 함수를 사용하는 것
  - 어떤 운영체제에서는 같은 동작을 수행하기 위해 이 섹션에 있는 BSD 유래 함수를 사용할 수 있음
  - 많은 운영 체제에서는 이 함수들이 존재하지 않음
  - GNU C 라이브러리에서도 Linux를 포함하여 많은 커널에서 `errno=ENOSYS`로 함수가 동작하지 못함
- 이 섹션에서 사용된 기호는 `sgtty.h`에서 선언됨

## Data Type: `struct sgttyb`

- 이 구조체는 `gtty`와 `stty`를 위한 입력 또는 출력 파라미터 리스트
- `char sg_ispeed`: 입력 회선 속도
- `char sg_ospeed`: 출력 회선 속도
- `char sg_erase`: 문자 지우기
- `char sg_kill`: 문자 제거
- `int sg_flags`: 다양한 플래그

## Function: `int gtty(int filedes, struct sgttyb *attributes)`

- Preliminary: | MT-Safe | AS-Safe | AC-Safe | [POSIX Safety Concepts](https://sourceware.org/glibc/manual/2.40/html_node/POSIX-Safety-Concepts.html) 참조
- 터미널의 속성 반환
- `gtty`는 `*attributes`를 파일 기술자 `filedes`로 연 터미널의 터미널 속성으로 설정함

## Function: `int stty(int filedes, const struct sgttyb *attributes)`

- Preliminary: | MT-Safe | AS-Safe | AC-Safe | [POSIX Safety Concepts](https://sourceware.org/glibc/manual/2.40/html_node/POSIX-Safety-Concepts.html) 참조
- 터미널의 속성을 설정함
- `stty`는 파일 기술자 `filedes`로 연 터미널의 터미널 속성을 `*attributes`로 설정함
