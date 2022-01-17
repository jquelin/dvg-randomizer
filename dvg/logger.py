import logging

logger_name = 'dvg'

try:
    import colorlog
except:
    # no colorlog available
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            '%(asctime)s %(module)s.%(funcName)s:%(lineno)d %(levelname)s %(message)s',
            datefmt='%H:%M:%S'
        )
    )

    log = logging.getLogger(logger_name)

else:
    # colorlog available
    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s %(module)s.%(funcName)s:%(lineno)d %(levelname)s %(message)s',
            datefmt='%H:%M:%S'
        )
    )
    log = colorlog.getLogger(logger_name)


log.setLevel(logging.DEBUG)
log.addHandler(handler)
