# -*- coding: utf-8 -*-
import tensorflow as tf
import numpy as np
import cv2
import copy

import model_zoo

import argparse

import pyrealsense2 as rs

import time
import datetime

from gtts import gTTS
import os
from darknet.python.darknet import *
import requests

with open('category.txt') as f:
    lines = map(lambda x: x.strip(), f.readlines())

ix2label = dict(zip(range(len(list(lines))), lines))

cwd = os.getcwd()
model_path = os.path.join('save_model', 'jester-finetune')
