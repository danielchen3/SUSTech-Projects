//Depend IMM or Data

`timescale 1ns / 1ps

module ALU_mux(
    input [31:0] Read_data_2,
    input [31:0] Immediate,
    input ALUSrc,
    output reg [31:0] data
);

always@(*) begin
    if(ALUSrc) data = Immediate;
    else data = Read_data_2;
end
endmodule