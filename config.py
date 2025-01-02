import cv2
from cvzone.ColorModule import ColorFinder

# Подключение видео или камеры
# cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture(o"http://192.168.50.74:8080/video")
# cap = cv2.VideoCapture("http://192.168.50.74:4747")
# cap = cv2.VideoCapture('video_speed_ball_patt_50cm/Standart_30FPS_golf_ball.mp4')
# cap = cv2.VideoCapture('video_speed_ball_patt_50cm/120FPS_golf_ball.mp4')
# cap = cv2.VideoCapture('video_speed_ball_patt_50cm/120FPS_golf_ball_light.mp4')
# cap = cv2.VideoCapture('video_speed_ball_patt_50cm/240FPS_golf_ball.mp4')
# cap = cv2.VideoCapture('video_speed_ball_patt_50cm/240FPS_golf_ball_light.mp4')
# cap = cv2.VideoCapture('S:\Python_project\Golf\\test_api_for_golf\\folder_test_all_open/VIDEO_20240904_191738.mp4')

cap = cv2.VideoCapture('videos/240FPS_fly_50cm.mp4')
# cap = cv2.VideoCapture('videos/Test_60FPS_50cm.mp4')

# cap = cv2.VideoCapture('videos/240FPS_fly_50cm.mp4')

# cap = cv2.VideoCapture('new_test_videos/SL_MO_VID_20240707_221515.mp4')
# cap = cv2.VideoCapture('new_test_videos/SL_MO_VID_20240707_221455.mp4')
# cap = cv2.VideoCapture('new_test_videos/SL_MO_VID_20240707_221545.mp4')
# cap = cv2.VideoCapture('new_test_videos/SL_MO_VID_20240707_221627.mp4')
# cap = cv2.VideoCapture('new_test_videos/SL_MO_VID_20240707_221645.mp4')


# Ищем цвет программой когда True
myColorFinder = ColorFinder(False)
# Цвет который мы нашли
hsvVals = {'hmin': 24, 'smin': 119, 'vmin': 62, 'hmax': 74, 'smax': 255, 'vmax': 255}  # Ball_test_img.png
# hsvVals = {'hmin': 21, 'smin': 86, 'vmin': 82, 'hmax': 46, 'smax': 255, 'vmax': 255}  # ball_1.jpg
# hsvVals = {'hmin': 23, 'smin': 0, 'vmin': 53, 'hmax': 57, 'smax': 255, 'vmax': 255}  # ball_2.jpg
# hsvVals = {'hmin': 16, 'smin': 60, 'vmin': 52, 'hmax': 43, 'smax': 178, 'vmax': 255}  #
# hsvVals = {'hmin': 20, 'smin': 107, 'vmin': 81, 'hmax': 73, 'smax': 255, 'vmax': 255}  # golf_ball_50cm_240FPS_light.png
# hsvVals = {'hmin': 0, 'smin': 160, 'vmin': 87, 'hmax': 17, 'smax': 255, 'vmax': 192}  #


"""Время на 1 кадр"""
frames_in_second = {
    "fps_30": 0.033978933061,
    "fps_60": 0.0169262017603,
    "fps_120": 0.0084796095462,
    "fps_240": 0.0043110881,
}

min_area = 5000  # добавить

