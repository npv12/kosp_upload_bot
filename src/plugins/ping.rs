use std::time::SystemTime;
use teloxide::{prelude::*, RequestError, adaptors::Throttle};

pub async fn ping(bot: AutoSend<Throttle<Bot>>, message: Message) -> Result<Message, RequestError> {
    let start = SystemTime::now();
    let msg = bot
        .send_message(message.chat.id, "Pinging........!")
        .await?;
    let end = SystemTime::now();
    let ping = end.duration_since(start).unwrap().as_millis();
    bot.edit_message_text(message.chat.id, msg.id, format!("Pong! {}ms", ping))
        .await?;
    return Ok(msg);
}
