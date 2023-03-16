# Javascript
웹페이지의 동적인 기능을 구현한다.
<br><br>

# DOM
웹페이지를 구조화된 객체로 제공하여 프로그래밍 언어가 웹페이지를 사용할 수 있게 연결시킨다.

## $\texttt{document}$ object
- 웹페이지 객체
- DOM Tree의 진입점
- 페이지를 구성하는 모든 객체 요소를 포함한다.

## DOM Query
### $\texttt{document.querySelector()}$
- 제공한 선택자와 일치하는 element를 한 개 선택한다.
- 제공한 CSS selector를 만족하는 첫 번째 element 객체를 반환한다. (없다면 null 반환)

### $\texttt{document.querySelectorAll()}$
- 제공한 선택자와 일치하는 여러 element를 선택한다.
- 매칭할 하나 이상의 선택자를 포함하는 유효한 CSS selector를 인자(문자열)로 받는다.
- 제공한 CSS selector를 만족하는 NodeList를 반환한다.

## DOM Manipulation
### $\texttt{classList}$ property
- 요소의 클래스 목록을 DOMTokenList(유사 배열) 형태로 반환한다.
- $\texttt{add}$와 $\texttt{remove}$ 메서드를 사용해 지정한 클래스 값을 추가 혹은 제거한다.

#### $\texttt{element.classList.add()}$
- 지정한 클래스 값을 추가한다.

#### $\texttt{element.classList.remove()}$
- 지정한 클래스 값을 제거한다.

### Attribute Manipulation
#### $\texttt{element.getAttribute()}$
- 해당 요소에 지정된 값을 반환한다.

#### $\texttt{element.setAttribute()}$
- 지정된 요소의 속성 값을 설정한다.
- 속성이 이미 있으면 값을 업데이트 한다.
- 속성이 없으면 지정된 이름과 값으로 새 속성을 추가한다.

#### $\texttt{element.removeAttribute()}$
- 요소에서 지정된 이름을 가진 속성을 제거한다.

### $\texttt{textContent}$ property
요소의 텍스트 콘텐츠를 표현한다.

### DOM Element Manipulation
- $\texttt{.createElement()}$
- $\texttt{.appendChild()}$
- $\texttt{.removeChild()}$

### $\texttt{style}$ property
$\texttt{color}$, $\texttt{fontSize}$ 등으로 스타일을 변경할 수 있다.
<br>

# JavaScript 문법
## 변수
### 식별자 작성 규칙
- 반드시 문자, $, _로 시작한다.
- 대소문자를 구분하며, 클래스명 이외의 경우 모두 소문자로 시작한다.
- 예약어 사용 불가
- 카멜 케이스(camelCase): 변수, 객체, 함수에 사용한다.
- 파스칼 케이스(PascalCase): 클래스, 생성자에 사용한다.
- 대문자 스네이크 케이스(SNAKE_CASE): 상수에 사용한다.

### 변수 선언 키워드
- 기본적으로 $\texttt{const}$ 사용을 권장한다.
- 재할당해야 하는 경우에만 $\texttt{let}$을 사용한다.
- $\texttt{let}$
    - 블록 스코프를 가지는 지역 변수를 선언한다.
    - 재할당이 가능하지만 재선언은 불가능하다.
- $\texttt{const}$
    - 블록 스코프를 가지는 지역 변수를 선언한다.
    - 재할당과 재선언이 불가능하다.
- $\texttt{var}$
    - 재할당과 재선언이 가능하다.
    - ES6 이전에 변수를 선언할 때 사용했다.
    - 함수 스코프를 가진다.
    - 호이스팅되는 특성으로 예기치 못한 문제가 발생할 수 있다.
        - 변수를 선언 이전에 참조할 수 있는 현상. 변수 선언 이전의 위치에서 접근하면 `undefined`를 반환한다.
        - ES6부터 $\texttt{var}$ 대신 $\texttt{const}$와 $\texttt{let}$ 사용을 권장한다.
    - 변수 선언 시 $\texttt{var}$, $\texttt{const}$, $\texttt{let}$ 키워드 중 하나를 사용하지 않으면 자동으로 $\texttt{var}$로 선언된다.

#### 블록 스코프
- $\texttt{if}$, $\texttt{for}$, 함수 등의 중괄호 내부를 가리킨다.
- 블록 스코프를 가지는 변수는 블록 바깥에서 접근할 수 없다.
<br><br>

