use crate::cancel_cmds::CancelableCommands;
use grammers_client::{types::Message, Client};

type Result = std::result::Result<(), Box<dyn std::error::Error>>;

pub async fn release(
    client: Client,
    message: Message,
    mut cancel_cmds: CancelableCommands,
    links: Vec<String>,
) -> Result {
    if links.len() < 2 {
        client
            .send_message(message.chat(), "Please provide a link to the file")
            .await?;
        return Ok(());
    }

    let id = rand::random::<u32>();
    if id == 0 {
        client
            .send_message(message.chat(), "Failed to generate a random id")
            .await?;
        return Ok(());
    }
    cancel_cmds.insert(id);

    let mut msg = client
        .send_message(
            message.chat(),
            format!("Creating a release post for you with {:?}\nUse `/cancel {}` to cancel it", links, id),
        )
        .await?;

    // Final check to see if the user canceled the command before making the post
    if cancel_cmds.get_cancel_status(id) {
        msg.edit(format!("Process cancelled by user")).await?;
        return Ok(());
    }

    msg.edit(format!("Successfully created a release post"))
        .await?;
    cancel_cmds.remove(id);
    return Ok(());
}
