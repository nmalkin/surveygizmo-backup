import argparse
import logging
import queue
import threading
import typing

import download_survey
import get_ids


def worker(q: queue.Queue, thread_id: int):
    logging.debug(f'starting worker {thread_id}')
    while True:
        survey = q.get()
        if survey is None:
            break
        logging.debug(f'survey {survey} assigned to worker {thread_id}')

        try:
            download_survey.download_survey(survey)
        except Exception as e:
            logging.error(f'something went wrong with survey {survey}: {e}')

        q.task_done()


def download_parallel(num_worker_threads: int, all_surveys: typing.Iterable[str]):
    q: queue.Queue = queue.Queue()
    threads = []
    for i in range(num_worker_threads):
        t = threading.Thread(target=worker, args=(q, i))
        t.start()
        threads.append(t)

    for item in all_surveys:
        q.put(item)

    # Block until all tasks are done
    q.join()

    # Stop workers
    for i in range(num_worker_threads):
        q.put(None)
    for t in threads:
        t.join()


def download_sequentially(all_surveys: typing.Iterable[str]):
    for survey in all_surveys:
        download_survey.download_survey(survey)


def main():
    parser = argparse.ArgumentParser(description='Download all surveys')
    parser.add_argument('--parallel', '-p', default=1, type=int,
                        help='How many downloads to do in parallel')
    parser.add_argument('--shuffle', '-s', action='store_true',
                        help='Process surveys in random order')
    parser.add_argument('--wait', '-w', default=30, type=int,
                        help='How long to wait before checking if export is ready')
    parser.add_argument('--timeout', '-t', default=600, type=int,
                        help="Don't wait more than this for an export")
    args = parser.parse_args()

    # Set time-related configs
    download_survey.WAIT_TIME = args.wait
    download_survey.TOO_LONG = args.timeout

    # Get IDs in random order or sequentially
    if args.shuffle:
        all_surveys = get_ids.get_shuffled_ids()
    else:
        all_surveys = get_ids.get_ids()

    # Download in parallel or sequentially
    if args.parallel == 1:
        download_sequentially(all_surveys)
    else:
        download_parallel(args.parallel, all_surveys)


if __name__ == '__main__':
    main()
