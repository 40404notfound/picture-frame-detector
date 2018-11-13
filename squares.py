import cv2
import numpy as np
from PIL import Image
import io

N=10
canny1=5
canny2=50
canny3=1
appro=0.02
def test():
    im=cv2.imread("photos/IMG_5978.JPG",1)
    squares=getsquare(im)
    #print(squares)

    for i in squares:
        print(i)
    pass
def getsquare(image):
    image=cv2.resize(image,(600,800))
    squares=[]
    timg=image.copy()


    gray0 = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)


    timg=cv2.medianBlur(image,9)

    for c in range(3):
        ch=[c, 0]
        cv2.mixChannels([timg],[gray0],ch)

        for l in range(N):
            if l==0:
                gray=cv2.Canny(gray0,canny1,canny2,canny3*2+1)
                gray=cv2.dilate(gray,cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3)))
            else:

                _,gray=cv2.threshold(gray0,(l+1)*255/N,255,cv2.THRESH_BINARY)
                #gray=cv2.convertScaleAbs(gray)
                #cv2.Mat()
            _,contour,_=cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

            for i in range(len(contour)):
                approx=cv2.approxPolyDP(contour[i],cv2.arcLength(contour[i],True)*appro,True)
                if len(approx)==4 and abs(cv2.contourArea(approx))>1000 and cv2.isContourConvex(approx):
                    maxCosine=0.0
                    for j in range(2,5):
                        cosine=abs(angle(approx[j%4],approx[j-2],approx[j-1]))
                        maxCosine=max(maxCosine,cosine)
                    if maxCosine<0.3:
                        yield approx

def angle(pt1,pt2,pt0):
    dx1=float(pt1[0][0]-pt0[0][0])
    dy1=float(pt1[0][1]-pt0[0][1])
    dx2=float(pt2[0][0]-pt0[0][0])
    dy2=float(pt2[0][1]-pt0[0][1])

    return(dx1*dx2 + dy1*dy2)/np.sqrt((dx1*dx1 + dy1*dy1)*(dx2*dx2 + dy2*dy2)+1e-10)

def raw_to_array(raw_image):
    return np.asanyarray(Image.open(io.BytesIO(raw_image)))

def crop_image(image, box):
    return image.crop(box)

if __name__=="__main__":
    raw = open('photos/IMG_6832.JPG','rb').read()
    image = Image.open(io.BytesIO(raw))
    image = crop_image(image, (100, 100, 900, 900))
    image.show()
    exit(0)
    test()