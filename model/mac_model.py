"""Golden reference model for a single MAC unit.

This model is intentionally simple.
It emulates the cycle-by-cycle behavior of the RTL that will be written later.

The RTL will wrap signed arithmetic modulo 2**ACC_WIDTH.
This model matches that behavior.
"""


class MACModel:
    """Cycle-accurate model of a signed multiply-accumulate unit."""

    def __init__(self, data_width: int = 8, acc_width: int = 32):
        if data_width <= 0:
            raise ValueError("data_width must be positive")
        if acc_width <= 0:
            raise ValueError("acc_width must be positive")

        self.data_width = data_width
        self.acc_width = acc_width

        self.acc = 0

        self.acc_mask = (1 << acc_width) - 1
        self.acc_sign_bit = 1 << (acc_width - 1)
        self.acc_range = 1 << acc_width

    def reset(self) -> None:
        """Clear the accumulator."""
        self.acc = 0

    def step(
        self,
        *,
        clear: bool,
        en: bool,
        a: int,
        b: int,
    ) -> int:
        """Advance one clock cycle.

        clear has priority over en.
        """
        if clear:
            self.acc = 0
        elif en:
            product = a * b
            self.acc = self.acc + product
            self.acc = self._wrap_signed(self.acc)

        return self.acc

    def _wrap_signed(self, value: int) -> int:
        """Wrap value to signed acc_width-bit two's complement."""
        value &= self.acc_mask
        if value & self.acc_sign_bit:
            value -= self.acc_range
        return value
