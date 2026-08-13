# Tools
SIM = iverilog
VVP = vvp

# RTL source files
RTL = rtl/mac.sv

# Testbench source files
TB = tb/tb_mac.sv

# All sources
SRC = $(RTL) $(TB)

# Output binary
OUT = sim

# Default target
all: sim

# Compile and run simulation
sim:
	$(SIM) -g2012 -o $(OUT) $(SRC)
	$(VVP) $(OUT)

# Clean generated files
clean:
	rm -f $(OUT) *.vcd
