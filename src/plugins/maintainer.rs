use crate::database;
use grammers_client::{types::Message, Client};

type Result = std::result::Result<(), Box<dyn std::error::Error>>;

pub async fn add_maintainer(
    client: Client,
    message: Message,
    database: database::Db,
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
            .send_message(message.chat(), "You didn't provide a device name")
            .await?;
        return Ok(());
    }
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

    let maintainer_name = reply_msg
        .clone()
        .unwrap()
        .sender()
        .unwrap()
        .name()
        .to_string();
    let device_name = cmds[1].to_string();
    let maintainer_id = reply_msg.clone().unwrap().sender().unwrap().id();

    database
        .add_maintainer(maintainer_name, maintainer_id, device_name)
        .await?;

    client
        .send_message(
            message.chat(),
            format!("Successfully added {} as a maintainer", cmds[1]),
        )
        .await?;
    return Ok(());
}

pub async fn remove_maintainer(client: Client, message: Message, database: database::Db) -> Result {
    // Sanity checks
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

    database.remove_maintainer(maintainer_id).await?;

    client
        .send_message(message.chat(), format!("Successfully removed a maintainer"))
        .await?;
    return Ok(());
}
