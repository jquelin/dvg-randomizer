
import colorlog
import logging

handler = colorlog.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s %(module)s.%(funcName)s:%(lineno)d %(levelname)s %(message)s',
        datefmt='%H:%M:%S'
    )
)
log = colorlog.getLogger('dvg')
log.setLevel(logging.DEBUG)
log.addHandler(handler)

