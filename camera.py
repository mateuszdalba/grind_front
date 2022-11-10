from threading import Thread
import cv2, time
import mediapipe as mp
import numpy as np

# defining a helper class for implementing multi-threading 
class WebcamStream:
    # initialization method 
    def __init__(self, stream_id=0):
        self.stream_id = stream_id #default is 0 for main camera 
        
        # opening video capture stream 
        self.vcap = cv2.VideoCapture(self.stream_id)

        self.vcap.set(3, 720)
        self.vcap.set(4, 1280)
        #self.vcap.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
        #self.vcap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1000)
        #self.vcap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        #self.vcap.set(cv2.CAP_PROP_FPS, 30)
            
        # reading a single frame from vcap stream for initializing 
        self.grabbed , self.frame = self.vcap.read()
        #if self.grabbed is False :
        #    print('[Exiting] No more frames to read')
        #    exit(0)
        # self.stopped is initialized to False 
        self.stopped = True
        # thread instantiation  
        self.t = Thread(target=self.update, args=())
        self.t.daemon = True # daemon threads run in background 
        
    # method to start thread 
    def start(self):
        self.stopped = False
        self.t.start()

    # method passed to thread to read next available frame  
    def update(self):
        while True :
            if self.stopped is True :
                break
            self.grabbed , self.frame = self.vcap.read()
            if self.grabbed is False :
                print('[Exiting] No more frames to read')
                self.stopped = True
                break 
        self.vcap.release()
    # method to return latest read frame 

    def read(self):
        return self.frame
    # method to stop reading frames 
    
    def stop(self):
        self.stopped = True



class CustomSquats():

    def __init__(self):

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose

        # thread instantiation  
        #self.t = Thread(target=self.process, args=())
        #self.t.daemon = True # daemon threads run in background 

     # method to start thread 
    #def start(self):
        #self.stopped = False
        #self.t.start()

    def process(self, frame_in):
        i = 0
        #Curl counter
        counter = 0 
        stage = None
        technique = None

        with self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            prevTime = 0

            # while True:
            #     if video.stopped is True:
            #         break
            i +=1

            #frame = video.read()
            frame = frame_in

            print(frame.shape)
        
            #Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            #Make detection
            results = pose.process(image)
            image.flags.writeable = True

            #Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
            
                #Get cordianates
                l_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                l_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                l_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            
                r_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                r_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                r_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            
                l_angle = calculate_angle(l_hip, l_knee, l_ankle)
                r_angle = calculate_angle(r_hip, r_knee, r_ankle)
            
                #Shoulder distances
                l_shoulder_x= landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x
                l_shoulder_y= landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y
                right_shoulder_x = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x
                right_shoulder_y = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y
            
                shoulder_distance =  np.round(np.sqrt((right_shoulder_x - l_shoulder_x)**2 + (right_shoulder_y - l_shoulder_y)**2),2)
            
            
                l_ankle_x= landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x
                l_ankle_y= landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y
                r_ankle_x = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x
                r_ankle_y = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y
            
                ankle_distance =  np.round(np.sqrt((r_ankle_x - l_ankle_x)**2 + (r_ankle_y - l_ankle_y)**2),2)

                #Put angle of left knee
                cv2.putText(image, str(np.round(l_angle,2)),
                        tuple(np.multiply(l_knee, [480, 640]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            
                #Put angle of right knee
                cv2.putText(image, str(np.round(r_angle,2)),
                        tuple(np.multiply(r_knee, [480, 640]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

            except:
                pass


            #Rendering
            self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                                    self.mp_drawing.DrawingSpec(color=(255,250,250), thickness=2, circle_radius=2),
                                    self.mp_drawing.DrawingSpec(color=(255,250,250), thickness=2, circle_radius=2) 
                                        )


            return image



