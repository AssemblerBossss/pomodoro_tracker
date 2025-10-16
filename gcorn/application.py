from fastapi import FastAPI
from gunicorn.app.base import BaseApplication


class GunicornApplication(BaseApplication):
    """
    Пользовательский класс приложения Gunicorn для интеграции с FastAPI.
    Этот класс позволяет запускать приложение FastAPI с помощью Gunicorn,
    предоставляя мост между ними. Он обрабатывает опции конфигурации
    и загружает приложение FastAPI для обслуживания Gunicorn.
    """

    def __init__(self, application: FastAPI, options: dict | None = None):
        """
        Initialize the Gunicorn application with a FastAPI app and configuration options.
        Args:
            application (FastAPI): The FastAPI application instance to be served.
            options (dict | None): A dictionary of Gunicorn configuration options.
                Only valid options will be applied.
        """

        self.options = options
        self.application = application
        super().__init__()

    def load(self):
        """
        Загружает и возвращает приложение FastAPI.
        Return:
            FastAPI: Экземпляр приложения FastAPI.
        """
        return self.application

    @property
    def config_options(self) -> dict:
        """
        Фильтрует и возвращает допустимые опции конфигурации Gunicorn из предоставленных опций.
        Это свойство обрабатывает словарь опций, чтобы включить только те ключи,
        которые являются допустимыми настройками Gunicorn и имеют значения, не равные None.
        Возвращает:
            dict: Словарь отфильтрованных опций конфигурации.
        """
        return {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }

    def load_config(self):
        """
        Загружает отфильтрованные опции конфигурации в настройки Gunicorn.
        Этот метод устанавливает конфигурацию Gunicorn на основе предоставленных
        допустимых опций. Ключи преобразуются в нижний регистр, если нужно.
        """
        for key, value in self.config_options.items():
            self.cfg.set(key.lower(), value)
