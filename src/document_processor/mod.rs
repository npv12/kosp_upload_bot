use async_trait::async_trait;
use grammers_client::{types::Message, Client};

mod direct_link;
mod document;
mod factory;
mod gdrive;

#[async_trait]
pub trait Downloader {
    async fn download(&self) -> Result<(), Box<dyn std::error::Error>>;
}
