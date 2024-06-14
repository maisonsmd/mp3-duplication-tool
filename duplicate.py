#!/bin/env python3

import shutil, sys, os, random

# for mp3 metadata manipulation
from mutagen.id3 import ID3, APIC, TRCK, TDRC, TIT2, TALB, TPE1, TCON

# for drawing images
from PIL import Image, ImageDraw, ImageFont

def main():
    if len(sys.argv) != 2:
        print('Need 1 argument: number of songs to duplicate')
        exit()

    number_of_songs = int(sys.argv[1])
    if number_of_songs <= 0:
        exit()

    print(f'Duplicating {number_of_songs} songs')

    def get_random_color():
        r = random.randint(0,100)
        g = random.randint(0,100)
        b = random.randint(0,100)
        return (r, g, b, 255)

    def get_inverted_color(color):
        r, g, b, _ = color
        return (255 - r, 255 - g, 255 - b, 255)

    def get_image(text):
        size = (500, 500)
        bg = get_random_color()
        fg = get_inverted_color(bg)

        img = Image.new("RGB", size, color=bg)

        draw = ImageDraw.Draw(img)
        draw.rectangle((0, 0) + size, outline=fg, width=20)

        fnt = ImageFont.truetype("C:\Windows\Fonts\consola.ttf", 150)
        draw.text((80, 170), text, font=fnt, fill=fg)

        return img

    os.makedirs('out', exist_ok=True)
    for i in range(1, number_of_songs + 1):
        padded_number = str(i).zfill(4) # 4 digits number with zero padding
        title = f'#{padded_number} This is a test track'
        new_file = f'out\{title}.mp3'

        print(new_file)

        # duplicate the file
        shutil.copy('_original.mp3', new_file)

        tags = ID3(new_file)
        tags.clear()

        image = get_image(padded_number)
        image.save('_temp.jpg')

        # exit()
        tags.add(APIC(
            encoding=3,
            mime='image/jpg',
            type=3, desc=u'Cover',
            data=open('_temp.jpg', 'rb').read()
        ))

        # change its property
        tags.add(TRCK(encoding=3, text=f'{i}'))                         # track number
        tags.add(TDRC(encoding=3, text='2022'))                         # year
        tags.add(TIT2(encoding=3, text='Title of ' + title))            # title
        tags.add(TALB(encoding=3, text=f'Test album #{i}'))             # album
        tags.add(TPE1(encoding=3, text=f'Test artist #{i}'))            # artist
        tags.add(TCON(encoding=3, text=f'Test Genre #{i}'))             # genre

        tags.save()
        os.remove('_temp.jpg')

if __name__ == 'main':
    main()