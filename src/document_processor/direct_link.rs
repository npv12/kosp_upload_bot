use super::{document::Document, Downloader};
use async_trait::async_trait;

pub struct DirectLink {
    document: Document,
}

#[async_trait]
impl Downloader for DirectLink {
    async fn download(&self) -> Result<(), Box<dyn std::error::Error>> {
        Ok(())
    }
}

impl DirectLink {
    pub fn new(document: Document) -> Self {
        Self { document }
    }
}
