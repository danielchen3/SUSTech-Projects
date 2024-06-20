`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2024/05/22 21:18:50
// Design Name: 
// Module Name: switch_control
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


module switch_control(
    input switchclk,
    input switchrst,
    input switchread,
    input[15:0] datafromswitch,
    input [31:0] address,
    input enter,
    output reg[15:0] datatoIO,
    output enter_debounced
    );
    //assign enter_debounced = enter;
    debounce db(
          .switchclk(switchclk),
          .reset_n(switchrst),
          .btn(enter),
          .out(enter_debounced)
      );
      
    always@(posedge switchclk or posedge switchrst)
    begin
    if(switchrst)begin
    datatoIO <= 16'h0000;
    end
    else if(switchread && address == 32'hffff_fff5 ) begin//16¦Ë    
    datatoIO <= datafromswitch;
    end
    else if(switchread && address == 32'hffff_fff3) begin//8¦Ë  
    datatoIO <= {{8{datafromswitch[15]}},datafromswitch[15:8]};
    end
    else if(switchread && address == 32'hffff_fff3) begin//12¦Ë    
    datatoIO <= {{4{datafromswitch[15]}},datafromswitch[15:4]};
    end
    else if(switchread && address == 32'hffff_fff2) begin//3¦Ë    
    datatoIO <= {13'b0,datafromswitch[15:13]};
    end
    else if(switchread && address == 32'hffff_fff1) begin//1¦Ë    
    datatoIO <= {15'b0,enter_debounced};
    end
    else if(switchread && address == 32'hffff_fff8) begin//12¦Ë    
    datatoIO <= {8'b0,datafromswitch[15:8]};
    end
        
            
    else begin
    datatoIO <= datatoIO;
    end
    end
endmodule
