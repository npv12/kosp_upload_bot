use grammers_client::{types::Message, Client};

pub struct Document {
    message: Message,
    client: Client,
    device_name: String,
}

impl Document {
    pub fn new(message: Message, client: Client, device_name: String) -> Self {
        Self {
            message,
            client,
            device_name,
        }
    }
    pub async fn upload() -> Result<(), Box<dyn std::error::Error>> {
        Ok(())
    }
}
