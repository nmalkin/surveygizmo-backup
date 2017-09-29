import logging
import queue
import threading

from download_survey import download_survey
from get_ids import get_ids

NUM_WORKER_THREADS = 4


def worker(q: queue.Queue, thread_id: int):
    logging.debug(f'starting worker {thread_id}')
    while True:
        survey = q.get()
        if survey is None:
            break
        logging.debug(f'survey {survey} assigned to worker {thread_id}')

        try:
            download_survey(survey)
        except Exception as e:
            logging.error(f'something went wrong with survey {survey}: {e}')

        q.task_done()


def download_parallel():
    all_surveys = get_ids()

    q = queue.Queue()
    threads = []
    for i in range(NUM_WORKER_THREADS):
        t = threading.Thread(target=worker, args=(q, i))
        t.start()
        threads.append(t)

    for item in all_surveys:
        q.put(item)

    # Block until all tasks are done
    q.join()

    # Stop workers
    for i in range(NUM_WORKER_THREADS):
        q.put(None)
    for t in threads:
        t.join()


def download_sequentially():
    all_surveys = get_ids()
    for survey in all_surveys:
        download_survey(survey)


if __name__ == '__main__':
    download_parallel()
    # Alternately,
    # download_sequentially()
