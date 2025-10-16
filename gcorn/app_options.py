from gcorn.logger import GunicornLogger


def get_app_options(
    host: str,
    port: str,
    workers: int,
    timeout: int,
    loglevel: str,
) -> dict:

    return {
        "bind": f"{host}:{port}",
        "worker_class": "uvicorn.workers.UvicornWorker",
        "workers": workers,
        "loglevel": loglevel,
        "logger_class": GunicornLogger,
        "timeout": timeout,
        "access_log": "-",
        "error_log": "-",
    }
