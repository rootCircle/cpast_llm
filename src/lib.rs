use pyo3::prelude::*;
use cpast::generator;

#[pyfunction]
fn generate(lang: String) -> PyResult<String> {
    let generated_lang = generator(lang);
    if let Err(err) = generated_lang {
        return Ok(err.get_msg());
    }
    Ok(generated_lang.unwrap())
}

#[pymodule]
fn cpast_lib(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate, m)?)?;
    Ok(())
}
