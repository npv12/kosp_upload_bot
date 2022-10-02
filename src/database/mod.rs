use std::sync::Arc;

use mongodb::{
    options::{ClientOptions, ResolverConfig},
    Client, Database,
};

mod admin;
mod maintainer;

#[derive(Clone)]
pub struct Db {
    db: Arc<Database>,
}

impl Db {
    pub async fn new(uri: String) -> Self {
        let options = ClientOptions::parse_with_resolver_config(&uri, ResolverConfig::cloudflare())
            .await
            .unwrap();
        let client = Client::with_options(options).unwrap();
        Self { db: Arc::new(client.database("kosp")) }
    }
}