## 데이터 타입
### 원시 자료형(Primitive type)
- $\texttt{Number}$, $\texttt{String}$, $\texttt{Boolean}$, $\texttt{undefined}$, $\texttt{null}$
- 변수에 값이 직접 저장되는 자료형
- 불변, 값이 복사된다.

#### $\texttt{String}$
- 덧셈을 통해 문자열끼리 붙일 수 있다.
- `backtick`을 통한 `Template Literal`을 사용하여 문자열 사이에 변수를 삽입할 수 있다.

#### $\texttt{Boolean}$
- 조건문 또는 반복문에서 `boolean`이 아닌 데이터 타입은 자동 형변환 규칙에 의해 `true` 또는 `false`로 변환된다.

### 참조 자료형(Reference type)
- $\texttt{Object}$, $\texttt{Array}$, $\texttt{Function}$
- 객체의 주소가 저장되는 자료형
- 가변, 주소가 복사된다.

### ToBoolean conversions (자동 형변환)
| 데이터 타입 | false | true |
| --- | --- | --- |
| undefined | 항상 false | X |
| null | 항상 false | X |
| Number | 0, -0, NaN | 나머지 모든 경우 |
| String | 빈 문자열 | 나머지 모든 경우 |

<br><br>

## 연산자
### 할당 연산자
- 오른쪽에 있는 피연산자의 평가 결과를 왼쪽 피연산자에 할당하는 연산자
- 다양한 연산에 대한 단축 연산자를 지원한다.
- `++`, `--`, `+=`, `-=` 등

### 비교 연산자
- 피연산자(숫자, 문자, Boolean 등)를 비교하고 결과값을 boolean으로 반환하는 연산자

### 동등 연산자 `==`
- 두 피연산자가 같은 값으로 평가되는지 비교 후 boolean 값을 반환한다.
- 비교할 때 암묵적 타입 변환을 통해 타입을 일치시킨 후 같은 값인지 비교한다.
- 두 피연산자가 모두 객체일 경우 메모리의 같은 객체를 바라보는지 판별한다.
- 예상치 못한 결과가 발생할 수 있으므로 특별한 경우를 제외하면 사용하지 않는다.

### 일치 연산자 `===`
- 두 피연산자의 값과 타입이 모두 같은 경우 `true`를 반환한다.
- 같은 객체를 가리키거나 같은 타입이면서 같은 값인지 비교한다.
- 엄격한 비교가 이루어지며, 암묵적 타입 변환이 발생하지 않는다.

### 논리 연산자
| 역할 | 표기 |
| --- | --- |
| and | `&&` |
| or | `\|\|` |
| not | `!` |

<br><br>

## 조건문
### $\texttt{if}$
조건 표현식의 결과값을 boolean 타입으로 변환 후 참/거짓을 판단한다.
```javascript
if (조건문) {
  명령문
} else if (조건문) {
  명령문
} else {
  명령문
}
```
<br><br>

## 반복문
| 키워드 | 연관 키워드 | 스코프 |
| --- | --- | --- |
| $\texttt{while}$ | break, continue | 블록 스코프 |
| $\texttt{for}$ | break, continue | 블록 스코프 |
| $\texttt{for...in}$ | object 순회 | 블록 스코프 |
| $\texttt{for...of}$ | iterable 순회 | 블록 스코프 |

### $\texttt{while}$
조건문이 참이면 문장을 계속해서 수행한다.
```javascript
while (조건문) {
  // do something
}
```

### $\texttt{for}$
특정한 조건이 거짓으로 판별될 때까지 반복한다.
```javascript
for ([초기문]; [조건문]; [증감문]) {
  // do something
}
```

### $\texttt{for...in}$
객체의 속성을 순회할 때 사용한다.<br>
배열도 순회할 수 있으나 인덱스 순으로 순회한다는 보장이 없으므로 권장하지 않는다.
```javascript
for (variable in object) {
  statements
}
```

### $\texttt{for...of}$
반복 가능한 객체(배열, 문자열 등)를 순회할 때 사용한다.
```javascript
for (variable of object) {
  statements
}
```
<br><br>

# Function
참조 자료형에 속한다. `type: Function object`

## 함수의 구조
```javascript
function name ([param[, param, [..., param]]]) {
  statements
  return value
}
```
- 함수의 이름
- 함수의 매개변수
- 함수의 body를 구성하는 statement
- `return`이 없으면 `undefined`를 반환한다.

## 함수의 정의
### 선언식: function declaration
```javascript
function funcName () {
  statements
}
```

