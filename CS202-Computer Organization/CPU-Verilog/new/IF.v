`timescale 1ns / 1ps

module IF (
    input clk,
    input rst,
    input [31:0] Immediate,
    input [31:0] ALU_result,
    input Branch_jump,
    input zero,
    input Jr,
    input Jal,
    output reg [31:0] PC_out,
    output [31:0] Instruction
     //output [31:0] PC_plus_4
);

    wire [13:0] rom_addr;
    wire [31:0] Instruct_o;
    reg [31:0] PC_in;
    assign rom_addr = PC_in[15:2]; // 指令地址对齐到 4 字节

    initial begin
        PC_in = 32'h0;
    end

    // 指令存储器实例
    Instruction_mem inst_mem_inst (
        .rom_clk_i(clk),
        .rom_adr_i(rom_addr),
        .Instruction_o(Instruction)
        // .upg_rst_i(1'b0), // 这里假设 UART 编程功能不使用
        // .upg_clk_i(1'b0),
        // .upg_wen_i(1'b0),
        // .upg_adr_i(14'b0),
        // .upg_dat_i(32'b0),
        // .upg_done_i(1'b0)
    );

    always @(negedge clk or posedge rst) begin
        if (rst) begin
            PC_in <= 32'h0;
            PC_out <= 32'h0;
        end else begin
            if (Jal)begin
                PC_in <= PC_in + Immediate;
                PC_out <= PC_in + 4;
            end
            else if(Branch_jump)
                PC_in <= PC_in + Immediate;
                //$display("pc_in = %d, clk = %d", PC_in, clk); // IF is B,JAL,JALR,
            else if(Jr)
                PC_in <= ALU_result;
            else 
                PC_in <= PC_in + 4;
        end
    end

    // always @(posedge clk) begin
    //     Instruction <= Instruct_o; // Fetch instruction on posedge
    // end


endmodule
