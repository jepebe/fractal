from fractal import Range2D
from fractal import py_create_fractal


class Terminal(dict):
    def set_pixel(self, x, y, c):
        self[(x, y)] = c


def _colored_char(color, filler="\u2588"):
    r, g, b = [round(c) for c in color]
    return "\x1b[38;2;{r};{g};{b}m{f}\x1b[0m".format(r=r, g=g, b=b, f=filler)


def get_term(width, height, iterations, fra=Range2D(-2, 1, 1, -1)):
    pix = Range2D(0, 0, width, height)
    data = Terminal()
    py_create_fractal(pix, fra, iterations, data)
    return data


def _run(width, height, iterations):
    term_fractal(width, height, iterations=iterations)


def term_fractal(width=80, height=50, iterations=128, fra=Range2D(-2, 1, 1, -1)):
    data = get_term(width, height, iterations, fra)

    for row in range(height):
        print("".join(_colored_char(data[(col, row)]) for col in range(width)))


def main():
    import sys

    if len(sys.argv) not in (3, 4):
        msg = "Usage: py_fractal width height [iterations]\n"
        msg += "       py_fractal 72 32\n"
        msg += "       py_fractal 72 32 2048\n"
        sys.exit(msg)

    width = int(sys.argv[1])
    height = int(sys.argv[2])
    iterations = 2048
    if len(sys.argv) == 4:
        iterations = int(sys.argv[3])

    _run(width, height, iterations)


if __name__ == "__main__":
    main()
