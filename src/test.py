import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles
from cocotb.binary import BinaryValue

THRESHOLD = 0x8000 

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
    dut.ui_in.value = BinaryValue("00000000")
    dut.uio_in.value = BinaryValue("00000000")

    await ClockCycles(dut.clk, 100)

    # Check that no spikes occurred
    assert dut.uo_out.value.binstr == "00000000", "Spikes incorrectly generated"

@cocotb.test()
async def test_spike(dut):
    dut.rst_n.value = 0
    await RisingEdge(dut.clk)
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)
    
    dut.spike_current.value = THRESHOLD + 1
    
    await RisingEdge(dut.clk)
    
    assert dut.spike.value == 1, "Expected a spike when current exceeds the threshold"
    