import sys

from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QFontDatabase

from design import Ui_MainWindow


class Calculator(QMainWindow):
    def __init__(self):
        super(Calculator, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        QFontDatabase.addApplicationFont("fonts/Rubik-Regular.ttf")

        self.current_operator = None
        self.stored_value = None
        self.new_number = True

        # Цифры: реальные имена кнопок из design.py -> какую цифру они вставляют
        digit_buttons = {
            self.ui.pushButton_6: '0',
            self.ui.pushButton_4: '1',
            self.ui.pushButton_11: '2',
            self.ui.pushButton_12: '3',
            self.ui.pushButton_3: '4',
            self.ui.pushButton_10: '5',
            self.ui.pushButton_37: '6',
            self.ui.pushButton_2: '7',
            self.ui.pushButton_39: '8',
            self.ui.pushButton_38: '9',
        }
        for btn, digit in digit_buttons.items():
            # d=digit нужен, чтобы каждая кнопка "запомнила" свою цифру,
            # иначе все они будут использовать последнее значение digit из цикла
            btn.clicked.connect(lambda checked=False, d=digit: self.add_digit(d))

        # Операторы
        self.ui.pushButton_35.clicked.connect(lambda: self.set_operator('+'))
        self.ui.pushButton_36.clicked.connect(lambda: self.set_operator('-'))
        self.ui.pushButton_43.clicked.connect(lambda: self.set_operator('*'))
        self.ui.pushButton_42.clicked.connect(lambda: self.set_operator('/'))

        # Остальные кнопки
        self.ui.pushButton_7.clicked.connect(self.add_dot)      # .
        self.ui.pushButton_5.clicked.connect(self.toggle_sign)  # +/-
        self.ui.pushButton_9.clicked.connect(self.clear_all)    # C
        self.ui.pushButton_40.clicked.connect(self.clear_entry) # CE
        self.ui.pushButton_41.clicked.connect(self.backspace)   # backspace icon
        self.ui.pushButton_8.clicked.connect(self.calculate)    # =

    def add_digit(self, digit: str) -> None:
        if self.new_number or self.ui.lineEdit.text() == "0":
            self.ui.lineEdit.setText(digit)
            self.new_number = False
        else:
            self.ui.lineEdit.setText(self.ui.lineEdit.text() + digit)

    def add_dot(self) -> None:
        if self.new_number:
            self.ui.lineEdit.setText("0.")
            self.new_number = False
        elif "." not in self.ui.lineEdit.text():
            self.ui.lineEdit.setText(self.ui.lineEdit.text() + ".")

    def toggle_sign(self) -> None:
        text = self.ui.lineEdit.text()
        if text.startswith("-"):
            self.ui.lineEdit.setText(text[1:])
        elif text != "0":
            self.ui.lineEdit.setText("-" + text)

    def clear_all(self) -> None:
        self.ui.lineEdit.setText("0")
        self.ui.label.setText("")
        self.current_operator = None
        self.stored_value = None
        self.new_number = True

    def clear_entry(self) -> None:
        self.ui.lineEdit.setText("0")
        self.new_number = True

    def backspace(self) -> None:
        text = self.ui.lineEdit.text()
        if len(text) > 1:
            self.ui.lineEdit.setText(text[:-1])
        else:
            self.ui.lineEdit.setText("0")
            self.new_number = True

    def set_operator(self, operator: str) -> None:
        if self.stored_value is not None and not self.new_number:
            self.calculate()
        else:
            self.stored_value = float(self.ui.lineEdit.text())
        self.current_operator = operator
        self.ui.label.setText(f"{self.format_number(self.stored_value)} {operator}")
        self.new_number = True

    def calculate(self) -> None:
        if self.current_operator is None or self.stored_value is None:
            return
        current_value = float(self.ui.lineEdit.text())
        try:
            if self.current_operator == '+':
                result = self.stored_value + current_value
            elif self.current_operator == '-':
                result = self.stored_value - current_value
            elif self.current_operator == '*':
                result = self.stored_value * current_value
            elif self.current_operator == '/':
                result = self.stored_value / current_value
        except ZeroDivisionError:
            self.ui.lineEdit.setText("Error")
            self.current_operator = None
            self.stored_value = None
            self.new_number = True
            return

        self.ui.lineEdit.setText(self.format_number(result))
        self.ui.label.setText("")
        self.stored_value = result
        self.current_operator = None
        self.new_number = True

    @staticmethod
    def format_number(value: float) -> str:
        if value == int(value):
            return str(int(value))
        return str(value)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Calculator()
    window.show()  # без этой строки окно никогда не появится на экране

    sys.exit(app.exec())