import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av


flip = st.checkbox("Flip")

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")

    flipped = img[::-1,:,:] if flip else img
    #image processing

    return av.VideoFrame.from_ndarray(flipped, format="bgr24")


webrtc_streamer(key="example", video_frame_callback=video_frame_callback, media_stream_constraints= {"video": 
                                                                                {"width": {"ideal": 1920, "min": 1280}, 
                                                                                "height": {"ideal": 1080, "min": 720}}})

                                                                                