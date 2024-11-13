from PyQt5 import QtCore, QtGui, QtWidgets

import pygetwindow as gw  # For bringing the window into focus
import keyboard  # For detecting hotkeys
import pyperclip
from calc import evaluate_expression, operations
import sys
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QLabel, QWidget
from PyQt5.QtGui import QFont, QMouseEvent
from PyQt5 import QtWidgets
import os
from PyQt5.QtCore import Qt
import math
from math import sqrt
import re
from fractions import Fraction

CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
WIDTH = 800
HEIGHT = 205
PADDING = 20
EQUATION_INPUT_HEIGHT = 65
EQUATION_INPUT_PADDING = 65
ANSWER_CONTAINER_HEIGHT = 100

CONTAINER_COLOR = 'rgba(38, 38, 38, 250)'
CONTAINER_BORDER_COLOR = 'rgba(102, 102, 102, 255)'
ANSWER_CONTAINER_COLOR = 'rgba(75, 75, 75, 250)'
ANSWER_CONTAINER_BORDER_COLOR = 'rgba(123, 123, 123, 255)'

CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


def prettify_equation(equation):
    equation = equation.replace('√', 'sqrt')
    equation = equation.replace(',', '')
    equation = equation.replace('**', '^')

    operations = "+-*/^!()"

    # square roots
    def square_root(eq):
        start = eq.find('sqrt')
        if start == -1:
            return eq

        if eq[start + 4] == '(':
            p_count = 1
            for i in range(start + 5, len(eq)):
                if eq[i] == '(':
                    p_count += 1
                if eq[i] == ')':
                    p_count -= 1

                if p_count == 0:
                    eq = eq.replace(
                        f'''sqrt({eq[start + 5: i]})''', f'''√<span style=\"text-decoration: overline;\">{eq[start + 5: i]}</span>''')
                    return eq

                if i == len(eq) - 1:
                    eq = eq.replace(
                        f'''sqrt({eq[start + 5:]})''', f'''√<span style=\"text-decoration: overline;\">{eq[start + 5:]}</span>''')
                    return eq
        else:
            for i in range(start + 4, len(eq)):
                if eq[i] in operations or eq[i] in '<':
                    eq = eq.replace(
                        f'''sqrt{eq[start + 4: i]}{eq[i]}''', f'''√<span style=\"text-decoration: overline;\">{eq[start + 4:i]}{eq[i]}</span>''')
                    return eq

                if i == len(eq) - 1:
                    eq = eq.replace(
                        f'''sqrt{eq[start + 4:]}''', f'''√<span style=\"text-decoration: overline;\">{eq[start + 4:]}</span>''')
                    return eq
        return eq

    # powers
    def power(eq):
        start = eq.find('^')
        if start == -1:
            return eq

        if eq[start + 1] == '(':
            p_count = 1
            for i in range(start + 2, len(eq)):
                if eq[i] == '(':
                    p_count += 1
                if eq[i] == ')':
                    p_count -= 1

                if p_count == 0:
                    eq = eq.replace(
                        f'''^({eq[start + 2: i]})''', f'''<sup>{eq[start + 2: i]}</sup>''')
                    return eq

                if i == len(eq) - 1:
                    eq = eq.replace(
                        f'''^({eq[start + 2:]}''', f'''<sup>{eq[start + 2:]}</sup>''')
                    return eq
        else:
            for i in range(start + 1, len(eq)):
                if eq[i] in operations or eq[i] in '<':
                    eq = eq.replace(
                        f'''^{eq[start + 1: i]}''', f'''<sup>{eq[start + 1: i]}</sup>''')
                    return eq

                if i == len(eq) - 1:
                    eq = eq.replace(
                        f'''^{eq[start + 1:]}''', f'''<sup>{eq[start + 1:]}</sup>''')
                    return eq
        return eq

    # Apply square root and power formatting iteratively
    while 'sqrt' in equation:
        equation = square_root(equation)
        print(equation, 1)

    while '^' in equation:
        equation = power(equation)
        print(equation, 2)

    equation = equation.replace('*', '•')
    equation = equation.replace('</span>', '<!span>')
    equation = equation.replace('</sup>', '<!sup>')
    equation = equation.replace('/', '÷')
    equation = equation.replace('<!span>', '</span>')
    equation = equation.replace('<!sup>', '</sup>')
    equation = equation.replace('deg', '°')
    equation = equation.replace('pi', 'π')

    return equation


