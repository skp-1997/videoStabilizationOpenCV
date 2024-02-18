Video Stabilization

Before Stabilization:



https://github.com/skp-1997/videoStabilizationOpenCV/assets/97504177/57ede448-0148-406a-bbaf-116b76d0135c

After Stabilization:



https://github.com/skp-1997/videoStabilizationOpenCV/assets/97504177/b94ef27a-0a35-4172-b1b2-dcc467fa83a8





Steps for the Video Stabilization

[1] Detectng features from the frame

Here, I am using 'goodFeaturesToTrack' from OpenCV to detect feature points
<img width="600" alt="Screenshot 2024-02-17 at 7 11 31 PM" src="https://github.com/skp-1997/videoStabilizationOpenCV/assets/97504177/10f914a1-6df9-4a3b-b2df-38773ebf300b">






[2] Calculating Optical Flow

I am using 'calcOpticalFlowPyrLK' from OpenCV to calculate optical flow in concurrent frames from features ppints detected in previous frame. It uses Lucas-Kanade Pyramid method to calculate the pixel positions.
<img width="614" alt="Screenshot 2024-02-17 at 7 11 31 PM" src="https://github.com/skp-1997/videoStabilizationOpenCV/assets/97504177/bcafc23b-33d9-47b4-b7b8-26cec5d2412b">


[3] Estimate motion b/w two frames

With the help of 'estimateRigidTransform' module, I calculated the transformation values [x, y, theta] b/w frames.

<img width="614" alt="Screenshot 2024-02-17 at 7 11 31 PM" src="https://github.com/skp-1997/videoStabilizationOpenCV/assets/97504177/db84705d-3e05-484c-bca6-3634ac6461f2">

To get the idea of how it smoothen the curve, here is the picturization.

<img width="615" alt="Screenshot 2024-02-17 at 7 16 17 PM" src="https://github.com/skp-1997/videoStabilizationOpenCV/assets/97504177/49f4a21f-f4e9-4fa8-bb63-4c5581d539da">


[4] Calculate the smooth motion for entire video

First, I use 'numpy.cumsum' to get trajectory for entire video, which later was used to smoothen the transformation using filtering.
I am using 'MovingAverageFilter', the logic is defined below.



The filter is applied trajectory matrix which smoothen values along translation along x, y and rotation along x direction. 

[5] Warping using smoothen transformation matrix calculated before.

Using 'cv2.warpAffine' to wrap consecutive frames from the filtered trajectory matrix.
<img width="615" alt="Screenshot 2024-02-17 at 8 25 22 PM" src="https://github.com/skp-1997/videoStabilizationOpenCV/assets/97504177/f048ea51-e11b-4f0f-aeb2-5743d9a1765b">


[6] Fixing the borders

Since we are warping image, to maintain the frame size. This will led to some dead pixels along border which will be visible in the output video.
