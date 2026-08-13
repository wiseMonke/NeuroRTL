`timescale 1ns / 1ps

module tb_and_gate;

    logic a;
    logic b;
    logic y;

    // Instantiate the design under test
    and_gate dut (
        .a(a),
        .b(b),
        .y(y)
    );

    // Test procedure
    initial begin
        $display("Starting AND gate test");

        a = 0; b = 0; #10;
        if (y !== 0) $fatal(1, "Test failed: 0 & 0 should be 0");

        a = 0; b = 1; #10;
        if (y !== 0) $fatal(1, "Test failed: 0 & 1 should be 0");

        a = 1; b = 0; #10;
        if (y !== 0) $fatal(1, "Test failed: 1 & 0 should be 0");

        a = 1; b = 1; #10;
        if (y !== 1) $fatal(1, "Test failed: 1 & 1 should be 1");

        $display("All AND gate tests passed");
        $finish;
    end

endmodule
