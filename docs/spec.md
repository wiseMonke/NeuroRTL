# MAC Unit Specification

## 1. Overview

A multiply-accumulate unit computes:

    acc = acc + (a * b)

when enabled.

It is the fundamental arithmetic block for dot products, filters,
and matrix multiplication.

This document defines the single-MAC version that will be
implemented first.

## 2. Parameters

| Parameter    | Type | Default | Description                         |
|--------------|------|---------|-------------------------------------|
| DATA_WIDTH   | int  | 8       | Signed bit width of inputs a and b  |
| ACC_WIDTH    | int  | 32      | Signed bit width of accumulator     |

## 3. Interface

| Signal | Direction | Width       | Description                        |
|--------|-----------|-------------|------------------------------------|
| clk    | input     | 1           | Clock                              |
| rst_n  | input     | 1           | Active-low asynchronous reset      |
| clear  | input     | 1           | Synchronous clear of accumulator   |
| en     | input     | 1           | Accumulate enable                  |
| a      | input     | DATA_WIDTH  | First signed operand               |
| b      | input     | DATA_WIDTH  | Second signed operand              |
| acc    | output    | ACC_WIDTH   | Current accumulator value          |

## 4. Operation

On reset:

    acc = 0

At each rising edge of the clock:

1. If `clear == 1`, then `acc = 0`.
2. Else if `en == 1`, then `acc = acc + (a * b)`.
3. Otherwise, `acc` holds its previous value.

The product `a * b` is computed exactly before addition.
The accumulator wraps modulo `2^ACC_WIDTH` in signed two's complement.

## 5. Timing

- Inputs `a`, `b`, `en`, and `clear` are sampled at the rising edge.
- The updated accumulator appears after a small clock-to-output delay.
- This first version is not pipelined.

## 6. Overflow behavior

- If the accumulator exceeds the representable signed range,
  the result wraps in two's complement.
- No saturation and no overflow flag in the first version.

## 7. Out of scope for this phase

- valid/ready handshaking
- pipelining
- multiple MACs
- saturation
- configurable accumulation length
