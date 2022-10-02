use grammers_client::{Client, Update};

type Result = std::result::Result<(), Box<dyn std::error::Error>>;

pub async fn handle_update(client: Client, update: Update) -> Result {
    match update {
        Update::NewMessage(message) if !message.outgoing() => {
            let chat = message.chat();
            println!("Responding to {}", chat.name());
            client.send_message(&chat, message.text()).await?;
        }
        _ => {}
    }

    Ok(())
}
