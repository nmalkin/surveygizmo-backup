import logging
import os.path
import re
import time

import requests

logging.basicConfig(level=logging.DEBUG)

WAIT_TIME = 3  # seconds
"""
How long to wait before checking if export is ready
"""
TOO_LONG = 90  # seconds
"""
Don't wait more than this for an export
"""
TARGET_DIRECTORY = 'surveygizmo'

HEADERS = {
    'Accept-Language': 'en-US,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/61.0.3163.100 Safari/537.36',
}


def download_csv(session, survey_id):
    logging.info(f'downloading csv for {survey_id}')

    # Check that the export hasn't been done already
    filename = os.path.join(TARGET_DIRECTORY, f'{survey_id}.csv')
    if os.path.exists(filename):
        logging.error(f'{filename} already exists. Has this export been finished already?')
        return

    # Trigger the export
    r = session.get(f"https://app.surveygizmo.com/Reports/simpleexport/?id={survey_id}&view=6073")

    # Extract the report ID
    page = r.text
    match = re.search('var reportID = (\d+);', page)
    report_id = match.group(1)
    logging.debug(f'report ID is {report_id}')

    # Wait for export to be ready
    logging.debug('waiting for export to be ready')
    waited = 0
    while True:
        time.sleep(WAIT_TIME)
        waited += WAIT_TIME

        r = session.get(f"https://app.surveygizmo.com/Reports/simple-export-percent-check?reportid={report_id}")
        percentage = r.json()['response']['percent']

        if percentage == 100:
            break
        elif waited > TOO_LONG:
            logging.warning(f'waited {TOO_LONG}; trying to go ahead with the export.')
            break

    # Download the data
    r = session.get(
        f'https://app.surveygizmo.com/Reports/simpleexportdownload?sid={survey_id}&report_id={report_id}&mode=html')
    data = r.text

    # Store it
    with open(filename, 'w') as f:
        f.write(data)


def download_pdf(session, survey_id):
    logging.info(f'downloading pdf for {survey_id}')

    # Check that the export hasn't been done already
    filename = os.path.join(TARGET_DIRECTORY, f'{survey_id}.pdf')
    if os.path.exists(filename):
        logging.error(f'{filename} already exists. Has this export been finished already?')
        return

    # Trigger the export
    session.get(
        f"https://app.surveygizmo.com/projects/pdfdownloadstart?id={survey_id}&include-page-desc=true&include-ids=true&include-instructions=true&include-validation=true&include-piping=true&include-alias=true&include-logic=true&include-actions=true&include-icons=true&PoweredByShowDefault=true&PoweredByShowSetting=check+theme&HasLogic=true&HasActions=true&HasPiping=true&HasTheme=true&HasOptionRandomization=true")

    # Wait for export to be ready
    logging.debug('waiting for export to be ready')
    waited = 0
    while True:
        time.sleep(WAIT_TIME)
        waited += WAIT_TIME

        r = session.get(f"https://app.surveygizmo.com/projects/pdf-export-percent-check?sid={survey_id}")
        percentage = r.json()['response']['percent']

        if percentage == 100:
            break
        elif waited > TOO_LONG:
            logging.warning(f'waited {TOO_LONG}; trying to go ahead with the export.')
            break

    # Download the data
    r = session.get(
        f'https://app.surveygizmo.com/projects/pdf-export-download?sid={survey_id}')
    data = r.content

    # Store it
    with open(filename, 'wb') as f:
        f.write(data)


def download_word(session, survey_id):
    logging.info(f'downloading word for {survey_id}')

    # Check that the export hasn't been done already
    filename = os.path.join(TARGET_DIRECTORY, f'{survey_id}.doc')
    if os.path.exists(filename):
        logging.error(f'{filename} already exists. Has this export been finished already?')
        return

    # Download the data
    r = session.post(
        'https://app.surveygizmo.com/projects/wordexport',
        headers={'Referer': 'https://app.surveygizmo.com/projects/download/id/3227678'},
        data={'id': survey_id,
              'include-page-desc': 'true',
              'include-ids': 'true',
              'include-instructions': 'true',
              'include-validation': 'true',
              'include-piping': 'true',
              'include-alias': 'true',
              'include-logic': 'true',
              'include-actions': 'true',
              'include-icons': 'true',
              'include-logo': 'true',
              'PoweredByShowDefault': 'true',
              'PoweredByShowSetting': 'check+theme',
              'HasLogic': 'true',
              'HasActions': 'true',
              'HasPiping': 'true',
              'HasTheme': 'true',
              'HasOptionRandomization': 'true'})

    data = r.content

    # Store it
    with open(filename, 'wb') as f:
        f.write(data)


def download_survey(survey_id):
    logging.info(f'downloading survey {survey_id}')
    with requests.Session() as session:
        session.headers.update(HEADERS)
        session.cookies.update({'PHPSESSID': os.environ['PHPSESSID'], 'appsact': os.environ['APPSACT']})

        #download_csv(session, survey_id)
        download_pdf(session, survey_id)
        download_word(session, survey_id)


if __name__ == '__main__':
    test_survey_id = 662351
    download_survey(test_survey_id)