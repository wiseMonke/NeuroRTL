import pytest

from model.mac_model import MACModel


def make_model(data_width=8, acc_width=32):
    return MACModel(data_width=data_width, acc_width=acc_width)


def test_reset_clears_accumulator():
    mac = make_model()
    mac.step(clear=False, en=True, a=3, b=4)
    assert mac.acc != 0

    mac.reset()
    assert mac.acc == 0


def test_enable_false_holds_value():
    mac = make_model()
    mac.step(clear=False, en=True, a=3, b=4)
    acc_before = mac.acc

    mac.step(clear=False, en=False, a=99, b=99)
    assert mac.acc == acc_before


def test_clear_overrides_enable():
    mac = make_model()
    mac.step(clear=False, en=True, a=3, b=4)
    assert mac.acc == 12

    mac.step(clear=True, en=True, a=7, b=8)
    assert mac.acc == 0


def test_positive_accumulation():
    mac = make_model()
    mac.step(clear=False, en=True, a=3, b=4)
    assert mac.acc == 12

    mac.step(clear=False, en=True, a=2, b=5)
    assert mac.acc == 22


def test_negative_inputs():
    mac = make_model()
    mac.step(clear=False, en=True, a=-3, b=4)
    assert mac.acc == -12

    mac.step(clear=False, en=True, a=2, b=-5)
    assert mac.acc == -22


def test_accumulator_wraps_in_signed_two_complement():
    # Use a small accumulator width to make overflow easy to observe.
    mac = MACModel(data_width=8, acc_width=8)

    # 10 * 10 = 100
    mac.step(clear=False, en=True, a=10, b=10)
    assert mac.acc == 100

    # 100 + 100 = 200, which wraps to -56 in signed 8-bit.
    mac.step(clear=False, en=True, a=10, b=10)
    assert mac.acc == -56
