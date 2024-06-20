`timescale 1ns / 1ps

module view(
    input clk,//system clk
    input [7:0] seg_led1,////use 6 segled 1-6 to print the numbers and names of the songs 
    input [7:0] seg_led2,
    input [7:0] seg_led3,
    input [7:0] seg_led4,
    input [7:0] seg_led5,
    input [7:0] seg_led6,
    input [7:0] seg_led7,
    input [7:0] seg_led8,//Show ratings
    output reg [7:0] tub_sel,//Joint enable signal of seven segment digital tube
    output reg [7:0] seg_led1234,//Four seven segment digital tubes on the left
    output reg [7:0] seg_led5678//Four seven segment digital tubes on the right
    );
    reg [2:0] count = 3'b000;
    wire clk_out = clk;
    //view_back divider(.clk_in1(clk),.clk_out1(clk_out));
    
always @(posedge clk_out) begin
        count = count + 1'b1;
        case(count)
            3'b000: begin
                tub_sel <= 8'b10000000;
                seg_led1234<= seg_led1;
                end
            3'b001: begin
                tub_sel <= 8'b01000000;
                seg_led1234 <= seg_led2;
                end
            3'b010: begin
                tub_sel <= 8'b00100000;
                seg_led1234 <= seg_led3;
                end
            3'b011: begin
                tub_sel <= 8'b00010000;
                seg_led1234 <= seg_led4;
                end
            3'b100: begin
                tub_sel <= 8'b00001000;
                seg_led5678 <= seg_led5;
                end
            3'b101: begin
                tub_sel <= 8'b00000100;
                seg_led5678 <= seg_led6;
                end
             3'b110:begin
                tub_sel<=8'b00000010;
                seg_led5678 <= seg_led7;
                end 
             3'b111:begin
                tub_sel<=8'b00000001;
                seg_led5678 <= seg_led8;
                end 
            default: begin
                tub_sel <= 8'b1110_1011;
                end
        endcase
     end


endmodule
