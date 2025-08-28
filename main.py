import os

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.uix.image import Image

from config import *
from database import *
from header import Header, TableHeader


# Цвет фона приложения - устанавливается для всего окна
Window.clearcolor = DARK_CHOCOLATE
# Размер экрана
Window.size = (560, 780)


class ArticleButton(ButtonBehavior, BoxLayout):
    """
    Кастомный виджет статьи, который заменяет стандартную кнопку
    Состоит из двух частей: даты и названия статьи
    """
    def __init__(self, title, date, **kwargs):
        super().__init__(**kwargs)

        # Настройки размера виджета
        self.size_hint_y = None # Отключаем автоматическое определение высоты
        self.height = dp(60)
        # Настройки фона (прозрачный)
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        self.orientation = 'horizontal'
        # Внутренние отступы: [левый, верхний, правый, нижний]
        self.padding = [dp(30), 0, dp(30), 0]

        # Левая часть - дата
        self.date_label = Label(
            text=date,
            size_hint=(0.25, 1), # Занимает 25% ширины и всю высоту
            color=BRIGHT_ORANGE,
            halign='left',
            valign='middle',
            opacity=0.9,
            text_size=(None, None),
            padding=[0, 0, 0, 0]
        )
        # Привязка изменения размера к обновлению text_size
        self.date_label.bind(size=self.date_label.setter('text_size'))
        
        # Правая часть - название статьи
        self.title_label = Label(
            text=title,
            size_hint=(0.75, 1), # Занимает 75% ширины и всю высоту
            color=BRIGHT_ORANGE,
            halign='center',
            valign='middle',
            text_size=(None, None),
        )
        # Привязка изменения размера к обновлению text_size
        self.title_label.bind(size=self.title_label.setter('text_size'))

        # Добавляем оба label в layout
        self.add_widget(self.date_label)
        self.add_widget(self.title_label)


class ArticlesList(BoxLayout):
    """
    Контейнер для отображения статей на странице
    """
    def __init__(self, category_id=1, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [dp(3), 0, dp(3), 0]
        self.spacing = dp(1)
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))

        self.category_id = category_id
        self.load_articles()

    def load_articles(self, category_id=None):
        """Загрузка статей только из категории с ID 1"""
        if category_id is not None:
            self.category_id = category_id
        # Получаем статьи из базы данных
        app = App.get_running_app()

        article_list = app.db.get_articles_by_category_id(
            category_id=self.category_id,
            sort_by_start_year_desc=True  # Сортировка от большего к меньшему
        )
        
        # Очищаем предыдущие статьи
        self.clear_widgets()

        if not article_list:
            article_list = {
                "Хараппская цивилизация": "3300-1300 до н.э.",
                "Древняя Месопотамия: Шумеры и Аккада": "3500-2000 до н.э.",
                "Империя Хань: Золотой век Китая": "206 до н.э. - 220 н.э.",
                "Период Сражающихся царств в Китае": "475-221 до н.э.",
                "Династия Чосон в Корее: 500 лет правления": "1392-1897",
                "Эпоха самураев: Япония периода Сэнгоку": "1467-1603",
                "Цивилизация долины Инда: Мохенджо-Даро": "2600-1900 до н.э.",
                "Кхмерская империя: Ангкор-Ват и наследие": "802-1431",
            }

        # Создание виджетов для каждой статьи
        for title, date in article_list.items():
            # Создаем кнопку для каждой статьи
            article_widget = ArticleButton(title=title, date=date)
            # Добавляем обработчик нажатия
            article_widget.bind(on_press=lambda instance, t=title, d=date: 
                               App.get_running_app().show_article(t, d))
            # Пока просто добавляем кнопку в макет
            self.add_widget(article_widget)

    def change_category(self, category_id):
        """Метод для смены категории"""
        self.load_articles(category_id)


