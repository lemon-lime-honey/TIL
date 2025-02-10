# Variables and the Cache

## Local Variables

먼저 변수를 다룬다. 지역 변수는 다음과 같이 설정한다:

```cmake
set(MY_VARIABLE "value")
```

변수의 이름은 대개 대문자로 이루어지며, 값이 그 뒤에 온다. `${MY_VARIABLE}` 처럼 `${}` 을 사용해 변수에 접근한다. CMake는 변수 영역 개념을 가진다. 같은 영역에 있다면 변수를 설정한 후 그 변수의 값에 접근할 수 있다. 함수나 서브 디렉토리 안의 파일에서 벗어난다면 변수는 더이상 정의된 상태가 아니다. 마지막에 `PARENT_SCOPE` 를 추가해 영역 내에서 현재 영역의 바로 상위 영역에 변수를 설정할 수 있다.

리스트를 설정할 때, 이는 단순히 일련의 여러 값일 뿐이다:

```cmake
set(MY_LIST "one" "two")
```

내부적으로는 `;`으로 구분된 값이 된다. 따라서 다음과 동일하다:

```cmake
set(MY_LIST "one;two)
```

`list(` 명령은 리스트를 다루기 위한 유틸리티를 가지며, `separate_arguments`는 공백으로 구분된 문자열을 그 자리에서 리스트로 변환한다. CMake에서는 따옴표로 감싸지 않은 값은 공백을 포함하지 않고 따옴표로 감싼 값과 동일하다는 점에 유의한다. 이는 공백을 포함할 수 없다는 것을 하는 값을 다룰 때 따움표로 감싸는 것을 생략할 수 있게 한다.

`${}` 문법을 사용해 변수가 확장될 때, 공백에 관한 모든 같은 규칙이 적용된다. 경로에는 특별히 주의를 기울여야 한다. 경로는 언제든지 공백을 포함할 수 있으며, 변수일 때 언제나 따옴표로 감싸져야 한다. (절대 `${MY_PATH}`라고 쓰면 안 된다. 무조건 `"${MY_PATH}"`로 작성해야 한다.)

## Cache Variables

명령줄에서 변수를 설정하고 싶다면, CMake는 변수 캐시를 제공한다. `CMAKE_BUILD_TYPE`과 같은 어떤 변수들은 이미 포함되어 있다. 이미 설정되지 않은 변수를 선언하고 설정할 때 사용하는 문법은 다음과 같다:

```cmake
set(MY_CACHE_VARIABLE "VALUE" CACHE STRING "Description")
```

이는 이미 존재하는 값을 대체하지 **않는다**. 그렇기 때문에 명령줄에서 설정하고 CMake 파일이 실행될 때 덮어쓰지 않게 된다. 이러한 변수를 임시적인 전역 변수로 만들고 싶다면 다음을 수행한다:

```cmake
set(MY_CACHE_VARIABLE "VALUE" CACHE STRING "" FORCE)
mark_as_advanced(MY_CACHE_VARIABLE)
```

첫 번째 줄은 무조건 값이 설정되도록 하며, 두 번째 줄은 `cmake -L ..` 또는 GUI를 사용해 변수 목록을 불러올 때 그 변수를 유지하게 한다. `INTERNAL` 타입을 사용해 같은 동작을 수행할 수도 있다. (정확히는 STRING 타입으로 강제하지만, 이는 변수에 의존하는 모든 CMake 코드에 영향을 주지 않는다.)

```cmake
set(MY_CACHE_VARIABLE "VALUE" CACHE INTERNAL "")
```

`BOOL`이 일반적인 변수 타입이므로, 단축어를 사용해 좀 더 간결히 설정할 수 있다:

```cmake
option(MY_OPTION "This is settable from the command line" OFF)
```

`BOOL` 데이터 타입에 대해서는, `ON` 과 `OFF` 대신 사용할 수 있는 용어가 여럿 있다.

CMake의 알려진 변수 목록은 [cmake-variables](https://cmake.org/cmake/help/latest/manual/cmake-variables.7.html)에서 확인할 수 있다.

## Environment Variables

일반적으로는 사용하지 않는 것이 좋지만, 환경 변수를 `set(ENV{variable_name} value)` 로 설정하고 `$ENV{variable_name}` 로 불러올 수도 있다.

## The Cache

캐시는 CMake를 실행할 때 빌드 디렉토리에 생성되는 텍스트 파일, `CMakeCache.txt` 이다. 설정한 것을 CMake가 기억하는 이유이며, 그래서 CMake를 다시 실행할 때마다 매번 옵션을 다시 나열할 필요가 없다.

## Properties

CMake가 정보를 저장하는 다른 방법으로는 properties에 저장하는 법이 있다. 이는 변수와 유사하지만, 디렉토리 또는 타켓과 같은 다른 아이템에 첨부된다. 전역 property는 유용한 캐시되지 않은 전역 변수가 될 수 있다. 많은 타겟 property는 `CMAKE_` 로 시작하는 변수로 초기화된다. 그러므로 예를 들어, `CMAKE_CXX_STANDARD`를 설정하는 것은 모든 새로운 타겟은 생성될 때 `CXX_STANDARD` 가 설정된다는 것을 의미한다. Property를 설정하는 데에는 두 가지 방법이 있다:

```cmake
set_property(TARGET TargetName
             PROPERTY CXX_STANDARD 11)

set_target_properties(TargetName PROPERTIES
                      CXX_STANDARD 11)
```

첫 번째 형태가 좀 더 일반적이며, 한 번에 복수의 타겟/파일/테스트를 설정할 수 있고, 유용한 옵션을 가진다. 두 번째는 하나의 타겟에 여러 property를 설정하기 위한 단축어이다. 그리고 비슷하게 propery를 불러올 수 있다:

```cmake
get_property(ResultVariable TARGET TargetName PROPERTY CXX_STANDARD)
```

모든 알려진 property 목록은 [`cmake_properties`](https://cmake.org/cmake/help/latest/manual/cmake-properties.7.html)에서 확인할 수 있다. 일부 경우(Interface 타겟에는 허용되는 사용자 정의 property에 제한이 존재할 수 있다.)에는 property를 새로 정의할 수도 있다.
