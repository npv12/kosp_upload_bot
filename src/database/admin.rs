use bson::doc;
use mongodb::Collection;
use std::error::Error;

use super::Db;

impl Db {
    pub async fn promote_admin(
        &self,
        user_id: i64,
    ) -> Result<(), Box<dyn Error>> {
        let is_admin =  self.is_admin(user_id).await?;
        if !is_admin {
            log::error!("User is not an admin");
            return Ok(());
        }
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

    pub async fn is_admin(
        &self,
        user_id: i64,
    ) -> Result<bool, Box<dyn Error>> {
        let collection: Collection<bson::Document> = self.db.collection("maintainer");
        let filter: bson::Document = doc! { "user_id": user_id, "is_admin": true };

        if collection.find_one(filter.clone(), None).await? != None {
            return Ok(true);
        } else {
            return Ok(false);
        }
    }
}
