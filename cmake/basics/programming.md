# Programming in CMake

## Control flow

CMake는 시간이 흐르며 복잡해지기는 했으나, [`if` 문](https://cmake.org/cmake/help/latest/command/if.html)을 가지고 있다. if문 내부에서 사용할 수 있는 일련의 모든 대문자 키워드가 있으며, 이름으로 직접, 또는 `${}` 문법을 사용해 변수를 참조할 수 있다. (if문은 역사적으로 변수 확장 이전에 존재한다.) 다음은 if문 예시이다:

```cmake
if(variable)
    # If variable is `ON`, `YES`, `TRUE`, `Y`, or non zero number
else()
    # If variable is `0`, `OFF`, `NO`, `FALSE`, `N`, `IGNORE`, `NOTFOUND`, `""`, or ends in `-NOTFOUND`
endif()
# If variable does not expand to one of the above, CMake will expand it then try again
```

`${variable}` 처럼 변수 확장을 명시적으로 추가하면 혼동될 수 있으므로, 확장에 관한 확장 가능성 때문에 따옴표로 감싸진 확장이 다시 확장되는 것을 방지하는 정책 ([CMP0054](https://cmake.org/cmake/help/latest/policy/CMP0054.html))이 CMake 3.1+에서 추가되었다. 그러므로 CMake의 최소 버전이 3.1+라면, 다음을 사용할 수 있다:

```cmake
if("${variable}")
    # True if variable is not false-like
else()
    # Note that undefined variables would be `""` thus false
endif()
```

다음과 같은 여러 키워드 또한 존재한다.

- Unary: `NOT`, `TARGET`, `EXISTS` (파일), `DEFINED`, etc.
- Binary: `STREQUAL`, `AND`, `OR`, `MATCHES` (정규식), `VERSION_LESS`, `VERSION_LESS_EQUAL` (CMake 3.7+), etc.
- 괄호는 그룹으로 묶는데 사용될 수 있다.

## generator-expressions

[generator-expressions](https://cmake.org/cmake/help/latest/manual/cmake-generator-expressions.7.html)는 매우 강력하지만 약간 특이하고 특수하다. 위에서 다루었던 if문을 포함한 대부분의 CMake 명령은 구성 시간(configure time)에 발생한다. 그런데 만약 빌드 시간(build time)이나 심지어 설치 시간(install time)에 로직이 발생할 필요가 있다면? 생성자 표현식은 이러한 목적을 위해 추가되었다. (실제로는 각 빌드 구성에서 산출됨에도 불구하고 빌드/설치 시간에 산출된 것처럼 동작한다.) 타겟 property에서 산출된다.

가장 단순한 생성자 표현식은 정보 표현식이며, `$<KEYWORD>` 의 형식을 가지고 현재 구성에 관한 정보를 산출한다. 다른 형식은 `$<KEYWORD:value>` 로, `KEYWORD` 는 산출을 제어하는 키워드, `value` 는 산출할 아이템(여기서도 정보 표현식 키워드가 허용된다.)이다. 만약 `KEYWORD` 가 0 또는 1을 산출하는 생성자 표현식 또는 변수라면, `value` 는 1이면 치환, 0이면 치환되지 않는다. 생성자 표현식을 중첩할 수 있으며, 중첩된 변수를 읽기 용이하게 하도록 변수를 사용할 수 있다. 어떤 표현식은 콤마로 분리된 복수의 값을 허용한다. (CMake 문서는 표현식을 정보, 논리, 그리고 출력으로 분리한다.)

예를 들어 DEBUG 구성 한정으로 컴파일 플래그를 추가하고 싶다면 다음과 같이 작성할 수 있다:

```cmake
target_compile_options(MyTarget PRIVATE "$<$<CONFIG:Debug>:--my-flag>")
```

## Macros and Functions

## Arguments
