use teloxide::{prelude::*, utils::command::BotCommands};

use std::error::Error;
mod plugins;

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
    log::info!(
        "Command received: {}",
        message.text().unwrap().replace("/", "")
    );
    //ping::ping();
    match command {
        Command::Help => {
            bot.send_message(message.chat.id, Command::descriptions().to_string())
                .await?
        }
        Command::Ping => plugins::ping::ping(bot, message).await?,
        Command::Release(cmd) => plugins::release::release(bot, message, cmd).await?,
        Command::Start => bot.send_message(message.chat.id, "I am alive!").await?,
    };

    Ok(())
}
