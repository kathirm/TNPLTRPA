import base64

img_data="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"

with open("imageToSave.png", "wb") as fh:
        fh.write(base64.decodestring(img_data))