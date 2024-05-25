import cv2

img = cv2.imread("qrcode.png")
detect = cv2.QRCodeDetector()
value, _, _ = detect.detectAndDecode(img)
print(value)