import shutil,os,sys
import cv2
import numpy
from skimage import measure,morphology
''' The code is used to detect humans accurately on bi-modal histogram images using Otsu's method for 
clustering-based image thresholding.

Usage : python *path of test images*
        example: python ./Sample_Pics
        if the test images have extensions other than jpeg/jpg/png use
        python *path of test images* *extension*
        example: python ./Sample_Pics ['.jpeg','.jpg','.png','.bmp']
'''
def find_nearest(array,value): # function to find the nearest value in an array to the given value
    x = (numpy.abs(array-value)).argmin()
    return array[x]

dir = './results/'  # required output folder
if not os.path.exists(dir):
    os.makedirs(dir)
else:
    shutil.rmtree(dir)
    os.makedirs(dir)

if __name__ == '__main__':
    ext = ['.jpeg','.jpg','.png'] # default extensions
    path = sys.argv[1] # input folder path
    if len(sys.argv) > 2:
        ext = sys.argv[2:] # optional extensions
    Images = [i for i in os.listdir(path) if any( [i.endswith(j) for j in ext])] # array with names of input images 

for file in Images:
    I = cv2.imread(path+'/'+file) # Input image
    Ig = cv2.cvtColor( I, cv2.COLOR_RGB2GRAY ) # grayscale of input image
    r,c = Ig.shape # Image resolution
    Ix = cv2.GaussianBlur(Ig, (5, 5), 0) # Blurring with Gaussian kernel of 5 and standard deviation of 0 in X direction
    #Applying Otsu binarization to segment the image...
    th_val, Iseg = cv2.threshold(Ix, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    bgrnd = numpy.count_nonzero(Iseg) # nadir pixel count
    fgrnd = numpy.size(Ig)-bgrnd # highlighted pixel count
    if bgrnd > fgrnd: #Making sure that Human gets segmented and not the background 
    	Iseg = ~Iseg 
    Creg = morphology.label(Iseg) # connected region of the segmented image
    Preg = measure.regionprops(Creg) # Properties of the connected regions
    temp = [[0, 0, 0, 0, 0]] # storing the parameters of the required bbox
    for i in Preg:
    	if i.area >100:
    		ltcy, ltcx, rbcy, rbcx = i.bbox
    		# retrieve x,y locations of the left top corner and right bottom corner pertaining to the bbox
    		temp.append([ltcx,ltcy,rbcx,rbcy,(rbcx - ltcx)*(rbcy - ltcy)])
    temp = numpy.delete(temp, (0), axis=0) # deleting the row with zeros
    ind = numpy.argmax(temp[:,4]) # Index of the segment with biggest area
    ltcx,rbcx = numpy.min(temp[:,0]),max(temp[:,2]) # x pixel location of corners of bbox# temp[ind,0] #temp[ind,2]
    ltcy,rbcy = numpy.min(temp[:,1]),numpy.max(temp[:,3]) # y pixel location of corners of bbox
    H,W = rbcy - ltcy,rbcx - ltcx # Height and Width of the bbox
    if len(temp)>35 and 150<(H-W)<1000: # If too many segments found 
        ltcy,rbcy = temp[ind,1],temp[ind,3] # y pixel location corresponding to the biggest segment
        new = [[0, 0, 0, 0, 0]]
        XrangeA = (I.shape[1]/2)-100 # defining the range in which the bbox is required
        XrangeB = (I.shape[1]/2)+100
        for i in range(ind-4,ind+5): # selecting the segments around the biggest one
            new.append(temp[i])
        new = numpy.array(new)
        ltcx,rbcx=find_nearest(new[:,0],XrangeA),find_nearest(new[:,2],XrangeB) # selecting the x locations within the chosen range
    H,W = rbcy - ltcy,rbcx - ltcx# Height and Width of the bbox
    # Finally Drawing the bounding box
    cv2.rectangle(I, (ltcx, ltcy), (ltcx + W, ltcy + H), (198, 245, 174), 4)
    cv2.imwrite(dir+file,I)