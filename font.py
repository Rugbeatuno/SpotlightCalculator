import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLabel


class CalculatorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simple Calculator")
        self.setGeometry(100, 100, 300, 400)  # (x, y, width, height)

        layout = QVBoxLayout()

        # Create a label to display the calculator input and result
        self.display_label = QLabel("0", self)
        layout.addWidget(self.display_label)

        # Create a layout for the buttons
        button_layout = QGridLayout()

        # Create buttons for numbers 0-9
        for i in range(10):
            button = QPushButton(str(i), self)
            button.clicked.connect(
                lambda checked, num=i: self.on_digit_clicked(num))
            if i == 0:
                button_layout.addWidget(button, 3, 1)
            else:
                button_layout.addWidget(button, (9 - i) // 3, (i - 1) % 3)

        # Create buttons for operators (+, -, *, /)
        operators = ["+", "-", "*", "/"]
        for operator in operators:
            button = QPushButton(operator, self)
            button.clicked.connect(
                lambda checked, op=operator: self.on_operator_clicked(op))
            button_layout.addWidget(button, operators.index(operator), 3)

        # Create a button for equals (=)
        equals_button = QPushButton("=", self)
        equals_button.clicked.connect(self.calculate_result)
        button_layout.addWidget(equals_button, 3, 2)

        # Create a clear button (C)
        clear_button = QPushButton("C", self)
        clear_button.clicked.connect(self.clear_input)
        button_layout.addWidget(clear_button, 3, 0)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.current_input = ""

    def on_digit_clicked(self, digit):
        self.current_input += str(digit)
        self.display_label.setText(self.current_input)

    def on_operator_clicked(self, operator):
        if self.current_input and self.current_input[-1] not in ["+", "-", "*", "/"]:
            self.current_input += operator
            self.display_label.setText(self.current_input)

    def calculate_result(self):
        try:
            result = eval(self.current_input)
            self.display_label.setText(str(result))
            self.current_input = str(result)
        except Exception:
            self.display_label.setText("Error")
            self.current_input = ""

    def clear_input(self):
        self.current_input = ""
        self.display_label.setText("0")


def main():
    app = QApplication(sys.argv)
    window = CalculatorApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
