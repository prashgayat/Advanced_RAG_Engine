
use pyo3::prelude::*;

#[pyfunction]
fn split_text(text: &str, chunk_size: usize) -> Vec<String> {
    let chunks: Vec<String> = text
        .as_bytes()
        .chunks(chunk_size)
        .map(|c| String::from_utf8_lossy(c).to_string())
        .collect();
    chunks
}

#[pymodule]
fn semantic_text_splitter(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(split_text, m)?)?;
    Ok(())
}
