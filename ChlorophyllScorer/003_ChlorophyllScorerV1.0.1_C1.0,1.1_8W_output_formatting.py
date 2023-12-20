# importing libraries
import cv2
import numpy as np
import os
import time

# =============================================================================
# Function that counts the white/black pixels and calculates the ratio between them
# =============================================================================
"""
whiteThreshold is the threshold that distinguishes between for what is
considered black or white in the range of 0 (black) to 255 (white). Manual
examination of "D7 Pseudomonas 9.1 r1 680nm (chlorophyll) 80msec.Tif" showed
that the plastic could reach an intensity of up to 124 under 680 nm light, and
as such a threshold shouild be set above that, for example at 150.
"""
def ChlorophyllScorer(file,whiteThreshold,row):
    #credit: https://www.geeksforgeeks.org/opencv-counting-the-number-of-black-and-white-pixels-in-the-image/
    uncroppedImg=cv2.imread(file, cv2.IMREAD_GRAYSCALE)#import image as grayscale
    wholeImg=cv2.resize(uncroppedImg[0:2200, 244:2444],(512,512), interpolation=cv2.INTER_AREA)
    img=wholeImg[0:512,row*64:64+row*64]
    numberOfWhitePix = np.sum(img>=whiteThreshold)
    numberOfBlackPix = np.sum(img<whiteThreshold)
    """
    cv2.imshow("x", img)
    cv2.waitKey(0)
    """
    #defining the white to black ratio in image, .100f is to make sure that the
    #notaion does not convert to scientific as it confuses the program
    whiteToBlack = str(format(numberOfWhitePix/numberOfBlackPix, ".100f"))
    
    #loop that reduces the amount of decimals of the whiteToBlack variable to 5
    #non-zero decimals
    for i in range(len(whiteToBlack)):
        if whiteToBlack[i] != "0" and whiteToBlack[i] != ".":
            whiteToBlack = whiteToBlack[0:i+5]
            whiteToBlack = float(whiteToBlack)
            break
    
    #adding comma seperators to white/black count for readability
    print(f"White pixels:\t\t\t{numberOfWhitePix}\nBlack pixels:\t\t\t{numberOfBlackPix}\nWhite to black ratio:\t{whiteToBlack}")
    return(f"{numberOfWhitePix}")


# =============================================================================
# Main Script
# =============================================================================
# Opens the file directory for the pictures
os.chdir(input("Please imput picture file directory: "))

"""
whiteThreshold is the threshold that distinguishes between for what is
considered black or white in the range of 0 (black) to 255 (white). Manual
examination of "D7 Pseudomonas 9.1 r1 680nm (chlorophyll) 80msec.Tif" showed
that the plastic could reach an intensity of up to 124 under 680 nm light, and
as such a threshold shouild be set above that, for example at 150.
"""
whiteThresholdInput = int(input("Choose the white threshold (0-255, 150 recommended): "))

#Creates a file with a unique time stamp
fileName = time.strftime("Chlorophyll_Score_%d-%m-%Y_%H-%M-%S.txt")
outfile = open(fileName, "w")
outfile.write("treatment\twell\texposure\tday\treading\n")
#loop that goes through each files and score the Chlorophyll Content, and then
#writes it to the output file
for i in os.listdir():
	if i[-4:] != ".txt" and i[-4:] != ".ini":
		[boxNumber,exposure,day]=i[:-4].split("-")
		if day[0]=="d":
			day=day[1:]
		print(f"\n{i}:")
		for j in range(8):
			wellChloroScore = ChlorophyllScorer(i,whiteThresholdInput,j)
			outfile.write(f"box_{boxNumber}\twell_{j+1}\t{exposure}\t{day}\t{wellChloroScore}\n")
outfile.close()

"""
import cv2
import numpy as np
import os
import time
os.chdir(input("Please imput picture file directory: "))
print(os.listdir()[0])
img=cv2.imread(os.listdir()[0], cv2.IMREAD_GRAYSCALE)
croppedImg=cv2.resize(img[0:2200, 244:2444],(512,512), interpolation=cv2.INTER_AREA)
print(img.shape, croppedImg.shape)
cv2.imshow("x", croppedImg)
for i in range(8):
	cv2.imshow("x", croppedImg[0:512,64*i:64+64*i])
	cv2.waitKey(0)
"""


