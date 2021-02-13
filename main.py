import pygame
import requests
import pygame_gui
import os
API_SERVER = "http://static-maps.yandex.ru/1.x"
API_SERVER_GEOCODE = 'http://geocode-maps.yandex.ru/1.x/'
API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'


class Map:
    def __init__(self, x, y, spn):
        # указываем параметры
        self.x = x
        self.y = y
        self.spn = spn
        self.type = 'map'
        self.types = ['map', 'sat', 'sat,skl']
        self.map_file = "map.png"
        self.btn = Button()
        self.manager = pygame_gui.UIManager((600, 400))
        self.btn_del = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 60), (150, 50)),
            manager=self.manager,
            text='Сбросить точку'
        )
        self.entry = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((0, 30), (150, 50)), manager=self.manager
        )
        self.postal_menu = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
            options_list=['Без индекса', 'С индексом'], starting_option='Без индекса',
            relative_rect=pygame.Rect((0, 330), (150, 25)), manager=self.manager
        )
        self.points = []
        self.points_address = []
        self.postal_code = False
        self.set_request()

    def draw(self):
        # Запишем полученное изображение в файл.
        with open(self.map_file, "wb") as file:
            file.write(self.image.content)
        # копируем изображение
        screen.blit(pygame.image.load(self.map_file), (0, 0))
        screen.blit(self.btn.text, (0, 0))
        pygame.draw.rect(screen, (128, 128, 128), (0, 380, 600, 400), 0)
        # если есть адресс - выводим
        if self.points_address:
            # проверяем наличие почтового индекса
            if len(self.points_address[-1]) == 2 and self.postal_code:
                address = ', '.join(self.points_address[-1])
            else:
                address = self.points_address[-1][0]
            font = pygame.font.Font(None, 20)
            text = font.render(address, 1, (0, 0, 0))
            screen.blit(text, (0, 380))

    def set_request(self):
        # запрос
        self.params = {"ll": ",".join([self.x, self.y]),
                       "spn": ",".join([self.spn, self.spn]),
                       "l": self.type}
        # если есть точки - указываем их
        if self.points:
            self.params['pt'] = '~'.join(self.points)
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

    def update_type(self):
        self.btn.set_text()
        for i in range(len(self.types)):
            if self.type == self.types[i]:
                self.type = self.types[(i + 1) % 3]
                break

    def search(self, obj):
        try:
            # ищем объект
            geocoder_params = {
                "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                "geocode": obj,
                "format": "json"}
            response = requests.get(API_SERVER_GEOCODE, params=geocoder_params)
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"][
                "featureMember"][0]["GeoObject"]
            # получаем координаты объекта
            self.x, self.y = toponym["Point"]["pos"].split(" ")
            # добавляем координаты
            self.points.append(f'{self.x},{self.y}')
            # добавляем в список адресс
            self.points_address.append([toponym['metaDataProperty']['GeocoderMetaData']
                                       ['Address']['formatted']])
            # добавляем почтовый индекс
            self.points_address[-1].append(toponym['metaDataProperty']['GeocoderMetaData']
                                           ['Address']['postal_code'])
        except Exception:
            pass

    def del_point(self):
        # удаляем последнюю точку
        if self.points:
            del self.points[-2:]
            del self.points_address[-2:]


class Button:
    def __init__(self):
        self.texts = ['схема', 'спутник', 'гибрид']
        self.text_btn = self.texts[0]
        # инициализация переключателя
        self.font = pygame.font.Font(None, 30)
        self.text = self.font.render(self.text_btn, 1, (0, 0, 0))
        self.w = self.text.get_width()
        self.h = self.text.get_height()

    def set_text(self):
        for i in range(len(self.texts)):
            if self.text_btn == self.texts[i]:
                self.text_btn = self.texts[(i + 1) % 3]
                break
        self.text = self.font.render(self.text_btn, 1, (0, 0, 0))
        self.w = self.text.get_width()
        self.h = self.text.get_height()


# инициализируем программу
pygame.init()
running = True
map = Map('55.55', '55.55', '1')
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Карта')
clock = pygame.time.Clock()
# цикл программы
while running:
    time_delta = clock.tick(60) / 1000.0
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
        # Проверяем кнопку, отвечиющую за смену типа карты
        if event.type == pygame.MOUSEBUTTONDOWN and \
                (0 <= event.pos[0] <= map.btn.w and 0 <= event.pos[1] <= map.btn.h):
            map.update_type()
            map.set_request()
        # Проверяем ввод для поиска
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                map.search(event.text)
                map.set_request()
                break
            # проверяем нажатие кнопки для удаления точек
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == map.btn_del:
                    map.del_point()
                    map.set_request()
                    break
            # проверяем изменения
            if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                map.postal_code = True if event.text == 'С индексом' else False
        map.manager.process_events(event)
    map.manager.update(time_delta)
    screen.fill((0, 0, 0))
    # отображаем карту
    map.draw()
    map.manager.draw_ui(screen)
    pygame.display.flip()
    clock.tick(60)
# удаляем файл и выходим
os.remove(map.map_file)
pygame.quit()
