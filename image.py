from PIL import Image
dotsider = Image.open('/home/sean/projects/huck-the-hogs/images/dotsider.png')
nodotsider = Image.open('/home/sean/projects/huck-the-hogs/images/nodotsider.png')

def get_concat_h(image1, image2):
    dst = Image.new('RGB', (image1.width + image2.width, image1.height))
    dst.paste(image1, (0, 0))
    dst.paste(image2, (image1.width, 0))
    return dst

get_concat_h(dotsider, nodotsider).save('/home/sean/projects/huck-the-hogs/images/concat.png')
