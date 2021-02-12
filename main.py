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
        self.set_request()

    def draw(self):
        # Запишем полученное изображение в файл.
        with open(self.map_file, "wb") as file:
            file.write(self.image.content)
        # копируем изображение
        screen.blit(pygame.image.load(self.map_file), (0, 0))

    def set_request(self):
        # запрос
        self.params = {"ll": ",".join([self.x, self.y]),
                       "spn": ",".join([self.spn, self.spn]),
                       "l": self.type}
        # запрос
        self.image = requests.get(API_SERVER, self.params)

    def update_spn(self, condition):
        # узменяем масштаб
        if condition == 'up':
            self.spn = str(float(self.spn) / 2)
        else:
            self.spn = str(float(self.spn) * 2)
        # проверяем масштаб
        if float(self.spn) > 127:
            self.spn = str(float(self.spn) / 2)
        elif float(self.spn) < 0.0005:
            self.spn = str(float(self.spn) * 2)

    def move(self, condition):
        # узнаем, куда двигаться и проверяем критические значения
        if condition == 'up' and float(self.y) + float(self.spn) / 2 < 80:
            self.y = str(float(self.y) + float(self.spn) / 2)
        elif condition == 'down' and float(self.y) - float(self.spn) / 2 > -80:
            self.y = str(float(self.y) - float(self.spn) / 2)
        elif condition == 'right' and float(self.x) + float(self.spn) / 2 < 80:
            self.x = str(float(self.x) + float(self.spn) / 2)
        elif condition == 'left' and float(self.x) - float(self.spn) / 2 > -80:
            self.x = str(float(self.x) - float(self.spn) / 2)


# инициализируем программу
running = True
map = Map('55.55', '55.55', '1')
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Карта')
# цикл программы
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # при нажатии на кнопки меняем масшатб
        if event.type == pygame.KEYUP and event.key == pygame.K_PAGEUP:
            map.update_spn('up')
            map.set_request()
        if event.type == pygame.KEYUP and event.key == pygame.K_PAGEDOWN:
            map.update_spn('down')
            map.set_request()
        # перемещение
        if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            map.move('up')
            map.set_request()
        if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            map.move('down')
            map.set_request()
        if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            map.move('left')
            map.set_request()
        if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            map.move('right')
            map.set_request()
    screen.fill((0, 0, 0))
    # отображаем карту
    map.draw()
    pygame.display.flip()
# удаляем файл и выходим
os.remove(map.map_file)
pygame.quit()
