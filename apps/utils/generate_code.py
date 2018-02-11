"""
生成一个带有logo的二维码
"""

import qrcode
from PIL import Image, ImageDraw, ImageFont
import os


def gener_qrcode(string, path, logo=''):
    """
    生成中间带有logo的二维码，需要安装qrcode,PIL库，
    :param string: 二维码字符串
    :param path: 生成的二维码保护路径
    :param logo: logo文件的路径
    """
    # 生成二维码
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,box_size=8,border=1
    )
    qr.add_data(string)
    qr.make(fit=True)

    img_cord = qr.make_image()
    img_cord = img_cord.convert("RGBA")
    # 生成背景图
    back_img = Image.new("RGB", (200, 300), 0xffffff)
    # 调整二维码尺寸
    img_h = 160
    img_w = 160
    img_cord = img_cord.resize((img_w, img_h), Image.ANTIALIAS)
    # 把二维码贴到背景的 (20，100)坐标处
    back_img = back_img.convert("RGBA")
    back_img.paste(img_cord, (20, 100), img_cord)
    # 在背景图贴水印
    txt = '扫一扫上面二维码图案加我微信'  # 水印字
    print(type(txt))

    #font = ImageFont.truetype("symbol.ttf", 16, encoding="symb")  # 字体

    uni_text = txt.encode('utf-8').decode('unicode_escape')

    draw = ImageDraw.Draw(back_img)

    draw.text((60, 270), uni_text, fill='red')

    if logo and os.path.exists(logo):
        img_icon = Image.open(logo)
        img_w, img_h = img_cord.size  # 二维码的长和宽

        factor = 2
        size_w = int(img_w/factor)  # 缩小4倍
        size_h = int(img_h/factor)  # 缩小4倍

        icon_w, icon_h = img_icon.size  # logo的长和宽

        if icon_w > size_w:    # 如果logo的宽比二维码宽，那么就和二维码一样大
            icon_w=size_w
        if icon_h > size_h:   # 如果logo的高比二维码高，则就和二维码一样高
            icon_h = size_h
        img_icon = img_icon.resize((icon_w, icon_h), Image.ANTIALIAS)

        w = int((img_w-icon_w) / 2)
        h = int((img_h-icon_h) / 2)
        img_icon = img_icon.convert("RGBA")
        img_cord.paste(img_icon, (w, h), img_icon)

    back_img.show()
    img_cord.save(path)

if __name__ == "__main__":
    gener_qrcode("http://www.toutiao.com", "qr.png", "log.png")
