use teloxide::{prelude::*, utils::command::BotCommands};

use std::error::Error;
use std::time::SystemTime;

#[tokio::main]
async fn main() {
    pretty_env_logger::init();
    const VERSION: &str = env!("CARGO_PKG_VERSION");
    log::info!("Flamingo upload bot v{} is up and running...", VERSION);
    let bot: AutoSend<Bot> = Bot::from_env().auto_send();

    teloxide::commands_repl(bot, answer, Command::ty()).await;
}

#[derive(BotCommands, Clone)]
#[command(rename = "lowercase", description = "These commands are supported:")]
enum Command {
    #[command(description = "display this text.")]
    Help,
    #[command(description = "ping the bot.")]
    Ping,
    #[command(description = "creare a release post for FlamingoOS.")]
    Release(String),
    #[command(description = "start the bot and see if it is alive?")]
    Start,
}

async fn answer(
    bot: AutoSend<Bot>,
    message: Message,
    command: Command,
) -> Result<(), Box<dyn Error + Send + Sync>> {
    log::info!("Command received: {}", message.text().unwrap().replace("/", ""));
    match command {
        Command::Help => {
            bot.send_message(message.chat.id, Command::descriptions().to_string())
                .await?
        }
        Command::Ping => {
            let start = SystemTime::now();
            let msg = bot.send_message(message.chat.id, "Pinging........!").await?;
            let end = SystemTime::now();
            let ping = end.duration_since(start).unwrap().as_millis();
            bot.edit_message_text(message.chat.id, msg.id, format!("Pong! {}ms", ping))
                .await?
        },
        Command::Release(msg) => {
            let links = msg.split_whitespace().collect::<Vec<&str>>();
            bot.send_message(
                message.chat.id,
                format!("Creating a release post for you with {:?}", links),
            )
            .await?
        }
        Command::Start => {
            bot.send_message(message.chat.id, "I am alive!")
                .await?
        }
    };

    Ok(())
}
