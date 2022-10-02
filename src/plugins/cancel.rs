use crate::cancel_cmds::CancelableCommands;
use grammers_client::{types::Message, Client};

type Result = std::result::Result<(), Box<dyn std::error::Error>>;

pub async fn cancel(
    client: Client,
    message: Message,
    mut cancel_cmds: CancelableCommands,
    msg: String,
) -> Result {
    let cmds = msg.split(" ").into_iter().map(|s| s.into()).collect::<Vec<String>>();
    if cmds.len() < 2 {
        client
            .send_message(message.chat(), "You didn't provide a command id")
            .await?;
        return Ok(());
    }
    let id = cmds[1].parse::<u32>().unwrap_or(0);
    if id == 0 {
        client
            .send_message(message.chat(), "Invalid command id")
            .await?;
        return Ok(());
    }
    cancel_cmds.cancel(id);
    client
        .send_message(message.chat(), format!("Cancelling task with id {}", id))
        .await?;
    return Ok(());
}
