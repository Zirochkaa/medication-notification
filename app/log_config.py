log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",

        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "handlers.callbacks": {"handlers": ["default"], "level": "INFO"},
        "handlers.commands": {"handlers": ["default"], "level": "INFO"},
        "scheduler.helpers": {"handlers": ["default"], "level": "INFO"},
        "scheduler.tasks": {"handlers": ["default"], "level": "INFO"},
        "exception_handlers": {"handlers": ["default"], "level": "INFO"},
        "logs_notifications": {"handlers": ["default"], "level": "INFO"},
        "run": {"handlers": ["default"], "level": "INFO"},
    },
}
