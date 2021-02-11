import pygame
import requests
import os
API_SERVER = "http://static-maps.yandex.ru/1.x"


class Map:
    def __init__(self, x, y, spn):
        # указываем параметры
        self.x = x
        self.y = y
        self.spn = spn
        self.type = 'map'
        self.map_file = "map.png"
        self.params = {"ll": ",".join([self.x, self.y]),
                       "spn": ",".join([self.spn, self.spn]),
                       "l": self.type}
        # запрос
        self.image = requests.get(API_SERVER, self.params)

    def draw(self):
        # Запишем полученное изображение в файл.
        with open(self.map_file, "wb") as file:
            file.write(self.image.content)
        # копируем изображение
        screen.blit(pygame.image.load(self.map_file), (0, 0))


# инициализируем программу
running = True
map = Map('55.55', '55.55', '0.2')
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Карта')
# цикл программы
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    # отображаем карту
    map.draw()
    pygame.display.flip()
# удаляем файл и выходим
os.remove(map.map_file)
pygame.quit()
