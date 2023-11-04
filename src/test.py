import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles
from cocotb.binary import BinaryValue

async def reset(dut):
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 5)

@cocotb.test()
async def test_no_spike(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    await reset(dut)

    # Set inputs below threshold
    dut.ui_in <= 0
    dut.uio_in <= 0

    await ClockCycles(dut.clk, 100)

    # Check that no spikes occurred
    assert dut.uo_out.value.binstr == "0", "Spikes incorrectly generated"

@cocotb.test()
async def test_spike(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    await reset(dut)

    dut.ui_in = BinaryValue("00000001")
    dut.uio_in = BinaryValue("00000000")

    await ClockCycles(dut.clk, 1)

    spike = dut.uo_out.value.binstr[-2:]
    assert spike == "01", f"Single spike not generated as expected, output was {spike}"
    