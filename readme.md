## Pytest API Testing Accelerator

<br/>

>### This solution/accelerator helps in automating API scenarios in python using Pytest Framework. This will help in automating complex functional scenarios and can be executed on different environments as per the requirement. This solution supports different data parsers such as google sheets, excel, csv, json. This solution supports parallel and sequential execution and after completion of execution the standard html reports are available.


<br />

### Folder structure
    src
    |- readme.md
    |- requirements.txt
    |- config
        |-- ...                  
    |- data_providers
        |-- ...
    |- logs
        |-- ...               
    |- tests
        |-- scripts
            |--- ...
        |-- utils
            |--- ...
 
- **`Tests`:** under 'Scripts' keep all test cases implementation files with .py extension.
- **`Testdata`:** keep respective environment Test data here, Test data can be in the form of json, csv or excel. 
- **`Config`:** keep config files here such as db_config and google_config and in respective config file you can keep configurations as per the environment.
- **`Utils`:** keep Project utility files here .
- **`Helper`:** keep Common helper files here such as api_helper, db_helper etc.
- **`Data_providers`:** keep all the Data Provider implementation files in .py extension such as csv, json, excel, google sheet etc.

### Dependencies
-   please use Python version 2.7x and above.
-   pytest 4.6.11
-   WooCommerce 2.1.1
- 	PyMySQL 0.10.0
-   Faker 3.0.1
-   configparser 4.0.2
-   parse 1.17.0
-   xlrd 1.2.0
-   pymongo 3.11.0
- **`To use google-sheets, please install the given below packages:`**
  -   google-api-core 1.22.1
  -   google-api-python-client 1.11.0
  -   google-auth 1.21.1
  -   google-auth-httplib2 0.0.4
  -   httplib2 0.18.1
  -   oauth2client 4.1.3


### Prerequisite
- To execute the test cases, we would need to setup the website on our local machine, please refer to the document:<br />```Setup Application Under Test Locally.docx```

- To use google sheets in your project, follow the instructions given below:
  - In the folder src/config, go to google_config.json file and change the values for the following parameters:
    - project_id
    - private_key_id
    - private_key
    - client_email
    - client_id
    - client_x509_cert_url
  - Go to url ```https://console.cloud.google.com/home/dashboard``` <br /> and perform the below steps:
    - Login with your google account and create a new project.
    - Than enable search for the Sheets API on the url : ```https://console.cloud.google.com/apis/library``` and enable it.
    - Go to the url ```https://console.cloud.google.com/apis/credentials``` and create a service account key by clicking on `+ Create Creadentials > Service account`
    - Give the name and manage the permissions and click on done.
    - Visit the url ```https://console.cloud.google.com/iam-admin/serviceaccounts``` and click on the dots in actions and click on edit.
    - Under the Keys tab, click on `Add keys` and than get all the details from the page and replace the same in file `google_config.json`.<br/>  


- Download dependencies by using the following command: <br />`pip install -r requirements.txt`
- Copy the file ```sheets.googleapis.com-python-quickstart.json``` file from project root folder to ```C://users/{username}/.credentials``` folder.

### Config Parameters
- The base url of API is configurable and can be configured in `api_helper.py` in `Helper` folder.
- Database credentials and port are configurable and can be configured in `db_config.json` in `Config` folder.
- Google Sheets data are configurable and can be configured in `google_config.json` in `Config` folder.
- The Consumer Key and Consumer Secret is used as the credentials to connect to REST API and is added in system environment of the machine and is used in `api_helper.py` file. 


### Running Tests

- ### Execution from Pycharm IDE : To execute the tests from Pycharm IDE
  -   Navigate to `src\tests\scripts` in the project.
  -   All the tests are present in this folder by the name `test_*.py` and then go to any of the test and click green play button present on the left side on the test or any of the test case.

- ### Execution from Command line
  - ### Arguments and their usage explanation:
    -   **`-s`:** Shortcut for --capture=no, which means that it disables the capturing on the commandline.
    -   **`-v`:** Used to increase verbosity.
    -   **`-n`:** distributed and subprocess testing, -n or --numprocesses=numprocesses  is the shortcut for '--dist=load --tx=NUM*popen', you can use 'auto' here for auto detection CPUs number on host system and it will be 0 when used with --pdb.
    - **`--html`:** Used to create html report file at given path after test execution.
    - **`--log_level`:** Used to set the level of logging.<br/>


  - ### Execute test cases with html reports
    - Execute all tests in sequential with html-reports: 
      - Navigate to `src\tests` in cmd and run
      - ```pytest -s -v -n=1 --log_level=$LOG_LEVEL --env=qa --html=html_reports/$FILE_NAME.html```
  
    - Execute all tests in parallel with html-reports:
      -  Navigate to `src\tests` in cmd and run
      -   ```pytest -s -v --html=html_reports/$FILE_NAME.html -n=$NUM_OF_PROCESSES --log_level=$LOG_LEVEL --env=qa```

    - Execute specific scenario with html-reports :
      -  ```pytest file_name.py -s -v --html=html_reports/$FILE_NAME.html --log_level=$LOG_LEVEL```
  
  - ### Execute test cases with without html reports
    - Execute all tests in sequential without html-report:
      -  Navigate to `src\tests` in cmd and run
      -   ```pytest -s -v -n=1 --log_level=$LOG_LEVEL --env=qa```
  
    - Execute all tests in parallel mode browser without html-reports
      -  Navigate to `src\tests` in cmd and run
        -  ```pytest -s -v -n=$NUM_OF_PROCESSES --log_level=$LOG_LEVEL --env=qa```

    - Execute specific scenario without html-reports :<br />
       - ```pytest file_name.py -s -v --log_level=$LOG_LEVEL```
  
  
### Test Logs
-   Test Logs are saved in location after execution: <br />`src\tests\logs`.

### Test Reports
-   Test Reports are saved in location after execution: <br />`src\tests\html_reports`.
    
    - ##### Filters available in Html Reporting:
    - `Passed`: Shows the details of number of passed test cases. 
    - `Failed` : Shows the details of number of failed test cases.
    - `Skipped`: Shows the details of number of skipped tests marked with `@pytest.mark.skip` in the test cases. 
    - `Errors`: Shows the details of number of errors in the test cases, if there are error raised before a test execution.
    - `Expected Failures`: Shows the the details of number of Expected Failures marked with `@pytest.mark.xfail` in the test and is expected to fail.
    - `Unexpected Passes`: Shows the the details of number of Unexpected Passes, the test cases which passes unexpectedly even if marked with `@pytest.mark.xfail` in the test.