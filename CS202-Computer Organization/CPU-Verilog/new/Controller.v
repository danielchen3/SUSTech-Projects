`timescale 1ns / 1ps


module Controller(
    input [31:0] Instruction,
    input [31:0] Addr_result,
    output reg Jr,
    output reg Branch_lt,
    output reg Branch_ge,
    output reg Branch_ltu,
    output reg Branch_geu,
    output reg Branch, // beq
    output reg nBranch, // bne
    output reg Jal,
    output reg RegWrite, // 1 indicates that the instruction needs to write to the register
    output reg MemRead, // 1 indicates that the instruction needs to read from the memory
    output reg MemWrite, // 1 indicates that the instruction needs to write to the memory
    output reg MemorIOtoReg, // 1 indicates that data needs to be read from memory or I/O to the register
    output reg IORead, // 1 indicates I/O read
    output reg IOWrite, // 1 indicates I/O write
    output reg ALUSrc, // 1 indicate the 2nd data is immidiate (except "beq","bne")
    output reg Sftmd, // 1 indicate the instruction is shift instruction
    output reg[3:0] ALUOp
 );
    

    wire [2:0]func3;
    wire [6:0]func7;
    assign func3 = Instruction[14:12];
    assign func7 = Instruction[31:25];

    always @(*) begin
        Jr = 1'b0;
        Branch = 1'b0;
        Branch_lt = 1'b0;
        Branch_ge = 1'b0;
        Branch_ltu = 1'b0;
        Branch_geu = 1'b0;
        nBranch = 1'b0;
        Jal = 1'b0;
        MemorIOtoReg = 1'b0;
        RegWrite = 1'b0;
        MemRead = 1'b0;
        MemWrite = 1'b0;
        IORead = 1'b0;
        IOWrite = 1'b0;
        ALUSrc = 1'b0;
        Sftmd = 1'b0;
        ALUOp = 4'b0000;
        case(Instruction[6:0])
            //R-type
            7'b0110011:begin
                RegWrite = 1'b1;
                case({func7,func3})
                    10'b0000000000: ALUOp = 4'b0000; // ADD
                    10'b0100000000: ALUOp = 4'b0001; // SUB
                    10'b0000000111: ALUOp = 4'b0010; // AND
                    10'b0000000110: ALUOp = 4'b0011; // OR
                    10'b0000000100: ALUOp = 4'b0100; // XOR
                    10'b0000000001:begin
                        ALUOp = 4'b0101;Sftmd = 1'b1; // SLL
                    end 
                    10'b0000000101: begin
                        ALUOp = 4'b0110;Sftmd = 1'b1;  // SRL
                    end 
                    10'b0100000101:begin
                        ALUOp = 4'b0111;Sftmd = 1'b1;  // SRA
                    end 
                endcase
            end
            //I-type
            7'b0010011:begin
                RegWrite = 1'b1;
                ALUSrc = 1'b1;
                case (func3)
                    3'b000: ALUOp = 4'b0000; // ADDI
                    3'b111: ALUOp = 4'b0010; // ANDI
                    3'b110: ALUOp = 4'b0011; // ORI
                    3'b100: ALUOp = 4'b0100; // XORI
                    3'b001: ALUOp = 4'b0101; // SLLI
                    3'b010: ALUOp = 4'b1000; //SLTI
                    3'b101: ALUOp = (func7 == 7'b0000000) ? 4'b0110 : 4'b0111; // SRLI or SRAI
                endcase
            end
            //I-type(Load)
            7'b0000011:begin
                ALUSrc = 1'b1;
                RegWrite = 1'b1;
                ALUOp = 4'b0000; //ADD
                if (Instruction[19:15] == 5'b11011 & (Instruction[31:20] == 12'd8|Instruction[31:20] == 12'd1|Instruction[31:20] == 12'd2|Instruction[31:20] == 12'd3|Instruction[31:20] == 12'd4|Instruction[31:20] == 12'd5)) begin // h-position = 1 represent I/O input
                    IORead = 1'b1;
                end
                else begin
                    MemRead = 1;
                end
                MemorIOtoReg = 1'b1;
            end
            //S-type
            7'b0100011:begin
                ALUSrc = 1'b1;
                MemWrite = 1'b1;
                ALUOp = 4'b0000; //ADD
                if (Instruction[19:15] == 5'b11011 & ({Instruction[31:25],Instruction[11:7]} == 12'd6|{Instruction[31:25],Instruction[11:7]} == 12'd7)) begin //IO input
                    IOWrite = 1;
                end else begin
                    MemWrite = 1;
                end
            end
            //B-type
            7'b1100011:begin
                case(func3)
                    3'b000:begin
                        Branch = 1'b1; //beq,blt,bge,bltu,bgeu
                    end
                    3'b100:begin
                        Branch_lt = 1'b1;
                    end
                    3'b110:begin
                        Branch_ltu = 1'b1;
                    end
                    3'b101:begin
                        Branch_ge = 1'b1;
                    end
                    3'b111:begin
                        Branch_geu = 1'b1;
                    end
                    3'b001:begin
                        nBranch = 1'b1; //bne
                    end
                endcase
                ALUOp = 4'b0001; //SUB
            end
            //J-type
            7'b1101111:begin
                Jal = 1'b1;
                RegWrite = 1'b1;
            end
            //I-type(jalr)
            7'b1100111:begin
                Jr = 1'b1;
                RegWrite = 1'b1;
                ALUSrc = 1'b1;
            end
            //lui
            7'b0110111:begin
                RegWrite = 1'b1;
                ALUSrc = 1'b1;
                ALUOp = 4'b1000;//LUI
            end
            //auipc
            7'b0010111:begin
                RegWrite = 1'b1;
                ALUSrc = 1'b1;
                ALUOp = 4'b1001;//AUIPC
            end
        endcase
    end
    


endmodule
