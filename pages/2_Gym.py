import streamlit as st
import cv2, time
import mediapipe as mp
import numpy as np
from threading import Thread
from functions.utilities import calculate_angle, image_resize
from camera import WebcamStream
from functions.css import include_custom_styling

st.set_page_config(page_title='Grind', page_icon=":shark:", layout="wide")

include_custom_styling()

use_webcam = st.button('Start Training')

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

## Get Video

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown('<h1>Here is virtual gym <br> Ye it feel so good to train <br> online while COVID </h1>', unsafe_allow_html=True)

with col2:
    stframe = st.empty()

with col3:
    st.markdown('<h1>Reps</h1>', unsafe_allow_html=True)
    kpil_text = st.markdown('<h1>0</h1>', unsafe_allow_html=True)

    
    st.markdown('<h1>Stage</h1>', unsafe_allow_html=True)
    kpil2_text = st.markdown('<h1>None</h1>', unsafe_allow_html=True)

    
    st.markdown('<h1>Technique</h1>', unsafe_allow_html=True)
    kpil3_text = st.markdown('<h1>None</h1>', unsafe_allow_html=True)


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

         
            kpil_text.write(f"<h1>{str(counter)}</h1>", unsafe_allow_html=True)
                
                
            # st.write('STAGE: ', stage)
            kpil2_text.write(f"<h1>{stage}</h1>", unsafe_allow_html=True)
        

            #st.write('TECHNIQUE: ', technique)
            kpil3_text.write(f"<h1>{technique}</h1>", unsafe_allow_html=True)

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
            #frame = image_resize(image=frame_, width=500, height=1000)
            stframe.image(frame_, channels='RGB', use_column_width=True)