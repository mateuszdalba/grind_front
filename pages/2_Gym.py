import streamlit as st
import cv2, time
import mediapipe as mp
import numpy as np
from threading import Thread
from functions.utilities import calculate_angle
from camera import WebcamStream


use_webcam = st.sidebar.button('Use Webcam')

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

W, H = 1920, 1080


# Resize Images to fit Container
@st.cache()
# Get Image Dimensions
def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h,w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = width/float(w)
        dim = (int(w*r),height)
    else:
        r = width/float(w)
        dim = width, int(h*r)

    # Resize image
    resized = cv2.resize(image,dim,interpolation=inter)
    return resized





## Get Video
stframe = st.empty()

kpil, kpil2, kpil3 = st.columns(3)

with kpil:
    st.markdown('**Reps: **')
    kpil_text = st.markdown('0')

with kpil2:
    st.markdown('**Stage: **')
    kpil2_text = st.markdown('None')

with kpil3:
    st.markdown('**Technique: **')
    kpil3_text = st.markdown('None')

if use_webcam:
    video = WebcamStream(stream_id=0)
    video.start()

    fps = 0
    i = 0

    #Curl counter
    counter = 0 
    stage = None
    technique = None

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        prevTime = 0

        while True:
            if video.stopped is True :
                break
            i +=1
            frame = video.read()

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

            #setup status box
            #cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
        
            #rep data
            #cv2.putText(image, 'REPS', (15,12),
            #            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        
            #cv2.putText(image, str(counter),
            #            (10,60),
            #               cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

         
            kpil_text.write(f"<h1 style='text-align: center; color:red;'>{str(counter)}</h1>", unsafe_allow_html=True)
                
                
            #rep data
        
            #cv2.putText(image, 'STAGE', (65,12),
            #        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        
            #cv2.putText(image, stage,
            #        (60,60),
            #        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
            # st.write('STAGE: ', stage)
            kpil2_text.write(f"<h1 style='text-align: center; color:red;'>{stage}</h1>", unsafe_allow_html=True)
        
            #Technique
            #cv2.putText(image, 'TECHNIQUE', (600,12),
            #        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        
            #cv2.putText(image, technique,
            #        (600,60),
            #        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

            #st.write('TECHNIQUE: ', technique)
            kpil3_text.write(f"<h1 style='text-align: center; color:red;'>{technique}</h1>", unsafe_allow_html=True)

            #Rendering
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(255,250,250), thickness=2, circle_radius=2),
                                        mp_drawing.DrawingSpec(color=(255,250,250), thickness=2, circle_radius=2) 
                                        )

            # FPS Counter
            currTime = time.time()
            fps = 1/(currTime - prevTime)
            prevTime = currTime

            print(fps)
                

            frame_ = cv2.resize(image,(0,0), fx=0.8, fy=0.8)
            frame = image_resize(image=frame_, width=640)
            stframe.image(frame_, channels='RGB', use_column_width=True)