use std::error::Error;

use bson::doc;

use super::Db;

impl Db {
    pub async fn add_maintainer(&self, maintainer: String, user_id: i64, device: String) -> Result<(), Box<dyn Error>> {
        let collection = self.db.collection("maintainer");
        let doc = doc! {
            "name": maintainer,
            "user_id": user_id,
            "is_maintainer": true,
            "is_admin": false,
            "devices": [device],
            "support_group": ""
        };
        collection.insert_one(doc, None).await?;
        Ok(())
    }
}