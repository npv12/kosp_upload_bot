use std::sync::Arc;

use bson::Document;
use mongodb::{
    options::{ClientOptions, ResolverConfig},
    Client, Collection,
};

mod admin;
mod maintainer;
mod support_group;

#[derive(Clone)]
pub struct Db {
    collection: Arc<Collection<Document>>,
}

impl Db {
    pub async fn new(uri: String) -> Self {
        let options = ClientOptions::parse_with_resolver_config(&uri, ResolverConfig::cloudflare())
            .await
            .unwrap();
        let client = Client::with_options(options).unwrap();
        Self {
            collection: Arc::new(client.database("kosp").collection("maintainer")),
        }
    }
}
