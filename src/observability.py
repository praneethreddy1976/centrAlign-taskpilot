import json
import logging
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage()
        }

        event = getattr(record, "event", None)
        if event is not None:
            log_entry["event"] = event

        context = getattr(record, "context", None)
        if isinstance(context, dict):
            log_entry.update(context)

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry, default=str)


def configure_logging(level=logging.INFO):
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    for existing_handler in root_logger.handlers[:]:
        root_logger.removeHandler(existing_handler)
        existing_handler.close()

    root_logger.addHandler(handler)


def get_logger(name):
    return logging.getLogger(name)


def log_event(logger, level, event, **context):
    logger.log(
        level,
        event,
        extra={
            "event": event,
            "context": context
        }
    )
