import cv2, time
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a,b,c):
    a = np.array(a) #First
    b = np.array(b) #Mid
    c = np.array(c) #End
    
    radians = np.arctan2(c[1] - b[1], c[0]-b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360-angle
        
    return angle


def squats(frame):

    #writer = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"MJPG"), 30,(640,480))
    W, H = 1920, 1080
    #Curl counter
    counter = 0 
    stage = None
    technique = None

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
      
            
        
        #Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        #Make detection
        results = pose.process(image)
        
        #Recoloring back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
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
                        tuple(np.multiply(l_knee, [W, H]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            
            #Put angle of right knee
            cv2.putText(image, str(np.round(r_angle,2)),
                        tuple(np.multiply(r_knee, [W, H]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            
                       
            #Curl counter logic
            if l_angle > 160 and r_angle > 160:
                stage = "up"
                
            if (l_angle < 90 and r_angle < 90) and stage == 'up':
                stage = "down"
                counter += 1
                #print(stage)
            
            #Technique
            
            if ankle_distance > 1.2*shoulder_distance:
                technique = 'legs too wide!'
            elif ankle_distance < 0.8*shoulder_distance:
                technique = 'legs too close!'
            else:
                technique = 'good technique!'
    
        except:
            pass
        
        #setup status box
        cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
        
        #rep data
        
        cv2.putText(image, 'REPS', (15,12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        
        cv2.putText(image, str(counter),
                (10,60),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        
        #rep data
        cv2.putText(image, 'STAGE', (65,12),
                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        
        cv2.putText(image, stage,
                (60,60),
                cv2.FONT_HERSHEY_COMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        
        #Technique
        cv2.putText(image, 'TECHNIQUE', (600,12),
                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        
        cv2.putText(image, technique,
                (600,60),
                cv2.FONT_HERSHEY_COMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        
        
        #Rendering
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                )
        
        #writer.write(image)
        #cv2.imshow('Mediapipe feed', image)
            
        return image