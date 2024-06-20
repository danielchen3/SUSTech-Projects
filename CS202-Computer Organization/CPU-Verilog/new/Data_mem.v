`timescale 1ns / 1ps

//Using IP-core?

module Data_mem (
    input clk,
    input [31:0] Addr,
    input [31:0] Read_data_2,
    input MemRead,
    input MemWrite,
    output [31:0] read_data
);


     RAM udram(.clka(~clk), .wea(MemWrite), .addra(Addr[13:0]), .dina(Read_data_2), .douta(read_data));
//    reg [31:0] memory [0:1023];

//    always @(posedge MemWrite) begin
//        if (MemWrite)
//            memory[Addr >> 2] <= Read_data_2;
//    end

//    assign read_data = (MemRead) ? memory[Addr >> 2] : 32'bz; //ÉèÎª¸ß×èÌ¬
endmodule
