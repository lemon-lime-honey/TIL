# Pseudo-Terminals

- 가상 터미널은 터미널처럼 동작하는 특수한 프로세스 통신 채널
  - 채널의 한쪽 끝은 *마스터* 측 또는 *마스터 가상 터미널 디바이스*
  - 반대쪽 끝은 *슬레이브* 측
  - 마스터 측에 쓰인 데이터는 마치 그 데이터가 일반적인 터미널에 사용자가 입력한 결과인 것처럼 슬레이브 측에서 전달 받음
  - 슬레이브 측에 쓰인 데이터는 일반적인 터미널에 쓰인 데이터처럼 마스터 측으로 전송됨
- 가상 터미널은 `xterm`과 `emacs`와 같은 프로그램이 터미널 에뮬레이션 기능을 구현하는 방법
  - [Allocating Pseudo-Terminals](./low_level_terminal_pseudo_terminals_allocation.md)
  - [Opening a Pseudo-Terminal Pair](./low_level_terminal_pseudo_terminals_pair.md)