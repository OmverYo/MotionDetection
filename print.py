import os
import cv2
import numpy as np
import mediapipe as mp
import matplotlib.pyplot as plt
import time

# Initializing mediapipe segmentation class.
mp_selfie_segmentation = mp.solutions.selfie_segmentation
 
# Setting up Segmentation function.
segment = mp_selfie_segmentation.SelfieSegmentation(0)

def modifyBackground(image, background_image = 255, blur = 95, threshold = 0.3, display = True, method='changeBackground'):
    # Convert the input image from BGR to RGB format.
    RGB_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
 
    # Perform the segmentation.
    result = segment.process(RGB_img)
    
    # Get a binary mask having pixel value 1 for the object and 0 for the background.
    # Pixel values greater than the threshold value will become 1 and the remainings will become 0.
    binary_mask = result.segmentation_mask
    
    # Stack the same mask three times to make it a three channel image.
    binary_mask_3 = np.dstack((binary_mask,binary_mask,binary_mask))
    
    if method == 'changeBackground':
    
        # Resize the background image to become equal to the size of the input image.
        background_image = cv2.resize(background_image, (image.shape[1], image.shape[0]))
 
        # Create an output image with the pixel values from the original sample image at the indexes where the mask have 
        # value 1 and replace the other pixel values (where mask have zero) with the new background image.
        output_image = np.where(binary_mask_3, image, background_image)
        
    elif method == 'blurBackground':
        
        # Create a blurred copy of the input image.
        blurred_image = cv2.GaussianBlur(image, (blur, blur), 0)
 
        # Create an output image with the pixel values from the original sample image at the indexes where the mask have 
        # value 1 and replace the other pixel values (where mask have zero) with the new background image.
        output_image = np.where(binary_mask_3, image, blurred_image)
    
    elif method == 'desatureBackground':
        
        # Create a gray-scale copy of the input image.
        grayscale = cv2.cvtColor(src = image, code = cv2.COLOR_BGR2GRAY)
 
        # Stack the same grayscale image three times to make it a three channel image.
        grayscale_3 = np.dstack((grayscale,grayscale,grayscale))
 
        # Create an output image with the pixel values from the original sample image at the indexes where the mask have 
        # value 1 and replace the other pixel values (where mask have zero) with the new background image.
        output_image = np.where(binary_mask_3, image, grayscale_3)
        
    elif method == 'transparentBackground':
        
        # Stack the input image and the mask image to get a four channel image. 
        # Here the mask image will act as an alpha channel. 
        # Also multiply the mask with 255 to convert all the 1s into 255.  
        output_image = np.dstack((image, binary_mask * 255))
        
    else:
        # Display the error message.
        print('Invalid Method')
        
        # Return
        return
    
    # Check if the original input image and the resultant image are specified to be displayed.
    if display:
    
        # Display the original input image and the resultant image.
        plt.figure(figsize=[22,22])
        plt.subplot(121);plt.imshow(image[:,:,::-1]);plt.title("Original Image");plt.axis('off');
        plt.subplot(122);plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off');
    
    # Otherwise
    else:
        
        # Return the output image and the binary mask.
        # Also convert all the 1s in the mask into 255 and the 0s will remain the same.
        # The mask is returned in case you want to troubleshoot.
        return output_image, (binary_mask_3 * 255).astype('uint8')

# Specify the path of a sample image.
img_path = 'sample.jpg'
 
# Read the input image from the specified path.
image = cv2.imread(img_path)
 
# Make the background of the sample image transparent.
trans_background_img, _ = modifyBackground(image, threshold = 0.9, display=False, method='transparentBackground')
 
# Specify the path to store the resultant image
resultant_img_path = "C:/Users/pc/Documents/GitHub/MotionDetection/"
 
# Store the resultant image into the disk. Make sure it's stored as `PNG`
cv2.imwrite(resultant_img_path + "asd.png", trans_background_img)
 
# Show a success message.
print('The Image with transparent background is successfully stored in the disk')