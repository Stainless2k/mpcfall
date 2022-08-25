import pathlib

import requests
import scrython
import waifu2x

import image_utils

IMAGE_FOLDER: pathlib.Path = pathlib.Path('cards')
CARDS_TXT: pathlib.Path = pathlib.Path('cards.txt')


def download_image(card_name: str):
    card_url = scrython.cards.Named(exact=card_name).image_uris().get('png')
    img_data = requests.get(card_url).content
    with open(IMAGE_FOLDER / f'{card_name}.png', 'wb') as handler:
        handler.write(img_data)


if __name__ == '__main__':
    IMAGE_FOLDER.mkdir(exist_ok=True)

    with CARDS_TXT.open('r') as file:
        names = file.readlines()

    for x in names:
        print('DOWNLOADING: ', x)
        download_image(x)

    for x in IMAGE_FOLDER.glob('*.png'):
        output = x.parent / 'scaled' / x.name
        if not output.is_file():
            print('SCALING: ', x)
            waifu2x.run(input_img_path=str(x), output_img_path=str(x.parent / 'scaled' / x.name))
        else:
            print('SKIP SCALING: ', x)

    for x in (IMAGE_FOLDER / 'scaled').glob('*.png'):
        print('BLEEDING: ', x)
        image_utils.add_bleed(x)
