# Code pair #p74
# Code B


def divide() -> None:
    number = 1
    divisor = 0
    log.debug("in divide")
    try:
        number / divisor
    except:
        log.exception("An error of some kind occurred!")
