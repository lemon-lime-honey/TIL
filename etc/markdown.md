# Introduction to Markdown
## Markdown?
* 텍스트 형식 문법의 일종
* 특정한 형식의 텍스트를 HTML로 변환시켜주는 도구
* 읽기 용이한 것을 목표로 한다.
    
## Basic Syntax
***띄어쓰기와 줄바꿈 매우 중요***

### ***Heading***
> 제목. 가장 큰 것부터 가장 작은 것까지 여섯가지.
>
>문서의 구조를 위해 사용되기 때문에 글자 크기를 조절하기 위한 목적으로는 사용하지 않는다.

#### **Example**
    # Yoda
    ## Dooku
    ### Qui-Gon Jinn
    #### Obi-Wan Kenobi
    ##### Anakin Skywalker
    ###### Ahsoka Tano


### ***Bold***
> 볼드체. 글자를 두껍게 만들어준다.

#### **Example**
**Grogu**

`**Grogu**`


### ***Italic***
> 이탤릭체. 글자를 기울여준다.

#### **Example**
*Din Djarin*

`*Din Djarin*`


### ***Blockquote***
> 인용문

#### **Example**
> Mandalorian is not a race, it's a creed.

`> Mandalorian is not a race, it's a creed.`


### ***Ordered List***
> 순서가 있는 리스트.
>
> 숫자를 임의로 지정해도 알아서 첫번째 숫자부터 순서가 정해진다.

#### **Example**
1. Qui-Gon Jinn
2. Obi-Wan Kenobi
3. Anakin Skywalker
```
1. Qui-Gon Jinn
2. Obi-Wan Kenobi
3. Anakin Skywalker
```


### ***Unordered List***
> 순서가 없는 리스트.
>
> -, *, +를 사용할 수 있는데, 같은 수준에서는 동일하게 나타난다.

#### **Example**
- Qui-Gon Jinn
* Obi-Wan Kenobi
+ Anakin Skywalker
```
- Qui-Gon Jinn
* Obi-Wan Kenobi
+ Anakin Skywalker
```


### ***Code***
> inline 코드 강조.
>
> 단독으로도, 문장 중간에 넣어서도 사용할 수 있다.

#### **Example**
`Mandalorian`

Din Djarin is a `Mandalorian`.
```
`Mandalorian`
Din Djarin is a `Mandalorian`
```


### ***Horizontal Rule***
> 가로선. 구분을 할 때 쓰기 좋다.
>
> 3개 이상의 *, -, _를 사용해 나타내는데, 셋 모두 동일한 결과가 나온다.

#### **Example**
---
```
***
---
___
```


### ***Link***
> 누르면 웹페이지로 연결된다.

#### **Example**
[The Mandalorian](https://en.wikipedia.org/wiki/The_Mandalorian)
```
[The Mandalorian](https://en.wikipedia.org/wiki/The_Mandalorian)
```


### ***Image***
> 이미지를 첨부할 때 사용한다.
#### **Example**
```
![name](image.jpg)
```


## Extended Syntax
***모든 환경에서 지원하는 것은 아님***
<br/>
*(GH): GitHub에서 지원함*

### ***Table (GH)***
> 표를 만든다.
#### **Example**
| name | rank |
| --- | --- |
| Obi-Wan Kenobi | Master |
| Anakin Skywalker | Knight |
```
| name | rank |
| --- | --- |
| Obi-Wan Kenobi | Master |
| Anakin Skywalker | Knight |
```


### ***Fenced Code Block (GH)***
> backtick 세 개 씩을 사이에 두고 사용한다.
>
> 특정 언어를 명시하면 Syntax Highlighting을 적용할 수 있다.

#### **Example**
```Python
    def sith():
        theMostBad = "Darth Sidious"
        wasJediBefore = "Darth Vader"
```

    ```Python
    def sith():
        theMostBad = "Darth Sidious"
        wasJediBefore = "Darth Vader"
    ```


### ***Footnote (GH)***
>각주를 달 수 있다.

#### **Example**
Obi-Wan Kenobi: So, what I told you was true...from a certain point of view. [^1]

[^1]: 스타워즈 에피소드 6

```
Obi-Wan Kenobi: So, what I told you was true...from a certain point of view. [^1]

[^1]: 스타워즈 에피소드 6
```

### ***Heading ID (GH)***
> Heading에 ID를 부여하고 싶을 때 사용한다.
#### **Example**
##### Coruscant {#1}
```
##### Coruscant {#1}
```


### ***Definition List***
> 어떤 용어와 그에 관한 설명을 사전처럼 나타내고 싶을 때 사용할 수 있다.
#### **Example**
Anakin Skywalker
: Padawan of Obi-Wan Kenobi
```
Anakin Skywalker
: Padawan of Obi-Wan Kenobi
```


### ***Strikethrough (GH)***
> 취소선
#### **Example**
~~Chancellor Sheev Palpatine is Darth Sidious.~~
```
~~Chancellor Sheev Palpatine is Darth Sidious.~~
```


### ***Task List (GH)***
> 체크 리스트를 만들 수 있다.
#### **Example**
- [X] Go to Padme's Apartment
- [ ] Meditate with Obi-Wan
- [ ] Have dinner with Ahsoka
```
- [X] Go to Padme's Apartment
- [ ] Meditate with Obi-Wan
- [ ] Have dinner with Ahsoka
```

### ***Emoji (GH)***
> 이모지를 사용할 수 있다.
#### **Example**
Live long and prosper! :vulcan_salute:
```
Live long and prosper! :vulcan salute:
```


### ***Highlight***
> 형광펜으로 강조한 효과를 얻을 수 있다.
#### **Example**
Vulcan? There is ==no== Vulcan in ==Star Wars==!
```
Vulcan? There is ==no== Vulcan in ==Star Wars==!
```


### ***Subscript***
> 아래 첨자
#### **Example**
SF~6~ Gas
```
SF~6~ Gas
```


### ***Superscript***
> 위 첨자
#### **Example**
2^2^ = 4
```
2^2^ = 4
```