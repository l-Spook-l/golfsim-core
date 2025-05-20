import asyncio

# Сторонние библиотеки
import cv2
import cvzone

# Локальные модули
import find_angle
from data_base.config_db import async_session_maker
from data_base.db import DataBase
from config import hsvVals, frames_in_second, myColorFinder, min_area
from config import cap
"""
Посчитать сколько пикселей проходишь по горизонтали 
Посчитать сколько пикселей проходишь по вертикали
сложить и получить ответ
"""


# X - horizont
# Y - vertical

# =====================================================================================================================

async def add_data_db(shot_result: dict):
    # Получаем сессию
    async with async_session_maker() as session:
        # Вызываем метод add_data с передачей сессии
        success = await DataBase.add_data(shot_result, session=session)
        if success:
            print("Data added successfully")
        else:
            print("Failed to add data")


async def find_golf_ball(name_vidio_file: str = None):
    # cap = cv2.VideoCapture(f'folder_test_all_open/{name_vidio_file}')

    # Список для позиций
    pos_list = []
    # Счетчик списков которые были сохранены
    list_counter = 1
    # Счетчик количества координат, -1 для лучшего обращения к списку
    counter = -1
    # Дистанция в пикселях по горизонтали (X) (вперед) и по вертикали (Y) (вверх)
    distance_pix_x, distance_pix_y = 0, 0
    # Дистанция по осям (X, Y)
    distance_cm_x, distance_cm_y = 0, 0
    # Для сохранения расстояния по горизонтали (X)
    distance_list_x = []
    # Для сохранения расстояния по вертикали (Y)
    distance_list_y = []
    # Скорость по осям X и Y, максимальная скорость
    speed, speed_x, speed_y, max_speed = 0, 0, 0, 0
    # Список для определения угла
    coordinates_angle = []
    # Для проверки на новые координаты
    len_pos_list = 0
    # Счетчик кадров
    frame_count = 0
    # Время в секундах
    seconds = 0
    # Список времени
    # timeList = []

    fps = frames_in_second["fps_240"]

    import datetime

    now = datetime.datetime.now()
    # def find_golf_ball():
    try:
        while True:
            # Обновляем счетчик кадров
            frame_count += 1

            # Время на 1 кадр
            seconds += fps  # Для 240FPS
            # timeList.append(seconds)  # Добавление времени кадра в список

            print(f'Кадр - {frame_count}')
            print(f'Время - {seconds} s')
            print('-----------------------')
            # print(f'Список времени - {timeList}')

            # Рисунок для определения цвета мяча
            # img = cv2.imread("image/Ball_test_img.png")
            success, img = cap.read()
            # if not success:
            #     print(f"Конец видео или ошибка чтения кадра. Обработано {frame_count} кадров.")
            #     break
            # Находим цвет мяча
            imgColor, mask = myColorFinder.update(img, hsvVals)

            # Обводим контур мяча (находим самый большой контур, или чувствительность)
            # imgContours, contours, www, my_area = cvzone.findContours(img, mask, minArea=2500)  # Для 30FPS и (60 FPS ?)
            # imgContours, contours, my_area = cvzone.findContours(img, mask, minArea=7000)  # Для 120FPS
            # imgContours, contours = cvzone.findContours(img, mask, minArea=1000)  # Для 120FPS
            # imgContours, contours = cvzone.findContours(img, mask, minArea=5000)  # Для 240FPS
            # imgContours, contours, www, my_area = cvzone.findContours(img, mask, minArea=3800)  # Онлайн камера 50см
            # imgContours, contours = cvzone.findContours(img, mask, minArea=3800)  # Онлайн камера 50см
            # imgContours, contours, www, my_area = cvzone.findContours(img, mask, minArea=1300)  # Онлайн камера 40см
            # imgContours, contours, width, high = cvzone.findContours(img, mask, minArea=1000)  # Для 240FPS

            # print('ширина квадрата = ', width)
            # print('высота квадрата = ', high)
            imgContours, contours, width, high, area = cvzone.findContours(img, mask, minArea=min_area)  # Для 240FPS
            print('ширина квадрата = ', width)
            print('высота квадрата = ', high)
            print('площадь квадрата = ', area)
            # print('imgContours', type(imgContours), imgContours)
            # print('ширина квадрата = ', www)  # надо чтобы возвращалось 4 аргумента, а не 2 (findContours)
            # print('площадь квадрата = ', my_area)

            if contours:
                # Координаты мяча
                if contours[0]['center'] not in pos_list:
                    # Добавляем найденные координаты в список
                    pos_list.append(contours[0]['center'])
                    # Счетчик количества координат
                    counter += 1
                print('список координат = ', pos_list)  # список координат
                # print('counter = ', counter)
                print('Координаты = ', contours[0]['center'])
                # Если в списке координат что-то есть выводим разницу между пикселями
                if len(pos_list) != 0:
                    if len_pos_list < len(pos_list):
                        # Обновляем счетчик длинны списка
                        len_pos_list = len(pos_list)
                        # Определяем пройденную длину в пикселях по горизонтали (X) (Вычитаем прошлую координату с текущей)
                        distance_pix_x += pos_list[counter][0] - pos_list[counter - 1][0]
                        # Определяем пройденную длину в пикселях по вертикали (Y) (Вычитаем прошлую координату с текущей)
                        distance_pix_y += pos_list[counter - 1][1] - pos_list[counter][1]
                        # Определяем пройденную длину по горизонтали (X) в сантиметрах
                        # (Делим пройденную длину за один кадр в пикселях на 30 (1см - 30пикселей)
                        distance_cm_x = distance_pix_x / 30  # 30 - для 120FPS и 240FPS, 10 - для (60 live) или (30 хз)
                        # Определяем пройденную длину по вертикали (Y) в сантиметрах
                        distance_cm_y = distance_pix_y / 30  # 30 - для 120FPS и 240FPS, 10 - для (60 live) или (30 хз)
                        # Добавление дистанции в список по горизонтали (X)
                        distance_list_x.append(distance_cm_x)
                        # Добавление дистанции в список по вертикали (Y)
                        distance_list_y.append(distance_cm_y)
                        # Определяем скорость (скорость = расстояние / время), по осям X и Y
                        speed_x = ((distance_cm_x - distance_list_x[len(distance_list_x) - 2]) / fps) / 100
                        speed_y = ((distance_cm_y - distance_list_y[len(distance_list_y) - 2]) / fps) / 100
                        # Получаем общую скорость, складывая скорости по осям X и Y
                        # Speed = Speed_X + Speed_Y
                        # Реальная скорость тела в некоторый момент времени - это
                        # векторная сумма горизонтальной составляющей скорости Vx и вертикальной скорости Vy.
                        # V = √(Vx² + Vy²)
                        speed = ((speed_x ** 2) + (speed_y ** 2)) ** 0.5

                        # Находим максимальную скорость
                        if speed > max_speed:
                            max_speed = round(speed, 2)

                    print()
                    print('Количество пикселей по X = ', pos_list[counter][0] - pos_list[counter - 1][0])
                    print('Количество пикселей по Y = ', pos_list[counter - 1][1] - pos_list[counter][1])
                    print()
                    print(f'Дистанция по оси X = {distance_pix_x} пикселей')
                    print(f'Дистанция по оси Y = {distance_pix_y} пикселей')
                    print()
                    print(f'Дистанция по оси X = {distance_cm_x} см')
                    print(f'Дистанция по оси Y = {distance_cm_y} см')
                    print()

                    # print(f'Дистанция = {distanceCm} см')
                    # print(f'Дистанция список X = {distanceList_X}')
                    # print(f'Дистанция список Y = {distanceList_Y}')

                    # Смотрим на пройденной расстояния за 1 кадр по осям (Вычитаем текущую дистанцию от прошлой)
                    print(
                        f'Пройденное расстояние за 1 кадр по оси X = {distance_cm_x - distance_list_x[len(distance_list_x) - 2]}')
                    print(
                        f'Пройденное расстояние за 1 кадр по оси Y = {distance_cm_y - distance_list_y[len(distance_list_y) - 2]}')
                    print()
                    # Скорость
                    print(
                        f'Скорость по оси X = {(distance_cm_x - distance_list_x[len(distance_list_x) - 2])} cm / {fps} s = '
                        f'{(distance_cm_x - distance_list_x[len(distance_list_x) - 2]) / fps}')
                    print(
                        f'Скорость по оси Y = {(distance_cm_y - distance_list_y[len(distance_list_y) - 2])} cm / {fps} s = '
                        f'{(distance_cm_y - distance_list_y[len(distance_list_y) - 2]) / fps}')
                    print()
                    print(f'Скорость по оси X = {speed_x} m/s')
                    print(f'Скорость по оси Y = {speed_y} m/s')
                    print(f'Скорость {speed} m/s')
                    print(f'Макс. скорость {max_speed} m/s')

                for i, pos in enumerate(pos_list):
                    # Рисуем точку в найденных координатах
                    cv2.circle(imgContours, pos, 5, (0, 255, 9), cv2.FILLED)
                    if i == 0:
                        cv2.line(imgContours, pos, pos, (0, 255, 0), 5)
                    else:
                        cv2.line(imgContours, pos, (pos_list[i - 1]), (0, 255, 0), 2)

            # Если мяч не найден и список координат больше 10, то сохраняем данные в блокнот и очищаем список
            elif len(pos_list) > 10:
                # передаем последние две координаты для определения угла

                # берем 7й кадр и последний
                # pos_list[7]  pos_list[-1]   [pos_list[-1][0], pos_list[7][1]]
                coordinates_angle.append(pos_list[7])
                coordinates_angle.append(pos_list[-1])
                coordinates_angle.append([pos_list[-1][0], pos_list[7][1]])

                # Записываем в БД максимально найденную скорость и найденный угол
                await add_data_db(max_speed, find_angle.get_angle(coordinates_angle), 280)

                print(coordinates_angle)
                # Запись найденной макс. скорости, для Unity
                with open("Max_Speed.txt", "w") as file:
                    # file.write(str(int(MaxSpeed)))
                    file.write(str(max_speed))
                # Если мяч несколько раз будет в кадре, то записываем так
                with open(f"Test_list/test_{list_counter}.txt", "a") as f:
                    # Если мяч будет в кадре только 1 раз записываем так
                    # with open(f"Test_list/test_{listCounter} {datetime.datetime.now().strftime('%H-%M-%S, (%d-%m-%Y)')}.txt", "a") as f:
                    some_string_data = 'x; y'
                    f.write(some_string_data)
                    # Проходимся по всему списку
                    for i in range(len(pos_list)):
                        f.write(f'\n{pos_list[i][0]}; {pos_list[i][1]}')
                # Очищаем список
                pos_list.clear()
                # Очищаем список для угла
                coordinates_angle.clear()
                # Обнуляем переменную длинны списка
                len_pos_list = 0
                # Обнуляем счетчик количества координат
                counter = -1
                # Счетчик списков(ударов)
                list_counter += 1
                # Обнуляем максимальную скорость
                max_speed = 0
                speed = 0

            imgColor = cv2.resize(imgColor, (0, 0), None, 0.7, 0.7)
            # Отображаем окна скорости
            cvzone.putTextRect(imgContours, f"Speed : {round(speed, 2)} m/s", (0, 35), scale=3, offset=5)
            cvzone.putTextRect(imgContours, f"Max Speed : {max_speed} m/s", (0, 80), scale=3, offset=5)
            cvzone.putTextRect(imgContours, f"Time : {seconds} s", (0, 130), scale=3, offset=5)
            cvzone.putTextRect(imgContours, f"Area : {area}", (0, 180), scale=3, offset=5)
            cvzone.putTextRect(imgContours, f"width : {width}", (0, 375), scale=3, offset=5)
            cvzone.putTextRect(imgContours, f"high : {high}", (0, 420), scale=3, offset=5)
            # cv2.imshow("Image", img)
            cv2.imshow("imgColor", imgColor)
            cv2.imshow("imgContours", imgContours)  # Цветное изображение
            # print('---------------------------------------------------------------------------------------------------------')
            # print(len(posList))
            # print(len(timeList))
            # print(len(distanceList))
            print(
                '======================================================================================================')
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Нажатие 'q' для выхода
                break
        # Освобождаем ресурсы
        cap.release()
        cv2.destroyAllWindows()  # Закрываем все окна
        print(f"Обработка видео завершена.")

    except Exception as error:
        print(f'error {error}')

    finally:
        print(f'time {datetime.datetime.now() - now}')


if __name__ == "__main__":
    asyncio.run(find_golf_ball())
