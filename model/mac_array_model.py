"""Golden reference model for a MAC lane array.

Each lane is an independent MAC unit.
The array shares clock, reset, clear, and enable signals.

This model will be used later to verify the SystemVerilog
`mac_array` module with cocotb.
"""

from .mac_model import MACModel


class MACArrayModel:
    """Cycle-accurate model of a parallel MAC lane array."""

    def __init__(
        self,
        *,
        num_lanes: int = 4,
        data_width: int = 8,
        acc_width: int = 32,
    ):
        if num_lanes <= 0:
            raise ValueError("num_lanes must be positive")

        self.num_lanes = num_lanes
        self.data_width = data_width
        self.acc_width = acc_width

        self.lanes = [
            MACModel(data_width=data_width, acc_width=acc_width)
            for _ in range(num_lanes)
        ]

    def reset(self) -> None:
        """Clear all lanes."""
        for lane in self.lanes:
            lane.reset()

    def step(
        self,
        *,
        clear: bool,
        en: bool,
        a: list[int],
        b: list[int],
    ) -> list[int]:
        """Advance one clock cycle.

        `a` and `b` must be lists of length `num_lanes`,
        one value per lane.

        Returns a list of accumulator values after the cycle.
        """
        if len(a) != self.num_lanes:
            raise ValueError(
                f"a has length {len(a)}, expected {self.num_lanes}"
            )
        if len(b) != self.num_lanes:
            raise ValueError(
                f"b has length {len(b)}, expected {self.num_lanes}"
            )

        results = []
        for lane, a_val, b_val in zip(self.lanes, a, b):
            acc = lane.step(clear=clear, en=en, a=a_val, b=b_val)
            results.append(acc)

        return results
