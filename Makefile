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
OUT = simv

# Default target
all: $(OUT)

# Compile and run simulation
$(OUT):
	$(SIM) -g2012 -o $(OUT) $(SRC)
	$(VVP) $(OUT)

# Phony target to explicitly run simulation
run: $(OUT)
	$(VVP) $(OUT)

# Clean generated files
clean:
	rm -f $(OUT) *.vcd
