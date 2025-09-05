import svgpathtools as svg  
from scipy.interpolate import splprep, splev
import cv2
import numpy as np
import numpy as np
from scipy.optimize import minimize
import requests
from algorithm.pngtosvg.superResolution import super_resolution_predict
SR_MODEL = r"algorithm/pngtosvg/0925-x4_rep_epoch151_x4.pth"
sr_model = super_resolution_predict(SR_MODEL)
import cv2.mat_wrapper
from scipy import stats
from typing import Iterable
from PIL import Image
import vtracer


# waifu2x_init = Waifu2x(gpuid=0, scale=2, noise=3)
def resize_max(image:np.array, max_size: int = 2048):
    height, width = image.shape[:2]
    
    # 计算缩放比例
    if max(height, width) > max_size:
        if height > width:
            scale = max_size / height
        else:
            scale = max_size / width
    else:
        return image
    
    # 缩放图片
    resized_img = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    
    return resized_img


def RGB_to_Hex(rgb):
    strs = '#'
    for i in rgb:
        num = int(i) 
        strs += str(hex(num))[-2:].replace('x', '0').upper()
    return strs


def png2svg_vtracer(image):
    img = Image.fromarray(cv2.cvtColor(image,cv2.COLOR_BGRA2RGBA)) 
    pixels: list[tuple[int, int, int, int]] = list(img.getdata())
    svg_str: str = vtracer.convert_pixels_to_svg(pixels,size=(img.size[0],img.size[1]))

    return svg_str

def shift_demo(image):   #均值迁移
    image_rgb = image[:,:,:3]

    image_a = image[:,:,3]
    image_rgb = cv2.pyrMeanShiftFiltering(image_rgb, 10, 50)
    image[:,:,:3] = image_rgb

    binary_alpha = np.where(image_a < 127, 0, 255).astype(np.uint8)
    image[:,:,3] = binary_alpha

    return image

   
def change_channel(image):
    if len(image.shape) == 2:
        image = cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)
    
    is_background = 0
    bg_color = "#000"
    if image.shape[2] == 3:
        b, g, r = image[0,0]
        bg_color = RGB_to_Hex([r,g,b])
        image = cv2.cvtColor(image,cv2.COLOR_BGR2BGRA)
        is_background = 1 
    elif image.shape[2] == 4 and not np.any(image[:,:,-1] == 0):
        b, g, r, a = image[0,0]
        bg_color = RGB_to_Hex([r,g,b])
        image = cv2.cvtColor(image,cv2.COLOR_BGR2BGRA)
        is_background = 1 
    else:
        image = cv2.copyMakeBorder(image,10,10,10,10,cv2.BORDER_CONSTANT,value=(0,0,0,0))
    return is_background,bg_color,image
    

def upscale2x(image):
    image_rgb = image[:,:,:3]
    
    image_rgb = sr_model.forward(image[:,:,:3])

    image = cv2.resize(image,dsize=None,fx=4,fy=4, interpolation=cv2.INTER_LINEAR)

    image[:,:,:3] = image_rgb
    return image

def getlogo(logo_url):
    
    image_np = np.frombuffer(requests.get(logo_url, timeout=30).content, dtype=np.uint8)
    logo = cv2.imdecode(image_np, cv2.IMREAD_UNCHANGED)
    if logo.dtype != np.uint8:
        logo = cv2.normalize(logo, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    return logo

def bitmap_to_bezier(logo_url):
    image = getlogo(logo_url)  
    is_background,bg_color,image = change_channel(image)
    image = resize_max(image, max_size=2048)
    while min(image.shape[0],image.shape[1]) < 300:
        image = upscale2x(image)
    svg_content = png2svg_vtracer(image)
    return svg_content
