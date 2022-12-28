# Git?
- 분산 버전 관리 시스템. 코드의 버전을 관리하는 도구
- 2005년 리눅스 커널을 위한 도구로 리누스 토르발스가 개발
- 컴퓨터 파일의 변경사항을 추적하고 여러 사용자들 간에 파일들의 작업을 조율
<br><br/>

# 중앙 집중식 버전 관리 시스템 <br/> vs. 분산 버전 관리 시스템
- 중앙 집중식 버전 관리 시스템
    - 로컬에서는 파일을 편집하고 서버에 반영
    - 중앙 서버에서만 버전을 관리
- 분산 버전 관리 시스템
    - 로컬에서도 버전을 기록하고 관리
    - 원격 저장소를 활용하여 협업
<br><br/>

# Git 버전 관리
*Working Directory - Staging Area - Repository*
1. 작업을 한다.
2. 변경된 파일들을 `add`하여 staging area에 모은다.
3. `commit`으로 버전을 기록한다.
<br><br/>

## 파일의 상태
- `modified`: 파일이 수정된 상태
- `staged`: 수정한 파일을 곧 커밋할 것이라고 표시한 상태
- `committed`: 커밋이 된 상태
<br><br/>

## Git 버전 관리의 특징
- Git은 데이터를 파일 시스템의 스냅샷으로 관리하는데, 크기가 매우 작다.
- 파일이 달라지지 않으면 성능을 위해 파일을 새로 저장하지 않는다.
- 기존의 델타 기반 버전 관리시스템과 가장 큰 차이를 가진다.


### 파일 관리 상태
- `$ git status`로 확인할 수 있는 파일의 상태
    - `Tracked`: 이전부터 버전으로 관리되고 있는 파일 상태
        - `Unmodified`: Git Status에 나타나지 않음
        - `Modified`: add가 안된 상태
        - `Staged`: add는 했으나 commit은 안한 상태
    - `Untracked`: 버전으로 관리된 적 없는 파일 상태(파일을 새로 만든 경우)
<br><br/>

# Git 저장소
## 필수 설정
### 사용자 정보(commit author): 커밋을 하기 위해 반드시 필요
*GitHub에서 설정한 username과 email 이용*
- `git config --global user.name "username"`
- `git config --global user.email "my@email.com"`

### 설정 확인
- `git config -l`
- `git config --global -l`
- `git config user.name`

### Git Config 플래그
- --system
    - `/etc/gitconfig`
    - 시스템의 모든 사용자와 모든 저장소에 적용(관리자 권한)
- --global
    - `~/.gitconfig`
    - 현재 사용자에게 적용되는 설정
- --local
    - `.git/config`
    - 특정 저장소에만 적용되는 설정
<br><br/>

## 기본 명령어
### $ git init
- 특정 폴더에 git 저장소(repository)를 만들고 버전 관리
    - .git 폴더(숨김)가 생성되며 git bash에서는 `(master)`라는 표기를 확인할 수 있음

### $ git add <file>
- working directory 상의 변경 내용을 staging area에 추가하기 위해 사용
    - `untracked` 상태의 파일을 `staged`로 변경
    - `modified` 상태의 파일을 `staged`로 변경

### $ git commit -m '<커밋메시지>'
- staged 상태의 파일들을 커밋을 통해 버전으로 기록
- SHA-1 해시를 사용하여 40자 길이의 체크섬을 생성하여 고유한 커밋을 표기
- 커밋 메시지는 변경 사항을 나타낼 수 있도록 명확히 작성해야 함

### $ git log
- 현재 저장소에 기록된 커밋을 조회
- 다양한 옵션을 통해 로그를 조회할 수 있음
#### **Example**
    $ git log -1
    $ git log --oneline
    $ git log -2 --oneline

### $ git status
- Git 저장소에 있는 파일의 상태를 확인하기 위해 활용
    - 파일의 상태를 알 수 있음
        - `Untracked files`
        - `Changes not staged for commit`
        - `Changes to be commited`
    - `Nothing to commit, working tree clean`: 파일이 모두 최신 상태로 커밋됨

## 원격 저장소 활용하기
### $ git push
- 로컬 저장소의 버전을 원격 저장소로 보낸다.

### $ git pull
- 원격 저장소의 버전을 로컬 저장소로 가져온다.
<br><br/>

# GitHub
## 원격 저장소 설정하기
1. GitHub에서 `New Repository`를 선택해 저장소를 만든다.
2. URL을 복사한다.
3. 로컬에서 `$ git remote add origin [url]`을 이용해 로컬 저장소에 원격 저장소 정보를 설정한다.
4. `$ git remote -v`로 원격 저장소의 정보를 확인할 수 있다.
<br><br/>

## 로컬 저장소 버전을 원격 저장소로 Push하기
**`$ git push [remote_name] [branch_name]`**
- 원격 저장소로 로컬 저장소 변경 사항(커밋)을 push
    - 원격 저장소는 로컬 폴더의 파일이나 폴더가 아닌 저장소의 버전(커밋)을 관리한다.
- 참고: push를 할 때에는 인증 정보가 필수적이다.
<br><br/>

## 원격 저장소의 버전을 로컬 저장소로 Pull하기
**`$ git pull [remote_name] [branch_name]
- 원격 저장소로부터 변경된 내역을 받아와 이력을 병합한다.
<br><br/>

## 원격 저장소 복제하기
**`$ git clone [url]`**
- 원격 저장소를 복제하여 가져온다.
- 원격 저장소의 `커밋`을 가져오는 pull과는 다르다.

## 명령어
| 명령어 | 내용|
| :-- | --: |
| `git clone [url]` | 원격 저장소 복제 |
| `git remote -v` | 원격 저장소 정보 확인 |
| `git remote add [remote_name] [url]` | 원격 저장소 추가 <br/> (일반적으로 origin)|
| `git remote rm [remote_name]` | 원격 저장소 삭제|
| `git push [remote_name] [branch_name]` | 원격 저장소에 push |
| `git pull [remote_name] [branch_name]` | 원격저장소로부터 pull |
<br><br/>

# Push Conflict
- 로컬과 원격 저장소의 커밋 이력이 다를 때 발생한다.
- 해결방법
    1. 원격 저장소의 커밋을 로컬 저장소로 가져온다. (pull)
    2. 로컬에서 두 커밋을 병합한다. (추가 커밋 발생)
    3. 다시 GitHub로 push한다.
<br><br/>

# .gitignore
- 버전 관리를 하지 않아도 되는 파일이나 디렉토리가 있을 때 사용한다.
- Git 저장소에 `.gitignore` 파일을 생성하고 해당 내용을 관리한다.
- ***이미 커밋된 파일***은 삭제를 해야 적용이 된다.
- [gitignore.io](https://gitignore.io)를 이용하면 편하다.