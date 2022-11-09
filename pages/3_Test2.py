import streamlit as st
import cv2, time
import mediapipe as mp
import numpy as np

st.set_option('deprecation.showfileUploaderEncoding', False)

use_webcam = st.sidebar.button('Use Webcam')


drawing_spec = mp.solutions.drawing_utils.DrawingSpec(thickness=2, circle_radius=1)

# Resize Images to fit Container
# @st.cache()
# # Get Image Dimensions
# def image_resize(image, width=None, height=None, inter=cv2.INSTER_AREA):
#     dim = None
#     (h,w) = image.shape[:2]

#     if width is None and height is None:
#         return image

#     if width is None:
#         r = width/float(w)
#         dim = (int(w*r),height)

#     else:
#         r = width/float(w)
#         dim = width, int(h*r)

#     # Resize image
#     resized = cv.resize(image,dim,interpolation=inter)

#     return resized





## Get Video
stframe = st.empty()


if use_webcam:
    video = cv2.VideoCapture(0)


width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps_input = int(video.get(cv2.CAP_PROP_FPS))


fps = 0
i = 0

## Face Mesh
with mp.solutions.face_mesh.FaceMesh(
    max_num_faces=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
    ) as face_mesh:

        prevTime = 0

        while video.isOpened():
            i +=1
            ret, frame = video.read()
            if not ret:
                continue


            results = face_mesh.process(frame)
            frame.flags.writeable = True

            face_count = 0
            if results.multi_face_landmarks:

                #Face Landmark Drawing
                for face_landmarks in results.multi_face_landmarks:
                    face_count += 1

                    mp.solutions.drawing_utils.draw_landmarks(
                        image=frame,
                        landmark_list=face_landmarks,
                        connections=mp.solutions.face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=drawing_spec,
                        connection_drawing_spec=drawing_spec
                        )

            # FPS Counter
            currTime = time.time()
            fps = 1/(currTime - prevTime)
            prevTime = currTime


            frame = cv2.resize(frame,(0,0), fx=0.8, fy=0.8)
            #frame = image_resize(image=frame, width=640)
            stframe.image(frame,channels='BGR', use_column_width=True)