import math

from fractal import Range2D


def py_create_fractal(pix: Range2D, frac: Range2D, iterations, data):
    x_scale = (frac.x2 - frac.x1) / (pix.x2 - pix.x1)
    y_scale = (frac.y2 - frac.y1) / (pix.y2 - pix.y1)

    colors = []
    for n in range(iterations + 1):
        # @Eriksonn referred to by OLC
        a = 0.1
        r = 0.5 * math.sin(a * n) + 0.5
        g = 0.5 * math.sin(a * n + 2.094) + 0.5
        b = 0.5 * math.sin(a * n + 4.188) + 0.5
        colors.append((r * 255, g * 255, b * 255))

    for y in range(pix.y1, pix.y2):
        for x in range(pix.x1, pix.x2):
            c = complex(x * x_scale + frac.x1, y * y_scale + frac.y1)
            z = complex(0, 0)

            n = 0
            while (z.real * z.real + z.imag * z.imag) < 4 and n < iterations:
                z = (z * z) + c
                n += 1
            data.set_pixel(x, y, colors[n])
