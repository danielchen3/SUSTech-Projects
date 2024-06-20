`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/12/19 15:28:32
// Design Name: 
// Module Name: debounce
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


module debounce (
    input wire switchclk, // Slow clock
    input wire reset_n, // System reset, active low
    input wire btn, // Button input
    output reg out // Debounced and confirmed output
  
);
    
    
    wire slow_clk;
    
    debounce_clk deb_clk(.clk_in1(switchclk),.clk_out1(slow_clk));
    
    reg q1, q2;
        always @(posedge slow_clk or negedge reset_n) begin
            if (reset_n) begin
                q1 <= 1'b0;
                q2 <= 1'b0;
            
            end else begin
                q1 <= btn;
                q2 <= q1;
                out <= q1 & q2;
            end
        end
endmodule
