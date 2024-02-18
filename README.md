Video Stabilization

Steps for the Video Stabilization

[1] Detectng features from the frame

Here, I am using 'goodFeaturesToTrack' from OpenCV to detect feature points 
![feature](https://github.com/skp-1997/videoStabilizationOpenCV/assets/97504177/f3c47f08-ccd5-4a0a-8c3f-116dac50765d)


[2] Calculating Optical Flow

I am using 'calcOpticalFlowPyrLK' from OpenCV to calculate optical flow in concurrent frames from features ppints detected in previous frame. It uses Lucas-Kanade Pyramid method to calculate the pixel positions.
<img width="614" alt="Screenshot 2024-02-17 at 7 11 31 PM" src="https://github.com/skp-1997/videoStabilizationOpenCV/assets/97504177/bcafc23b-33d9-47b4-b7b8-26cec5d2412b">


[3] Estimate motion b/w two frames

With the help of 'estimateRigidTransform' module, I calculated the transformation values [x, y, theta] b/w frames.

![R (2)](https://github.com/skp-1997/videoStabilizationOpenCV/assets/97504177/db84705d-3e05-484c-bca6-3634ac6461f2)


[4] Calculate the smooth motion for entire video

First, I use 'numpy.cumsum' to get trajectory for entire video, which later was used to smoothen the transformation using filtering.
I am using 'MovingAverageFilter', the logic is defined below.
<img width="618" alt="Screenshot 2024-02-17 at 7 16 17 PM" src="https://github.com/skp-1997/videoStabilizationOpenCV/assets/97504177/49f4a21f-f4e9-4fa8-bb63-4c5581d539da">


The filter is applied trajectory matrix which smoothen values along translation along x, y and rotation along x direction.

[5] Warping using smoothen transformation matrix calculated before.

Using 'cv2.warpAffine' to wrap consecutive frames from the filtered trajectory matrix.
<img width="686" alt="Screenshot 2024-02-17 at 8 25 22 PM" src="https://github.com/skp-1997/videoStabilizationOpenCV/assets/97504177/f048ea51-e11b-4f0f-aeb2-5743d9a1765b">


[6] Fixing the borders

Since we are warping image, to maintain the frame size. This will led to some dead pixels along border which will be visible in the output video.
