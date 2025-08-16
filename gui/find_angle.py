import math


class AngleCalculator:
    @staticmethod
    def gradient(pt1: list, pt2: list) -> float:
        """
        Calculates the slope (gradient) of the line between two points.

        Args:
            pt1 (list): The first point (x1, y1).
            pt2 (list): The second point (x2, y2).

        Returns:
            float: The slope of the line between pt1 and pt2. If the line is vertical, returns infinity.
        """
        if pt2[0] == pt1[0]:
            return math.inf  # Vertical line, slope is infinite
        return (pt2[1] - pt1[1]) / (pt2[0] - pt1[0])

    def get_angle(self, points_list: list) -> int:
        """
        Calculates the angle between two lines originating from the first point in the list.
        The first line is defined by pt1 and pt2, and the second line is defined by pt1 and pt3.

        Args:
            points_list (list): A list of points, where each point is a tuple (x, y).

        Returns:
            int: The angle between the two lines, rounded to the nearest integer, in degrees.

        Raises:
            ValueError: If there are fewer than three points in the input list.
        """
        if len(points_list) < 3:
            raise ValueError("At least three points are required to calculate the angle.")

        pt1, pt2, pt3 = points_list[-3:]  # Take the last three points
        m1 = self.gradient(pt1, pt2)  # Gradient of the first line (pt1 -> pt2)
        m2 = self.gradient(pt1, pt3)  # Gradient of the second line (pt1 -> pt3)

        # If either of the lines is vertical, the angle is 90 degrees (pi/2 radians)
        if m1 == float('inf') or m2 == float('inf'):
            ang_r = math.pi / 2
        else:
            # Calculate the angle between the two lines using the arctangent of the difference of slopes
            ang_r = math.atan((m2 - m1) / (1 + (m2 * m1)))

        # Convert the angle from radians to degrees and round to the nearest integer
        ang_d = round(math.degrees(ang_r))

        return ang_d
