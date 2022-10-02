use std::error::Error;

use bson::doc;
use mongodb::Collection;

use super::Db;

impl Db {
    pub async fn add_support_group(
        &self,
        user_id: i64,
        support_group: String,
    ) -> Result<(), Box<dyn Error>> {
        let collection: Collection<bson::Document> = self.db.collection("maintainer");
        let filter: bson::Document = doc! { "user_id": user_id, "is_maintainer": true };
        let found_col: Option<bson::Document> = collection.find_one(filter.clone(), None).await?;

        if found_col != None {
            log::info!("Adding support group");
            let update = doc! { "$set": { "support_group": support_group } };
            collection.update_one(filter.clone(), update, None).await?;
        } else {
            log::error!("User is not a maintainer");
        }
        Ok(())
    }
}