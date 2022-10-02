use std::time::SystemTime;

use grammers_client::{Client, types::Message};

type Result = std::result::Result<(), Box<dyn std::error::Error>>;

pub async fn ping(client: Client, message: Message) -> Result {
    let start = SystemTime::now();
    let mut msg = client
        .send_message(message.chat(), "Pinging........!")
        .await?;
    let end = SystemTime::now();
    let ping = end.duration_since(start).unwrap().as_millis();
    msg.edit(format!("Pong! {}ms", ping)).await?;
    return Ok(());
}