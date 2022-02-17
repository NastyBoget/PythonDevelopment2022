import locale
import sys
from time import strftime

from pyfiglet import Figlet


def date(date_format: str = "%Y %d %b, %A", font: str = "graceful") -> str:
    f = Figlet(font=font)
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    text = strftime(date_format)
    return f.renderText(text)


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:
        print(date())
    elif len(args) == 2:
        print(date(args[1]))
    elif len(args) == 3:
        print(date(args[1], args[2]))
    else:
        raise ValueError("Invalid parameters, use one of the following:\npython3 -m figdate\n"
                         "python3 -m figdate format\npython3 -m figdate format font")
