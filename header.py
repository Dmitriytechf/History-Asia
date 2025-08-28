from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from config import *


class Header(BoxLayout):
    """
    Шапка приложения - заголовок и навигационная панель
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(60)
        self.orientation = 'horizontal'

        with self.canvas.before:
            Color(*TACO_BROWN)
            self.rect = Rectangle(
                pos=self.pos,
                size=self.size
            )

        # Привязываем обновление позиции и размера прямоугольника фона
        self.bind(pos=self._update_rect, size=self._update_rect)

        # Создаем заголовок по центру
        self.title_label = Label(
            text="История Азии",
            color=YELLOW_ORANGE,
            font_size=dp(20),
            bold=True,
            halign='center',
            valign='middle'
        )
        self.title_label.bind(size=self.title_label.setter('text_size'))

        self.add_widget(self.title_label)

    def _update_rect(self, instance, value):
        """Обновляем позицию и размер прямоугольника фона"""
        self.rect.pos = self.pos
        self.rect.size = self.size


class TableHeader(BoxLayout):
    """
    Заголовок таблицы с датой и названием статьи
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(40)
        self.orientation = 'horizontal'
        self.padding = [dp(30), dp(10), dp(30), dp(10)]
        
        # Левая часть - "Дата"
        date_header = Label(
            text="Дата",
            size_hint=(0.25, 1),
            color=BRIGHT_ORANGE,
            halign='left',
            valign='middle',
            bold=True,
            font_size=dp(16)
        )
        date_header.bind(size=date_header.setter('text_size'))
        
        # Правая часть - "Название статьи"
        title_header = Label(
            text="Название статьи",
            size_hint=(0.75, 1),
            color=BRIGHT_ORANGE,
            halign='center',
            valign='middle',
            bold=True,
            font_size=dp(16)
        )
        title_header.bind(size=title_header.setter('text_size'))

        self.add_widget(date_header)
        self.add_widget(title_header)
