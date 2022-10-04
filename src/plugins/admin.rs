use crate::database;
use grammers_client::{types::Message, Client};

type Result = std::result::Result<(), Box<dyn std::error::Error>>;

pub async fn promote_maintainer(
    client: Client,
    message: Message,
    database: database::Db,
) -> Result {
    if message.reply_to_message_id() == None {
        client
            .send_message(message.chat(), "You didn't reply to a message")
            .await?;
        return Ok(());
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

    database.promote_admin(maintainer_id).await?;

    client
        .send_message(message.chat(), format!("Successfully added as an admin"))
        .await?;
    return Ok(());
}
