from razomy.python.logging import logger


def test_log():
    logger.debug('debug', '0', '1')
    logger.info('info')
    logger.error(Exception('error'))

def test_level():
    logger.logger.level = logger.LogLevels.debug.level
    logger.debug('debug showing')
    logger.error('debug showing')
    logger.info('debug showing')

    logger.logger.level = logger.LogLevels.info.level
    logger.debug('info not showing')
    logger.error('info showing')
    logger.info('info showing')

    logger.logger.level = logger.LogLevels.error.level
    logger.debug('info not showing')
    logger.error('error showing')
    logger.info('error showing')


def test_tree():
    child_logger = logger.create('n1')
    child_logger.debug('n1')
    child_logger.create('n2')
    child_logger.debug('n2')
    child_logger.create('n3')
    child_logger.debug('n3')
    child_logger.destroy('n3')
    child_logger.debug('n2')
    child_logger.destroy('n2')
    child_logger.debug('n1')
    child_logger.destroy('n1')


if __name__ == '__main__':
    test_log()
    test_level()
    test_tree()
