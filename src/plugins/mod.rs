use crate::{cancel_cmds::CancelableCommands, database};
use grammers_client::{types::Message, Client};

mod admin;
mod cancel;
mod help;
mod maintainer;
mod ping;
mod release;
mod support_group;

type Result = std::result::Result<(), Box<dyn std::error::Error>>;

#[derive(Debug)]
enum Command {
    AddMaintainer(String),
    AddSupportGroup(String),
    Cancel(String),
    Help,
    Ping,
    PromoteMaintainer(),
    Release(Vec<String>),
    RemoveMaintainer(),
    Start,
}

pub async fn handle_msg(
    client: Client,
    message: Message,
    cancel_cmds: CancelableCommands,
    database: database::Db,
) -> Result {
    let msg = message.text();
    let chat = message.chat();
    let cmd = msg.split_whitespace().next().unwrap();
    let args = msg.split(" ").into_iter().map(|s| s.into()).collect();
    let cmd = match cmd {
        "/add" => Command::AddMaintainer(msg.to_string()),
        "/add_support" => Command::AddSupportGroup(msg.to_string()),
        "/cancel" => Command::Cancel(msg.to_string()),
        "/help" => Command::Help,
        "/ping" => Command::Ping,
        "/promote" => Command::PromoteMaintainer(),
        "/release" => Command::Release(args),
        "/remove" => Command::RemoveMaintainer(),
        "/start" => Command::Start,
        _ => return Ok(()),
    };
    log::info!("Recieved request to handle command: {:?}", cmd);
    match cmd {
        Command::AddMaintainer(msg) => {
            maintainer::add_maintainer(client, message, database, msg).await?
        }
        Command::AddSupportGroup(msg) => {
            support_group::add_support_group(client, message, database, msg).await?
        }
        Command::Cancel(cmd) => cancel::cancel(client, message, cancel_cmds, cmd).await?,
        Command::Help => help::help(client, message).await?,
        Command::Ping => ping::ping(client, message).await?,
        Command::PromoteMaintainer() => {
            admin::promote_maintainer(client, message, database).await?
        }
        Command::Release(links) => {
            release::release(client, message, cancel_cmds, links, database).await?
        }
        Command::RemoveMaintainer() => {
            maintainer::remove_maintainer(client, message, database).await?
        }
        Command::Start => {
            client.send_message(chat, "Hello!").await?;
        }
    }

    Ok(())
}
