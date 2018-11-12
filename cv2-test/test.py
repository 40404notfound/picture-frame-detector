import cv2
import numpy as np
import Cards


if __name__ == '__main__':
    # Read image
    image = cv2.imread('1.png')

    # Pre-process image (gray, blur, and threshold it)
    pre_proc = Cards.preprocess_image(image)

    # Find and sort the contours of all cards in the image (query cards)
    cnts_sort, cnt_is_card = Cards.find_cards(pre_proc)

    print(cnts_sort)
    print(cnt_is_card)