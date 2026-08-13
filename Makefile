# Tools
SIM = iverilog
VVP = vvp

# Source files
RTL = rtl/and_gate.sv
TB  = tb/tb_and_gate.sv
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
