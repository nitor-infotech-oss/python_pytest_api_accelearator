"""
This is the common util file
"""
from faker import Faker
from pytest_practical.helper.api_helpers import woo_request_helper

fake = Faker()


def generate_random_email_and_password():
    """
    Function to generate random email id and password
    """
    email = fake.email()

    password_string = fake.password()

    random_info = {
        'email': email,
        'password': password_string
    }
    return random_info


def generate_random_coupon_code(suffix=None):
    """
    This function generates random coupon codes
    """
    code = fake.password(length=8, special_chars=False, digits=True, upper_case=True, lower_case=False)
    if suffix:
        code += suffix

    return code


def create_coupon(data):
    """
    This function is used to create a coupon using API call.
    """
    return woo_request_helper().post_details('coupons', data, expected_status_code=201)


def list_all_products():
    """
    This function returns the list of all products from the API.
    """
    all_products = []
    max_pages = 1000
    page_num = 1
    while page_num < max_pages:

        param = {
            'per_page': 100,
            'page': page_num,
        }
        rs_api = woo_request_helper().get_details(wc_endpoint='products', params=param)

        if rs_api:
            page_num += 1
            all_products.extend(rs_api)
        else:
            break

    return all_products


def get_products_by_id(product_id):
    """
    This function is used to get the product by product id using API call.
    """
    rs_api = woo_request_helper().get_details(wc_endpoint='products/{}'.format(product_id))
    return rs_api


def update_random_product_price(product_id, data):
    """
    This function is used to update the product by product id and data to update
    using the API call.
    """
    return woo_request_helper().put_details(wc_endpoint='products/{}'.format(product_id), params=data)


def create_user(data):
    """
    This function is used to create the user by user data using API call.
    """
    return woo_request_helper().post_details(wc_endpoint='customers', params=data)


def delete_user_by_id(user_id):
    """
    This function is used to delete the user by user id using API call.
    """
    return woo_request_helper().delete_details(wc_endpoint='customers/{}'.format(user_id))
