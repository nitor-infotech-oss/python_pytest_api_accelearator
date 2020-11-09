from pytest_practical.tests.utils import common
from pytest_practical.helper.db_helpers import db_helpers
from pytest_practical.data_providers.data_provider import DataProvider
from pytest_practical.data_providers import json_parser
from pytest_practical.data_providers import excel_util
import os
import logging

logger = logging.getLogger("root")


class users(object):
    """
    This Class is used for API operations on users.
    """

    def __init__(self):
        self.db_helper = db_helpers()
        self.user_id = None

    def get_user_by_email(self, email):
        """
        This function is used to get the user by email id from DataBase.
        """
        sql = "SELECT * FROM local.wp_users where user_email = '{}';".format(email)
        return self.db_helper.execute_select(sql)

    def get_random_user(self):
        """
        This function is used to get random used from DataBase.
        """
        sql = "SELECT * FROM local.wp_users WHERE ID > 3 ORDER BY RAND() limit 1;"
        return self.db_helper.execute_select(sql)

    def get_user_by_username(self, username):
        """
        This function is used to get user by username from DataBase.

        """
        sql = "SELECT * FROM local.wp_users where user_login = '{}';".format(username)
        return self.db_helper.execute_select(sql)

    # ------------------------------------------------Google Sheet-----------------------------------------------------#

    def create_user_by_gsheet(self, user):
        """
        This function is used to create a user from google sheet data.
        """
        google_sheet_id = '1KWXC8u1baB_zl_JhC4BJiKL1JZTbB_uDljaIbx4FCNM'
        google_sheet = DataProvider(google_sheet_id=google_sheet_id)
        user_data = google_sheet.read_google_sheet_create_customer_api(user=user)
        payload = {
            'email': user_data['email'],
            'password': user_data['password']
        }

        try:
            create_user_response = common.create_user(data=payload)

            if self.get_user_by_email(user_data['email']) is not None:
                logger.info("\nUser Created Successfully")
            else:
                logger.info("\n UserCreation failed")

            logger.info("\nUser ID: {}".format(create_user_response['id']))
            logger.info("\nUser Email: {}".format(create_user_response['email']))
            logger.info("\nUsername: {}".format(create_user_response['username']))

        except:
            logger.info("\nUser Already Exists !")

    def delete_user_by_gsheet(self, username):
        """
        This function is used to delete a user by google sheet data.
        """
        google_sheet_id = '1KWXC8u1baB_zl_JhC4BJiKL1JZTbB_uDljaIbx4FCNM'
        google_sheet = DataProvider(google_sheet_id=google_sheet_id)

        user_to_delete = google_sheet.read_google_sheet_delete_customer_api(username=username)
        user_data = self.get_user_by_email(email=user_to_delete['user_email'])

        try:
            self.user_id = user_data[0]['ID']
            user_email = user_data[0]['user_email']
            logger.info("USER DELETED: ")
            logger.info("USER ID: {}".format(str(self.user_id)))
            logger.info("USERNAME {}".format(username))
            logger.info("USER EMAIL {}".format(user_email))

            return common.delete_user_by_id(user_id=self.user_id)

        except:
            logger.info("User {} Deleted or does not Exist!".format(username))

    def verify_user_deleted_by_gsheet(self, username):
        """
        This function is used to verify the user is deleted by google sheet data.
        :param username:
        :return:
        """
        try:
            return common.delete_user_by_id(user_id=self.user_id)
        except:
            logger.info("\n\t\tUser {} Deleted or does not Exist!".format(username))

    # -------------------------------------------------------JSON------------------------------------------------------#
    def create_user_by_json(self, user, file_name):
        """
        This function is used to create a user from JSON data.
        """
        user_data = json_parser.read_json_by_key(inputfile=file_name, key=user)
        print user_data
        payload = {
            'email': user_data['email'],
            'password': user_data['password']
        }

        try:
            create_user_response = common.create_user(data=payload)

            if self.get_user_by_email(user_data['email']) is not None:
                logger.info("\nUser Created Successfully")
            else:
                logger.info("\n UserCreation failed")

            logger.info("\nUser ID: {}".format(create_user_response['id']))
            logger.info("\nUser Email: {}".format(create_user_response['email']))
            logger.info("\nUsername: {}".format(create_user_response['username']))

        except:
            logger.info("\nUser Already Exists !")
