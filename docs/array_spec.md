# MAC Lane Array Specification

## 1. Overview

The MAC lane array instantiates multiple independent MAC units.
Each lane computes:

    acc[i] = acc[i] + (a[i] * b[i])

when enabled.

All lanes share a common clock, reset, clear, and enable signal.

## 2. Parameters

| Parameter  | Type | Default | Description                        |
|------------|------|---------|------------------------------------|
| DATA_WIDTH | int  | 8       | Signed bit width of inputs a and b |
| ACC_WIDTH  | int  | 32      | Signed bit width of accumulator    |
| NUM_LANES  | int  | 4       | Number of parallel MAC lanes       |

## 3. Interface

| Signal     | Direction | Width                    | Description                          |
|------------|-----------|--------------------------|--------------------------------------|
| clk        | input     | 1                        | Clock                                |
| rst_n      | input     | 1                        | Active-low asynchronous reset        |
| clear      | input     | 1                        | Synchronous clear for all lanes      |
| en         | input     | 1                        | Accumulate enable for all lanes      |
| a          | input     | NUM_LANES*DATA_WIDTH     | Packed signed inputs for each lane   |
| b          | input     | NUM_LANES*DATA_WIDTH     | Packed signed inputs for each lane   |
| acc        | output    | NUM_LANES*ACC_WIDTH      | Packed signed accumulators per lane  |

Packing order: lane 0 occupies the least significant bits.
For example, with NUM_LANES=4 and DATA_WIDTH=8, `a[7:0]`
belongs to lane 0, `a[15:8]` belongs to lane 1, and so on.

## 4. Operation

On reset, all accumulators are cleared to zero.

At each rising edge of the clock:

1. If `clear == 1`, all accumulators are set to zero.
2. Else if `en == 1`, each lane independently computes
   `acc[i] = acc[i] + (a[i] * b[i])`.
3. Otherwise, all accumulators hold their previous values.

Overflow behavior is identical to the single MAC:
signed two's complement wrap modulo 2^ACC_WIDTH.

## 5. Timing

Same as the single MAC. The array is combinational between
register stages, but all registers update on the rising edge.
There is no inter-lane communication.

## 6. Out of scope for this phase

- Adder tree / dot-product summation
- Systolic array dataflow
- Per-lane enable or clear
- valid/ready handshaking
- pipelining
