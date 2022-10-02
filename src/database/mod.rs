use mongodb::{
    options::{ClientOptions, ResolverConfig},
    Client, Database,
};
use std::error::Error;

pub struct Db {
    client: Client,
    flamingo_db: Database
}

impl Db {
    pub async fn new(uri: String) -> Self {
        let options = ClientOptions::parse_with_resolver_config(&uri, ResolverConfig::cloudflare())
            .await
            .unwrap();
        let client = Client::with_options(options).unwrap();
        Self { client: client.clone(), flamingo_db: client.database("kosp") }
    }
    // temp fun for future ref
    // TODO: drop this later on
    async fn print(&self) -> Result<(), Box<dyn Error>> {
        println!("Databases:");
        Ok(for name in self.client.list_database_names(None, None).await? {
            println!("- {}", name);
        })
    }
}
