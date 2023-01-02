# Object
- 객체: 숫자, 문자, 클래스 등 값을 가지고 있는 모든 것
- 파이썬은 객체지향 언어이며, 모든 것이 객체로 구현되어 있다.
- 파이썬에서는 변수, 함수, 모듈, 클래스 등이 있다.

# Variable
- 컴퓨터 메모리 어딘가에 저장되어 있는 객체를 참조하기 위해 사용되는 이름
- 동일 이름에 다른 객체를 언제든지 할당할 수 있기 때문에 `변수`라고 불린다.
- 변수는 할당 연산자(=)를 통해 값을 할당`assignment`한다.
- `type()`: 변수에 할당된 값의 타입을 반환한다.
- `id()`: 변수에 할당된 객체의 고유한 아이텐티티 값이다. 메모리 주소

## 변수 할당
- `x = y = 0`처럼 같은 값을 동시에 할당할 수 있다.
- `x, y = 0, 1`처럼 다른 값을 동시에 할당할 수 있다.
- 두 변수에 할당된 값을 서로 바꿀 때 `x, y = y, x`로 바꾸는 것이 가능하다.
```C
// 한편 C에서는...
void swap(int* a, int* b) {
        int temp = *a;
        *a = *b;
        *b = temp;
}
```

# Identifiers
- 파이썬 객체를 식별하는데 사용하는 이름
- 규칙
    - 영문 알파벳, 언더스코어(_), 숫자로 구성
    - 숫자로 시작할 수 없다.
    - 길이 제한이 없고, 대소문자가 구별된다.
    - 다음의 예약어들은 이름으로 사용할 수 없다.
        ```
        False, None, True, and, as, assert, async, await, break, 
        class, continue, def, del, elif, else, except, finally, 
        for, from, global, if, import, in, is, lambda, nonlocal, 
        not, or, pass, raise, return, try, while, with, yield
        ```
    - 또한 내장함수나 모듈 등의 이름으로도 선언하면 안된다.