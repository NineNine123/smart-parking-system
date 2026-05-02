# Install first:
# pip install qrcode[pil]

import qrcode

# Link you want the QR code to open
# url = "https://second-coping-reversal.ngrok-free.dev"

url = "https://smart-parking-system-qx7c.onrender.com"

# Create QR code
qr = qrcode.make(url)

# Save QR code image
qr.save("app.png")

print("QR code generated successfully as qrcode.png")