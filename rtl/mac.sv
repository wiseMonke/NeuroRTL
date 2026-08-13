`timescale 1ns / 1ps

module mac #(
    parameter int DATA_WIDTH = 8,
    parameter int ACC_WIDTH  = 32
) (
    input  logic                    clk,
    input  logic                    rst_n,
    input  logic                    clear,
    input  logic                    en,
    input  logic signed [DATA_WIDTH-1:0] a,
    input  logic signed [DATA_WIDTH-1:0] b,
    output logic signed [ACC_WIDTH-1:0]  acc
);

    // Accumulator register.
    // Signed arithmetic wraps naturally in two's complement.
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            acc <= '0;
        end else if (clear) begin
            acc <= '0;
        end else if (en) begin
            // The product a * b is computed as signed.
            // The expression is sized to ACC_WIDTH because acc is ACC_WIDTH wide.
            acc <= acc + a * b;
        end
    end

endmodule
