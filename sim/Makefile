# cocotb simulation makefile

TOPLEVEL_LANG ?= verilog

# Path to RTL source(s)
VERILOG_SOURCES = $(PWD)/../rtl/mac.sv

# Top-level module to simulate
TOPLEVEL = mac

# cocotb v2 uses COCOTB_TEST_MODULES instead of MODULE
COCOTB_TEST_MODULES = test_mac

include $(shell cocotb-config --makefiles)/Makefile.sim
