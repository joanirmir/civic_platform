import base64

# Read the image file as binary
with open('/home/user/Downloads/image.png', 'rb') as image_file:
    image_data = image_file.read()

# Encode the image data as base64
base64_image = base64.b64encode(image_data).decode('utf-8')

print(base64_image)