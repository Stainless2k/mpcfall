import pathlib

import requests as requests
import scrython

import image_utils

XML_FILE = 'cards_to_be.xml'
IMAGE_FOLDER: pathlib.Path = pathlib.Path('cards')
XML_END_STRING = f'''    </fronts>
    <cardback>1YLKR61hlmaBiHDRhhSQNlnDg6f8w8UjW</cardback>
</order>
'''


def generate_card_xml(card_name: str, index: int):
    return f'''        <card>
            <id>DoWeNeedThis</id>
            <slots>{index}</slots>
            <name>{card_name}.jpg</name>
            <query>DoWeNeedThis</query>
        </card>
'''


def generate_start_xml(quantity: int):
    # todo get bracket
    bracket = 18
    return f'''<order>
    <details>
        <quantity>{quantity}</quantity>
        <bracket>{bracket}</bracket>
        <stock>(S30) Standard Smooth</stock>
        <foil>false</foil>
    </details>
    <fronts>
'''


def download_image(card_name: str):
    card_url = scrython.cards.Named(exact=card_name).image_uris().get('png')
    img_data = requests.get(card_url).content
    with open(IMAGE_FOLDER / f'{card_name}.png', 'wb') as handler:
        handler.write(img_data)


def add_card_to_xml(card_name: str, index: int):
    with open(XML_FILE, 'a') as file:
        file.write(generate_card_xml(card_name, index))


def create_xml(quantity: int):
    with open(XML_FILE, 'w') as file:
        file.write(generate_start_xml(quantity))


def finish_xml():
    with open(XML_FILE, 'a') as file:
        file.write(XML_END_STRING)


if __name__ == '__main__':
    IMAGE_FOLDER.mkdir(exist_ok=True)

    create_xml(1)

    name = ['brainstorm', 'mox opal']
    for index, x in enumerate(name):
        download_image(x)
        add_card_to_xml(x, index)

    for x in IMAGE_FOLDER.glob('*.png'):
        image_utils.add_bleed(x)

    finish_xml()
