"""
Stub module for interacting with the FlightScope simulator.
The original implementation uses Selenium and is private.

Instructions:
- To implement the functionality, you need to create a `ParserFlightscope` class
  that opens the website https://trajectory.flightscope.com/,
  inputs the shot data, and returns the calculated results.
- The methods `set_data()`, `get_data()`, and `get_shot_result()` must retain the same signatures
  to ensure compatibility between the real and the "fake" version.
"""

import asyncio
from typing import Any

from core.logging_config import logger


class ParserFlightscope:
    """
    Stub for working with shot simulation.
    The original implementation is private.
    """

    def __init__(self) -> None:
        """
        Initialization (in the real version, Selenium WebDriver is configured).
        """
        pass

    def set_data(self, type_data: str, value: float | int) -> None:
        """
        Sets data fields in the simulator.

        Args:
            type_data (str): Parameter type ("angle_v", "angle_h", "ball_speed", "spin").
            value (float | int): Value to set.
        """
        raise NotImplementedError("This function is only available in the private version of the project.")

    def get_data(self) -> dict[str, Any]:
        """
        Returns simulation results (implementation is private).

        Returns:
            dict: A dictionary with calculated values.
        """
        raise NotImplementedError("This function is only available in the private version of the project.")

    async def get_shot_result(
        self,
        ball_speed: float = 190.0,
        angle_v: float = 11.0,
        angle_h: str | float = 0.0,
        spin: int = 2000
    ) -> dict[str, Any]:
        """
        Stub method for shot simulation.

        Args:
            ball_speed (float): Ball speed.
            angle_v (float): Vertical launch angle.
            angle_h (str | float): Horizontal launch angle.
            spin (int): Spin rate.

        Returns:
            dict: In the real version — simulation results.
        """
        raise NotImplementedError("This function is only available in the private version of the project.")


if __name__ == "__main__":
    parser = ParserFlightscope()
    result = asyncio.run(parser.get_shot_result())
    logger.info(result)
