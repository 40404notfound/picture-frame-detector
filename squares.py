import cv2
import numpy as np

N=10
canny1=5
canny2=50
canny3=1
appro=0.02
def test():
    im=cv2.imread("photos/IMG_5978.JPG",1)
    squares=getsquare(im)
    pass
def getsquare(image):
    squares=[]
    timg=image.copy()
    gray0 =timg.copy()

    timg=cv2.medianBlur(image,9)

    for c in range(3):
        ch=[c, 0]
        cv2.mixChannels(timg,gray0,ch)

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
                        squares.append(approx)
    return squares

def angle(pt1,pt2,pt0):
    dx1=float(pt1[0][0]-pt0[0][0])
    dy1=float(pt1[0][1]-pt0[0][1])
    dx2=float(pt2[0][0]-pt0[0][0])
    dy2=float(pt2[0][1]-pt0[0][1])

    return(dx1*dx2 + dy1*dy2)/np.sqrt((dx1*dx1 + dy1*dy1)*(dx2*dx2 + dy2*dy2)+1e-10)

if __name__=="__main__":
    test()