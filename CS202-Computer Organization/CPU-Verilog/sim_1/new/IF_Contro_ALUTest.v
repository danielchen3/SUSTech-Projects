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


module IF_Contro_ALUTest(
    );
    
    reg clk,rst;
    wire [31:0] Instruction;
    wire [31:0] Immediate;
    wire Branch_jump,Zero,Jr,Branch_lt,Branch_ge,Branch_ltu,Branch_geu,Jal,Branch,nBranch,RegWrite,MemRead,MemWrite,MemorIOtoReg,IORead,IOWrite,ALUSrc,Sftmd;
    wire [3:0] ALUOp;
    wire [31:0]Read_data_1;
    wire [31:0] Read_data_2;
    //reg [31:0] Addr_result;
    wire [31:0] data;
    wire [31:0] ALU_result;
    wire [31:0] Mem_data;
    wire [31:0] Writeback_data;
//    reg [31:0] PC_in;
    wire [31:0] PC_out;
//    initial begin
//        PC_in = 32'h0;
//    end
    
    //CPU_Top cpu_top(clk,rst,Instruction,Jr,Jal,Branch,nBranch,RegWrite,MemRead,MemWrite,MemorIOtoReg,IORead,IOWrite,ALUSrc,Sftmd,ALUOp);
    IF instructionfetch(clk,rst,Immediate,ALU_result,Branch_jump,Zero,Jr,Jal,PC_out,Instruction);
    ImmGen imm_gen(Instruction,Immediate);
    Controller control(Instruction,ALU_result,Jr,Branch_lt,Branch_ge,Branch_ltu,Branch_geu,Branch,nBranch,Jal,RegWrite,MemRead,MemWrite,MemorIOtoReg,IORead,IOWrite,ALUSrc,Sftmd,ALUOp);
    ALU_mux alu_mux(Read_data_2,Immediate,ALUSrc,data);
    ALU alu(Branch,nBranch,Branch_lt,Branch_ge,Branch_ltu,Branch_geu,Read_data_1,data,ALUOp,Zero,ALU_result,Branch_jump);
    WriteBack_mux writeback(MemorIOtoReg,Mem_data,ALU_result,PC_out,Jal,Writeback_data);
    Data_mem data_mem(clk,ALU_result,Read_data_2,MemRead,MemWrite,Mem_data);
    Reg_File reg_file(clk,rst,Instruction,Writeback_data,RegWrite,Read_data_1,Read_data_2);
        
    initial begin
            clk = 1'b0;
            rst = 1'b0;
            #5 rst = 1'b1;
            #5 rst = 1'b0;
        end
    initial begin
         forever #20 clk = ~clk; 
    end
    
initial begin
        forever begin
            @(posedge clk) begin
                if (Instruction == 32'h001c8c93) begin
                    $display("Time: %0t, PC_in: %0h, Instruction: %0h, rom_addr:%0h, ALU_result: %0h, Writeback_data: %0h", 
                             $time, instructionfetch.PC_in, Instruction, instructionfetch.rom_addr, ALU_result, Writeback_data);
                end
            end
        end
    end
    
    initial begin

        #5000
        $display("Simulation complete at time %0t", $time);
        $finish;
    end
    
endmodule
