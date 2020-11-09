"""
This file consist of test related to the Coupon.
"""
import pytest
from pytest_practical.tests.utils.coupon_util import coupons


@pytest.mark.api
@pytest.mark.couponapi
class Test_coupon_api:
    """
    This test class consist of test cases:

    1. test_create_coupon : to create a coupon using API.
    2. test_check_coupon_exist : to check if the coupon exist in the DataBase
    """

    @pytest.fixture(autouse=True)
    def class_setup(self, setup):
        self.coupons = coupons()

    @pytest.mark.parametrize('discount_type,amount', [("percent", 40), ("fixed_cart", 100)])
    @pytest.mark.run(order=1)
    def test_create_coupon(self, discount_type, amount, setup):
        self.coupons.create_coupon(discount_type=discount_type, amount=amount)

    """
    This test is marked as xfail to display unexpected passes and expected fails in the pytest html-report.
    """
    @pytest.mark.xfail(reason="Failed to create coupon")
    @pytest.mark.parametrize('coupon_id', [10001, 101, 117, 124])
    @pytest.mark.run(order=1)
    def test_check_coupon_exist(self, coupon_id, setup):
        self.coupons.check_coupon_in_db(coupon_id=coupon_id)


