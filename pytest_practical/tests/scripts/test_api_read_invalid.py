"""
This file consist of test related to the error cases.
"""
import pytest


class Test_read_invalid_data:
    """
    This test reads invalid-data to display error tests in the pytest html-report.
    """

    @pytest.yield_fixture(scope="class")
    def read_invalid_file(self):
        """
        This function is used as a fixture to read invalid file.

        in pytest 2.4 and above, we yield is used instead of return statement
        to provide a fixture value while otherwise fully supporting all other fixture features.
        """
        f = open("demofile.txt", "r")
        f.read()

        yield f.close()

    def test_this_is_error(self, read_invalid_file):
        pass
