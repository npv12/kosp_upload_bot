use std::sync::Arc;

use grammers_client::{Client, Config, InitParams, Update};
use grammers_session::Session;
use log;
use simple_logger::SimpleLogger;
use tokio::{runtime, task};

mod cfg;

type Result = std::result::Result<(), Box<dyn std::error::Error>>;

const SESSION_FILE: &str = "echo.session";

async fn handle_update(client: Client, update: Update) -> Result {
    match update {
        Update::NewMessage(message) if !message.outgoing() => {
            let chat = message.chat();
            println!("Responding to {}", chat.name());
            client.send_message(&chat, message.text()).await?;
        }
        _ => {}
    }

    Ok(())
}

async fn async_main() -> Result {
    SimpleLogger::new()
        .with_level(log::LevelFilter::Info)
        .init()
        .unwrap();

    let config = Arc::new(cfg::Config::read().expect("couldn't read config"));
    let api_id = config.clone().api_id;
    let api_hash = &config.api_hash;
    let token = &config.bot_token;

    log::warn!("Connecting to Telegram...");
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
    log::warn!("Connected!");

    if !client.is_authorized().await? {
        log::info!("Signing in...");
        client.bot_sign_in(&token, api_id, &api_hash).await?;
        client.session().save_to_file(SESSION_FILE)?;
        log::info!("Signed in!");
    }

    log::debug!("Waiting for messages...");

    // This code uses `select!` on Ctrl+C to gracefully stop the client and have a chance to
    // save the session. You could have fancier logic to save the session if you wanted to
    // (or even save it on every update). Or you could also ignore Ctrl+C and just use
    // `while let Some(updates) =  client.next_updates().await?`.
    while let Some(update) = tokio::select! {
        _ = tokio::signal::ctrl_c() => Ok(None),
        result = client.next_update() => result,
    }? {
        let handle = client.clone();
        task::spawn(async move {
            match handle_update(handle, update).await {
                Ok(_) => {}
                Err(e) => log::error!("Error handling updates!: {}", e),
            }
        });
    }

    log::warn!("Saving session file and exiting...");
    client.session().save_to_file(SESSION_FILE)?;
    Ok(())
}

fn main() -> Result {
    runtime::Builder::new_current_thread()
        .enable_all()
        .build()
        .unwrap()
        .block_on(async_main())
}
