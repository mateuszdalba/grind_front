from threading import Thread
import cv2, time

# defining a helper class for implementing multi-threading 
class WebcamStream:
    # initialization method 
    def __init__(self, stream_id=0):
        self.stream_id = stream_id #default is 0 for main camera 
        
        # opening video capture stream 
        self.vcap = cv2.VideoCapture(self.stream_id)

        #self.vcap.set(cv2.CAP_PROP_FRAME_WIDTH, W)
        #self.vcap.set(cv2.CAP_PROP_FRAME_HEIGHT, H)
        #self.vcap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        #self.vcap.set(cv2.CAP_PROP_FPS, 30)
            
        # reading a single frame from vcap stream for initializing 
        self.grabbed , self.frame = self.vcap.read()
        if self.grabbed is False :
            print('[Exiting] No more frames to read')
            exit(0)
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

