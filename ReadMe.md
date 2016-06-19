# Accurate Object Detection For Bi-modal Histogram Images

The code is demonstration of clustering-based image thresholding or the reduction of a graylevel image to a binary image. It uses Otsu's thresholding algorithm and assumes that the image contains two classes of pixels following bi-modal histogram (foreground pixels and background pixels), it then calculates the optimum threshold separating the two classes so that their combined spread (intra-class variance) is minimal, or equivalently

## Human Detection
A human detector has been implemented that accurately bounds a person in the given input image set.

## Approach
* The input image is converted into a binary image using OTSU‘s algorithm. OTSU algorithm is a very simple idea. 
* It searches the threshold that the weighted within class variance and minimizes the intra-class variance, maximizes the intervariance for black and white pixels 0/1. 
* Smoothening is done in order to remove the noises and to prepare the histograms for further processing. Smoothening is helpful in connectivity.
* The connectivity of the pixels can be done into 4-way connectivity and 8-way connectivity. Connectivity with 0 is the background and with the 1 is the component. 
* The component which has maximum area are labled with some id and the co-ordinates of the object are extracted from labeled area.
* Finally, the bbox rectangle is drawn using OpenCV  

# Environment
Python 2.7 https://www.python.org/download/releases/2.7/
OpenCV 3.1 http://opencv.org/downloads.html
skimage http://scikit-image.org/download.html

# Usage : 

* Default

<br /> python < .py file > < path of test images > <br />
example: <br /><code>python detect.py ./Sample_Pics</code><br />
        
* if the test images have extensions other than jpeg/jpg/png use:

<br /> python < .py file > < path of test images > < extension > <br />
example: <br /><code>python detect.py ./Sample_Pics ['.jpeg','.jpg','.png','.bmp']</code><br />
