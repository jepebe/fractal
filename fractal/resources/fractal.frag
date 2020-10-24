#version 400 core
uniform int iterations;
uniform dvec4 fractal_space;

out vec4 out_color;
in vec2 tex_coord;

void main() {
    double fx = mix(fractal_space[0], fractal_space[2], double(tex_coord.x));
    double fy = mix(fractal_space[3], fractal_space[1], double(tex_coord.y));

    double cr = fx;
    double ci = fy;
    double zr = 0;
    double zi = 0;
    double re = 0;
    double im = 0;

    int n = 0;
    while ((zr * zr + zi * zi) < 4.0 && n < iterations) {
        re = zr * zr - zi * zi + cr;
        im = zr * zi * 2.0 + ci;
        zr = re;
        zi = im;
        n++;
    }

    // The burning ship fractal
//    while ((zr*zr + zi*zi) < 4 && n < iterations) {
//        double temp = zr * zr - zi * zi + fx;
//        zi = abs(2 * zr * zi) + fy;
//        zr = temp;
//        n++;
//    }

    float a = 0.1;
    float r = 0.5 * sin(a * n) + 0.5;
    float g = 0.5 * sin(a * n + 2.094) + 0.5;
    float b = 0.5 * sin(a * n + 4.188) + 0.5;
    out_color = vec4(r, g, b, 1);
}