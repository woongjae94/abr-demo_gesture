from TF_model_cam import TFModel, CAM

import requests
import json
import numpy as np
import time
import socket
#from socket import *
import threading
#import multiprocessing

global data
data = 'None'
global send_count
send_count = 3

class Gesture:
    def main_loop(self):
        while True:
            self.run_demo()

    def run_demo(self):
        result = 'None'; confidence = 0.0
        frames = cam.get_frames(num=cam.args.video_length,
                                  fps=cam.args.fps,
                                  cam=0)
        
        if not frames:
            t_lock.acquire()
            global data
            global send_count
            data = "LostContact"
            send_count = 3
            t_lock.release()
            pass

        if frames and cam.center_detect and cam.move_detect:
            result, confidence, top_3 = model.run_demo_wrapper(np.expand_dims(frames,0))
            print("result :{}, confidence:{}, top_3:({})".format(result, confidence, top_3))
            
        if confidence > 0.5:
            #requests.get('http://192.168.0.21:3001/api/v1/actions/action/{}/{}_{}_{}_{}_{}'.format('home', result, confidence, 'phue_lamp', 'controlA', 'controlB'))
            t_lock.acquire()
            global data
            global send_count
            send_count = 3
            data = result
            t_lock.release()


def send_handler(client_socket):
    try:
        while True:
            t_lock.acquire()
            global send_count
            if send_count is not 0:
                global data
                senddata = 3*(data+'$')
                client_socket.send(senddata.encode('utf-8'))
            send_count = 0
            t_lock.release()
    except:
        client_socket.close()

if __name__ == '__main__':
    print("## load TF model")
    model = TFModel()
    print("## load complete\n## set camera")
    cam = CAM()
    print("## setting complete\n")
    multi_device = Gesture()

    server_ip = 'Localhost'
    port = 3019
    t_lock = threading.Lock()

    client = "Gesture"
    print("## try to connect socket server")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))
    client_socket.send(client.encode('utf-8'))
    print("connect complete")

    send_thread = threading.Thread(target=send_handler, args=(client_socket,))
    send_thread.daemon = True
    send_thread.start()
    print("## start socket thread")

    print("## start demo")
    multi_device.main_loop()