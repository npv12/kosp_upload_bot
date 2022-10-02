use tokio::runtime;

mod cfg;
mod plugins;
mod telegram;

type Result = std::result::Result<(), Box<dyn std::error::Error>>;

fn main() -> Result {
    runtime::Builder::new_current_thread()
        .enable_all()
        .build()
        .unwrap()
        .block_on(telegram::async_main())
}
