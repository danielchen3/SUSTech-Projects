`timescale 1ns / 1ps

module WriteBack_mux(MemorIOtoReg,IORead,Mem_data,r_wdata,ALU_result,PC_out,Jal,Writeback_data);
    input MemorIOtoReg;
    input IORead;
    input [31:0]Mem_data;
    input [31:0] r_wdata;
    input [31:0]ALU_result;
    input [31:0] PC_out;
    input Jal;
    output reg [31:0] Writeback_data;

    always @(*) begin
        if(MemorIOtoReg == 1 & IORead != 1) Writeback_data = Mem_data;
        else if(MemorIOtoReg == 1 & IORead == 1) Writeback_data = r_wdata;
        else if(Jal == 1)Writeback_data = PC_out;
        else Writeback_data = ALU_result;
    end

endmodule