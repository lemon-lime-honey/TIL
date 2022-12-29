# Branch
Branch는 독립적인 작업 흐름을 만들고 관리하기 위해 사용한다.

다양한 방법으로 사용할 수 있겠지만, 작업의 주제에 따라 분류해서 branch를 나누는 것이 좋아 보인다.
<br><br/>

# Commands
| 명령어 | 내용 |
| --- | ---: |
| `(master) $ git branch (branch_name)` | branch 생성 |
| `(master) $ git checkout (branch_name)` | branch 이동 |
| `(master) $ git checkout -b (branch_name)` | branch 생성 및 이동 |
| `(master) $ git branch` | branch 목록 |
| `(master) $ git branch -d (branch_name)` | branch 삭제 |
<br><br/>

# Merge
- 각 branch에서 작업을 한 후 이력을 합치기 위해 merge 명령어를 사용한다.
- 병합을 진행할 때, 서로 다른 commit에서
    - 동일한 파일을 수정한 경우 충돌 발생
        1. 직접 해당 파일을 확인하고 적절하게 수정한다.
        2. 수정 후 커밋을 실행한다.
    - 다른 파일을 수정한 경우
        - 충돌 없이 자동으로 Merge Commit이 생성된다.

## Fast Forward
기존 master branch에 변경사항이 없어 단순히 앞으로 이동

## Merge Commit
기존 master branch에 변경사항이 있어 병합 커밋 발생
