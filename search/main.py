from PIL import Image
from io import BytesIO
import base64
import image_match
from elasticsearch import Elasticsearch
from elasticsearch_driver import AuraMazeSignatureES

# data = '''R0lGODlhDwAPAKECAAAAzMzM/////wAAACwAAAAADwAPAAACIISPeQHsrZ5ModrLlN48CXF8m2iQ3YmmKqVlRtW4MLwWACH+H09wdGltaXplZCBieSBVbGVhZCBTbWFydFNhdmVyIQAAOw=='''
#
# im = Image.open(BytesIO(base64.b64decode(data)))
# im.show()

with open('9223372032559808999.jpg', "rb") as imageFile:
    f = imageFile.read()
    print(f)
es = Elasticsearch(['https://search-auramaze-test-lvic4eihmds7zwtnqganecktha.us-east-2.es.amazonaws.com'])
ses = AuraMazeSignatureES(es)

print(ses.search_image(f, bytestream=True))
print(ses.search_image('https://www.vangoghmuseum.nl/download/61fbedad-1d68-4b96-8f08-2c6ec01eb911.jpg?size=s'))