def get_resource_path(filename):
    return os.path.join(CURRENT_DIRECTORY, filename)


def get_textbox_dimenssions(textbox):
    width = textbox.fontMetrics().boundingRect(textbox.text()).width()
    height = textbox.fontMetrics().boundingRect(textbox.text()).height()
    return width, height


def format_result(result, decimal_mode, inputted_equation):
    if str(result) == 'Undefined':
        return 'Undefined'

    result = float(str(result))
    formatted = result

    def is_whole(x):
        return not x % 1

    # if π or e are in the equations and in fraction mode, display as fractions of π or e
    # i know shit hits the fan if pi and e are in the same expression
    if not decimal_mode and ('π' in inputted_equation or 'pi' in inputted_equation):
        fraction = str(Fraction(result / math.pi).limit_denominator())
        parts = fraction.split('/')
        if len(parts) == 1:
            return f'''{fraction}π'''
        else:
            if parts[0] == 1:
                return f'''π/{parts[1]}'''
            return f'''{parts[0]}π/{parts[1]}'''

    without_deg = inputted_equation.replace('deg', '')
    without_deg = without_deg.replace('sec', '')
    if not decimal_mode and 'e' in without_deg:
        fraction = str(Fraction(result / math.e).limit_denominator())
        parts = fraction.split('/')
        if len(parts) == 1:
            return f'''{fraction}e'''
        else:
            if parts[0] == 1:
                return f'''e/{parts[1]}'''
            return f'''{parts[0]}e/{parts[1]}'''

    trig_approximations = {
        0: "0",
        0.5: "1/2",
        sqrt(2)/2: "√2/2",
        sqrt(3)/2: "√3/2",
        1: "1",
        sqrt(3): "√3",
        1/sqrt(3): "1/√3",
        -0.5: "-1/2",
        -sqrt(2)/2: "-√2/2",
        -sqrt(3)/2: "-√3/2",
        -1: "-1",
        -sqrt(3): "-√3",
        -1/sqrt(3): "-1/√3",
        # Used for undefined cases like sec(90°), csc(0°), etc.
        16331239353195370: "∞",
        -16331239353195370: "-∞",
    }

    # Additional tangent, cotangent, secant, and cosecant specific values
    tan_cot_approximations = {
        0: "0",
        sqrt(3)/3: "√3/3",
        1: "1",
        sqrt(3): "√3",
        -sqrt(3)/3: "-√3/3",
        -1: "-1",
        -sqrt(3): "-√3",
    }

    sec_csc_approximations = {
        1: "1",
        2: "2",
        sqrt(2): "√2",
        2/sqrt(3): "2/√3",
        -1: "-1",
        -2: "-2",
        -sqrt(2): "-√2",
        -2/sqrt(3): "-2/√3",
    }

    if not decimal_mode:
        for key, value in {**trig_approximations, **tan_cot_approximations, **sec_csc_approximations}.items():
            if abs(result - float(key)) < 1e-10:
                return value

    # if integer return w/o decimal but w/ commas
    integer = is_whole(result)
    if integer:
        formatted = f"{int(result):,}"
    else:
        if not decimal_mode:  # fraction mode, only use fractions for non-whole numbers that are reasonably small not e20 or e-10
            formatted = str(Fraction(result).limit_denominator())
        else:
            formatted = f"{result:,}"

    # large numbers e20, small e10
    if result > 1e20 or (result < 1e-10 and result > 0) or result < -1e20 or (result > -1e-10 and result < 0):
        formatted = f"{result:.10e}"

    return formatted


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.initUI()
        self.result = ''
        self.copied = False
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.dragging_position = None
        self.is_window_visible = True
        self.ans_value = None
        self.decimal_mode = True

    def initUI(self):
        self.setGeometry(200, 200, WIDTH, HEIGHT)
        self.setFixedHeight(EQUATION_INPUT_HEIGHT + 1)

        self.container = QWidget(self)
        self.container.setStyleSheet(
            f'''background-color: {CONTAINER_COLOR};
            border-radius: 25px;
            border: 1px solid {
                CONTAINER_BORDER_COLOR};'''
        )
        self.container.resize(WIDTH, HEIGHT)

        self.logo_button = QtWidgets.QPushButton(self.container)

        self.logo_button.setIcon(QtGui.QIcon(
            get_resource_path('./icons/calc.svg')))
        icon_size = 40
        self.logo_button.setIconSize(QtCore.QSize(icon_size, icon_size))
        self.logo_button.move(int(PADDING / 1.5), int(PADDING / 1.5))
        self.logo_button.resize(icon_size, icon_size)
        self.logo_button.setStyleSheet(
            "border: none; background: transparent; ")
        self.logo_button.mousePressEvent = self.mousePressEvent
        self.logo_button.mouseMoveEvent = self.mouseMoveEvent
        self.logo_button.mouseReleaseEvent = self.mouseReleaseEvent

        # Textbox for input expression
        self.textbox = QLineEdit(self.container)
        self.textbox.move(EQUATION_INPUT_PADDING, 0)
        self.textbox.resize(self.container.width() -
                            EQUATION_INPUT_PADDING, EQUATION_INPUT_HEIGHT)
        self.textbox.setPlaceholderText("Enter an expression...")
        self.textbox.textChanged.connect(self.recalculate)
        self.textbox.setFont(QFont("Roboto", 30))
        self.textbox.setStyleSheet(
            f'''color: white; border: none; font-weight: 200; background: transparent;''')

        # dividing line
        self.line = QtWidgets.QFrame(self.container)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setStyleSheet("color: rgba(255, 255, 255, 150);")
        self.line.setGeometry(0, EQUATION_INPUT_HEIGHT, WIDTH, 1)

        # answer container - will have the repeated equation, the answer, and copy button
        self.answer_container = QWidget(self.container)
        self.answer_container.move(PADDING, EQUATION_INPUT_HEIGHT + PADDING)
        self.answer_container.resize(
            self.container.width() - PADDING * 2, ANSWER_CONTAINER_HEIGHT)
        self.answer_container.setStyleSheet(
            f'''background-color: {
                ANSWER_CONTAINER_COLOR};
            border-radius: 20px;
            border: 3px solid {ANSWER_CONTAINER_BORDER_COLOR};
            '''
        )

        # Label for the equation (in smaller font and lighter color)
        self.equation_label = QtWidgets.QLabel(self.answer_container)
        self.equation_label.setFont(QFont("Roboto", 14))
        self.equation_label.move(0, 1000)
        self.equation_label.setStyleSheet(
            "color: rgba(255, 255, 255, 150); border: none;")  # Lighter color

        self.result_label = QtWidgets.QLabel(self.answer_container)
        self.result_label.move(0, 1000)
        self.result_label.setFont(QFont("Roboto", 20))
        self.result_label.setStyleSheet(
            "color: white; border: none; font-weight: 500;")

        icon_size = 30
        button_size = 50

        # fraction decimal convert button
        self.cvt_btn = QtWidgets.QPushButton(self.answer_container)
        self.cvt_btn.setIcon(QtGui.QIcon(
            get_resource_path('./icons/fraction.svg')))
        self.cvt_btn.setIconSize(QtCore.QSize(icon_size, icon_size))
        self.cvt_btn.setStyleSheet(
            f'''border-radius: 25px; background: {ANSWER_CONTAINER_BORDER_COLOR}''')
        self.cvt_btn.clicked.connect(self.toggle_decimal_mode)
        self.cvt_btn.hide()

        self.cvt_btn.resize(button_size, button_size)
        self.cvt_btn.move(int(self.answer_container.width() - button_size * 3 - PADDING * 3),
                          int((self.answer_container.height() - button_size) / 2))

        # answer button
        self.ans = QtWidgets.QPushButton(self.answer_container)
        self.ans.setIcon(QtGui.QIcon(get_resource_path('./icons/answer.svg')))
        self.ans.setIconSize(QtCore.QSize(icon_size, icon_size))
        self.ans.setStyleSheet(
            f'''border-radius: 25px; background: {ANSWER_CONTAINER_BORDER_COLOR}''')
        self.ans.clicked.connect(self.use_answer)
        self.ans.hide()

        self.ans.resize(button_size, button_size)
        self.ans.move(int(self.answer_container.width() - button_size * 2 - PADDING * 2),
                      int((self.answer_container.height() - button_size) / 2))

        # Copy button
        self.b1 = QtWidgets.QPushButton(self.answer_container)

        self.b1.setIcon(QtGui.QIcon(get_resource_path('./icons/copy.svg')))
        self.b1.setIconSize(QtCore.QSize(icon_size, icon_size))

        self.b1.setStyleSheet(
            f"border-radius: 25px; background: {ANSWER_CONTAINER_BORDER_COLOR}")
        self.b1.clicked.connect(self.copy_result)
        self.b1.hide()

        self.b1.resize(button_size, button_size)
        self.b1.move(int(self.answer_container.width() - button_size - PADDING),
                     int((self.answer_container.height() - button_size) / 2))

    def use_answer(self):
        self.ans_value = self.result
        # self.equation_label.setText('ans')
        self.textbox.setText('ans')
        self.recalculate()

    def toggle_decimal_mode(self):
        self.decimal_mode = not self.decimal_mode

        icon = QtGui.QIcon(get_resource_path('./icons/decimal.svg'))
        if self.decimal_mode:
            icon = QtGui.QIcon(get_resource_path('./icons/fraction.svg'))
        self.cvt_btn.setIcon(icon)

        self.recalculate()

    def recalculate(self):
        text = self.textbox.text()
        if text:
            try:
                self.equation_label.setText(
                    f"{prettify_equation(text)} =")

                variables = None
                if self.ans_value:
                    variables = {'ans': self.ans_value}

                self.result = evaluate_expression(text, variables)
                self.b1.setIcon(QtGui.QIcon(
                    get_resource_path('./icons/copy.svg')))
                self.result_label.setText(
                    format_result(self.result, self.decimal_mode, self.textbox.text()))
                self.setFixedHeight(EQUATION_INPUT_HEIGHT +
                                    ANSWER_CONTAINER_HEIGHT + PADDING * 2 + 1)
                self.b1.show()
                self.ans.show()
                self.cvt_btn.show()
            except Exception:
                self.result = ""
                self.result_label.setText('')
                self.equation_label.setText('')
                self.setFixedHeight(EQUATION_INPUT_HEIGHT + 1)
                self.b1.hide()
                self.ans.hide()
                self.cvt_btn.hide()

        else:
            self.result = ''
            self.result_label.setText("")
            self.setFixedHeight(EQUATION_INPUT_HEIGHT + 1)
            self.b1.hide()

        self.equation_label.move(int(PADDING * 1.1), int(self.answer_container.height(
        ) / 2 - get_textbox_dimenssions(self.equation_label)[1]))

        self.result_label.move(PADDING,  int(
            self.answer_container.height() / 2))

        self.result_label.adjustSize()
        self.equation_label.adjustSize()

    def copy_result(self):
        if self.decimal_mode:
            pyperclip.copy(self.result)
        else:
            pyperclip.copy(self.result_label.text())

        self.b1.setIcon(QtGui.QIcon(
                        get_resource_path('./icons/check.svg')))

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragging_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton and self.dragging_position is not None:
            self.move(event.globalPos() - self.dragging_position)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.dragging_position = None

    def bring_to_front(self):
        """Bring the window to the front and give it focus."""
        self.show()  # Ensure the window is visible
        self.activateWindow()  # Ensure the window is focused
        self.raise_()  # Bring the window to the top of other windows

    def toggle_window_visibility(self):
        """Toggle window visibility with Command+C / Ctrl+C."""
        if self.is_window_visible:
            self.hide()  # Hide the window
        else:
            self.bring_to_front()  # Bring the window to the front and focus
        self.is_window_visible = not self.is_window_visible  # Toggle visibility state


def window():
    try:
        app = QApplication(sys.argv)

        _id = QtGui.QFontDatabase.addApplicationFont(
            './Roboto/Roboto-Regular.ttf')

        win = MyWindow()
        win.show()
        keyboard.add_hotkey(
            'windows+space', lambda: win.toggle_window_visibility())
        sys.exit(app.exec_())
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    window()
