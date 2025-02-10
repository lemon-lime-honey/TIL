# Introduction to the basics

## Minimum Version

다음은 CMake가 필요로 하고, 찾는 파일인 `CMakeLists.txt`의 첫 줄이다.

```cmake
cmake_minimum_required(VERSION 3.15)
```

CMake 문법에 관해 약간 언급한다. 명령어 [`cmake_minimum_required`](https://cmake.org/cmake/help/latest/command/cmake_minimum_required.html) 는 대소문자를 구분하지 않으므로 보통 관습적으로 소문자를 사용한다. `VERSION`은 이 함수를 위한 특수 키워드이다. 그리고 버전의 값이 키워드 다음에 온다.

이 첫 줄은 특별하다! 이 CMake의 버전은 동작 변화를 정의하는 정책에도 영향을 미친다. 그러므로, 예를 들어 `minimum_required`를 `VERSION 2.8`로 설정한다면 가장 최신 CMake 버전을 사용하더라도 macOS에서 잘못된 링크 동작이 수행될 것이다. 비슷하게, 3.3 이하를 설정한다면 숨겨진 기호(hidden symbols)의 동작이 잘못 수행될 것이다. 정책과 버전의 리스트는 [여기](https://cmake.org/cmake/help/latest/manual/cmake-policies.7.html)에서 확인 가능하다.

CMake 3.12부터는 `VERSION 3.15...3.31`과 같이 범위를 지원한다. 이는 최소 3.15를 지원하지만 3.31까지의 새로운 정책 설정으로도 시험했다는 것을 의미한다. 더 나은 설정을 필요로 하는 사용자에게 유용하며, 문법적인 트릭 덕에 (CMake 3.1-3.11을 구동하면 옛 버전이 이를 특별히 다루지 않기 때문에 구버전 정책만 설정될 것임에도 불구하고) CMake의 이전 버전에 대해 하위 호환성을 가지게 된다. 보통 CMake의 가장 최신 버전을 사용하기 때문에 새로운 버전의 정책은 macOS와 Windows 사용자에게 제일 중요한 경향이 있다.

다음은 새로운 프로젝트에 적용되어야 할 것이다:

```cmake
cmake_minimum_required(VERSION 3.15...3.31)
```

- 팁
  - 정말로 낮은 값을 여기에 적용하려면 [`cmake_policy`](https://cmake.org/cmake/help/latest/command/cmake_policy.html)를 사용해 조건부로 정책 레벨을 올리거나 특정 정책을 설정할 수 있다.

## Setting a project

이제 모든 CMake 파일의 최상위 레벨은 다음 줄을 가지게 된다:

```cmake
project(MyProject VERSION 1.0
                  DESCRIPTION "Very nice project"
                  LANGUAGES CXX)
```

더 많은 문법을 보게 되었다. 문자열은 따옴표로 감싸져 공백이 문제가 되지 않고, 프로젝트의 이름은 첫 번째 인자(위치상)이다. 여기의 모든 키워드 인자는 선택인자이다. 버전은 `MyProject_VERSION`과 `PROJECT_VERSION`과 같은 많은 변수를 설정한다. 언어는 `C`, `CXX`, `Fortran`, `ASM`, `CUDA`(CMake 3.8+), `CSharp`(3.8+), `SWIFT`(CMake 3.15+ experimental). `C CXX`가 기본값이다. CMake 3.9에서는 `DESCRIPTION`이 프로젝트 설명으로 설정되도록 추가되었다. [`project`](https://cmake.org/cmake/help/latest/command/project.html)에 관한 문서가 도움이 될 것이다.

- 팁
  - `#` 문자를 사용해 [주석](https://cmake.org/cmake/help/latest/manual/cmake-language.7.html#comments)을 추가할 수 있다. CMake는 주석에 관한 인라인 문법을 가지지만 드물게 사용된다.

프로젝트 이름에 관해서는 특별한 것이 없다. 이 지점에서는 타겟이 추가되지 않는다.

## Making an executable

라이브러리가 훨씬 더 흥미롭고, 대부분의 시간을 그것을 가지고 보내겠지만 지금은 단순한 실행파일을 가지고 시작한다.

```cmake
add_executable(one two.cpp three.h)
```

여기에는 언팩해야할 것이 여럿 있다. `one`은 생성되는 실행파일의 이름이자 생성되는 CMake 타겟의 이름이기도 하다. 소스 파일 리스트가 그 다음으로 오는데, 필요한 만큼 추가할 수 있다. CMake는 똑똑해서 소스 파일 확장자만 컴파일할 것이다. 헤더는 대부분의 목적과 의도에 따라 무시된다. 헤더를 리스트에 추가하는 것은 IDE에 나타나게 하기 위함이다. 타겟은 많은 IDE에서 폴더로 나타난다. 일반적인 빌드 시스템과 타겟에 관한 것은 [빌드 시스템](https://cmake.org/cmake/help/latest/manual/cmake-buildsystem.7.html)에서 확인 가능하다.

## Making a library

라이브러리 생성은 [`add_library`](https://cmake.org/cmake/help/latest/command/add_library.html)로 끝나며, 단순하다:

```cmake
add_library(one STATIC two.cpp three.h)
```

library, STATIC, SHARED 또는 MODULE 중 하나의 종류를 선택한다. 이를 선택하지 않으면, `BUILD_SHARED_LIBS`의 값이 STATIC과 SHARED 중 하나의 값을 선택하기 위해 사용된다.

이후의 섹션에서 보게 되듯이, 헤더만 존재하는 라이브러리처럼 컴파일할 것이 없는 타겟을 만들어야 할 때가 있다. 이것은 INTERFACE library로 불리며, 또 다른 선택이다. 파일 이름이 뒤에 올 수 없다는 것이 유일한 차이이다.

단순히 타겟에 새 이름을 부여하도록 이미 존재하는 라이브러리를 가지고 `ALIAS` 라이브러리를 만들 수 있다. 이것의 한 가지 이점은 이름에 `::`을 넣어 라이브러리를 만들 수 있다는 점이다.

## Targets are your friend

타겟을 명시할 때 그에 대한 정보는 어떻게 추가하는가? 예를 들어, 디렉토리를 include할 필요가 있을지도 모른다.

```cmake
target_include_directories(one PUBLIC include)
```

[`target_include_directories`](https://cmake.org/cmake/help/latest/command/target_include_directories.html)는 타겟에 include 디렉토리를 추가한다. `PUBLIC`은 실행 파일에서 큰 의미를 갖지 않는다. 라이브러리에 대해서는 이에 연결되는 모든 타겟에도 그 디렉토리를 include해야만 하는지 CMake가 알 수 있게 한다. 다른 옵션은 `PRIVATE`(의존성에는 영향을 미치지 않고 오직 현재 타겟에만 영향을 미친다.), 그리고 `INTERFACE`(의존성에만 필요함) 이다.

그 다음 타겟을 엮을 수 있다.

```cmake
add_library(another STATIC another.cpp another.h)
target_link_libraries(another PUBLIC one)
```

[`target_link_libraries`](https://cmake.org/cmake/help/latest/command/target_link_libraries.html)은 CMake에서 가장 유용하며 혼란스러운 명령어일 것이다. 타겟(`another`)를 가지고, 타겟이 주어졌을 때 의존성에 추가한다. 만약 그 이름(`one`)을 가진 타겟이 없다면, 경로에 `one`이라고 불리는 라이브러리 (즉 명령어의 이름) 의 링크를 추가한다. 또는 라이브러리의 전체 경로를 줄 수도 있다. 또는 링커 플래그를 전달할 수도 있다. 마지막으로 혼란스러움을 조금 더 더하자면, 고전 CMake는 `PUBLIC` 등의 키워드 선택을 생략할 수 있게 했다. 이 동작에 타겟에 수행되었고, 체인에 여러 형식을 섞으려고 하면 오류가 발생한다.

어디에서나 타겟과 키워드를 사용하는 것에 집중한다면 괜찮을 것이다.

타겟은 디렉토리, 링크된 라이브러리(또는 링크된 타겟), 컴파일 옵션, 컴파일 정의, 컴파일 특징(C++11 챕터 확인) 등을 포함할 수 있다. 두 프로젝트 include 챕터에서 확인하게 되듯이, 사용하는 모든 라이브러리를 대표하기 위해 종종 타겟을 가져올 수 (그리고 언제나 타겟을 생성할 수) 있다. OpenMP처럼 진짜 라이브러리가 아니더라도 타겟으로 대표할 수 있다.

## Dive in

다음 파일의 내용을 따라올 수 있는지 확인하자. 간단한 C++11 라이브러리와 이를 사용하는 프로그램을 생성한다. 의존성도 없다. C++ 표준 옵션에 대해서는 이후에 논의할 것이지만, 지금은 CMake 3.8 시스템을 사용한다.

```cmake
cmake_minimum_required(VERSION 3.15...3.31)

project (Calculator LANGUAGES CXX)

add_library(calclib STATIC src/calclib.cpp include/calc/lib.hpp)
target_include_directories(calclib PUBLIC include)
target_compile_features(calclib PUBLIC cxx_std_11)

add_executable(calc apps/calc.cpp)
target_link_libraries(calc PUBLIC calclib)
```
