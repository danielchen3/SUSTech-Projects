`timescale 1ns / 1ps
    module CPU_Top(clk_FPGA,rst,
    //Instruction,
//    Immediate,Branch_jump,Zero,Jr,Branch_lt,Branch_ge,Branch_ltu,Branch_geu,Jal,Branch,nBranch,RegWrite,MemRead,MemWrite,MemorIOtoReg,IORead,IOWrite,ALUSrc,Sftmd,ALUOp,
//    Read_data_1,Read_data_2,data,ALU_result,
//    Mem_data,Writeback_data,PC_out,addr_out,
//    io_rdata,r_wdata,write_data,
    enter,
    dataout,
    tub_sel,
    seg_led1234,seg_led5678,
    datafromswitch
//    LEDCtrl, SwitchCtrl
    
);

    input clk_FPGA,rst;
    wire clk;
    //assign clk = clk_FPGA;
    cpu_clk clk_divider(.clk_in1(clk_FPGA),.clk_out1(clk));
   wire [31:0] Instruction;
        wire [31:0] Immediate;
        wire Branch_jump,Zero,Jr,Branch_lt,Branch_ge,Branch_ltu,Branch_geu,Jal,Branch,nBranch,RegWrite,MemRead,MemWrite,MemorIOtoReg,IORead,ALUSrc,Sftmd;
        wire [3:0] ALUOp;
        wire IOWrite;
        wire [31:0]Read_data_1;
        wire [31:0] Read_data_2;
        wire [31:0] data;
        wire [31:0] ALU_result;
        wire [31:0] Mem_data;
        wire [31:0] Writeback_data;
    //    reg [31:0] PC_in;
        wire [31:0] PC_out;
    //    initial begin
    //        PC_in = 32'h0;
    //    end
        wire [31:0] addr_out;
        wire [15:0] io_rdata;
        wire [31:0] r_wdata;
        wire enter_debounce;
        wire LEDCtrl,SwitchCtrl;
        
        //to IO
        wire [31:0] write_data;
        input enter;
        output [15:0]dataout;
        output [7:0] tub_sel;//Joint enable signal of seven segment digital tube
        output [7:0] seg_led1234;//Four seven segment digital tubes on the left
        output [7:0] seg_led5678;
        input [15:0] datafromswitch ;
        
        //CPU_Top cpu_top(clk,rst,Instruction,Jr,Jal,Branch,nBranch,RegWrite,MemRead,MemWrite,MemorIOtoReg,IORead,IOWrite,ALUSrc,Sftmd,ALUOp);
        IF instructionfetch(clk,~rst,Immediate,ALU_result,Branch_jump,Zero,Jr,Jal,PC_out,Instruction);
        ImmGen imm_gen(Instruction,Immediate);
        Controller control(Instruction,ALU_result,Jr,Branch_lt,Branch_ge,Branch_ltu,Branch_geu,Branch,nBranch,Jal,RegWrite,MemRead,MemWrite,MemorIOtoReg,IORead,IOWrite,ALUSrc,Sftmd,ALUOp);
        ALU_mux alu_mux(Read_data_2,Immediate,ALUSrc,data);
        ALU alu(Branch,nBranch,Branch_lt,Branch_ge,Branch_ltu,Branch_geu,Read_data_1,data,ALUOp,Zero,ALU_result,Branch_jump);
        WriteBack_mux writeback(MemorIOtoReg,IORead,Mem_data,r_wdata,ALU_result,PC_out,Jal,Writeback_data);
        Data_mem data_mem(clk,ALU_result,Read_data_2,MemRead,MemWrite,Mem_data);
        Reg_File reg_file(clk,~rst,Instruction,Writeback_data,RegWrite,Read_data_1,Read_data_2);
        MemOrIO memorio(MemRead, MemWrite, IORead, IOWrite,ALU_result, addr_out, Mem_data, io_rdata, r_wdata, Read_data_2, write_data, LEDCtrl, SwitchCtrl);   
        IO_TOP io_top(~clk,~rst,addr_out,write_data,LEDCtrl,SwitchCtrl,enter,datafromswitch,enter_debounce,dataout,io_rdata,tub_sel,seg_led1234,seg_led5678);



endmodule