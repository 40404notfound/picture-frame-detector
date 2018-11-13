from elasticsearch import Elasticsearch
from elasticsearch_driver import AuraMazeSignatureES
from photo import Photo
from operator import itemgetter


# data = '''R0lGODlhDwAPAKECAAAAzMzM/////wAAACwAAAAADwAPAAACIISPeQHsrZ5ModrLlN48CXF8m2iQ3YmmKqVlRtW4MLwWACH+H09wdGltaXplZCBieSBVbGVhZCBTbWFydFNhdmVyIQAAOw=='''
#
# im = Image.open(BytesIO(base64.b64decode(data)))
# im.show()

def search_image(ses, raw):
    photo = Photo(raw)
    paintings = photo.generate_paintings()
    results = []
    for _, painting in zip(range(6), paintings):
        l = ses.search_image(painting, all_orientations=True, bytestream=True)
        if len(l):
            min_dist_index, min_dist_item = min(enumerate(l), key=lambda item: item[1]['dist'])
            if min_dist_item['dist'] < 0.3:
                return min_dist_item
            results.extend(l)

    ids = set()
    unique = []
    for item in results:
        if item['id'] not in ids:
            unique.append(item)
            ids.add(item['id'])

    return sorted(unique, key=itemgetter('dist'))


if __name__ == '__main__':
    es = Elasticsearch(['https://search-auramaze-test-lvic4eihmds7zwtnqganecktha.us-east-2.es.amazonaws.com'])
    ses = AuraMazeSignatureES(es, distance_cutoff=0.5)

    raw = open("photos/IMG_6832.JPG", 'rb').read()

    print(search_image(ses, raw))
