from bot.database import init
from bot.utils.logging import logger


class MaintainerDetails:

    def __init__(self):
        logger.info("Initializing Maintainer Details")
        self.maintainer_db = init()["maintainer"]

    #Check if user is a maintainer or not
    def is_maintainer(self, user_id) -> bool:
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
    def add_maintainer(self, requested_id: int, user_id: int, name: str,
                       device: str) -> bool:
        logger.info(
            f"Adding user {user_id} to maintainer database since {requested_id} requested it"
        )

        if not self.is_admin(requested_id):
            logger.info(f"User {requested_id} is not an admin")
            return False

        if self.is_maintainer(user_id):
            logger.info(f"User {user_id} is already a maintainer")
            if device in self.get_devices(user_id):
                logger.info(f"User {user_id} already has {device}")
                return False
            else:
                logger.info(f"Adding {device} to user {user_id}")
                self.maintainer_db.update_one({"user_id": user_id},
                                              {"$push": {
                                                  "device": device
                                              }})
                return True
        else:
            self.maintainer_db.insert_one({
                "user_id": user_id,
                "name": name,
                "is_maintainer": True,
                "is_admin": False,
                "device": [device],
                "support_group": ""
            })
            logger.info("Added the user to a maintainer")
            return True

    #Remove a maintainer
    def remove_maintainer(self, user_id) -> bool:
        logger.info(f"Removing user {user_id} from maintainer database")
        if not self.is_maintainer(user_id):
            logger.info(f"User {user_id} is not a maintainer")
            return False
        else:
            self.maintainer_db.delete_one({"user_id": user_id})
            return True

    # is an admin
    def is_admin(self, user_id: int) -> bool:
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
    def add_admin(self, requester_id: int, user_id: int) -> bool:
        logger.info(
            f"Adding user {user_id} to admin database since {requester_id} requested it"
        )

        if not self.is_admin(requester_id):
            logger.info(f"User {requester_id} is not an admin")
            return False

        if self.is_admin(user_id):
            logger.info(f"User {user_id} is already an admin")
            return False
        else:
            logger.info("Promoting the user to admin status")
            self.maintainer_db.update_one({"user_id": user_id},
                                          {"$set": {
                                              "is_admin": True
                                          }})
            return True

    # Get devicrs
    def get_devices(self, user_id: int) -> list:
        logger.info(f"Getting devices for user {user_id}")
        get_user = self.maintainer_db.find_one({"user_id": user_id})

        #User is new to the database
        if get_user is None:
            logger.info(f"user {user_id} not found in maintainer database")
            return False
        else:
            logger.info(f"user {user_id} is a maintainer")
            return get_user["device"]


maintainer_details = MaintainerDetails()