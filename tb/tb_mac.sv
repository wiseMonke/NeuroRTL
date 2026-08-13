`timescale 1ns / 1ps

module tb_mac;

    // Parameters matching the DUT defaults
    localparam int DATA_WIDTH = 8;
    localparam int ACC_WIDTH  = 32;

    // Signals
    logic                    clk;
    logic                    rst_n;
    logic                    clear;
    logic                    en;
    logic signed [DATA_WIDTH-1:0] a;
    logic signed [DATA_WIDTH-1:0] b;
    logic signed [ACC_WIDTH-1:0]  acc;

    // Instantiate the design under test
    mac #(
        .DATA_WIDTH(DATA_WIDTH),
        .ACC_WIDTH(ACC_WIDTH)
    ) dut (
        .clk   (clk),
        .rst_n (rst_n),
        .clear (clear),
        .en    (en),
        .a     (a),
        .b     (b),
        .acc   (acc)
    );

    // Clock generation: 100 MHz, 10 ns period
    always #5 clk = ~clk;

    // Test sequence
    initial begin
        $display("Starting MAC test");

        // Initialize signals
        clk   = 0;
        rst_n = 0;
        clear = 0;
        en    = 0;
        a     = 0;
        b     = 0;

        // Hold reset for a few cycles
        repeat (2) @(posedge clk);
        rst_n = 1;
        @(posedge clk);

        // Test 1: Simple multiplication 3 * 4 = 12
        en = 1; a = 3; b = 4;
        @(posedge clk);
        if (acc !== 12) $fatal(1, "Test 1 failed: expected 12, got %0d", acc);
        $display("Test 1 passed: 3 * 4 = %0d", acc);

        // Test 2: Accumulate 2 * 5 => 22
        en = 1; a = 2; b = 5;
        @(posedge clk);
        if (acc !== 22) $fatal(1, "Test 2 failed: expected 22, got %0d", acc);
        $display("Test 2 passed: acc = %0d", acc);

        // Test 3: Disable accumulation, should hold 22
        en = 0; a = 10; b = 10;
        @(posedge clk);
        if (acc !== 22) $fatal(1, "Test 3 failed: expected 22, got %0d", acc);
        $display("Test 3 passed: acc held at %0d", acc);

        // Test 4: Clear overrides enable
        en = 1; a = 7; b = 8;
        clear = 1;
        @(posedge clk);
        if (acc !== 0) $fatal(1, "Test 4 failed: expected 0, got %0d", acc);
        $display("Test 4 passed: clear = 0");

        // Test 5: Negative input
        clear = 0;
        en = 1;
        a = -3;
        b = 4;
        @(posedge clk);
        if (acc !== -12) $fatal(1, "Test 5 failed: expected -12, got %0d", acc);
        $display("Test 5 passed: -3 * 4 = %0d", acc);

        // Test 6: Overflow wrap (using 8-bit accumulator for demonstration)
        // This uses default 32-bit, so no overflow here; we'll test overflow with small acc width later.
        $display("All MAC tests passed");
        $finish;
    end

    // Dump waveform for debugging
    initial begin
        $dumpfile("mac.vcd");
        $dumpvars(0, tb_mac);
    end

endmodule
