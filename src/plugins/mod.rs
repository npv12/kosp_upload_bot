use crate::{cancel_cmds::CancelableCommands, database};
use grammers_client::{types::Message, Client};

mod add_maintainer;
mod cancel;
mod ping;
mod release;

type Result = std::result::Result<(), Box<dyn std::error::Error>>;

enum Command {
    AddMaintainer(String),
    Cancel(String),
    Help,
    Ping,
    Release(Vec<String>),
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
        "/cancel" => Command::Cancel(msg.to_string()),
        "/help" => Command::Help,
        "/ping" => Command::Ping,
        "/release" => Command::Release(args),
        "/start" => Command::Start,
        _ => return Ok(()),
    };

    match cmd {
        Command::AddMaintainer(msg) => {
            add_maintainer::add_maintainer(client, message, database, msg).await?
        }
        Command::Cancel(cmd) => cancel::cancel(client, message, cancel_cmds, cmd).await?,
        Command::Help => {
            let help_msg = "Hello! I'm Flamingo upload bot. I can upload files to your server. \
            These are the available commands:\n\
            /help - Show this message\n\
            /ping - Check how slow I am responding ;)\n\
            /release - Upload a file to your server and make a release post\n\
            /start - Check if I'm alive\n";
            client.send_message(chat, help_msg).await?;
        }
        Command::Ping => ping::ping(client, message).await?,
        Command::Release(links) => release::release(client, message, cancel_cmds, links).await?,
        Command::Start => {
            client.send_message(chat, "Hello!").await?;
        }
    }

    Ok(())
}
