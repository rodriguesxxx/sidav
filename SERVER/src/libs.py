#EXTERNO
import cv2 as cv
import imutils
import numpy as np
import jinja2
import aiohttp_jinja2
import torch
from aiohttp import web
from aiohttp import WSMsgType
import queue
import asyncio

#NATIVO
from collections import deque
from argparse import ArgumentParser
from typing import Dict, Any
import os
import threading
import base64