`timescale 1ns / 1ps

module ImmGen (
    input [31:0] Instruction,
    output reg [31:0] Immediate
);
    wire [6:0] opcode = Instruction[6:0];
    
    always @(*) begin
        case (opcode)
            7'b0010011, // I-type (e.g., ADDI)
            7'b0000011, // Load (e.g., LW)
            7'b1100111: // JALR
                Immediate = {{20{Instruction[31]}}, Instruction[31:20]};
            
            7'b0100011: // S-type 
                Immediate = {{20{Instruction[31]}}, Instruction[31:25], Instruction[11:7]};
            
            7'b1100011: // B-type 
                Immediate = {{19{Instruction[31]}}, Instruction[31], Instruction[7], Instruction[30:25], Instruction[11:8], 1'b0};
            
            7'b0110111, // LUI
            7'b0010111: // AUIPC
                Immediate = {Instruction[31:12], 12'b0};
            
            7'b1101111: // J-type (e.g., JAL)
                Immediate = {{11{Instruction[31]}}, Instruction[31], Instruction[19:12], Instruction[20], Instruction[30:21], 1'b0};
            default:
                Immediate = 32'b0;
        endcase
    end
endmodule