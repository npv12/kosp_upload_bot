use bson::doc;
use mongodb::Collection;
use std::error::Error;

use super::Db;

impl Db {
    pub async fn add_maintainer(
        &self,
        maintainer: String,
        user_id: i64,
        device: String,
    ) -> Result<(), Box<dyn Error>> {
        let is_admin = self.is_admin(user_id).await?;
        if !is_admin {
            log::error!("User is not an admin");
            return Ok(());
        }
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

    pub async fn remove_maintainer(&self, user_id: i64) -> Result<(), Box<dyn Error>> {
        let is_admin = self.is_admin(user_id).await?;
        if !is_admin {
            log::error!("User is not an admin");
            return Ok(());
        }
        let collection: Collection<bson::Document> = self.db.collection("maintainer");
        let filter: bson::Document = doc! { "user_id": user_id };
        let found_col = collection.find_one(filter.clone(), None).await?;

        if found_col != None {
            log::info!("Removing the user");
            collection.delete_one(filter.clone(), None).await?;
        } else {
            log::error!("User is not a maintainer");
        }
        Ok(())
    }

    pub async fn is_maintainer(
        &self,
        user_id: i64,
        device_name: &str,
    ) -> Result<bool, Box<dyn Error>> {
        let collection: Collection<bson::Document> = self.db.collection("maintainer");
        let filter: bson::Document = doc! { "user_id": user_id, "is_maintainer": true };
        let found_col: Option<bson::Document> = collection.find_one(filter.clone(), None).await?;

        if found_col != None {
            let data = found_col.unwrap();
            let devices = data.get_array("devices").unwrap();
            for device in devices {
                if device.as_str().unwrap() == device_name {
                    return Ok(true);
                }
            }
        }
        return Ok(false);
    }
}
