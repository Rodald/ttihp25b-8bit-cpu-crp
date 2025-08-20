# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0
import os

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer


class SimpleMemory:
    def __init__(self, addr_width=15, data_width=8):
        self.ADDR_WIDTH = addr_width
        self.DATA_WIDTH = data_width
        self.MEM_DEPTH = 1 << addr_width
        self.mem = [0 for _ in range(self.MEM_DEPTH)]
        self.writeDataReg = 0
        self.writeState = 0

    def reset(self):
        self.mem = [None for _ in range(self.MEM_DEPTH)]
        self.writeState = 0

    async def load_file(self, filename):
        with open(filename, "r") as f:
            for addr, line in enumerate(f):
                if addr < self.MEM_DEPTH:
                    try:
                        self.mem[addr] = int(line.strip(), 2)
                    except ValueError:
                        pass



@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")
    dut.clk.value = 1
    dut.rst_n.value = 0

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 20, units="ns")
    cocotb.start_soon(clock.start())

    await Timer(15, units="ns")
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # Set the input values you want to test
    dut.ui_in.value = 20
    dut.uio_in.value = 30

    print(dir(dut))

    # Wait for one clock cycle to see the output values
    await ClockCycles(dut.clk, 1)

    # The following assersion is just an example of how to check the output values.
    # Change it to match the actual expected output of your module:
    assert dut.uo_out.value == 50

    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.


async def run_test(dut, test_name, memory):
    dut.clk.value = 1
    dut.rst_n.value = 0
    clock = Clock(dut.clk, 20, units="ns")
    cocotb.start_soon(clock.start())

    await Timer(15, units="ns")
    dut.rst_n.value = 1
    dut._log.info(f"--- Running test: {test_name} ---")

    filename = os.path.join(os.path.dirname(__file__), "tests", f"{test_name}.mem")
    await memory.load_file(filename)

    await ClockCycles(dut.clk, 25)


@cocotb.test()
async def test_add(dut):
    mem = SimpleMemory(dut, depth=1 << 15)

    await run_test(dut, "testAdd", mem)

    dut._log.info(f"Register Output: {dut.some_output.value}")
