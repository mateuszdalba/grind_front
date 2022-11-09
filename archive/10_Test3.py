import streamlit as st
import av
import cv2
from streamlit_webrtc import VideoProcessorBase, WebRtcMode, webrtc_streamer
from functions.squats import squats

flip = st.checkbox("Flip")

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")

    #flipped = img[::-1,:,:] if flip else img
    #image processing

    flipped = squats(img)


    return av.VideoFrame.from_ndarray(flipped, format="bgr24")


# webrtc_streamer(key="example", video_frame_callback=video_frame_callback,
#                 rtc_configuration={  # Add this config
#                 "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
#             async_processing=True,
#             media_stream_constraints={"video": 
#                                                 {"width": {"min": 1280}, 
#                                                 "height": {"min": 720}},
#                                         "audio": False,
#                                         })



webrtc_streamer(key='example',
                video_frame_callback=video_frame_callback,
                async_processing=True,
                media_stream_constraints={"video": 
                                                {"width": {"min": 1920}, 
                                                "height": {"min": 1080}},
                                        "audio": False})    