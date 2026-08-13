import random
import sys
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

# Add project root to sys.path so we can import the golden model
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from model.mac_model import MACModel


DATA_WIDTH = 8
ACC_WIDTH = 32


@cocotb.test()
async def test_mac_random(dut):
    """Compare RTL MAC against golden model with random inputs."""

    # Start a 100 MHz clock (10 ns period)
    clock = Clock(dut.clk, 10, unit="ns")
    cocotb.start_soon(clock.start())

    # Initial values
    dut.rst_n.value = 0
    dut.clear.value = 0
    dut.en.value = 0
    dut.a.value = 0
    dut.b.value = 0

    # Hold reset for 20 ns
    await Timer(20, unit="ns")

    # Release reset and wait for one full clock edge
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")  # let non-blocking assignments settle

    # Create reference model
    model = MACModel(data_width=DATA_WIDTH, acc_width=ACC_WIDTH)

    # Random test loop
    for i in range(200):
        # Generate random stimulus
        clear = random.randint(0, 1)
        en = random.randint(0, 1)
        a = random.randint(-(2 ** (DATA_WIDTH - 1)), 2 ** (DATA_WIDTH - 1) - 1)
        b = random.randint(-(2 ** (DATA_WIDTH - 1)), 2 ** (DATA_WIDTH - 1) - 1)

        # Drive DUT inputs
        dut.clear.value = clear
        dut.en.value = en
        dut.a.value = a
        dut.b.value = b

        # Wait for next rising edge
        await RisingEdge(dut.clk)
        # Allow RTL non-blocking assignments to settle
        await Timer(1, unit="ns")

        # Advance golden model using the same inputs
        expected_acc = model.step(clear=clear, en=en, a=a, b=b)

        # Read RTL output as signed integer
        rtl_acc = dut.acc.value.to_signed()

        # Compare
        assert rtl_acc == expected_acc, (
            f"Mismatch at cycle {i}: "
            f"RTL={rtl_acc}, model={expected_acc}, "
            f"a={a}, b={b}, en={en}, clear={clear}"
        )

    dut._log.info("Randomized cocotb test passed: 200 cycles matched.")
