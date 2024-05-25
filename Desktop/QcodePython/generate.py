import qrcode

img = qrcode.make("https://t.me/danyafrontender")
type(img)
img.save("qrcode.png")