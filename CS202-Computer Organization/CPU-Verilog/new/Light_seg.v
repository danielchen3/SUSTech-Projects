`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/12/10 22:41:54
// Design Name: 
// Module Name: Light_seg
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



module Light_seg( // Control seven segment digital tubes to display different content based on different s
    input [3:0] s,
    input segwrite,
    output reg [7:0] light
    
);

always @(*)begin
//if(segwrite == 1'b0) light = light;
//else begin
    case(s)//Because a total of 15 characters are required, along with initialization, 
    //There are a total of 16 scenarios, so 4 bits are chosen to represent 16 scenarios
        4'b0000: light = 8'b1111_1100;//0
        4'b0001: light = 8'b0110_0000;//1
        4'b0010: light = 8'b1101_1010;//2
        4'b0011: light = 8'b1111_0010;//3
        4'b0100: light = 8'b0110_0110;//4
        4'b0101: light = 8'b1011_0110;//5
        4'b0110: light = 8'b1011_1110;//6
        4'b0111: light = 8'b1110_0000;//7
        4'b1000:light = 8'b1111_1110;//8
        4'b1001: light = 8'b1110_0110;//9
        4'b1010: light = 8'b1110_1110;//A
        4'b1011: light = 8'b0011_1110;//b
        4'b1100: light = 8'b1001_1100;//C
        4'b1101: light = 8'b0111_1010;//d
        4'b1110: light = 8'b1001_1110;//E
        4'b1111: light = 8'b1000_1110;//F
        default:light = 8'b1111_1111;
        endcase
       // end
end
endmodule