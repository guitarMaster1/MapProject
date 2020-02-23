import os
import sys
from io import BytesIO

import pygame
import requests
from PIL import Image

pygame.init()

WIDTH, HEIGHT = 650, 450

toponym_to_find = 'Москва Троицк Сиреневый 15'


def get_request(toponym):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        print('Error:', response.text)

    return response.json()


toponym = \
    get_request(toponym_to_find)["response"]["GeoObjectCollection"]["featureMember"][0][
        "GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

delta = "0.02"

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "l": "map",
    "z": 14
}


def send_request(params):
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=params)
    img = Image.open(BytesIO(response.content))
    img.save('1.png')


pygame.init()
# размеры окна:
size = WIDTH, HEIGHT
# screen — холст, на котором нужно рисовать:
screen = pygame.display.set_mode(size)
w = pygame.Color('white')


def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def draw():
    screen.fill((0, 0, 0))
    screen.blit(pygame.transform.scale(load_image('1.png'), (WIDTH, HEIGHT)), (0, 0))


send_request(map_params)
draw()

while pygame.event.wait().type != pygame.QUIT:
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_PAGEUP]:
            send_request(map_params)
            print('send')
            map_params['z'] -= 1 if map_params['z'] > 1 else 0
        if keys[pygame.K_PAGEDOWN]:
            send_request(map_params)
            print('send')
            map_params['z'] += 1
        draw()
        pygame.display.flip()
pygame.quit()
