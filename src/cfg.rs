use std::{error::Error, fs::File, io::Read};

#[derive(Debug, serde::Deserialize)]
pub struct Config {
    /// API from telegram
    pub api_id: i32,
    pub api_hash: String,
    /// Token of the telegram bot
    pub bot_token: String,
    // monogoDB uri
    pub mongo_uri: String,
}

impl Config {
    pub fn read() -> Result<Self, Box<dyn Error>> {
        let mut str = String::new();
        File::open("./config.toml")?.read_to_string(&mut str)?;
        Ok(toml::from_str(&str)?)
    }
}