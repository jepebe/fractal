use pyo3::prelude::*;
use pyo3::types::{PyAny};
use pyo3::wrap_pyfunction;
use num::complex::Complex;
use numpy::PyArrayDyn;
use ndarray::ArrayViewMutD;

fn create_colors(iterations: usize) -> Vec<u8> {
    let mut colors : Vec<u8> = Vec::with_capacity(iterations * 3);
    for i in 0..iterations {
        let r: u8 = ((0.5 * f64::sin(0.1 * i as f64) + 0.5) * 255.0) as u8;
        let g: u8 = ((0.5 * f64::sin(0.1 * i as f64 + 2.094) + 0.5) * 255.0) as u8;
        let b: u8 = ((0.5 * f64::sin(0.1 * i as f64 + 4.188) + 0.5) * 255.0) as u8;
        colors.push(r);
        colors.push(g);
        colors.push(b);
    }
    colors
}

#[pyfunction]
pub fn create_fractal(_py: Python<'_>, pix: &PyAny, frac: &PyAny, iterations: usize, data: &PyArrayDyn<u8>) -> PyResult<()> {
    let px1: usize = pix.getattr("x1")?.extract()?;
    let py1: usize = pix.getattr("y1")?.extract()?;
    let px2: usize = pix.getattr("x2")?.extract()?;
    let py2: usize = pix.getattr("y2")?.extract()?;

    let fx1: f64 = frac.getattr("x1")?.extract()?;
    let fy1: f64 = frac.getattr("y1")?.extract()?;
    let fx2: f64 = frac.getattr("x2")?.extract()?;
    let fy2: f64 = frac.getattr("y2")?.extract()?;

    let x_scale = (fx2 - fx1) / (px2 - px1) as f64;
    let y_scale = (fy2 - fy1) / (py2 - py1) as f64;

    let colors = create_colors(iterations + 1);

    let mut data = unsafe { data.as_array_mut() };
    for y in py1..py2 {
        for x in px1..px2 {
            let c = Complex::new(x as f64 * x_scale + fx1, y as f64 * y_scale + fy1);
            let mut z = Complex::new(0.0, 0.0);

            let mut n = 0;
            while (z.re * z.re + z.im * z.im) < 4.0 && n < iterations {
                z = (z * z) + c;
                n += 1;
            }
            data[[y, x, 0]] = colors[n * 3];
            data[[y, x, 1]] = colors[n * 3 + 1];
            data[[y, x, 2]] = colors[n * 3 + 2];
        }
    }
    Ok(())
}

#[pymodule]
fn _fractal(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(create_fractal))?;

    Ok(())
}