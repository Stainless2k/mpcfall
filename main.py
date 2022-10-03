import multiprocessing
import pathlib
from typing import Optional

import requests
import scrython

import image_utils
import inference_realesrgan

IMAGE_FOLDER: pathlib.Path = pathlib.Path('cards')
CARDS_TXT: pathlib.Path = pathlib.Path('cards.txt')
CPUS_TO_USE = multiprocessing.cpu_count() - 1


def download_image(card_name: str, set_code: Optional[str]):
    if set_code is not None:
        try:
            card_url = scrython.cards.Named(exact=card_name, set=set_code).image_uris().get('png')
        except scrython.foundation.ScryfallError:
            card_url = scrython.cards.Named(exact=card_name).image_uris().get('png')
            set_code = 'NOT_FOUND_' + set_code
    else:
        card_url = scrython.cards.Named(exact=card_name).image_uris().get('png')
        set_code = ''

    img_data = requests.get(card_url).content
    with open(IMAGE_FOLDER / f'{card_name}_{set_code}.png', 'wb') as handler:
        handler.write(img_data)


def scale_images(image_path: pathlib.Path):
    output_path = image_path.parent / 'scaled' / image_path.name
    if not output_path.is_file():
        print('SCALING: ', image_path)
        # waifu2x.run(input_img_path=str(image_path), output_img_path=str(output_path))
        inference_realesrgan.run(input_path=str(image_path), output_path=str(output_path), outscale=2)
    else:
        print('SKIP SCALING: ', image_path)


if __name__ == '__main__':
    IMAGE_FOLDER.mkdir(exist_ok=True)
    names_and_set_codes = []

    with CARDS_TXT.open('r') as file:
        lines = file.readlines()
        for line in lines:
            split = line.split('|', maxsplit=1)
            if len(split) < 2:
                names_and_set_codes.append([split[0].strip(), None])
            else:
                names_and_set_codes.append([split[0].strip(), split[1].strip()])

    for name, code in names_and_set_codes:
        print('DOWNLOADING: ', f"{name} {code}")
        download_image(card_name=name, set_code=code)

    downloaded_images = IMAGE_FOLDER.glob('*.png')
    for img in downloaded_images:
        scale_images(img)

    for x in (IMAGE_FOLDER / 'scaled').glob('*.png'):
        print('Bleeding: ', x)
        image_utils.add_bleed(x)
