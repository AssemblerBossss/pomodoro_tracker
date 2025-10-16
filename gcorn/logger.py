from gunicorn.glogging import Logger
from logging import Formatter
from settings import settings


class GunicornLogger(Logger):
    """Custom Gunicorn logger that uses application logging format.

    Overrides default Gunicorn logging format with application-specific
    format from settings for consistent log output across the application.
    """

    def setup(self, config) -> None:
        super().setup(cfg=config)

        self._set_handler(
            log=self.access_log,
            output=self.cfg.accesslog,
            fmt=Formatter(settings.logging.log_format),
        )
        self._set_handler(
            log=self.error_log,
            output=self.cfg.errorlog,
            fmt=Formatter(settings.logging.log_format),
        )
