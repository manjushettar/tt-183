import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles
from cocotb.binary import BinaryValue

async def reset(dut):
    dut.rst_n = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n = 1
    await ClockCycles(dut.clk, 5)

@cocotb.test()
async def test_no_spike(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    await reset(dut)

    dut.ui_in = BinaryValue("00000000")
    dut.uio_in = BinaryValue("00000000")

    await ClockCycles(dut.clk, 100)

    assert dut.uo_out.value.binstr == "00000000", "Spikes incorrectly generated"

@cocotb.test()
async def test_spike(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    await reset(dut)

    dut.ui_in <= BinaryValue("10000000")
    await ClockCycles(dut.clk, 1)

    await ClockCycles(dut.clk, 10)

    spike = dut.uo_out.value.binstr[-2:]
    assert dut.uo_out.value.binstr == "00000001", f"Expected a single spike, got {dut.uo_out.value.binstr}"
    