use simple_logger::SimpleLogger;
use tokio::runtime;

mod cfg;
mod plugins;
mod telegram;

type Result = std::result::Result<(), Box<dyn std::error::Error>>;

const VERSION: &str = env!("CARGO_PKG_VERSION");
fn main() -> Result {
    SimpleLogger::new()
        .with_level(log::LevelFilter::Info)
        .init()
        .unwrap();

    log::info!("Flamingo upload bot v{} is initiating...", VERSION);
    runtime::Builder::new_current_thread()
        .enable_all()
        .build()
        .unwrap()
        .block_on(telegram::async_main())
}
