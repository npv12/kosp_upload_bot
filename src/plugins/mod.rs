use crate::cancel_cmds::{add_cmds, drop_cmds, CancelableCommands};
use grammers_client::{Client, Update};
use std::sync::{Arc, Mutex};

type Result = std::result::Result<(), Box<dyn std::error::Error>>;

pub async fn handle_update(
    client: Client,
    update: Update,
    tasks: Arc<Mutex<CancelableCommands>>,
) -> Result {
    match update {
        Update::NewMessage(message) if !message.outgoing() => {
            let id = rand::random::<i32>();
            let chat = message.chat();

            add_cmds(&tasks, &id);
            client.send_message(&chat, message.text()).await?;
            drop_cmds(&tasks, &id);
        }
        _ => {}
    }

    Ok(())
}
