use super::{document::Document, Downloader};
use async_trait::async_trait;

pub struct Gdrive {
    document: Document,
}

#[async_trait]
impl Downloader for Gdrive {
    async fn download(&self) -> Result<(), Box<dyn std::error::Error>> {
        Ok(())
    }
}

impl Gdrive {
    pub fn new(document: Document) -> Self {
        Self { document }
    }
}
