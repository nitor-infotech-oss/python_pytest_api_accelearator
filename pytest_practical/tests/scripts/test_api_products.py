"""c
This file consist of test related to the Products.
"""
import pytest
from pytest_practical.tests.utils.product_util import products


@pytest.mark.api
@pytest.mark.productapi
class Test_product_api:
    """
    This Test class consist of test cases:

    1. test_get_all_products_from_api : to get number of all the products from API.
    2. test_get_product_by_id : to get product by product ID.
    3. test_get_random_products_from_api : to get random products from the API.

    """

    @pytest.fixture(autouse=True)
    def class_setup(self, setup):
        self.products = products()

    @pytest.mark.run(order=1)
    def test_get_all_products_from_api(self):
        self.products.get_all_products_api()

    @pytest.mark.run(order=2)
    @pytest.mark.parametrize("product_id", ["34", "35"])
    def test_get_product_by_id(self, product_id):
        self.products.get_product_by_id(product_id)

    @pytest.mark.run(order=3)
    @pytest.mark.parametrize("qty", [6])
    def test_get_random_products_from_api(self, qty):
        self.products.get_random_products_by_qty(qty)
