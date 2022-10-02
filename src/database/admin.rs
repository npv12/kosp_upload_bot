use bson::doc;
use mongodb::Collection;
use std::error::Error;

use super::Db;

impl Db {
    pub async fn promote_admin(
        &self,
        user_id: i64,
    ) -> Result<(), Box<dyn Error>> {
        let collection: Collection<bson::Document> = self.db.collection("maintainer");
        let filter: bson::Document = doc! { "user_id": user_id };
        let found_col: Option<bson::Document> = collection.find_one(filter.clone(), None).await?;

        if found_col != None {
            log::info!("Promoting the user");
            let update = doc! { "$set": { "is_admin": true } };
            collection.update_one(filter.clone(), update, None).await?;
        } else {
            log::error!("User is not a maintainer");
        }
        Ok(())
    }
}
