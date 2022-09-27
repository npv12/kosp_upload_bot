use crate::{Bot, cfg::Config, plugins};
use std::{fmt::Debug, ops::Not, sync::Arc};
use teloxide::{
    dptree::deps,
    prelude::{Requester, *},
    utils::command::BotCommands,
    RequestError,
};

#[derive(BotCommands, Clone, PartialEq, Eq, Debug)]
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

#[derive(Debug, derive_more::Display, derive_more::From, derive_more::Error)]
enum HErr {
    Tg(RequestError),
    GetUser,
    NotAdmin,
}

pub async fn run(bot: Bot, cfg: Arc<Config>) {
    let commands = |bot: Bot, message: Message, command: Command| async move {
        log::info!(
            "Command received: {}",
            message.text().unwrap().replace("/", "")
        );
        check_privileges(&bot, &message).await?;
        match command {
            Command::Help => {
                bot.send_message(message.chat.id, Command::descriptions().to_string())
                    .await?
            }
            Command::Ping => plugins::ping::ping(bot, message).await?,
            Command::Release(cmd) => plugins::release::release(bot, message, cmd).await?,
            Command::Start => bot.send_message(message.chat.id, "I am alive!").await?,
        };

        Ok::<_, HErr>(())
    };

    let handler = dptree::entry().branch(
        Update::filter_message()
            .filter_command::<Command>()
            .endpoint(commands),
    );

    Dispatcher::builder(bot, handler)
        .dependencies(deps![cfg])
        .default_handler(|_| async {})
        .build()
        .dispatch()
        .await;
}

async fn check_privileges(bot: &Bot, msg: &Message) -> Result<(), HErr> {
    if !msg.chat.is_private() {
        let admins = bot.get_chat_administrators(msg.chat.id).await?;

        let user_id = msg.from().ok_or(HErr::GetUser)?.id;
        if admins
            .iter()
            .map(|admin| admin.user.id)
            .any(|id| id == user_id)
            .not()
        {
            return Err(HErr::NotAdmin);
        }
    };

    Ok(())
}
