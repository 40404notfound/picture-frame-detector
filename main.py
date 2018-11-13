from elasticsearch import Elasticsearch
from elasticsearch_driver import AuraMazeSignatureES
from photo import Photo
from operator import itemgetter
from queue import Queue
from threading import Thread
import hashlib
import time
import sys

num_trials = 6
num_workers = 3


def search_image_sync(ses, raw):
    photo = Photo(raw)
    paintings = photo.generate_paintings()
    results = []
    for _, painting in zip(range(num_trials), paintings):
        l = ses.search_image(painting, all_orientations=True, bytestream=True)
        if len(l):
            min_dist_index, min_dist_item = min(enumerate(l), key=lambda item: item[1]['dist'])
            if min_dist_item['dist'] < 0.3:
                return min_dist_item
            results.extend(l)

    results = sorted(results, key=itemgetter('dist'))
    ids = set()
    unique = []
    for item in results:
        if item['id'] not in ids:
            unique.append(item)
            ids.add(item['id'])

    return unique


def painting_hash(painting):
    return hashlib.md5(str(painting).encode('utf-8')).hexdigest()


def worker(q, ses, results):
    while True:
        painting = q.get()
        if painting is None:
            break
        if results['best'] is None:
            l = ses.search_image(painting, all_orientations=True, bytestream=True)
            if len(l):
                min_dist_index, min_dist_item = min(enumerate(l), key=lambda item: item[1]['dist'])
                if min_dist_item['dist'] < 0.3:
                    results['best'] = min_dist_item
                results['list'].extend(l)
        q.task_done()


def search_image(ses, raw):
    photo = Photo(raw)
    paintings = photo.generate_paintings()
    results = {'list': [], 'best': None}

    q = Queue()
    threads = []
    for i in range(num_workers):
        t = Thread(target=worker, args=(q, ses, results))
        t.start()
        threads.append(t)

    for _, painting in zip(range(num_trials), paintings):
        if results['best']:
            break
        q.put(painting)

    def block_queue(q):
        # block until all tasks are done
        q.join()

    t = Thread(target=block_queue, args=(q,), daemon=True)
    t.start()

    while results['best'] is None and t.is_alive():
        time.sleep(0.1)

    # stop workers
    for i in range(num_workers):
        q.put(None)
    # for t in threads:
    #     t.join()

    if results['best']:
        return results['best']

    results['list'] = sorted(results['list'], key=itemgetter('dist'))
    ids = set()
    unique = []
    for item in results['list']:
        if item['id'] not in ids:
            unique.append(item)
            ids.add(item['id'])

    return unique


if __name__ == '__main__':
    es = Elasticsearch(['https://search-auramaze-test-lvic4eihmds7zwtnqganecktha.us-east-2.es.amazonaws.com'])
    ses = AuraMazeSignatureES(es, distance_cutoff=0.5)

    raw = open(sys.argv[1], 'rb').read()

    start = time.time()
    print(search_image(ses, raw))
    end = time.time()
    print(end - start)
