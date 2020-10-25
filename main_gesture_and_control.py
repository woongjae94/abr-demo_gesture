from TF_model_cam import TFModel, CAM

import requests
import json
import numpy as np
import time
from socket import *


class Test:
    def main_loop(self):

        while True:
            self.run_demo()

    def run_demo(self):
        result = 'None'; confidence = 0.0
        frames = cam.get_frames(num=cam.args.video_length,
                                  fps=cam.args.fps,
                                  cam=0)

        if frames and cam.center_detect and cam.move_detect:
            result, confidence, top_3 = model.run_demo_wrapper(np.expand_dims(frames,0))
            print("result :{}, confidence:{}, top_3:({})".format(result, confidence, top_3))
            
        if confidence > 0.7:    
            requests.get('http://192.168.0.21:3001/api/v1/actions/action/{}/{}_{}_{}_{}_{}'.format('home', result, confidence, 'device', 'controlA', 'controlB'))


        # if confidence > 0.3 and result!='Doing other things':
        #     self.activation, self.device_status, paramA, paramB = self.response(result)

        #     print('home', self.device, self.device_status, paramA, paramB, result)

        else:
            result = 'Waiting...'

        # if not eval(cam.args.debug) and result != 'Waiting...':
        
        #     #print('control')
        #     # to main controller...
        #     try:
        #         #print('test')
        #         #requests.get(
        #         #'https://ceslea.ml:50001/api/v1/actions/action/{}/{}'.format('home', result)) # ceslea.ml > domain error
        #         # requests.get('http://192.168.0.4:3001/api/v1/actions/action/{}/{}_{}_{}_{}_{}'.format('home', self.device, self.device_status, paramA, paramB, result))
        #         requests.get('http://192.168.0.21:3001/api/v1/actions/action/{}/{}_{}_{}_{}_{}'.format('home', self.device, self.device_status, paramA, paramB, result))
        
        #     except:
        #         pass
        
        # # to local webdemo page...
        # requests.get(
        #     'http://127.0.0.1:5000/state/set/gesture',params={'gesture': result})
        # # time.sleep(0.5)


if __name__ == '__main__':
    print("## load TF model")
    model = TFModel()
    print("## load complete\n## set camera")
    cam = CAM()
    print("## setting complete\n## connect controlable devices")
    multi_device = Test()

    print("## connect complete\n## start demo")
    multi_device.main_loop()