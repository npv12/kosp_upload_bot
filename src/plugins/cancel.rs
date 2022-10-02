use crate::cancel_cmds::{cancel_cmds, CancelableCommands};
use grammers_client::{types::Message, Client};
use std::sync::{Arc, Mutex};

type Result = std::result::Result<(), Box<dyn std::error::Error>>;

pub async fn cancel(
    client: Client,
    message: Message,
    cancel_cmd: Arc<Mutex<CancelableCommands>>,
    cmd: String
) -> Result {
    let id = cmd.parse::<i32>().unwrap_or(0);
    cancel_cmds(&cancel_cmd, &id);
    client
        .send_message(message.chat(), format!("Cancelling task with id {}", id))
        .await?;
    return Ok(());
}
