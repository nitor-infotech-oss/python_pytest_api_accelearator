"""
This file consist of test related to the failed and skipped cases.
"""
import pytest
from pytest_practical.tests.utils.coupon_util import coupons


class Test_skip_fail:
    """
    This test is marked as skip to display skipped tests in the pytest html-report.
    """

    @pytest.mark.skip(reason="To Display skipped test in reports")
    def test_this_is_skipped(self):
        self.coupons = coupons()

    @pytest.mark.parametrize('coupon_id', [10001])
    def test_check_coupon_exist_failed(self, coupon_id, setup):
        self.coupons.check_coupon_in_db(coupon_id=coupon_id)