### 표현식: function expression
```javascript
const funcName = function () {
  statements
}
```
- 함수 이름이 없는 `익명함수`를 사용할 수 있다.
- 선언식과 달리 표현식으로 정의한 함수는 호이스팅 되지 않기 때문에 코드에서 나타나기 전에 먼저 사용할 수 없다.

### 선언식과 표현식 비교
|  | 선언식 | 표현식 |
| --- | --- | --- |
| 특징 | 익명 함수 사용 불가능<br>호이스팅 있음 | 익명함수 사용 가능<br>호이스팅 없음 |
| 비고 |  | 사용 권장 |

### 기본 함수 매개변수(Default function parameter)
```javascript
const greeting = function (name = 'Anakin') {
  return `Hi ${name}`
}

greeting() // Hi Anakin
```
값이 없거나 `undedfined`가 전달될 경우 이름이 붙은 매개변수를 기본값으로 초기화한다.

#### 매개변수와 인자의 개수가 일치하지 않을 때
매개변수 개수 < 인자 개수
```javascript
const noArgs = function () {
  return 0
}
noArgs(1, 2, 3) // 0

const twoArgs = function (arg1, arg2) {
  return [arg1, arg2]
}
twoArgs(1, 2, 3) // [1, 2]
```

매개변수 개수 > 인자 개수
```javascript
const threeArgs = function (arg1, arg2, arg3) {
  return [arg1, arg2, arg3]
}

threeArgs()      // [undefined, undefined, undefined]
threeArgs(1)     // [1, undefined, undefined]
threeArgs(2, 3)  // [2, 3, undefined]
```

### 나머지 매개변수(Rest parameters)
```javascript
const myFunc = function (arg1, arg2, ...restArgs) {
  return [arg1, arg2, restArgs]
}

myFunc(1, 2, 3, 4, 5) // [1, 2, [3, 4, 5]]
myFunc(1, 2)          // [1, 2, []]
```
- 무한한 수의 인자를 배열로 허용하여 가변 함수를 나타낸다.
- 함수 정의에는 하나의 나머지 매개변수만 존재할 수 있다.
- 나머지 매개변수는 함수 정의에서 마지막 매개변수여야 한다.

### 화살표 함수 표현식(Arrow function expression)
```javascript
const arrow = function (name) {
  return `hello, ${name}`
}

const arrow1 = (name) => { return `hello, ${name}` }
const arrow2 = name => { return `hello, ${name}` }
const arrow3 = name => `hello, ${name}`
```
함수 표현식의 간결한 표현법
1. function 키워드 제거 후 매개변수와 중괄호 사이에 화살표 작성
2. 함수의 매개변수가 하나 뿐이라면 매개변수의 `()` 제거 가능
3. 함수 본문의 표현식이 한 줄이라면 `{}`와 `return` 제거 가능

#### 응용
```javascript
// 1. 인자가 없다면 () 또는 _로 표시 가능
const noArgs1 = () => 'No args'
const noArgs2 = _ => 'No args'

// 2-1. 객체를 반환한다면 return을 명시적으로 작성해야 한다.
const returnObject1 = () => { return { key: 'value' } }

// 2-2. return을 쓰지 않으려면 소괄호로 감싸야 한다.
const returnObject2 = () => ({ key: 'value' })
```
<br><br>

# Object
키로 구분된 데이터 집합(data collection)을 저장하는 자료형

## 객체의 구조
```javascript
const user = {
  name: 'Obi-Wan', 
  age: '38'
  'key with space' : true, 
  // trailing comma: 속성을 추가, 삭제, 이동하기가 용이해진다.
}
```
- 중괄호를 이용해 작성한다.
- 중괄호 안에는 `key:value` 쌍으로 구성된 속성(property)를 여러 개 넣을 수 있다.
- `key`는 문자형, `value`는 모든 자료형이 허용된다.

## 객체의 속성
### Property 활용
```javascript
// 조회
console.log(user.age)               // 38
console.log(user['key with space']) // true

// 추가
user.address = 'coruscant'
console.log(user)
// {name: 'Obi-Wan', age: 38, key with space: true, address: 'coruscant'}

// 수정
user.age = 25
console.log(user.age)               // 25

// 삭제
delete user.address
console.log(user)
// {name: 'Obi-Wan', age: 38, key with space: true}
```

### Property 존재 여부 확인: `in`
```javascript
console.log('age' in user)      // true
console.log('country' in user)  // false
```

### 단축 Property
```javascript
const age = 22
const address = 'coruscant'

const oldUser = {
  age: age,
  address: address,
}

const newUser = {
  age,
  address,
}
```
키 이름과 값으로 쓰이는 변수의 이름이 같은 경우 단축 구문을 사용할 수 있다.

