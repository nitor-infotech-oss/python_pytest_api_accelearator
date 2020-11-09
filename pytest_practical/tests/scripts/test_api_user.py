"""
This file consist of test related to the Users.
"""
import pytest
from pytest_practical.tests.utils.user_util import users


@pytest.mark.api
@pytest.mark.userapi
class Test_user_api:
    """
    This Test class consist of test cases:

    1. test_create_user : to create a user in API by google sheet data.
    2. test_create_user_with_json_data : to create a user in API by json file data.
    3. test_delete_user : to delete a user in API by google sheet data.

    """

    @pytest.fixture(autouse=True)
    def class_setup(self, setup):
        self.users = users()
        self.filename = self.directory + '\\python_pytest_api.json'

    @pytest.mark.run(order=1)
    @pytest.mark.parametrize('user', ["wjones", "gsmith", "vfisher", "breannasharp"])
    def test_create_user(self, user):
        self.users.create_user_by_gsheet(user=user)

    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('user', ["test_user", "dishant", "ysmith"])
    def test_create_user_with_json_data(self, user):
        self.users.create_user_by_json(file_name=self.filename, user=user)

    @pytest.mark.run(order=3)
    @pytest.mark.parametrize('username', ["ysmith"])
    def test_delete_user(self, username):
        self.users.delete_user_by_gsheet(username=username)
        self.users.verify_user_deleted_by_gsheet(username=username)
