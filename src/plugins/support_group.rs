use grammers_client::{types::Message, Client};

use crate::database::Db;

type Result = std::result::Result<(), Box<dyn std::error::Error>>;

pub async fn add_support_group(
    client: Client,
    message: Message,
    database: Db,
    msg: String,
) -> Result {
    // Sanity checks
    let cmds = msg
        .split(" ")
        .into_iter()
        .map(|s| s.into())
        .collect::<Vec<String>>();

    if cmds.len() < 2 {
        client
            .send_message(message.chat(), "You didn't provide a device link")
            .await?;
        return Ok(());
    }

    let support_group: String = cmds.get(1).unwrap().to_string();

    if message.reply_to_message_id() == None {
        database
            .add_support_group(message.sender().unwrap().id(), support_group)
            .await?;
        return Ok(());
    } else {
        let is_admin = database.is_admin(message.sender().unwrap().id()).await?;
        if !is_admin {
            client
                .send_message(
                    message.chat(),
                    "Only admin can change support groups of others",
                )
                .await?;
        }

        // get the message being replied to separately
        let reply_msgs = client
            .get_messages_by_id(
                message.chat(),
                &message
                    .reply_to_message_id()
                    .into_iter()
                    .map(|s| s.into())
                    .collect::<Vec<i32>>(),
            )
            .await?;

        let reply_msg = reply_msgs.get(0).unwrap();

        let maintainer_id = reply_msg.clone().unwrap().sender().unwrap().id();
        database
            .add_support_group(maintainer_id, support_group)
            .await?;
    }

    client
        .send_message(message.chat(), format!("Successfully removed a maintainer"))
        .await?;
    return Ok(());
}
