use cpast::generator;
use pyo3::prelude::*;
use pyo3::types::PyDict;
use pyo3::Python;

#[pyfunction]
fn generate(py: Python<'_>, lang: String) -> PyResult<&PyDict> {
    let generated_lang = generator(lang);
    let response = PyDict::new(py);
    match generated_lang {
        Err(err) => response.set_item("Err", err.get_msg()),
        Ok(lang) => response.set_item("Ok", lang),
    }?;

    Ok(response)
}

#[pymodule]
fn cpast_lib(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(generate, m)?)?;
    Ok(())
}
