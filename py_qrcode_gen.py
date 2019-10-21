from qrtools import QR
import pyqrcode 

txt  = "KATHIRESAN M\nTERAFAST NETWORKS PVT LTD\nCHENNAI - 600 0091"
url = pyqrcode.create(txt)
url.svg("QR.png", scale = 8)

