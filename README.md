Video Stabilization

# Demonstration:



https://github.com/skp-1997/videoStabilizationOpenCV/assets/97504177/7abd54a9-cde6-4c06-968b-88dc28d48825








# Steps for the Video Stabilization

## [1] Detectng features from the frame

Here, I am using 'goodFeaturesToTrack' from OpenCV to detect feature points
<img width="600" alt="Screenshot 2024-02-17 at 7 11 31 PM" src="https://github.com/skp-1997/videoStabilizationOpenCV/assets/97504177/10f914a1-6df9-4a3b-b2df-38773ebf300b">






## [2] Calculating Optical Flow

I am using 'calcOpticalFlowPyrLK' from OpenCV to calculate optical flow in concurrent frames from features ppints detected in previous frame. It uses Lucas-Kanade Pyramid method to calculate the pixel positions.
<img width="614" alt="Screenshot 2024-02-17 at 7 11 31 PM" src="https://github.com/skp-1997/videoStabilizationOpenCV/assets/97504177/bcafc23b-33d9-47b4-b7b8-26cec5d2412b">


## [3] Estimate motion b/w two frames

With the help of 'estimateRigidTransform' module, I calculated the transformation values [x, y, theta] b/w frames.

<img width="614" alt="Screenshot 2024-02-17 at 7 11 31 PM" src="https://github.com/skp-1997/videoStabilizationOpenCV/assets/97504177/db84705d-3e05-484c-bca6-3634ac6461f2">

To get the idea of how it smoothen the curve, here is the picturization.

<img width="615" alt="Screenshot 2024-02-17 at 7 16 17 PM" src="https://github.com/skp-1997/videoStabilizationOpenCV/assets/97504177/49f4a21f-f4e9-4fa8-bb63-4c5581d539da">


## [4] Calculate the smooth motion for entire video

First, I use 'numpy.cumsum' to get trajectory for entire video, which later was used to smoothen the transformation using filtering.
I am using 'MovingAverageFilter', the logic is defined below.



The filter is applied trajectory matrix which smoothen values along translation along x, y and rotation along x direction. 

## [5] Warping using smoothen transformation matrix calculated before.

Using 'cv2.warpAffine' to wrap consecutive frames from the filtered trajectory matrix.
<img width="615" alt="Screenshot 2024-02-17 at 8 25 22 PM" src="https://github.com/skp-1997/videoStabilizationOpenCV/assets/97504177/f048ea51-e11b-4f0f-aeb2-5743d9a1765b">


## [6] Fixing the borders

Since we are warping image, to maintain the frame size. This will led to some dead pixels along border which will be visible in the output video.


# References:

1. Video Stabilization Using Point Feature Matching in OpenCV - Abhishek Singh Thakur
https://learnopencv.com/video-stabilization-using-point-feature-matching-in-opencv/

2. Optical Flow in OpenCV (C++/Python) - Maxim Kuklin (Xperience.AI)
https://learnopencv.com/optical-flow-in-opencv/

3. CS231M · Mobile Computer Vision - Standford University
https://web.stanford.edu/class/cs231m/lectures/lecture-7-optical-flow.pdf

# Scope of Improvement

The method is primitive and doesn't work if there are objects moving in video at faster pace. The other approached would be to find where optical flow is maximum and compensate for that using mathematical logic or use deep learning model.
