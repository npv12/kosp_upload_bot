use grammers_client::{types::Message, Client};

use super::{direct_link::DirectLink, document::Document, gdrive::Gdrive};

pub enum DocumentProcessor<S, T> {
    GDrive(S),
    DirectLink(T),
}
pub fn factory(
    link: String,
    client: Client,
    message: Message,
) -> DocumentProcessor<Gdrive, DirectLink> {
    if link.contains("drive.google.com") {
        DocumentProcessor::GDrive(Gdrive::new(Document::new(
            message,
            client,
            "gdrive".to_string(),
        )))
    } else {
        DocumentProcessor::DirectLink(DirectLink::new(Document::new(
            message,
            client,
            "direct_link".to_string(),
        )))
    }
}
