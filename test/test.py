# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0
import os

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer


class SimpleMemory:
    def __init__(self, dut, depth=1 << 15):
        self.dut = dut
        self.depth = depth

    async def reset(self):
        """Memory zurücksetzen (ähnlich wie always @(posedge reset))."""
        for i in range(self.depth):
            self.dut.mem.mem[i].value = 0  # oder 'X' wenn du magst
        self.dut._log.info("Memory reset")

    async def load_file(self, filename):
        """Lädt eine .mem Datei und schreibt sie ins DUT Memory."""
        with open(filename, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        for addr, value in enumerate(lines):
            # interpret binary string "10101010" -> int
            val = int(value, 2)
            self.dut.mem.mem[addr].value = val

        self.dut._log.info(f"Memory file {filename} geladen ({len(lines)} Zeilen)")


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")
    dut.clk.value = 1
    print(dir(dut))

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 5, units="ns")
    cocotb.start_soon(clock.start())
    dut._log.info("Test project behavior")

    # Set the input values you want to test
    dut.ui_in.value = 20
    dut.uio_in.value = 30

    print(dir(dut))


async def reset_dut(dut):
    dut.clk.value = 1
    dut.rst_n.value = 0
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    await Timer(15, units="ns")
    dut.rst_n.value = 1
    dut._log.info("finished Reset")


async def run_test(dut, test_name, mem: SimpleMemory):
    # Reset
    await reset_dut(dut)

    dut._log.info(f"--- Running test: {test_name} ---")

    # File laden
    filename = os.path.join(os.path.dirname(__file__), "tests", f"{test_name}.mem")
    await mem.load_file(filename)

    # 25 Takte warten
    await ClockCycles(dut.clk, 25)