### 계산된 Property
```javascript
const product = prompt('물건 이름을 입력해주세요')
const prefix = 'my'
const suffix = 'property'

const bag = {
  [product]: 5,
  [prefix + suffix]: 'value',
}

console.log(bag)
// {라이트세이버: 5, myproperty: 'value'}
```

## 객체와 함수
### Method
- 객체 속성에 정의된 함수
- 객체를 `행동`할 수 있게 한다.
- `this` 키워드를 사용해 객체에 관한 특정한 작업을 수행할 수 있다.

#### `this` keyword
```javascript
const jedi = {
  name: 'Anakin', 
  greeting: function () {
    return `Hello my name is ${this.name}`
  },
}

console.log(person.greeting())
// Hello my name is Anakin
```
- 함수나 메서드를 호출한 객체를 가리킨다.
- 함수 내에서 객체의 속성 및 메서드에 접근하기 위해 사용한다.
- 함수를 호출하는 방법에 따라 가리키는 대상이 다르다.
    - 단순 호출: 전역 객체
    - 메서드 호출: 메서드를 호출한 객체

##### 단순 호출
```javascript
const myFunc = function () {
  return this
}

console.log(myFunc())       // window
```

##### 메서드 호출
```javascript
const myObj = {
  data: 1,
  myFunc: function () {
    return this
  }
}

console.log(myObj.myFunc()) // myObj
```

### Nested 함수에서의 문제점과 해결책
```javascript
const myObj2 = {
  numbers: [1, 2, 3],
  myFunc: function () {
    this.numbers.forEach(function (number) {
        console.log(number) // 1 2 3
        console.log(this)   // window
    })
  }
}
```
`forEach`의 인자로 들어간 함수는 일반 함수 호출이기 때문에 `this`가 전역 객체를 가리킨다.

```javascript
const myObj3 = {
  numbers: [1, 2, 3]
  myFunc: function () {
    this.numbers.forEach((number) => {
        console.log(number) // 1 2 3
        console.log(this)   // myObj3
    })
  }
}
```
화살표 함수는 자신만의 `this`를 가지지 않기 때문에 외부 함수에서 `this` 값을 가져온다.
<br><br>

# Array
- 순서가 있는 데이터 집합을 저장하는 자료구조

## 배열의 구조
```javascript
const fruits = ['apple', 'banana', 'coconut']

console.log(fruits[0])
console.log(fruits[1])
console.log(fruits[2])

console.log(fruits.length)
```
- 대괄호를 이용해 작성한다.
- `length`를 사용해 배열에 담긴 요소가 몇 개인지 알 수 있다.
- 배열 요소의 자료형에는 제약이 없다.
- 배열의 마지막 요소는 객체와 마찬가지로 쉼표로 끝날 수 있다.

## 배열과 반복
```javascript
// for
for (let i = 0; i < fruits.length; i++) {
  console.log(fruits[i])
}

// for...of
for (const fruit of fruits) {
  console.log(fruit)
}
```

## 배열과 메서드
| 메서드 | 기능 | 역할 |
| --- | --- | --- |
| `push`/`pop` | 배열 끝 요소 추가/제거 | 요소 추가/제거 |
| `unshift`/`shift` | 배열 앞 요소 추가/제거 | 요소 추가/제거 |
| `forEach` | 인자로 주어진 함수(콜백함수)를 배열 요소 각각에 대해 실행 | 반복 |
| `map` | 배열 요소 전체를 대상으로 함수(콜백함수)를 호출하고,<br>함수 호출 결과를 배열로 반환 | 변형 |

### `pop`
```javascript
console.log(fruits.pop())    // coconut
console.log(fruits)          // ['apple', 'banana']
```
배열 끝 요소를 제거하고 제거한 요소를 반환한다.

### `push`
```javascript
fruits.push('orange')
console.log(fruits)          // ['apple', 'banana', 'orange']
```
배열 끝에 요소를 추가한다.

### `shift`
```javascript
console.log(fruits.shift())  // apple
console.log(fruits)          // ['banana', 'orange']
```
배열 앞 요소를 제거하고 제거한 요소를 반환한다.

### `unshift`
```javascript
fruits.unshift('melon')
console.log(fruits)          // ['melon', 'banana', 'orange']
```
배열 앞에 요소를 추가한다.

