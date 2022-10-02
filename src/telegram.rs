use crate::{cancel_cmds::CancelableCommands, cfg, plugins};
use grammers_client::{
    types::{Chat, Message},
    Client, Config, InitParams, Update,
};
use grammers_session::Session;
use log;
use std::sync::Arc;
use tokio::task;

type Result = std::result::Result<(), Box<dyn std::error::Error>>;

const SESSION_FILE: &str = "echo.session";

pub async fn async_main() -> Result {
    let config = Arc::new(cfg::Config::read().expect("cannot read the config"));
    let api_id = config.clone().api_id;
    let api_hash = &config.api_hash;
    let token = &config.bot_token;

    log::info!("Connecting to Telegram...");
    let mut client = Client::connect(Config {
        session: Session::load_file_or_create(SESSION_FILE)?,
        api_id,
        api_hash: api_hash.clone(),
        params: InitParams {
            // Fetch the updates we missed while we were offline
            catch_up: true,
            ..Default::default()
        },
    })
    .await?;
    log::info!("Connected!");

    if !client.is_authorized().await? {
        log::info!("Signing in...");
        client.bot_sign_in(&token, api_id, &api_hash).await?;
        client.session().save_to_file(SESSION_FILE)?;
        log::info!("Signed in!");
    }

    log::info!("Waiting for messages...");

    let cancel_cmd = CancelableCommands::new();

    while let Some(update) = tokio::select! {
        _ = tokio::signal::ctrl_c() => Ok(None),
        result = client.next_update() => result,
    }? {
        let handle = client.clone();
        let cmd = cancel_cmd.clone();
        task::spawn(async move {
            match handle_update(handle, update, cmd).await {
                Ok(_) => {}
                Err(e) => log::error!("Error handling updates!: {}", e),
            }
        });
    }

    log::warn!("Saving session file and exiting...");
    client.session().save_to_file(SESSION_FILE)?;
    Ok(())
}

async fn handle_update(client: Client, update: Update, cancel_cmds: CancelableCommands) -> Result {
    match update {
        Update::NewMessage(message) if check_privilages(&message) => {
            plugins::handle_msg(client, message, cancel_cmds).await?
        }
        _ => {}
    }
    Ok(())
}

fn check_privilages(message: &Message) -> bool {
    return !message.outgoing() && matches!(message.chat(), Chat::User(_));
}
