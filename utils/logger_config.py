import logging
import os

def get_root_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def setup_logging(log_level=logging.INFO, log_dir='output/logs', log_file=None):
    """
    Setup logging configuration
    :param log_level: Log level
    :param log_file: Log file path
    :return: None
    """

    logger = logging.getLogger()
    logger.setLevel(log_level)

    if logger.hasHandlers():
        logger.handlers.clear()

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    if log_file:
        log_file_path = os.path.join(log_dir, log_file)
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.info('Logging setup complete')

if __name__ == '__main__':
    par_dir = get_root_dir()
    setup_logging(log_level=logging.DEBUG, log_dir=f'{par_dir}/output/logs', log_file='log.txt')
    logger = logging.getLogger(__name__)
    logger.info('Hello, World!')