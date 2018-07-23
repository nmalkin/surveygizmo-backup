import csv
import random
from typing import Iterable

SURVEY_LIST = 'surveygizmo/all_surveys.csv'


def get_ids() -> Iterable[str]:
    """
    Extract the survey IDs from a CSV with the Survey List
    :return: a list with the survey ids
    """
    with open(SURVEY_LIST) as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        survey_ids = [row[0] for row in reader]

    return survey_ids


def get_shuffled_ids() -> Iterable[str]:
    """
    Return the IDs as provided by `get_ids` in random order
    """
    ids = list(get_ids())
    random.shuffle(ids)
    return ids


if __name__ == '__main__':
    get_ids()
