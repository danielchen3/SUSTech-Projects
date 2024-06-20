`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2024/05/29 20:30:23
// Design Name: 
// Module Name: IO_TOP
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


module IO_TOP(
input clk,
input rst,
input [31:0]address,
input [31:0]r_wdata,
input TotalCtrl,
input SwitchCtrl,
input enter,
input [15:0]datafromswitch,
output enter_debounced,
output [15:0]dataout,
output [15:0]io_rdata,
output [7:0] tub_sel,//Joint enable signal of seven segment digital tube
output [7:0] seg_led1234,//Four seven segment digital tubes on the left
output [7:0] seg_led5678
//Four seven segment digital tubes on the right
    );
    
     switch_control sc(
    .switchclk(clk),
    .switchrst(rst),
    .switchread(SwitchCtrl),
    .datafromswitch(datafromswitch),
    .address(address),
    .enter(enter),
    .datatoIO(io_rdata),
    .enter_debounced(enter_debounced)
    );
     led_control lc(
    .led_clk(clk),
    .rst(rst),
    .ledwrite(TotalCtrl),
    .r_wdata(r_wdata),
    .dataout(dataout)
);
reg segwrite;
reg [3:0]s1,s2,s3,s4,s5,s6,s7,s8;
wire view_clock;
always@(posedge clk or posedge rst )//or posedge rst)
begin
if(rst) begin
s1<=16'h0000;
s2<=16'h0000;
s3<=16'h0000;
s4<=16'h0000;
s5<=16'h0000;
s6<=16'h0000;
s7<=16'h0000;
s8<=16'h0000;
end
else if(segwrite) begin
s1 <=r_wdata[31:28];
s2 <=r_wdata[27:24];
s3 <=r_wdata[23:20];
s4 <=r_wdata[19:16];
s5 <=r_wdata[15:12];
s6 <=r_wdata[11:8];
s7 <=r_wdata[7:4];
s8 <=r_wdata[3:0];
end
else begin
s1 <= s1;
s2 <= s2;
s3 <= s3;
s4 <= s4;
s5 <= s5;
s6 <= s6;
s7 <= s7;
s8 <= s8;
end 
end
wire [7:0] seg_led1,seg_led2,seg_led3,seg_led4,seg_led5,seg_led6,seg_led7,seg_led8;
   Light_seg light_seg1(.s(s1),.segwrite(segwrite), .light(seg_led1));
   Light_seg light_seg2(.s(s2),.segwrite(segwrite), .light(seg_led2));
   Light_seg light_seg3(.s(s3),.segwrite(segwrite), .light(seg_led3));
   Light_seg light_seg4(.s(s4),.segwrite(segwrite), .light(seg_led4));
   Light_seg light_seg5(.s(s5),.segwrite(segwrite), .light(seg_led5));
   Light_seg light_seg6(.s(s6),.segwrite(segwrite), .light(seg_led6));
   Light_seg light_seg7(.s(s7), .segwrite(segwrite), .light(seg_led7));
   Light_seg light_seg8(.s(s8),.segwrite(segwrite), .light(seg_led8));
  // view_back back(.clk_in1(clk),.clk_out1(view_clock));  
   Divide2 divide2(  
   .clk(view_clock),//built-in clock
   .clk_out(view_clock));
     view vw(
        . clk(view_clock),
         .seg_led1(seg_led1),////use 6 segled 1-6 to print the numbers and names of the songs 
        . seg_led2(seg_led2),
        . seg_led3(seg_led3),
        . seg_led4(seg_led4),
        . seg_led5(seg_led5),
        . seg_led6(seg_led6),
        . seg_led7(seg_led7),
        . seg_led8(seg_led8),//Show ratings
        . tub_sel(tub_sel),//Joint enable signal of seven segment digital tube
        . seg_led1234(seg_led1234),//Four seven segment digital tubes on the left
        . seg_led5678(seg_led5678)//Four seven segment digital tubes on the right
    );
always@(*) begin
    if(address==32'hffff_fff7) segwrite = 1'b1;
    else segwrite = 1'b0;
end
endmodule