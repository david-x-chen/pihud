# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from widgets.util import map_value, in_range

class Text(QWidget):
    def __init__(self, parent, config):
        super(Text, self).__init__(parent)

        self.config = config
        self.value = config["min"]

        self.font      = QFont()
        self.note_font = QFont()
        self.color     = QColor(config["color"])
        self.red_color = QColor(config["redline_color"])
        self.no_color  = QColor()
        self.no_color.setAlpha(0)

        self.brush     = QBrush(self.color)
        self.red_brush = QBrush(self.red_color)

        self.pen       = QPen(self.color)
        self.red_pen   = QPen(self.red_color)
        self.no_pen    = QPen(self.no_color)

        self.font_db   = QFontDatabase()
        self.font_id   = self.font_db.addApplicationFont(config["custom_font"])
        self.font_families = self.font_db.applicationFontFamilies(self.font_id)
        self.led_font  = QFont(self.font_families[0]) #"Digital Dismay")
        self.led_font.setPixelSize(self.config["font_size"])

        self.font.setPixelSize(self.config["font_size"])
        self.note_font.setPixelSize(self.config["note_font_size"])
        self.pen.setWidth(3)
        self.red_pen.setWidth(3)

        self.red_value = config["redline"]
        if self.red_value is None:
            self.red_value = config["max"]


    def sizeHint(self):
        return QSize(300, 75)


    def render(self, response):
        if hasattr(response.value, 'magnitude'):
            self.value = response.value.magnitude
        else:
            self.value = response.value
        self.update()


    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)

        f_h = self.config["font_size"]
        self.t_height = f_h + 8

        painter.setFont(self.note_font)
        painter.setPen(self.pen)
        painter.setRenderHint(QPainter.Antialiasing)

        h = 0
        w = 8
        t_len = len(self.config["title"])
        if t_len > 0:
            h += self.t_height
            w += f_h * t_len
            r = QRect(0, 0, self.width(), self.t_height)
            painter.drawText(r, Qt.AlignVCenter, self.config["title"])

        fontBold = self.note_font
        fontBold.setBold(True)
        painter.setFont(fontBold)

        x = w - f_h
        if w <= 8:
            x = 0
        if hasattr(self.value, 'MIL'):
            faultyText = ""
            if self.value.MIL:
                painter.setPen(QPen(self.color))
                painter.setBackgroundMode(1)
                painter.setBackground(self.red_brush)
                faultyText = "故障"
            else:
                painter.setPen(QPen(self.color))
            r = QRect(x, 0, self.width(), self.t_height)
            painter.drawText(r, Qt.AlignVCenter, faultyText)
        else:
            painter.setPen(QPen(QColor(255, 255, 5)))
            #textValue = str(int(round(self.value))) + " " + self.config["unit"]
            textValue = str(round(self.value, 2)) + " " + self.config["unit"]

            if self.config["sensor"] == 'RUN_TIME':
                minutes, seconds = divmod(self.value, 60)
                hours, minutes = divmod(minutes, 60)
                periods = [("", hours), ("", minutes), ("", seconds)]
                textValue = ':'.join('{}{}'.format(value, name)
                                      for name, value in periods
                                      if value)

            if self.config["led_style"] and self.config["sensor"] != "MAF":
                #painter.setBackground(self.color)
                #painter.setBackgroundMode(1)
                painter.setFont(self.led_font)
            else:
                painter.setFont(fontBold)

            textWidth = 0
            if len(textValue):
                textWidth = len(textValue) * self.t_height
            r = QRect(x + 8, 0, textWidth, self.t_height)
            painter.drawText(r, Qt.AlignVCenter, textValue)

        #painter.drawText(r, Qt.AlignVCenter, str(int(round(self.value))) + " " + self.config["unit"])

        fontBold.setBold(False)

        painter.end()
