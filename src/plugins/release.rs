use crate::cancel_cmds::CancelableCommands;
use grammers_client::{types::Message, Client};

type Result = std::result::Result<(), Box<dyn std::error::Error>>;

pub async fn release(
    client: Client,
    message: Message,
    mut cancel_cmds: CancelableCommands,
    links: Vec<String>,
) -> Result {
    let id = rand::random::<i32>();
    cancel_cmds.insert(id);
    let mut msg = client
        .send_message(
            message.chat(),
            format!("Creating a release post for you with {:?}", links),
        )
        .await?;

    if cancel_cmds.get_cancel_status(id) {
        msg.edit(format!("Process cancelled by user")).await?;
        return Ok(());
    }

    msg.edit(format!("Successfully created a release post"))
        .await?;
    cancel_cmds.remove(id);
    return Ok(());
}
