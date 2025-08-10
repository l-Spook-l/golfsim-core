import math


class AngleCalculator:
    @staticmethod
    def gradient(pt1: list, pt2: list) -> float:
        if pt2[0] == pt1[0]:
            return math.inf
        return (pt2[1] - pt1[1]) / (pt2[0] - pt1[0])

    def get_angle(self, points_list: list) -> int:
        if len(points_list) < 3:
            raise ValueError("At least three points are required to calculate the angle.")

        pt1, pt2, pt3 = points_list[-3:]
        m1 = self.gradient(pt1, pt2)
        m2 = self.gradient(pt1, pt3)

        if m1 == float('inf') or m2 == float('inf'):
            ang_r = math.pi / 2
        else:
            ang_r = math.atan((m2 - m1) / (1 + (m2 * m1)))

        ang_d = round(math.degrees(ang_r))

        return ang_d