class ArticleWindow(ScrollView):
    """
    Окно для отображения конкретной статьи
    """
    def __init__(self, article_title, article_date, article_content, 
                 image_path=None, **kwargs):
        super().__init__(**kwargs)
        self.bar_width = dp(10)
        self.bar_color = [1, 1, 1, 0.3]
        self.scroll_type = ['bars', 'content']
        self.do_scroll_x = False

        container = BoxLayout(
            orientation='vertical',
            padding=dp(10),
            spacing=dp(5),
            size_hint_y=None
        )
        container.bind(minimum_height=container.setter('height'))

        # Горизонтальная панель для кнопки назад и заголовка
        header_panel = BoxLayout(
            size_hint_y=None,
            height=dp(40),
            orientation='horizontal',
            spacing=dp(10)
        )

       # Кнопка назад
        back_button = Button(
            text="<-",
            size_hint_x=None,
            width=dp(50),
            size_hint_y=1,
            background_color=YELLOW_ORANGE,
            color=YELLOW_ORANGE,
            font_size=dp(20)
        )
        back_button.bind(on_press=self.go_back)
        
        # Заголовок статьи
        title_label = Label(
            text=article_title,
            color=BRIGHT_ORANGE,
            font_size=dp(19),
            bold=True,
            halign='center',
            valign='middle'
        )
        title_label.bind(size=title_label.setter('text_size'))
        
        # Добавляем кнопку и заголовок в горизонтальную панель
        header_panel.add_widget(back_button)
        header_panel.add_widget(title_label)
        
        # Дата статьи
        date_label = Label(
            text=article_date,
            color=BRIGHT_ORANGE,
            font_size=dp(15),
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        date_label.bind(size=date_label.setter('text_size'))

        # Изображение (если есть)
        image_widget = None
        if image_path and os.path.exists(image_path):
            try:
                image_widget = Image(
                    source=image_path,
                    size_hint_y=None,
                    height=dp(300),
                    size_hint_x=1,
                    fit_mode="contain",
                    mipmap=True         # Улучшаем качество
                )
            except Exception as e:
                print(f"Ошибка загрузки изображения: {e}")

        def update_content_height(instance, value):
            instance.height = max(value[1], dp(50))

        content_label = Label(
            text=article_content,
            color=BRIGHT_ORANGE,
            font_size=dp(16),
            halign='left',
            valign='top',
            text_size=(Window.width - dp(40), None),
            size_hint_y=None,
            padding = [0, dp(10), 0, dp(20)]
        )
        content_label.text_size = (Window.width - dp(40), None)
        content_label.bind(
            size=lambda instance, size: setattr(instance, 'text_size', (size[0] - dp(40), None)),
            texture_size=update_content_height
        )
        
        container.add_widget(header_panel)
        if image_widget:
            container.add_widget(image_widget)
        container.add_widget(date_label)
        container.add_widget(content_label)
        container.height = container.minimum_height

        self.add_widget(container) 

    def go_back(self, instance):
        """Функция обработчик кнопки назад"""
        app = App.get_running_app()
        app.screen_manager.current = 'main'


class MainLayout(BoxLayout):
    """
    Отображение элементов на главная странице
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Главный макет будет вертикальным
        self.orientation = 'vertical'
        self.spacing = 0  # Убираем промежутки между виджетами
        
        # Добавляем хедер
        self.header = Header()
        self.add_widget(self.header)

        # Добавляем заголовок таблицы
        table_header = TableHeader()
        self.add_widget(table_header)

        # Добавляем нижнюю линию-разделитель
        bottom_line = BoxLayout(
            size_hint_y=None,
            height=dp(1),
            orientation='horizontal',
            padding=[0, 0, 0, 0]
        )
        
        with bottom_line.canvas.before:
            Color(*TACO_BROWN)
            bottom_line.rect = Rectangle(
                pos=bottom_line.pos,
                size=bottom_line.size
            )
        bottom_line.bind(pos=lambda obj, pos: setattr(bottom_line.rect, 'pos', pos))
        bottom_line.bind(size=lambda obj, size: setattr(bottom_line.rect, 'size', size))
        
        self.add_widget(bottom_line)

        self.scroll_view = ScrollView(size_hint=(1, 0.8))
        # Сохраняем ссылку на список статей для будущего обновления
        self.article_list = ArticlesList(category_id=1)
        self.scroll_view.add_widget(self.article_list)

        # Добавляем прокрутку
        self.add_widget(self.scroll_view)

    def change_category(self, category_id):
        """Публичный метод для смены категории"""
        self.article_list.change_category(category_id)


# Главный экран
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MainLayout())


# Экран отдельных статей
class ArticleScreen(Screen):
    def __init__(self, title, date, content, image_path, **kwargs):
        super().__init__(**kwargs)
        article_window = ArticleWindow(title, date, content, image_path)
        article_window.size_hint = (1, 1)
        self.add_widget(article_window)


class HistoryAsiaApp(App):
    """
    Главный класс приложения
    Наследуется от App и реализует метод build()
    """
    def build(self):
        """
        Метод, который вызывается при запуске приложения
        Возвращает корневой виджет
        """
        # Просто подключаемся к существующей базе
        self.db = DatabaseManager()

        # Проверим подключение к БД
        try:
            test_conn = sqlite3.connect(self.db.get_db_path())
            test_conn.close()
            print("База данных успешно подключена")
        except:
            print("Ошибка подключения к базе данных")

        self.screen_manager = ScreenManager()
        # Главный экран
        main_screen = MainScreen(name='main')
        self.screen_manager.add_widget(main_screen)

        return self.screen_manager

    def show_article(self, title, date):
        # Достаем из БД статью
        article_data = self.db.get_article_content(title)
        # Создаем или обновляем экран статьи
        if article_data:
            article_screen = ArticleScreen(
                title=article_data['title'],
                date=article_data['date'],
                content=article_data['content'],
                image_path=article_data['image_path'],
                name='article'
            )
        else:
            article_screen = ArticleScreen(
                title=title,
                date=date,
                content="Содержание не найдено",
                image_path=None,
                name='article'
            )
        
        # Удаляем старый экран статьи если есть
        if self.screen_manager.has_screen('article'):
            self.screen_manager.remove_widget(self.screen_manager.get_screen('article'))

        self.screen_manager.add_widget(article_screen)
        self.screen_manager.current = 'article'


if __name__ == '__main__':
    HistoryAsiaApp().run()
