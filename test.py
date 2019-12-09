import cv2 as cv
import numpy as np
import cb

path = "test/46.jpg"
img = cv.imread(path)
cv.imshow("res", img)
cv.waitKey(0)
cv.cv.destroyAllWindows()