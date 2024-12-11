__all__ = (
    "main_app",
    "main",
)

from application.core.config import settings
from application.core.gunicorn import Application, get_app_options
from main import main_app


def main():
    Application(
        application=main_app,
        options=get_app_options(
            host=settings.gunicorn.host,
            port=settings.gunicorn.port,
            timeout=settings.gunicorn.timeout,
            workers=settings.gunicorn.workers,
            log_level=settings.logging.log_level,
        ),
    ).run()


if __name__ == "__main__":
    main()
