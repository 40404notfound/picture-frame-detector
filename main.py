from elasticsearch import Elasticsearch
from elasticsearch_driver import AuraMazeSignatureES
from photo import Photo

# data = '''R0lGODlhDwAPAKECAAAAzMzM/////wAAACwAAAAADwAPAAACIISPeQHsrZ5ModrLlN48CXF8m2iQ3YmmKqVlRtW4MLwWACH+H09wdGltaXplZCBieSBVbGVhZCBTbWFydFNhdmVyIQAAOw=='''
#
# im = Image.open(BytesIO(base64.b64decode(data)))
# im.show()

if __name__ == '__main__':
    es = Elasticsearch(['https://search-auramaze-test-lvic4eihmds7zwtnqganecktha.us-east-2.es.amazonaws.com'])
    ses = AuraMazeSignatureES(es, distance_cutoff=0.6)

    raw = open("photos/IMG_0325.JPG", 'rb').read()
    photo = Photo(raw)
    paintings = photo.generate_paintings()

    for painting in paintings:
        print(ses.search_image(painting, all_orientations=True, bytestream=True))