### `forEach`
```javascript
array.forEach(function (item, index, array)) {
  // do something
}
```
- 인자로 주어진 함수(콜백 함수)를 배열 요소 각각에 대해 실행한다.
- 콜백 함수는 3가지 매개변수로 구성된다.
    1. `item`: 배열의 요소
    2. `index`: 배열 요소의 인덱스
    3. `array`: 배열
- 반환 값: `undefined`

## 콜백 함수(Callback function)
다른 함수에 인자로 전달되는 함수<br>
외부 함수 내에서 호출되어 일종의 루틴이나 특정 작업을 진행한다.

### `map`
배열 요소 전체를 대상으로 함수(콜백 함수)를 호출하고 함수 호출 결과를 모아 새로운 배열을 반환한다.

#### `map` 구조
```javascript
const result = array.map(function (item, index, array)) {
  // do something
}
```
기본적으로 `forEach`구조와 같으나 `forEach`와는 달리 새로운 배열을 반환한다.
<br><br>

# 이벤트
DOM 요소는 event를 받고, 받은 event를 처리할 수 있다.

## Event Handler
이벤트가 발생했을 때 실행되는 함수

### $\texttt{.addEventListener()}$
```javascript
EventTarget.addEventListener(type, handler)
```
- 대표적인 이벤트 핸들러 중 하나
- 특정 이벤트를 DOM 요소가 수신할 때마다 콜백 함수를 호출한다.
- `type`: 이벤트 이름
- `handler`
    - 발생한 이벤트 객체를 수신하는 콜백 함수
    - 콜백 함수는 발생한 Event object를 유일한 매개변수로 받는다.

#### 예시
```html
<body>
  <button id="btn">버튼</button>

  <script>
    // id가 btn인 요소 선택
    const btn = document.querySelector('#btn')
    console.log(btn)

    // 선택한 버튼에 이벤트 핸들러 부착
    // 버튼에서 click 이벤트가 발생할 때마다 함수가 실행된다
    btn.addEventListener('click', function (event)) {
      // 이벤트 객체
      console.log(event)

      // 이벤트가 발생한 대상
      console.log(event.target)
      console.log(this)
    }
  </script>
</body>
```

### click 이벤트
예시: 버튼을 누르면 숫자가 1씩 증가
```html
<button id="btn">버튼</button>
<p id="counter">0</p>

<script>
  // 초기값
  let countNumber = 0

  // id가 btn인 요소 선택
  const btn = document.querySelector('#btn')
  console.log(btn)

  // 선택한 버튼에 이벤트 핸들러 부착
  // 버튼에서 click 이벤트가 발생할 때마다 함수가 실행된다.
  btn.addEventListener('click', function () {
    console.log('click!')

    // countNumber를 증가시키고
    countNumber += 1

    // id가 counter 안의 요소의 컨텐츠를 변경한다.
    const counter = document.querySelector('#counter')
    counter.textcontent = countNumber
  })
</script>
```

### input 이벤트
예시: 입력 값을 실시간으로 출력하기
```html
<body>
  <input type="text" id="text-input">
  <p></p>

  <script>
    // 1. input 요소 선택
    const textInput = document.querySelector('#text-input')

    // 2. 이벤트 핸들러 부착
    textInput.addEventListener('input', function (event) {
      console.log(evnet.target.value)

      // 3. input에 작성한 value를 p 태그의 컨텐츠로 출력하기
      const pTag = document.querySelector('p')
      pTag.textContent = event.target.value
    })
  </script>
</body>
```

### click & input 이벤트
예시: 입력 값을 실시간으로 출력하기 + 버튼을 클릭하면 출력 값의 스타일을 변경하기
```html
<h1></h1>
<button id="btn">클릭</button>
<input type="text" id="text-input">

<script>
  // 인풋
  const input = document.querySelector('#text-input')

  input.addEventListener('input', function (event) {
    const h1Tag = document.querySelector('h1')
    h1Tag.textContent = event.target.value
  })

  // 버튼
  const btn = document.querySelector('#btn')

  btn.addEventListener('click', function () {
    const h1 = document.querySelector('h1')
    // 클래스 blue를 토글한다.
    h1.classList.toggle('blue')
  })
</script>
```

### 이벤트 취소하기
예시: 텍스트를 복사하려고 하면 알림 창을 띄우며 복사를 중단시키기
```html
<body>
  <h1>Copy?</h1>

  <script>
    const h1 = document.querySelector('h1')

    h1.addEventListener('copy', function (event) {
      // copy event 취소
      event.preventDefault()
      alert('Canceled.')
    })
  </script>
</body>
```