from gcorn import GunicornApplication, get_app_options
from main import app
from settings import settings

def main():
    GunicornApplication(
        application=app,
        options=get_app_options(
            host=settings.gunicorn.APP_HOST,
            port=settings.gunicorn.APP_PORT,
            workers=settings.gunicorn.WORKERS,
            timeout=settings.gunicorn.TIMEOUT,
            loglevel=settings.logging.log_level,
        )
    ).run()


if __name__ == "__main__":
    main()