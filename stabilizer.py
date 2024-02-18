import cv2
import numpy as np
from tqdm import tqdm


class videoStabilization:

    def __init__(self, PATH):
        self.count = 0
        self.video_path = PATH
        self.video = cv2.VideoCapture(self.video_path)
        self.n_frames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT)) 
        self.w = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.h = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.out = cv2.VideoWriter('video_out.avi', fourcc, 60, (self.w, self.h))
        self.transform = np.zeros((self.n_frames-1, 3), np.float32)
        self.points = None
        self.prev_frame = None
        self.curr_frame = None
        self.initial_frame = True
        self.SMOOTHING_RADIUS = 50

    # Detect the feature points in given frame
    def detect_features(self, frame):

        points = cv2.goodFeaturesToTrack(frame, 
                                         maxCorners=200,
                                         qualityLevel=0.01,
                                         minDistance=30,
                                         blockSize=3)
        return points

    # Calculate transformation along x, y and radian to transform 
    # previous frame to current frame
    def cal_transformation(self):
        pts1 = self.detect_features(self.prev_frame)
        pts2, status, err = cv2.calcOpticalFlowPyrLK(self.prev_frame, self.curr_frame, pts1, None)
        data = cv2.estimateAffinePartial2D(pts1, pts2)
        x = data[0][0,2]
        y = data[0][1,2]
        r = np.arctan2(data[0][1,0], data[0][0,0])

        return [x,y,r]

    # Append values in transoform matrix which gives 
    # motion of features acroos the video
    def cal_motion(self, idx):

        self.transform[idx] = self.cal_transformation()

    # Applies cumulative sum to transoform matrix
    def smooth_motion(self):
        transform = np.cumsum(self.transform, axis=0)
        return transform

    
    # Filter to smoothen the x, y and angle curves
    def movingAverage(self, curve, radius):
        window_size = 2 * radius + 1
        f = np.ones(window_size)/window_size
        curve_pad = np.lib.pad(curve, (radius, radius), 'edge')
        curve_smoothed = np.convolve(curve_pad, f, mode='same')
        curve_smoothed = curve_smoothed[radius:-radius]
        return curve_smoothed
    
    # Applies movingAverage filter to x, y and theta curves
    def smooth(self, trajectory):
        smoothed_trajectory = np.copy(trajectory)
        for i in range(3):
            smoothed_trajectory[:,i] = self.movingAverage(trajectory[:,i], radius=self.SMOOTHING_RADIUS)
        
        return smoothed_trajectory
    
    # Warp frame with transformation matrix
    def fixBorder(self, frame):
        s = frame.shape
        T = cv2.getRotationMatrix2D((s[1]/2, s[0]/2), 0, 1.04)
        frame = cv2.warpAffine(frame, T, (s[1], s[0]))
        return frame
    

    def main(self):
        print(f'[INFO] Calculating transformation needed for each frames...')
        for i in tqdm(range(self.n_frames-2)):
            # print(i)
            ret, frame = self.video.read()
            # print(ret)
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if self.initial_frame:
                    self.prev_frame = frame
                    self.initial_frame = False
                    continue
                else:
                    self.curr_frame = frame
                    self.cal_motion(i)
                    self.prev_frame = self.curr_frame

        # print(f'[INFO] transform : {self.transform.shape}')
        trajectory = self.smooth_motion()
        # print(f'[INFO] cumsum is {trajectory.shape}')

        # Calculate difference in smoothed_trajectory and trajectory
        difference = self.smooth(trajectory) - trajectory
        
        # Calculate newer transformation array
        transforms_smooth = self.transform + difference
        # Reset stream to first frame
        self.video.set(cv2.CAP_PROP_POS_FRAMES, 0) 
        
        # Write n_frames-1 transformed frames
        print(f'[INFO] Applying the transformation for each frame...')
        for i in tqdm(range(self.n_frames-2)):
            # Read next frame
            success, frame = self.video.read()
            if not success:
                break
            
            # Extract transformations from the new transformation array
            dx = transforms_smooth[i,0]
            dy = transforms_smooth[i,1]
            da = transforms_smooth[i,2]
            
            # Reconstruct transformation matrix accordingly to new values
            m = np.zeros((2,3), np.float32)
            m[0,0] = np.cos(da)
            m[0,1] = -np.sin(da)
            m[1,0] = np.sin(da)
            m[1,1] = np.cos(da)
            m[0,2] = dx
            m[1,2] = dy
            
            # Apply affine wrapping to the given frame
            frame_stabilized = cv2.warpAffine(frame, m, (self.w,self.h))
            
            # Fix border artifacts
            frame_stabilized = self.fixBorder(frame_stabilized) 

            self.out.write(frame_stabilized)
        print(f'[INFO] Video processed!')
                    



    

if __name__ == '__main__':
    obj = videoStabilization('input/input_video8.mp4')
    obj.main()
    


