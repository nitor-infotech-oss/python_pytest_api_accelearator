"""
This module provides an Excel like interface for Google Sheets.
"""
import os
import logging
import argparse
from googleapiclient import discovery
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials

logger = logging.getLogger("root")


class Workbook(object):
    """
     This class implements the functionality to interface with the Google Sheet.

     TBD: Currently the methods to interface with sheets are also defined in this class.
     Ideally this should be moved to the Worksheet class. This will avoid passing the sheet name
     every time.
     The sheet object will be created once a particular sheet is requested for.

    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--env', default='qa')
    args = parser.parse_args()

    __SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    __CONFIG_FILE = os.path.dirname(os.getcwd()) + '\\config\\' + args.env
    __GOOGLE_CONFIG_FILE = os.path.abspath(os.path.join(os.path.dirname(__CONFIG_FILE), 'google_config.json'))
    __SA_GOOGLE_CONFIG_FILE = os.path.abspath(os.path.join(os.path.dirname(__CONFIG_FILE), 'google_config.json'))
    __APPLICATION_NAME = 'Reusable'
    __VALUE_INPUT_OPTION = 'RAW'
    __NUM_RETRIES = 500

    def __init__(self, spreadsheet_id, discovery_url=None, client_cert_file=None, include_grid_data=False):
        logger.info("__GOOGLE_CONFIG_FILE:" + self.__GOOGLE_CONFIG_FILE)
        self.discovery_url = discovery_url
        self.spreadsheet_id = spreadsheet_id

        # GOOGLE_SHEETS_JENKINS_API_FILE is a Jenkins only environment variable.
        # It points to the location of the json file contains the auth tokens.
        # If you ever have to update this file, follow these steps:
        # 1) Select the pulldown under google-sheets-api.json and select "update".
        # 2) You will have the option of uploading a new file.
        self.jenkins_auth_file = os.environ.get("GOOGLE_SHEETS_JENKINS_API_FILE")

        # If that env var exists, use it to authenticate:
        if self.jenkins_auth_file:
            # ...then the system should have the authorization key file: jenkins_auth_file
            logger.info("...Running on Jenkins...")
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                self.jenkins_auth_file, scopes=self.__SCOPES)
        else:
            # ...otherwise start OAuth flow.
            logger.info("...Running on local machine...")
            credentials = self.__get_credentials()
            if client_cert_file:
                self.client_cert_file = client_cert_file
            else:
                self.client_cert_file = Workbook.__GOOGLE_CONFIG_FILE

        self.include_grid_data = include_grid_data
        self.service = discovery.build('sheets', 'v4', credentials=credentials, cache_discovery=False)

    def get_sheet_names(self):
        """
        This method returns a list of all the sheet with its properties defined in the Workbook
        :return:
        """
        response = self.service.spreadsheets().get(
            spreadsheetId=self.spreadsheet_id,
            includeGridData=self.include_grid_data).execute(num_retries=self.__NUM_RETRIES)
        logger.debug("Request to GoogleSheet")

        return response['sheets']

    def get_sheet_index(self, sheet_name):
        """
        This method returns the Index of the Sheet identified by name. The Sheet might be required
        in cases where the Google API Method can only access the Sheet contents by id/index and
        not name.

        :param sheet_name: Name of the sheet
        :return: Index of the Sheet identified by name
        :rtype: integer
        """
        sheet_props = self.get_sheet_names()
        for sheet in sheet_props:
            if str(sheet_name) == str(sheet['properties']['title']):
                return sheet['properties']['index']

    def get_row_values(self, sheet_name, row_num=None):
        """
        This method returns a list of values in that row number. If row_num is not passed all
        rows are returned.

        :param sheet_name: Name of the sheet
        :param row_num: The row number for which the values will be returned
        :return: list of values in that row number
        :rtype: list
        """
        if row_num is None:
            response = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range='{0}!A:ZZ'.format(sheet_name)).execute(num_retries=self.__NUM_RETRIES)

            logger.debug("Request to GoogleSheet")
        else:
            response = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range='{0}!A{1}:ZZ{1}'.format(
                    sheet_name, row_num)).execute(num_retries=self.__NUM_RETRIES)

            logger.debug("Request to GoogleSheet")

        return response['values']

    def get_column_value(self, sheet_name, col_num=None):
        """
        This method will return the values in a specific column
        :param sheet_name:
        :param col_num:
        :return:
        """
        response = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range='{0}!{1}'.format(sheet_name, col_num)).execute(num_retries=self.__NUM_RETRIES)
        logger.debug("Request to GoogleSheet")

        if "values" in response:
            return response['values']
        else:
            return False

    def nrows(self, sheet_name):
        """
        This method return the maximum number of rows in the sheet
        :param sheet_name: Name of the sheet
        :return: number of rows
        :rtype: integer
        """
        sheet_props = self.get_sheet_names()
        for sheet in sheet_props:
            if str(sheet['properties']['title']) == str(sheet_name):
                return sheet['properties']['gridProperties']['rowCount']

    def ncols(self, sheet_name):
        """
        This method returns the maximum number of columns in the sheet
        :param sheet_name: Name of the sheet
        :return: number of columns
        :rtype: integer
        """
        sheet_props = self.get_sheet_names()
        for sheet in sheet_props:
            if str(sheet['properties']['title']) == str(sheet_name):
                return sheet['properties']['gridProperties']['columnCount']

    def create_new_sheet(self, sheet_name):
        """
        Creates a new sheet named <sheet_name> if it doesn't already exist and returns the new
        sheet's sheetId for later use
        :param sheet_name: Name of the new sheet to be created
        :return: The ID of the sheet
        :rtype: integer
        """

        requests = []
        requests.append({
            'addSheet': {
                'properties': {
                    'title': sheet_name
                }
            },
        })

        body = {
            'requests': requests,
        }

        sheet_id = ""
        try:
            logger.debug("Request to GoogleSheet")
            response = self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=body).execute(num_retries=self.__NUM_RETRIES)

            sheet_id = response['replies'][0]['addSheet']['properties']['sheetId']
        except Exception as e:
            logger.error(e.message)

        return sheet_id

    def write_to_cell(self, sheet_name, cell_name, value):
        """
        This method writes a single value in a cell in the sheet.
        :param sheet_name: The Name of the sheet in which value needs to be written
        :param cell_name: The Name of the Cell e.g. A-Z{N} notation
        :param value: The Value of the Cell.
        """

        body = {'values': [[value]]}

        self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range='{0}!{1}'.format(sheet_name, cell_name),
            body=body,
            valueInputOption=Workbook.__VALUE_INPUT_OPTION).execute(num_retries=self.__NUM_RETRIES)

        logger.debug("Request to GoogleSheet")

    def append_cell(self, sheet_name, cell_location, cell_value):
        """
        Functionality TBD
        :param sheet_name:
        :param cell_location:
        :param cell_value:
        :return:
        """
        body = {'values': [cell_value]}

        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range='{0}!{1}'.format(sheet_name, cell_location),
            body=body,
            valueInputOption=Workbook.__VALUE_INPUT_OPTION).execute(num_retries=self.__NUM_RETRIES)

        logger.debug('{0} cells appended.'.format(result.get('updates').get('updatedCells')))

    def append_rows(self, sheet_name, starting_cells, row_values):
        """
        Functionality TBD
        :param sheet_name:
        :param starting_cells:
        :param row_values:
        :return:
        """
        body = {'values': [row_values]}

        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range='{0}!{1}'.format(sheet_name, starting_cells),
            body=body,
            valueInputOption=Workbook.__VALUE_INPUT_OPTION).execute(num_retries=self.__NUM_RETRIES)

        logger.debug("{0} cells appended.".format(result.get('updates').get('updatedCells')))

    def write_to_sheet(self, sheet_name, values):
        """
        This function batch writes values[] to a specific sheet (<sheet_name>)
        :param sheet_name:
        :param values:
        :return:
        """
        # The data will be written starting on the first cell (A1) on sheet
        # named <sheet_name>
        range_values = '{}!A1'.format(sheet_name)

        # Create a new sheet named <sheet_name> on the worksheet if it doesn't
        # exist
        if not self.get_sheet_id(sheet_name):
            self.spreadsheet_id = self.create_new_sheet(sheet_name=sheet_name)
        else:
            self.spreadsheet_id = self.get_sheet_id(sheet_name)

        data = {
            'range': range_values,
            'values': values,

        }
        body = {
            'value_input_option': Workbook.__VALUE_INPUT_OPTION,
            'data': data,

        }
        request = self.service.spreadsheets().values().batchUpdate(
            spreadsheetId=self.spreadsheet_id, body=body)
        request.execute(num_retries=self.__NUM_RETRIES)
        logger.debug("Request to GoogleSheet")
        self.format_sheet_column_width(sheet_name)

    def get_sheet_id(self, sheet_name):
        """
        This method returns the property sheetId for the sheet name.
        :param sheet_name: The Name of the Sheet for which the sheetId is required
        :return:
        """
        all_sheets = self.get_sheet_names()
        for sheet in all_sheets:
            if str(sheet['properties']['title']) == str(sheet_name):
                return sheet['properties']['sheetId']

    def format_sheet_column_width(self, sheet_name):
        """
        Automatically resize column width based on cell content of the specific sheet
        :param sheet_name:
        :return:
        """
        # Get Sheet ID of the sheet by name
        requests = []
        requests.append({
            'autoResizeDimensions': {
                'dimensions': {
                    'sheetId': self.get_sheet_id(sheet_name=sheet_name),
                    'dimension': 'COLUMNS',
                }

            }
        })

        body = {
            'requests': requests,
        }

        try:
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=body).execute(num_retries=self.__NUM_RETRIES)

            logger.debug("Request to GoogleSheet")
        except Exception as e:
            logger.error(e.message)

    def insert_blank_row(self, sheet_name, starting_row):
        """
        Automatically resize column width based on cell content of the specific sheet
        :param sheet_name:
        :param starting_row:
        :return:
        """
        # Get Sheet ID of the sheet by name
        requests = []
        requests.append({
            "insertDimension": {
                "range": {
                    "sheetId": self.get_sheet_id(sheet_name=sheet_name),
                    "dimension": "ROWS",
                    "startIndex": starting_row - 1,
                    "endIndex": starting_row
                },
                "inheritFromBefore": "false"
            }
        }, )

        body = {
            'requests': requests,
        }

        try:
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=body).execute(num_retries=self.__NUM_RETRIES)

            logger.debug("Request to GoogleSheet")
        except Exception as e:
            logger.error(e.message)

    def __get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')

        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'sheets.googleapis.com-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                self.__SA_GOOGLE_CONFIG_FILE, scopes=self.__SCOPES)
            logger.info('Storing credentials to ' + credential_path)
        return credentials
