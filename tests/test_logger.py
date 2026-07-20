import importlib
import sys


def test_logger_uses_a_single_log_file_name():
    sys.modules.pop("utils.logger", None)

    logger_module = importlib.import_module("utils.logger")

    assert logger_module.log_file.name == "scrape.log"
    assert logger_module.log_file.parent == logger_module.LOG_DIR
