use futures::future::{self, pending};
use std::{str, sync::Arc};
use teloxide::{
    adaptors::{throttle::Limits, AutoSend, Throttle},
    prelude::*,
};

use crate::cancel_tasks::CancelableTasks;

mod bot;
mod cancel_tasks;
mod cfg;
mod plugins;

type Bot = AutoSend<Throttle<teloxide::Bot>>;

#[tokio::main]
async fn main() {
    pretty_env_logger::init();
    const VERSION: &str = env!("CARGO_PKG_VERSION");
    let config = Arc::new(cfg::Config::read().expect("couldn't read config"));
    let bot = teloxide::Bot::new(&config.bot_token)
        .throttle(Limits::default())
        .auto_send();

    log::info!("Flamingo upload bot v{} is up and running...", VERSION);

    let mut tasks = CancelableTasks::new();

    let (_abortable, abort_handle) = future::abortable(pending::<()>());
    let tg_loop = async {
        bot::run(bot.clone(), &mut tasks).await;

        // When bot stopped executing (e.g. because of ^C) stop pull loop
        abort_handle.abort();
    };

    tokio::join!(tg_loop);
}
