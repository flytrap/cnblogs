# coding: utf8
# auto: flytrap
import logging

formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


def define_logger(name, log_path, leave=None):
    parser_logger = logging.getLogger(name)
    parser_logger.setLevel(logging.DEBUG if not leave else leave)

    parser_file = logging.FileHandler(log_path)
    parser_file.setFormatter(formatter)
    console_file = logging.StreamHandler()
    console_file.setFormatter(formatter)

    parser_logger.addHandler(parser_file)
    parser_logger.addHandler(console_file)


if __name__ == '__main__':
    define_logger('parser', 'test.txt')
    logger = logging.getLogger('parser')
    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('error')
