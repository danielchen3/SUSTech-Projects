`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/12/17 11:39:35
// Design Name: 
// Module Name: Divide
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


module clock_divider( //A division clock with a period of 10000
    input clk,//built-in clock
    output reg clk_out//Divided clock
    );
parameter period2 = 10000;
reg[24:0] cnt;
reg rst = 1'b0;
always@(posedge clk)
begin
    if(~rst)begin
        cnt <= 0;
        clk_out <= 0;
        rst <= 1'b1;
end
else if (cnt == ((period2 >> 1) - 1)) begin
    clk_out <= ~clk_out;
    cnt <= 0;
end
else begin
cnt<=cnt+1;
end
end
endmodule