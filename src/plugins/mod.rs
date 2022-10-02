use crate::cancel_cmds::{add_cmds, drop_cmds, CancelableCommands};
use grammers_client::{
    types::{Chat, Message},
    Client, Update,
};
use std::sync::{Arc, Mutex};

mod ping;

type Result = std::result::Result<(), Box<dyn std::error::Error>>;

enum Command {
    Help,
    Ping,
    Release(String),
    Start,
}

pub async fn handle_update(
    client: Client,
    update: Update,
    tasks: Arc<Mutex<CancelableCommands>>,
) -> Result {
    match update {
        Update::NewMessage(message) if check_privilages(&message) => {
            handle_msg(client, message, tasks).await?
        }
        _ => {}
    }

    Ok(())
}

async fn handle_msg(client: Client, message: Message, tasks: Arc<Mutex<CancelableCommands>>) -> Result {
    let msg = message.text();
    let chat = message.chat();
    let cmd = msg.split_whitespace().next().unwrap();
    let args = msg.split_whitespace().skip(1).collect::<Vec<_>>();
    let cmd = match cmd {
        "/help" => Command::Help,
        "/ping" => Command::Ping,
        "/release" => Command::Release(args.join(" ")),
        "/start" => Command::Start,
        _ => return Ok(()),
    };

    match cmd {
        Command::Help => {
            let help_msg = "Hello! I'm Flamingo upload bot. I can upload files to your server. \
            These are the available commands:\n\
            /help - Show this message\n\
            /ping - Check how slow I am responding ;)\n\
            /release - Upload a file to your server and make a release post\n\
            /start - Check if I'm alive\n";
            client.send_message(chat, help_msg).await?;
        }
        Command::Ping => {
            ping::ping(client, message).await?
        }
        Command::Release(release) => {
            let id = rand::random::<i32>();
            add_cmds(&tasks, &id);
            client.send_message(chat, format!("Creating a release post for you with {:?}", release)).await?;
            drop_cmds(&tasks, &id);
        }
        Command::Start => {
            client.send_message(chat, "Hello!").await?;
        }
    }

    Ok(())
}

fn check_privilages(message: &Message) -> bool {
    return !message.outgoing() && matches!(message.chat(), Chat::User(_));
}
