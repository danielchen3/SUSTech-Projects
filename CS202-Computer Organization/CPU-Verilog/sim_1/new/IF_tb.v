`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2024/05/27 12:43:54
// Design Name: 
// Module Name: CPU_tb
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module IF_tb(
    );
    
    reg clk,rst;
    wire [31:0] Instruction;
    reg [31:0] PC_in;
    wire Jr,Jal,Branch,nBranch,RegWrite,MemRead,MemWrite,MemorIOtoReg,IORead,IOWrite,ALUSrc,Sftmd;
    wire [3:0] ALUOp;
    wire zero;
    wire [31:0] Immediate;
    
    //CPU_Top cpu_top(clk,rst,Instruction,Jr,Jal,Branch,nBranch,RegWrite,MemRead,MemWrite,MemorIOtoReg,IORead,IOWrite,ALUSrc,Sftmd,ALUOp);
    IF IF_test(clk,rst,Immediate,Branch,nBranch,zero,Jr,Jal,Instruction);
    
     initial begin
               clk = 1'b0;
               rst = 1'b1;  // 初始化为复位状态
               #10 rst = 1'b0;  // 一段时间后取消复位
               forever #17 clk = ~clk;
           end
           
      initial begin
                           $monitor("Time: %0t, PC_in: %0h, Instruction: %0h, Instruction_o: %0h,", 
                                    $time, IF_test.PC_in, Instruction,IF_test.Instruct_o);
                       end
    
    
    
    
endmodule
