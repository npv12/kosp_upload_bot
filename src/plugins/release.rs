use crate::cancel_cmds::{add_cmds, drop_cmds, CancelableCommands};
use grammers_client::{types::Message, Client};
use std::sync::{Arc, Mutex};

type Result = std::result::Result<(), Box<dyn std::error::Error>>;

pub async fn release(
    client: Client,
    message: Message,
    cancel_cmd: Arc<Mutex<CancelableCommands>>,
    links: Vec<String>,
) -> Result {
    let id = rand::random::<i32>();
    add_cmds(&cancel_cmd, &id);
    let mut msg = client
        .send_message(
            message.chat(),
            format!("Creating a release post for you with {:?}", links),
        )
        .await?;

    msg.edit(format!("Successfully created a release post"))
        .await?;
    drop_cmds(&cancel_cmd, &id);
    return Ok(());
}
