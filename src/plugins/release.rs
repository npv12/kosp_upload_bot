use teloxide::{prelude::*, RequestError, adaptors::Throttle};

pub async fn release(bot: AutoSend<Throttle<Bot>>, message: Message, cmd: String) -> Result<Message, RequestError> {
    let links = cmd.split_whitespace().collect::<Vec<&str>>();
    let msg = bot
        .send_message(
            message.chat.id,
            format!("Creating a release post for you with {:?}", links),
        )
        .await?;
    return Ok(msg);
}
