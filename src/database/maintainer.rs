use bson::doc;
use std::error::Error;

use super::Db;

impl Db {
    pub async fn add_maintainer(
        &self,
        maintainer: String,
        user_id: i64,
        device: String,
    ) -> Result<(), Box<dyn Error>> {
        let collection = self.db.collection("maintainer");
        let filter = doc! { "user_id": user_id };
        let found_col = collection.find_one(filter.clone(), None).await?;

        if found_col != None {
            log::warn!("User is already a maintainer. So, adding device to the list");
            let update = doc! { "$push": { "devices": device } };
            collection.update_one(filter.clone(), update, None).await?;
        } else {
            log::warn!("User is not a maintainer. So, adding user to the list");
            let doc = doc! {
                "name": maintainer,
                "user_id": user_id,
                "is_maintainer": true,
                "is_admin": false,
                "devices": [device],
                "support_group": ""
            };
            collection.insert_one(doc, None).await?;
        }
        Ok(())
    }
}
