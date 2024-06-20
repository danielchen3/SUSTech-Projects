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


module CPU_tb(
    );
    
    reg clk,rst;
        wire [31:0] Instruction;
            wire [31:0] Immediate;
            wire Branch_jump,Zero,Jr,Branch_lt,Branch_ge,Branch_ltu,Branch_geu,Jal,Branch,nBranch,RegWrite,MemRead,MemWrite,MemorIOtoReg,IORead,IOWrite,ALUSrc,Sftmd;
            wire [3:0] ALUOp;
            wire [31:0]Read_data_1;
            wire [31:0] Read_data_2;
            //wire [31:0] Addr_result;
            wire [31:0] data;
            wire [31:0] ALU_result;
            wire [31:0] Mem_data;
            wire [31:0] Writeback_data;
            wire [31:0] PC_out;
            wire [31:0] addr_out;
            wire [15:0] io_rdata;
            wire[31:0] r_wdata;
            wire[15:0]dataout;
//            //to IO
            wire [31:0] write_data;
            wire LEDCtrl, SwitchCtrl;
            reg enter;
            wire enter_debounce;
            wire [7:0] tub_sel;//Joint enable signal of seven segment digital tube
            wire [7:0] seg_led1234;//Four seven segment digital tubes on the left
            wire [7:0] seg_led5678;
            reg [15:0] datafromswitch;
           // wire segwrite;
    //wire Jr,Jal,Branch,nBranch,RegWrite,MemRead,MemWrite,MemorIOtoReg,IORead,IOWrite,ALUSrc,Sftmd;
    //wire [3:0] ALUOp;
    
    //CPU_Top cpu_top(clk,rst,Instruction,Jr,Jal,Branch,nBranch,RegWrite,MemRead,MemWrite,MemorIOtoReg,IORead,IOWrite,ALUSrc,Sftmd,ALUOp);
    CPU_Top cpu_top(clk,rst,
        Instruction,
//        Immediate,Branch_jump,Zero,Jr,Branch_lt,Branch_ge,Branch_ltu,Branch_geu,Jal,Branch,nBranch,RegWrite,MemRead,MemWrite,MemorIOtoReg,IORead,IOWrite,ALUSrc,Sftmd,ALUOp,
//        Read_data_1,Read_data_2,data,ALU_result,
//        Mem_data,Writeback_data,PC_out,addr_out,
//        io_rdata,r_wdata,write_data,
        enter,
        dataout,
        tub_sel,
        seg_led1234,seg_led5678,
        datafromswitch
//        ,LEDCtrl, SwitchCtrl
);
    
    initial begin
                clk = 1'b0;
                rst = 1'b1;
//                enter = 1'b0;
                #1 rst = 1'b0;
                #1 rst = 1'b1;
//                #1 datafromswitch = 16'b1000_0100_0000_0000;
                #13 enter = 1'b1;
                #10 enter = 1'b0;
                #30 datafromswitch = 16'b0000_0000_0000_0000;
                #30 enter = 1'b1;
                #20 enter = 1'b0;
                // case0 input a
                #30 datafromswitch = 16'b0000_1000_0000_0000;
                #20 enter = 1'b1;
                #20 enter = 1'b0;
                //case0 input b
                #30 datafromswitch = 16'b0001_1000_0000_0000;
                #70 enter = 1'b1;
                #20 enter = 1'b0;
                //case 1
                #30 datafromswitch = 16'b0010_0000_0000_0000;
                #50 enter = 1'b1;
                #20 enter = 1'b0;
                //case1 input
                #30 datafromswitch = 16'b1000_0100_0000_0000;
                #60 enter = 1'b1;
                #20 enter = 1'b0;
                //case2
                #30 datafromswitch = 16'b0100_0000_0000_0000;
                #70 enter = 1'b1;
                #20 enter = 1'b0;
                //case2 input
                #30 datafromswitch = 16'b1000_0110_0000_0000;
                #60 enter = 1'b1;
                #20 enter = 1'b0;
                //case3
                #30 datafromswitch = 16'b0110_0000_0000_0000;
                #130 enter = 1'b1;
                #20 enter = 1'b0;
                //case 4
                #30 datafromswitch = 16'b1000_0000_0000_0000;
                #170 enter = 1'b1;
                #20 enter = 1'b0;
                //case 5
                #30 datafromswitch = 16'b1010_0000_0000_0000;
                #170 enter = 1'b1;
                #20 enter = 1'b0;
                //case 6
                #30 datafromswitch = 16'b1100_0000_0000_0000;
                #190 enter = 1'b1;
                #20 enter = 1'b0;
                //case7
                #30 datafromswitch = 16'b1110_0000_0000_0000;
                #230 enter =1'b1;
                #20 enter =1'b0;
                    #13 enter = 1'b1;
                    #500 enter = 1'b0;
                    
                
            end
        initial begin
             forever #5 clk = ~clk; 
        end
        
        
        initial begin
                forever begin
                    @(posedge clk) begin
                        if (Instruction == 32'h007da3a3|Instruction == 32'h124000ef) begin
                            $display("Time: %0t, Instruction: %0h,  ALU_result: %0h", 
                                     $time,  Instruction,  ALU_result);
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
