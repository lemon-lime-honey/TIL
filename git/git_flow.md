# Git Flow
- Git을 활용하여 협업하는 흐름. Branch를 활용하는 전략.
- GitHub Flow, GitLab Flow 등 각 서비스별로 제안되는 흐름이 있으며, 변형되어 활용된다.
<br><br/>

# GitHub Flow
### GitHub Flow의 기본 원칙
1. Master branch에 있는 모든 것은 언제나 배포 가능하여야 한다.
2. Branch의 이름은 다른 사람이 봐도 무슨 일이 진행되고 있는지 알 수 있도록 정해져야 한다.
3. Commit 메시지는 아주 중요하다. Commit 메시지를 명확하게 작성하면 다른 사람들이 잘 이해하게, 그리고 피드백을 제공하게 하기 쉽다.
4. Pull Request는 오픈소스 프로젝트에 기여하거나 공유 저장소의 변화를 관리하는데에 유용하다.
5. 변경사항을 반영하려면 master branch에 병합한다.

### GitHub Flow Models
#### **Shared Repository Model**
- 동일한 저장소를 공유하여 활용하는 방식
1. 팀원 초대 및 저장소 Clone
    - Collaborator에 등록: 저장소에 대한 push 권한 부여
2. branch에서 작업 및 GitHub Push
    - 작업은 독립적인 feature branch에서 한다.
    - master branch는 항상 배포 가능한 상태를 유지한다.
    - Commit으로 작업 이력을 남기는데, 이때 메시지를 일관된 형식으로 알아보기 좋게 작성한다.
    - 코드가 완성되면 원격 저장소에 push를 한다.
3. Pull Request 생성
    - GitHub에 들어가서 Pull Request 버튼을 누르고, PR에 관한 설정을 진행한 후 요청을 생성한다.
4. Review 및 Merge
    - (저장소 소유자) 작성된 코드를 확인한 후 판단에 따라 병합을 한다.
    - 병합 과정에서 충돌이 발생하면 충돌을 해결한 후 병합한다.
    - master branch로 병합할 경우 코드가 반드시 배포 가능한 상태여야 한다.
5. 병합 후
    - 로컬 저장소에서는 병합된 branch를 삭제하고 master branch를 업데이트 한다.

#### **Fork & Pull Model**
- Repository의 Collaborator에 등록되지 않은 상태에서 진행
- GitHub 기반의 오픈소스 참여 과정에서 쓰이는 방식
1. Fork & Clone
    - 원격 저장소를 fork한다.
    - Clone을 하는데, 이때 반드시 본인 저장소인지 확인한다.
2. branch에서 작업 및 GitHub Push
3. Pull Request 생성
4. 병합 후
    - 로컬 저장소에서는 merge된 branch를 삭제하고 master branch를 업데이트 한다.
        - **단, master branch에 원본 저장소를 받아와야 하며 별도의 원격 저장소를 추가하여 진행할 수 있다.**
        - **GitHub에서 fetch upstream을 할 수도 있다.**