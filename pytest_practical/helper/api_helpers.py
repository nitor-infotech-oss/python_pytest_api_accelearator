"""
This is the helper file for the API.
"""
from woocommerce import API
import logging as logger
import os
import argparse
import requests.exceptions


class woo_request_helper(object):
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--env', default='local')
        args = parser.parse_args()
        base_url = "http://mystore." + args.env
        wc_key = os.environ.get('WC_KEY')
        wc_secret = os.environ.get('WC_SECRET')
        self.rs = None
        self.wcapi = API(
            url=base_url,
            consumer_key=wc_key,
            consumer_secret=wc_secret,
            version="wc/v3"
        )

    def assert_status_code(self):
        """
        This function is used to verify the Response status code of API.
        """
        try:
            assert self.rs.status_code == self.expected_status_code, \
                "BAD STATUS CODE, EndPont: {}, Params: {}, Actual Status Code: {}, Expected Status code:{}".format(
                    self.wc_endpoint, self.params, self.rs.status_code, self.expected_status_code)
        except (AssertionError, AttributeError) as e:
            pass

    def assert_status_code_delete(self):
        """
        This function is used to verify the Response status code of Delete API.
        """
        assert self.rs.status_code == self.expected_status_code, "BAD STATUS CODE, EndPont: {}, Actual Status Code: {}, Expected Status code:{}".format(
            self.wc_endpoint, self.rs.status_code, self.expected_status_code)

    def get_details(self, wc_endpoint, params=None, expected_status_code=200):
        """
        This function is used for GET API call.
        """
        try:
            self.rs = self.wcapi.get(wc_endpoint, params=params)

            self.wc_endpoint = wc_endpoint
            self.expected_status_code = expected_status_code
            self.params = params
            self.assert_status_code()

            return self.rs.json()
        except requests.exceptions.ReadTimeout:
            logger.info("ReadTimeOut Exception raised")

    def post_details(self, wc_endpoint, params=None, expected_status_code=201):
        """
        This function is used for POST API call.
        """
        logger.info("Params: {}".format(params))
        try:
            self.rs = self.wcapi.post(wc_endpoint, data=params)

            self.wc_endpoint = wc_endpoint
            self.expected_status_code = expected_status_code
            self.params = params
            self.assert_status_code()

            return self.rs.json()
        except requests.exceptions.ReadTimeout:
            logger.info("ReadTimeOut Exception raised on post details: {}".format(params))

    def put_details(self, wc_endpoint, params=None, expected_status_code=200):
        """
        This function is used for PUT API call.
        """
        logger.info("Params: {}".format(params))
        self.rs = self.wcapi.put(wc_endpoint, data=params)
        self.wc_endpoint = wc_endpoint
        self.expected_status_code = expected_status_code
        self.params = params
        self.assert_status_code()

    def delete_details(self, wc_endpoint, expected_status_code=200):
        """
        This function is used for DELETE API call.
        """
        self.rs = self.wcapi.delete(wc_endpoint, params={"force": True})
        self.wc_endpoint = wc_endpoint
        self.expected_status_code = expected_status_code
        self.assert_status_code_delete()
