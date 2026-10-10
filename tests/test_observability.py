import json
import logging

from observability import JsonFormatter, log_event


def test_json_formatter_outputs_structured_fields():
    record = logging.LogRecord(
        name="taskpilot.test",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="task_started",
        args=(),
        exc_info=None
    )

    record.event = "task_started"
    record.context = {
        "task_id": "test-001",
        "invoice_number": "INV-1042"
    }

    output = JsonFormatter().format(record)
    data = json.loads(output)

    assert data["level"] == "INFO"
    assert data["logger"] == "taskpilot.test"
    assert data["message"] == "task_started"
    assert data["event"] == "task_started"
    assert data["task_id"] == "test-001"
    assert data["invoice_number"] == "INV-1042"
    assert "timestamp" in data


def test_json_formatter_handles_records_without_context():
    record = logging.LogRecord(
        name="taskpilot.test",
        level=logging.WARNING,
        pathname=__file__,
        lineno=20,
        msg="warning_message",
        args=(),
        exc_info=None
    )

    data = json.loads(JsonFormatter().format(record))

    assert data["level"] == "WARNING"
    assert data["message"] == "warning_message"
    assert "event" not in data


def test_json_formatter_includes_exception_details():
    try:
        raise ValueError("test error")
    except ValueError:
        import sys
        exc_info = sys.exc_info()

    record = logging.LogRecord(
        name="taskpilot.test",
        level=logging.ERROR,
        pathname=__file__,
        lineno=30,
        msg="execution_failed",
        args=(),
        exc_info=exc_info
    )

    data = json.loads(JsonFormatter().format(record))

    assert data["level"] == "ERROR"
    assert "exception" in data
    assert "ValueError: test error" in data["exception"]


def test_log_event_attaches_event_and_context(caplog):
    logger = logging.getLogger("taskpilot.observability_test")

    with caplog.at_level(logging.INFO, logger=logger.name):
        log_event(
            logger,
            logging.INFO,
            "invoice_processed",
            invoice_number="INV-1042",
            status="completed"
        )

    record = caplog.records[-1]

    assert record.event == "invoice_processed"
    assert record.context["invoice_number"] == "INV-1042"
    assert record.context["status"] == "completed"
