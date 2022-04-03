from bot.database import init
from bot.utils.logging import logger


class MaintainerDetails:

    def __init__(self):
        logger.info("Initializing Maintainer Details")
        self.maintainer_db = init()["maintainer"]

    #Check if user is a maintainer or not
    def is_maintainer(self, user_id):
        logger.info(f"Checking if user {user_id} is a maintainer")
        get_user = self.maintainer_db.find_one({"user_id": user_id})

        #User is new to the database
        if get_user is None:
            logger.info(f"user {user_id} not found in maintainer database")
            return False
        elif get_user["is_maintainer"]:
            logger.info(f"user {user_id} is a maintainer")
            return True
        else:
            logger.info(f"user {user_id} is a not a maintainer")
            return False

    #Add a maintainer
    def add_maintainer(self, user_id: int, device: str):
        logger.info(f"Adding user {user_id} to maintainer database")
        if self.is_maintainer(user_id):
            logger.info(f"User {user_id} is already a maintainer")
            return False
        else:
            self.pm_permit_db.insert_one({
                "user_id": user_id,
                "is_maintainer": False,
                "is_admin": False,
                "device": device,
            })
            return True

    #Remove a maintainer
    def remove_maintainer(self, user_id):
        logger.info(f"Removing user {user_id} from maintainer database")
        if not self.is_maintainer(user_id):
            logger.info(f"User {user_id} is not a maintainer")
            return False
        else:
            self.maintainer_db.delete_one({"user_id": user_id})
            return True

    # is an admin
    def is_admin(self, user_id):
        logger.info(f"Checking if user {user_id} is an admin")
        get_user = self.maintainer_db.find_one({"user_id": user_id})

        #User is new to the database
        if get_user is None:
            logger.info(f"user {user_id} not found in maintainer database")
            return False
        elif get_user["is_admin"]:
            logger.info(f"user {user_id} is an admin")
            return True
        else:
            logger.info(f"user {user_id} is a not an admin")
            return False

    # Add an admin
    def add_admin(self, user_id):
        logger.info(f"Adding user {user_id} to admin database")
        if self.is_admin(user_id):
            logger.info(f"User {user_id} is already an admin")
            return False
        else:
            self.maintainer_db.update_one({"user_id": user_id},
                                          {"$set": {
                                              "is_admin": True
                                          }})
            return True


maintainer_details = MaintainerDetails()