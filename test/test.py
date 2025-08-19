# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0
import os

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer


@cocotb.test()
async def test_project(dut):
    print(dir(dut))
    dut._log.info("Start")
    dut.clk.value = 1

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
    dut._log.info("Reset abgeschlossen")
