# Code pair #p1
# Code B




def divide() -> None:
    number = 1
    divisor = 0
    log.debug("in divide")
    try:
        number / divisor
    except ZeroDivisionError:
        log.exception("A division by zero error occurred!")
