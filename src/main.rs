use std::{str, sync::Arc};
use teloxide::{
    adaptors::{AutoSend},
    prelude::*
};
use futures::future::{self, pending};

mod bot;
mod cfg;
mod plugins;

type Bot = AutoSend<teloxide::Bot>;

#[tokio::main]
async fn main() {
    pretty_env_logger::init();
    const VERSION: &str = env!("CARGO_PKG_VERSION");
    let config = Arc::new(cfg::Config::read().expect("couldn't read config"));
    let bot = teloxide::Bot::new(&config.bot_token)
        .auto_send();

    log::info!("Flamingo upload bot v{} is up and running...", VERSION);

    let (_abortable, abort_handle) = future::abortable(pending::<()>());
    let tg_loop = async {
        bot::run(bot.clone(), config).await;

        // When bot stopped executing (e.g. because of ^C) stop pull loop
        abort_handle.abort();
    };

    tokio::join!(tg_loop);
}