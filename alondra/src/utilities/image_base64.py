import os
import sys
import uuid
from PIL import Image, ImageOps
import StringIO
import base64
from django.conf import settings

def image_exists(image, id):
    image_path = "%s/uploads/%s/%s" % (
                  settings.MEDIA_ROOT,
                  str(id),
                  image
                )
    #print image_path
    return os.path.isfile(image_path)

def encode_image(image,id, width=50, height=50):
    image_path = "%s/uploads/%s/%s" % (
                  settings.MEDIA_ROOT,
                  str(id),
                  image
                )
   
    if os.path.isfile(image_path):
        x = Image.open(image_path)
        #change 50,50 for set with and height
        x.thumbnail((width,height), Image.ANTIALIAS)
    else:
        #change 50,50 for set with and height
        x = Image.new('RGB',(width,height))
    
    if x.mode not in ("L", "RGB"):
        x = x.convert("RGB")
    output = StringIO.StringIO()
    x.save(output, format='PNG')
    output.seek(0)
    output_s = output.read()
    b64 = base64.b64encode(output_s)
    output.close()
    return b64

def encode_image_2(image, width=50, height=50):
    image_path = "%s/%s" % (
                  settings.MEDIA_ROOT,
                  image
                )
   
    if os.path.isfile(image_path):
        x = Image.open(image_path)
        #change 50,50 for set with and height
        x.thumbnail((width,height), Image.ANTIALIAS)
    else:
        #change 50,50 for set with and height
        x = Image.new('RGB',(width,height))
    
    if x.mode not in ("L", "RGB"):
        x = x.convert("RGB")
    output = StringIO.StringIO()
    x.save(output, format='PNG')
    output.seek(0)
    output_s = output.read()
    b64 = base64.b64encode(output_s)
    output.close()
    return b64

def encode_image_3(image, width=50, height=50):
    image  = image.rsplit("/", 1)
    image_path = "%s%s" % (
                  settings.MEDIA_UPLOAD_ROOT,
                  image[1]
                )

    if os.path.isfile(image_path):
        x = Image.open(image_path)
        #change 50,50 for set with and height
        x.thumbnail((width,height), Image.ANTIALIAS)
    else:
        #change 50,50 for set with and height
        x = Image.new('RGB',(width,height))
    
    if x.mode not in ("L", "RGB"):
        x = x.convert("RGB")
    output = StringIO.StringIO()
    x.save(output, format='PNG')
    output.seek(0)
    output_s = output.read()
    b64 = base64.b64encode(output_s)
    output.close()
    return b64