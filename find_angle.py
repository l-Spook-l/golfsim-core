import math


def gradient(pt1, pt2):
    # Проверка на деление на ноль
    if pt2[0] == pt1[0]:
        return float('inf')  # Вернуть бесконечность при вертикальной линии
    return (pt2[1] - pt1[1]) / (pt2[0] - pt1[0])


# Определение угла по трем точкам
# 1 - начальная
# 2 - на нужный угол
# 3 - на уровне начально (под, над угловой (2й))
def get_angle(points_list):
    if len(points_list) < 3:
        raise ValueError("Для вычисления угла необходимо минимум три точки.")

    pt1, pt2, pt3 = points_list[-3:]
    # print('pt1, pt2, pt3', pt1, pt2, pt3)
    m1 = gradient(pt1, pt2)
    m2 = gradient(pt1, pt3)
    # print('m1', 'm2', m1, m2)
    # Если одна из линий вертикальная
    if m1 == float('inf') or m2 == float('inf'):
        ang_r = math.pi / 2  # Угол 90 градусов в радианах
    else:
        ang_r = math.atan((m2 - m1) / (1 + (m2 * m1)))

    ang_d = round(math.degrees(ang_r))
    # print('Найденный угол', ang_d, ang_r)
    # print('pt1[0]', pt1[0], 'pt2[1]', pt2[0])
    # Запись найденного угла в блокнот, для Unity
    with open("Angle.txt", "w") as file:
        file.write(str(ang_d))
    return ang_d

