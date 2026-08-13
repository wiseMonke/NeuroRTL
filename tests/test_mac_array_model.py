import pytest

from model.mac_array_model import MACArrayModel


def make_array(num_lanes=4, data_width=8, acc_width=32):
    return MACArrayModel(
        num_lanes=num_lanes,
        data_width=data_width,
        acc_width=acc_width,
    )


def test_initial_values_are_zero():
    mac = make_array()
    assert mac.step(clear=False, en=False, a=[0] * 4, b=[0] * 4) == [0, 0, 0, 0]


def test_reset_clears_all_lanes():
    mac = make_array()
    mac.step(clear=False, en=True, a=[1, 2, 3, 4], b=[5, 6, 7, 8])
    assert mac.step(clear=False, en=False, a=[0] * 4, b=[0] * 4) != [0, 0, 0, 0]

    mac.reset()
    assert mac.step(clear=False, en=False, a=[0] * 4, b=[0] * 4) == [0, 0, 0, 0]


def test_clear_overrides_enable_for_all_lanes():
    mac = make_array()
    mac.step(clear=False, en=True, a=[1, 2, 3, 4], b=[2, 3, 4, 5])
    before = mac.step(clear=False, en=False, a=[0] * 4, b=[0] * 4)
    assert before == [2, 6, 12, 20]

    after_clear = mac.step(clear=True, en=True, a=[9, 9, 9, 9], b=[9, 9, 9, 9])
    assert after_clear == [0, 0, 0, 0]


def test_each_lane_accumulates_independently():
    mac = make_array()

    # First cycle: all lanes get their first product
    accs = mac.step(
        clear=False,
        en=True,
        a=[1, 2, 3, 4],
        b=[10, 10, 10, 10],
    )
    assert accs == [10, 20, 30, 40]

    # Second cycle: different inputs, values accumulate
    accs = mac.step(
        clear=False,
        en=True,
        a=[2, 3, 4, 5],
        b=[100, 100, 100, 100],
    )
    assert accs == [210, 320, 430, 540]


def test_enable_false_holds_all_lanes():
    mac = make_array()
    mac.step(clear=False, en=True, a=[1, 2, 3, 4], b=[5, 6, 7, 8])
    before = mac.step(clear=False, en=False, a=[0] * 4, b=[0] * 4)

    after = mac.step(clear=False, en=False, a=[100, 100, 100, 100], b=[100, 100, 100, 100])
    assert after == before


def test_length_mismatch_raises_error():
    mac = make_array()
    with pytest.raises(ValueError):
        mac.step(clear=False, en=True, a=[1, 2, 3], b=[4, 5, 6, 7])

    with pytest.raises(ValueError):
        mac.step(clear=False, en=True, a=[1, 2, 3, 4], b=[4, 5, 6])
