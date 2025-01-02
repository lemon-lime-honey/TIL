# I/O Queues

- 이 섹션에 있는 많은 함수는 터미널 디바이스의 입력과 출력 큐를 참조함
- 이러한 큐는 I/O 스트림에 의해 구현된 버퍼링과 독립적으로 *커널 내에서* 버퍼링 형태를 구현함 ([Input/Output on Streams](https://sourceware.org/glibc/manual/2.40/html_node/I_002fO-on-Streams.html) 참조)
- 또한 *터미널 입력 큐* 는 간혹 *typeahead buffer* 로 불림
  - 터미널로부터 받았으나 어느 프로세스에 의해서도 읽히지 않은 문자들을 저장함
- 입력 큐의 크기는 `MAX_INPUT`과 `_POSIX_MAX_INPUT` 파라미터로 정해짐
  - [Limits on File System Capacity](https://sourceware.org/glibc/manual/2.40/html_node/Limits-for-Files.html) 참조
  - 큐 크기가 최소 `MAX_INPUT`임이 보장되나, 큐가 더 크거나 동적으로 크기가 변할 수 있음
    - 입력 흐름 제어가 `IXOFF` 입력 모드 비트([Input Modes](https://sourceware.org/glibc/manual/2.40/html_node/Input-Modes.html) 참조)를 설정해 활성되었다면 터미널 드라이버는 큐가 오버플로우 되지 않도록 방지하기 위해 필요할 때 STOP과 START 문자를 터미널에 전송함
      - 그렇게 하지 않으면 터미널로부터 너무 빠르게 들어와 입력이 손실될 수 있음
      - 정규모드에서는 모든 입력은 개행 문자를 받을 때까지 큐에 머물러 매우 긴 문장을 입력할 때 터미널 입력 큐가 채워지도록 함
      - [Two Styles of Input: Canonical or Not](https://sourceware.org/glibc/manual/2.40/html_node/Canonical-or-Not.html) 참조
- *터미널 출력 큐* 는 입력 큐와 비슷하지만 출력을 위한 것
  - 프로세스가 입력했으나 터미널에 전송되지는 않은 문자들을 가짐
  - 출력 흐름 제어가 `IXON` 입력 모드 비트([Input Modes](https://sourceware.org/glibc/manual/2.40/html_node/Input-Modes.html) 참조)를 설정해 활성되었다면 터미널 드라이버는 출력 전송 중지와 재개를 위해 터미널이 전송한 START와 STOP 문자를 준수함
- 터미널 입력 큐를 *비운다는 것* 은 받았으나 아직 읽지 않은 모든 문자를 버리는 것을 의미함
  - 유사하게, 터미널 출력 큐를 비운다는 것은 입력되었으나 전송하지 않은 모든 문자를 버리는 것을 의미함