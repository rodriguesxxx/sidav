#EXTERNO
import cv2 as cv
import imutils
import numpy as np
import jinja2
import aiohttp_jinja2
import torch
from aiohttp import web

#NATIVO
from collections import deque
from argparse import ArgumentParser
from typing import Dict, Any