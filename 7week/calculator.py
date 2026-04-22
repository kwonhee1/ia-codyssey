import sys
from abc import ABC, abstractmethod

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QPushButton, QWidget


class Calculator:
    def __init__(self):
        self.value = '0'

    def input_value(self, value):
        self.value += value
        return self.value

    def input_operator(self, operator):
        self.value += operator
        return self.value

    def input_function(self, function_name):
        self.value += function_name
        return self.value


class UIEvent:
    pass


class ValueClickEvent(UIEvent):
    def __init__(self, label):
        self.label = label


class OperatorClickEvent(UIEvent):
    def __init__(self, label):
        self.label = label


class FunctionClickEvent(UIEvent):
    def __init__(self, label):
        self.label = label


class CalculatorView(QWidget):
    def __init__(self, rows, cols, click_action):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.display_widget = QLabel('0')
        self.buttons = []
        self.click_action = click_action
        self.grid_layout = QGridLayout()

        self.setLayout(self.grid_layout)
        self.setWindowTitle('Calculator')
        self.setFixedSize(360, 560)
        self.set_style()
        self.set_display_widget()

    def set_style(self):
        self.setStyleSheet(
            '''
            QWidget {
                background-color: #000000;
                color: #ffffff;
                font-family: Arial;
            }

            QLabel {
                color: #ffffff;
                font-size: 48px;
                padding: 20px;
            }

            QPushButton {
                background-color: #333333;
                border: none;
                border-radius: 34px;
                color: #ffffff;
                font-size: 24px;
                min-height: 68px;
            }
            '''
        )

    def set_display_widget(self):
        self.display_widget.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.grid_layout.addWidget(self.display_widget, 0, 0, 1, self.cols)

    def add_button(self, start, end, text, value, event_type):
        button = QPushButton(text)
        button.clicked.connect(
            lambda checked=False: self.emit_button_event(event_type, value)
        )

        start_row, start_col = start
        end_row, end_col = end
        row_span = end_row - start_row + 1
        col_span = end_col - start_col + 1

        self.buttons.append(button)
        self.grid_layout.addWidget(
            button,
            start_row,
            start_col,
            row_span,
            col_span,
        )

    def emit_button_event(self, event_type, value):
        event = event_type(value)
        self.click_action(event)

    def display(self, value):
        self.display_widget.setText(value)

    @staticmethod
    def iphone_view(click_action):
        view = CalculatorView(6, 4, click_action)
        button_infos = [
            ((1, 0), (1, 0), 'AC', 'AC', FunctionClickEvent),
            ((1, 1), (1, 1), '+/-', '+/-', FunctionClickEvent),
            ((1, 2), (1, 2), '%', '%', FunctionClickEvent),
            ((1, 3), (1, 3), '/', '/', OperatorClickEvent),
            ((2, 0), (2, 0), '7', '7', ValueClickEvent),
            ((2, 1), (2, 1), '8', '8', ValueClickEvent),
            ((2, 2), (2, 2), '9', '9', ValueClickEvent),
            ((2, 3), (2, 3), '*', '*', OperatorClickEvent),
            ((3, 0), (3, 0), '4', '4', ValueClickEvent),
            ((3, 1), (3, 1), '5', '5', ValueClickEvent),
            ((3, 2), (3, 2), '6', '6', ValueClickEvent),
            ((3, 3), (3, 3), '-', '-', OperatorClickEvent),
            ((4, 0), (4, 0), '1', '1', ValueClickEvent),
            ((4, 1), (4, 1), '2', '2', ValueClickEvent),
            ((4, 2), (4, 2), '3', '3', ValueClickEvent),
            ((4, 3), (4, 3), '+', '+', OperatorClickEvent),
            ((5, 0), (5, 1), '0', '0', ValueClickEvent),
            ((5, 2), (5, 2), '.', '.', ValueClickEvent),
            ((5, 3), (5, 3), '=', '=', FunctionClickEvent),
        ]

        for start, end, text, value, event_type in button_infos:
            view.add_button(start, end, text, value, event_type)

        return view


class EventHandlerInterface(ABC):
    @abstractmethod
    def handle(self, event):
        pass


class ClickEventHandlerInterface(ABC):
    @abstractmethod
    def handle(self, event):
        pass


class EventHandler(EventHandlerInterface):
    def __init__(self):
        self.handlers = {}

    def register(self, event_type, handler):
        self.handlers[event_type] = handler

    def handle(self, event):
        handler = self.handlers.get(type(event))

        if handler is None:
            return

        handler.handle(event)


class CalculatorController(ClickEventHandlerInterface):
    def __init__(self):
        self.calculator = Calculator()
        self.event_handler = EventHandler()
        self.view = CalculatorView.iphone_view(self.event_handler.handle)
        self.setup_handlers()
        self.view.show()

    def setup_handlers(self):
        self.event_handler.register(ValueClickEvent, self)
        self.event_handler.register(OperatorClickEvent, self)
        self.event_handler.register(FunctionClickEvent, self)

    def handle(self, event):
        value = None

        if isinstance(event, ValueClickEvent):
            value = self.calculator.input_value(event.label)
        elif isinstance(event, OperatorClickEvent):
            value = self.calculator.input_operator(event.label)
        elif isinstance(event, FunctionClickEvent):
            value = self.calculator.input_function(event.label)
        else:
            return

        self.view.display(value)


def main():
    app = QApplication(sys.argv)
    CalculatorController()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
