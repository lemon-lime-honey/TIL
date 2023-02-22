# CSS
- **C**ascading **S**tyle **S**heet
- 웹 페이지의 디자인과 레이아웃을 구성하는 언어

## CSS 적용방법
## Inline
```html
<!DOCTYPE html>
<html lang="en">
<head>
...
</head>
<body>
  <h1 style="color:#FFF700; background-color:#003153;">Hello, there.</h1>
</body>
```

## Internal
```html
<!DOCTYPE html>
<html lang="en">
<head>
...
  <title>Obi-Wan met R2-D2</title>
  <style>
    h1 {
        color:#FFF700;
        background-color:#003153;
    }
  </style>
</head>
<body>
  <h1>Hello, there.</h1>
</body>
```


## External
```html
<!DOCTYPE html>
<html lang="en">
<head>
...
  <link rel="stylesheet" href="style.css">
  <title>Obi-Wan met R2-D2</title>
</head>
<body>
  <h1>Hello, there.</h1>
</body>
```
```css
/* style.css*/
h1 {
  color:#FFF700;
  background-color:#003153;
}
```
<br><br>

# CSS Selectors
- HTML 요소를 선택하여 스타일을 적용할 수 있게 한다.

## CSS Selectors 종류
- 기본 선택자
    - 전체(`*`) 선택자
    - 요소(`tag`) 선택자
    - 클래스(`class`) 선택자
    - 아이디(`id`) 선택자
    - 속성(`attr`) 선택자
- 결합자(Combinators)
    - 자손결합자(` `)
    - 자식 결합자(`>`)

## CSS Selectors 특징
- 요소 선택자: 지정한 모든 태그를 선택한다.
- 클래스 선택자
    - 주어진 클래스 속성을 가진 모든 요소를 선택한다.
    - ex) `.index`는 `class="index"`를 가진 모든 요소를 선택한다.
- 아이디 선택자
    - 주어진 아이디 속성을 가진 요소를 선택한다.
    - 문서에는 주어진 아이디를 가진 요소가 하나만 있어야 한다.
    - ex) `#index`는 `id="index"`를 가진 요소를 선택한다.
- 자손 선택자(The space combinator)
    - 첫 번째 요소의 자손 요소들을 선택한다.
    - ex) `p span`은 `<p>` 안에 있는 모든 `<span>`을 선택한다.
- 자식 선택자
    - 첫 번째 요소의 직계 자식만 선택한다.
    - ex) `ul > li`는 `<ul>` 안에 있는 모든 `li`를 선택한다.

# Cascade & Specificity
## Cascade
- 동일한 우선순위를 가지는 규칙이 적용될 때 마지막에 나오는 규칙이 적용된다.
- 아래 예시의 경우: `blue`가 적용된다.
```CSS
h1 {
    color:red;
}

h1 {
    color:blue;
}
```

## Specificity
- 선택자 별로 정해진 우선순위에 따라 높은 우선순위를 가지는 규칙이 적용된다.
- 아래 예시의 경우: `red`가 적용된다.
```CSS
.make-red {
    color:red;
}

h1 {
    color:blue;
}
```

### 우선순위
1. Importance: `!important`
    - 반드시 필요한 경우가 아니라면 사용하지 않는 게 낫다.
2. 인라인 > id 선택자 > class 선택자 > 요소 선택자
3. 소스코드 순서

## 상속
- 기본적으로 CSS는 상속을 통해 부모 요소의 속성을 자식에게 상속한다.
- 이를 통해 코드의 재사용성을 높인다.
- 상속되는 속성
    - 텍스트 관련 요소(font, color, text-align)
    - opacity
    - visibility 등
- 상속되지 않는 속성
    - Box model 관련 요소(width, height, margin, padding, border, box-sizing, display)
    - position 관련 요소(position, top/right/bottom/left, z-index) 등