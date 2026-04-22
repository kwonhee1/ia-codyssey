# 요구 사항 분석하기

PyQT 라이브러리를 사용하여 iphone 모양의 계산기를 UI를 만든다
각각의 버튼을 누를 때 마다 event를 처리하여 계산한다
계산기의 기능은 구현하지 않는다

# 제한 사항
- python 버전은 3.x를 사용한다
- 별도의 라이브러리나 패키지를 사용하지 않는다 (PyQT 제외)
- Python conding style guide를 확인하고 준수한다
- 문자열은 ' 으로 사용하며 부득이한 경우에는 " 을 사용할 수 있다
- foo = (0,) 와 같이 대입문의  = 앞 뒤로는 공백을 준다
- 경고 메시지 없이 모든 코드는 실행 되어야 한다
- 전채 코드를 calculator.py  에 작성한다

# class 정리
## 1. Calculator
### 책임
- 계산기 상태를 관리하고, 버튼 입력에 따라 상태를 변경한다.
- 처리 결과로 현재 display 문자열을 반환한다.

### 내부 변수
- `display_text: str`  
  현재 화면에 표시할 문자열
- `current_input: str`  
  현재 입력 중인 값
- `pending_operator: str | None`  
  대기 중인 연산자
- `stored_value: str | None`  
  이전에 저장된 값

### 필요한 method
- `input_value(value: str) -> str`  
- `input_operator(operator: str) -> str`  
- `input_function(function_name: str) -> str`  
- `get_display() -> str`

---

## 2. CalculatorView
### 책임
- 계산기 UI를 구성하고 버튼 클릭을 UI 이벤트로 발생시킨다.
- controller가 전달한 display 문자열을 화면에 출력한다.

### 내부 변수
- `rows: int`  
- `cols: int`  
- `display_widget`  
- `buttons: list`  
- `event_handler: EventHandlerInterface | None`

### 필요한 method
- `__init__(rows: int, cols: int)`  
- `add_button(start: tuple[int, int], end: tuple[int, int], text: str)`  
- `set_event_handler(handler: EventHandlerInterface)`  
- `emit_button_event(label: str)`  
- `display(text: str)`  
- `iphone_view() -> CalculatorView`

---

## 3. UIEvent
### 책임
- UI에서 발생한 이벤트의 공통 부모 타입이다.
- view와 controller 사이 이벤트 전달 규약을 제공한다.

### 내부 변수
- 없음

### 필요한 method
- 없음

---

## 4. ButtonClickEvent
### 책임
- 눌린 버튼의 label 정보를 담아 전달한다.
- UI 입력을 controller가 해석할 수 있도록 전달한다.

### 상속
- `UIEvent` 상속

### 내부 변수
- `label: str`

### 필요한 method
- `__init__(label: str)`

---

## 5. EventHandlerInterface
### 책임
- 이벤트 처리 handler의 공통 인터페이스 정의
- view가 구체 구현이 아닌 추상 타입에 의존하도록 한다

### 내부 변수
- 없음

### 필요한 method
- `handle(event: UIEvent)`

---

## 6. ButtonClickEventHandlerInterface
### 책임
- ButtonClickEvent 처리 handler 인터페이스 정의
- EventHandler가 구체 controller 대신 추상 handler에 의존하도록 한다

### 내부 변수
- 없음

### 필요한 method
- `handle(event: ButtonClickEvent)`

---

## 7. EventHandler
### 책임
- 이벤트 타입별 handler 등록 및 호출
- view에서 발생한 이벤트를 적절한 handler로 전달

### 구현 관계
- `EventHandlerInterface` 구현

### 내부 변수
- `handlers: dict[type[UIEvent], ButtonClickEventHandlerInterface]`

### 필요한 method
- `register(event_type: type[UIEvent], handler: ButtonClickEventHandlerInterface)`  
- `handle(event: UIEvent)`

---

## 8. CalculatorController
### 책임
- Calculator, View, EventHandler 생성 및 연결
- 버튼 이벤트 해석 후 Calculator 호출 및 결과를 View에 반영

### 구현 관계
- `ButtonClickEventHandlerInterface` 구현

### 내부 변수
- `calculator: Calculator`  
- `view: CalculatorView`  
- `event_handler: EventHandler`

### 필요한 method
- `__init__()`  
- `setup_handlers()`  
- `start()`  
- `handle(event: ButtonClickEvent)`