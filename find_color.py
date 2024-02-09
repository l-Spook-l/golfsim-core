import cv2
from cvzone.ColorModule import ColorFinder

"""Находим нужный цвет"""
"""Есть ползунки при запуске"""

color_finder = ColorFinder(True)
hsvVals = {'hmin': 16, 'smin': 60, 'vmin': 52, 'hmax': 43, 'smax': 178, 'vmax': 255}

while True:
    # img = cv2.imread("images/IMG_20230302_170212.jpg")
    # img = cv2.imread("images/ball_1.jpg")
    # img = cv2.imread("images/ball_2.jpg")
    img = cv2.imread("images/golf_ball_50cm_240FPS_light.png")
    # размеры окна
    # img = img[1500:2600, :]
    img = img[200:700, :]

    imgColor, mask = color_finder.update(img, hsvVals)

    imgColor = cv2.resize(imgColor, (0, 0), None, 0.7, 0.7)
    # cv2.imshow("Image", img)
    cv2.imshow("imgColor", imgColor)

    cv2.waitKey(50)
