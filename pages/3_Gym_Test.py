import streamlit as st
import cv2, time
import mediapipe as mp
import numpy as np
from threading import Thread
from functions.utilities import calculate_angle, image_resize
from camera import WebcamStream, CustomSquats
from functions.css import include_custom_styling
from queue import Queue


include_custom_styling()

use_webcam = st.button('Use Webcam')

#mp_drawing = mp.solutions.drawing_utils
#mp_pose = mp.solutions.pose

W, H = 1920, 1080


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
    prevTime = 0

    obj_squats = CustomSquats()


    que = Queue()
    t = Thread(target = lambda q, video: q.put(obj_squats.process(video)), args=(que,) )
    t.start()
    t.join()
    
    result = que.get()
    print(result)

    
    #image = obj1.process(video)



    

         
    #kpil_text.write(f"<h1 style='text-align: center; color:red;'>{str(counter)}</h1>", unsafe_allow_html=True)
                
                
    # st.write('STAGE: ', stage)
    #kpil2_text.write(f"<h1 style='text-align: center; color:red;'>{stage}</h1>", unsafe_allow_html=True)
        

    ##st.write('TECHNIQUE: ', technique)
    #kpil3_text.write(f"<h1 style='text-align: center; color:red;'>{technique}</h1>", unsafe_allow_html=True)



    # FPS Counter
    currTime = time.time()
    fps = 1/(currTime - prevTime)
    prevTime = currTime

    print(fps)
                

    frame_ = cv2.resize(image,(0,0), fx=0.8, fy=0.8)
    frame = image_resize(image=frame_, width=640)
    stframe.image(frame_, channels='RGB', use_column_width=True)