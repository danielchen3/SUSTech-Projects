`timescale 1ns / 1ps

module Reg_File (
    input clk,
    input rst,
    input [31:0] Instruction,
    input [31:0] Writeback_data,
    input RegWrite,
    output [31:0] Read_data_1, // first register_data
    output [31:0] Read_data_2  //second_register_data
);
    reg [31:0] registers [0:31];
    integer i;
    
    initial begin
        for(i = 0; i<32; i=i+1)begin
            if(i == 27) registers[i] = 32'hffff_fff0;
            else if(i == 2)registers[i] = 32'h0fff_ffff;
            else if (i == 23) registers[i] = 32'h0007_04e0;
            else registers[i]=0;
        end
    end

    wire [4:0] rs1 = Instruction[19:15];
    wire [4:0] rs2 = Instruction[24:20];
    wire [4:0] rd = Instruction[11:7];

    assign Read_data_1 = registers[rs1];
    assign Read_data_2 = registers[rs2];
    always @(posedge clk or posedge rst) begin
            if (rst) begin
                for (i = 0; i < 32; i = i + 1) begin
                    if(i == 27) registers[i] <= 32'hffff_fff0;
                    else if(i == 2)registers[i] = 32'h0fff_ffff;
                    else if (i == 23) registers[i] = 32'h0007_04e0;
                    else registers[i]<=0;
                end
            end else if (RegWrite & rd!=5'd0) begin
                registers[rd] <= Writeback_data;
            end
        end
endmodule
