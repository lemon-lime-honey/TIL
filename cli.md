# CLI: Command Line Interface
- 가상 터미널 또는 텍스트 터미널을 통해 사용자와 컴퓨터가 상호 작용하는 방식
- 문자열의 형태로 작업 명령을 입력하면 문자열의 형태로 출력이 나타난다.
- 명령 줄 해석기, 또는 셸은 이러한 인터페이스를 제공하는 프로그램인데 유닉스 셸(bash 등), CP/M, 명령 프롬프트 등이 있다.
<br><br/>

# CLI 구성 요소
- 프롬프트 기본 인터페이스
    - 컴퓨터 정보
    - 디렉토리(cf. ~는 홈 디렉토리를 의미)
    - $
<br><br/>

# CLI 명령어
## 명령어 기본 구조
- 특정 프로그램을 어떤 인자와 함께 호출하도록 명령
- 예) echo 'hello world'

## 기초 파일시스템 명령어
- pwd: print working directory. 현재 디렉토리 출력
- cd <dir_name>: change directory. 디렉토리 이동.
    - .: 현재 디렉토리, ..: 상위 디렉토리
- ls: list. 목록
- mkdir: make directory. 디렉토리 생성
- touch: 파일 생성
- rm 파일명: 파일 삭제하기
    - rm -r <dir_name>: 폴더 삭제하기