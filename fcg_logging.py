import logging
from flowcat import utils


def create_logging_handlers(logging_path):
    """Create logging to both file and stderr."""
    return [
        utils.logs.create_handler(logging.FileHandler(str(logging_path))),
        utils.logs.create_handler(utils.logs.print_stream()),
    ]


def setup_logging(logging_path, name):
    logging_path.parent.mkdir()

    logger = logging.getLogger(name)
    handlers = create_logging_handlers(logging_path)
    utils.logs.add_logger(logger, handlers)
    return logger
