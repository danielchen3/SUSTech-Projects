`timescale 1ns/1ps
module led_control(
input led_clk,
input rst,
input ledwrite,
input [31:0] r_wdata,
output reg [15:0]dataout                                       
);


  
//通过什么信号判读数码管还是led（现在的设想是通过多路选择器）

//      Light_seg light_seg1(.s(temp[31:28]),.segwrite(segwrite), .light(seg_led1));
//      Light_seg light_seg2(.s(temp[27:24]),.segwrite(segwrite), .light(seg_led2));
//      Light_seg light_seg3(.s(temp[23:20]),.segwrite(segwrite), .light(seg_led3));
//      Light_seg light_seg4(.s(temp[19:16]),.segwrite(segwrite), .light(seg_led4));
//      Light_seg light_seg5(.s(temp[15:12]),.segwrite(segwrite), .light(seg_led5));
//      Light_seg light_seg6(.s(temp[11:8]),.segwrite(segwrite), .light(seg_led6));
//      Light_seg light_seg7(.s(temp[7:4]), .segwrite(segwrite),.light(seg_led7));
//      Light_seg light_seg8(.s(temp[3:0]),.segwrite(segwrite), .light(seg_led8));
 
always@(posedge led_clk or posedge rst )//or posedge rst)
begin
if(rst) begin
dataout <=16'h0000;
end
else if( ledwrite) begin
dataout <=r_wdata[15:0];
end
else begin
dataout <=dataout;
end 
end
//view vw(
endmodule