use grammers_client::{types::Message, Client};

type Result = std::result::Result<(), Box<dyn std::error::Error>>;

pub async fn help(client: Client, message: Message) -> Result {
    let help_msg = "Hello! I'm Flamingo upload bot. I can upload files to your server. \
            These are the available commands:\n\
            /help - Show this message\n\
            /cancel - Cancel the release post\n\
            /ping - Check how slow I am responding ;)\n\
            /release - Upload a file to your server and make a release post\n\
            /start - Check if I'm alive\n\n\
            These commands are restricted to an admin\n\
            /add - Add a maintainer\n\
            /promote - Promote a maintainer to admin\n\
            /remove - Remove a maintainer\n\
            ";
    client.send_message(message.chat(), help_msg).await?;
    return Ok(());
}
