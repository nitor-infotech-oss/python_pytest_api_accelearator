from pytest_practical.tests.utils import common
import logging
from pytest_practical.helper.db_helpers import db_helpers

logger = logging.getLogger("root")


class coupons(object):
    """
        This Class is used as coupon utility.
    """

    def __init__(self):
        self.expected_discount_type = ''
        self.new_coupon_info = ''
        self.db_helper = db_helpers()

    def get_coupon_by_id(self, coupon_id):
        """
        This function is used to return the coupon by coupon id from the DataBase.
        """

        sql = 'SELECT * FROM local.wp_posts where ID = {} AND post_type = "shop_coupon";'.format(coupon_id)

        return self.db_helper.execute_select(sql)

    def create_coupon(self, discount_type=None, amount=None):
        """
        This function is used to create a coupon using api call.
        """
        data = {
            "code": common.generate_random_coupon_code(),
        }

        if discount_type.lower() is not None:
            self.expected_discount_type = discount_type
            data["discount_type"] = discount_type
            data["amount"] = str(amount)

        else:
            self.expected_discount_type = 'fixed_cart'
            data["amount"] = str(amount)

        response_api = common.create_coupon(data)
        try:
            logger.info("Coupon created with coupon id : {} and code : {}".format(response_api['id'], response_api['code']))
            self.new_coupon_info = response_api
        except TypeError:
            pass

    def check_coupon_in_db(self, coupon_id):
        """
        This function is used to check for a coupon by coupon code in DataBase.
        """
        db_coupon = self.get_coupon_by_id(coupon_id)
        assert db_coupon, 'Coupon not found in DB, Coupon ID: {}'.format(coupon_id)
