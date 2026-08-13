`timescale 1ns / 1ps

module and_gate (
    input  logic a,
    input  logic b,
    output logic y
);

    assign y = a & b;

endmodule
