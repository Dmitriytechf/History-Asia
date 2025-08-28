import sqlite3


class DatabaseManager:
    """
    Класс для работы с БД
    """
    def __init__(self, db_name='asia.db'):
        self.db_name = db_name
        # Не создаем таблицы автоматически.
        # Только проверяем доступность

    def get_db_path(self):
        """Получаем путь к БД"""
        # Пока база данных в той же папке, что и приложение
        return self.db_name

    def get_all_articles(self):
        """Получение всех статей, но только для чтения"""
        try:
            conn = sqlite3.connect(self.get_db_path())
            cursor = conn.cursor()

            cursor.execute('''
                SELECT a.title, a.date_text 
                FROM articles a
                ORDER BY a.title
            ''')

            articles = cursor.fetchall()
            conn.close()
            # Преобразуем в словарь для совместимости
            return {title: date_text for title, date_text in articles}

        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")

    def get_article_content(self, title):
        """Получение содержимого статьи"""
        try:
            conn =sqlite3.connect(self.get_db_path())
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT title, date_text, content, image_path 
            FROM articles WHERE title = ?
            ''', (title,))

            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'title': result[0],
                    'date': result[1], 
                    'content': result[2],
                    'image_path': result[3]
                }
            return None

        except sqlite3.Error as e:
            return "Ошибка загрузки содержимого!"

    def get_articles_by_category(self, category_name):
        """Получение статей по категории"""
        try:
            conn = sqlite3.connect(self.get_db_path())
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT a.title, a.date_text 
                FROM articles a
                JOIN categories c ON a.category_id = c.id
                WHERE c.name = ?
                ORDER BY a.title
            ''', (category_name,)
            )
            
            articles =cursor.fetchall()
            conn.close()
            
            return dict(articles) if articles else {}

        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")

    def get_articles_by_category_id(self, category_id, sort_by_start_year_desc=True):
        """Получение статей по ID категории с сортировкой по start_year"""
        try:
            conn = sqlite3.connect(self.get_db_path())
            cursor = conn.cursor()
            
            # Сортировка по start_year от большего к меньшему
            order_clause = "ORDER BY a.start_year DESC" if sort_by_start_year_desc else "ORDER BY a.start_year ASC"

            cursor.execute(f'''
                SELECT a.title, a.date_text 
                FROM articles a
                WHERE a.category_id = ?
                {order_clause}
            ''', (category_id,))
            
            articles = cursor.fetchall()
            conn.close()
            
            return dict(articles) if articles else {}

        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")
            return {}

    def get_categories(self):
        """Получение списка категорий"""
        try:
            conn = sqlite3.connect(self.get_db_path())
            cursor = conn.cursor()
            
            cursor.execute('SELECT id, name FROM categories ORDER BY name')
            categories = cursor.fetchall()
            conn.close()
            
            return categories
            
        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")
