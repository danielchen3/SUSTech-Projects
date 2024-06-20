`timescale 1ns / 1ps

module ALU(
    input Branch,
    input nBranch,
    input Branch_lt,
    input Branch_ge,
    input Branch_ltu,
    input Branch_geu,
    input [31:0] Read_data_1,
    input [31:0] data,//From ALU_mux
    input [3:0] ALUOp,
    output reg Zero,
    output reg [31:0] ALU_result,
    output reg Branch_jump
    //output reg [31:0] Addr_result
    );
    
    reg [31:0] res;

    always @(*) begin
        case (ALUOp)
            4'b0000: ALU_result = Read_data_1 + data; // ADD
            4'b0001: ALU_result = Read_data_1 - data; // SUB
            4'b0010: ALU_result = Read_data_1 & data; // AND
            4'b0011: ALU_result = Read_data_1 | data; // OR
            4'b0100: ALU_result = Read_data_1 ^ data; // XOR
            4'b0101: ALU_result = Read_data_1 << data[4:0]; // SLL
            4'b0110: ALU_result = Read_data_1 >> data[4:0]; // SRL
            4'b0111: ALU_result = $signed(Read_data_1) >>> data[4:0]; // SRA
            4'b1000:ALU_result = Read_data_1<data?1:0;
            default: ALU_result = 32'b0;
        endcase
        Zero = (ALU_result == 0);
    end
    
    always @(*)begin
        if(Branch&&(Read_data_1 - data == 0)) Branch_jump = 1'b1;
        else if(nBranch&&(Read_data_1 - data != 0)) Branch_jump = 1'b1;
        else if(Branch_ltu && Read_data_1 < data) Branch_jump = 1'b1;
        else if(Branch_geu && Read_data_1 >= data) Branch_jump = 1'b1;
        else if(Branch_lt && $signed(Read_data_1) < $signed(data)) Branch_jump = 1'b1;
        else if(Branch_ge && $signed(Read_data_1) >= $signed(data)) Branch_jump = 1'b1;
        else Branch_jump = 1'b0;
    end
    

    // always @(*) begin
    //     if(ALUOp == 2'b00)begin
    //         if(ALUSrc == 1'b0)
    //             ALU_result = ReadData1+ReadData2;
    //         else ALU_result = ReadData1+imm32;
    //         if(ALU_result == 32'd0) zero = 1'b1;
    //         else zero = 1'b0;
    //     end
    //     else if(ALUOp == 2'b01)begin
    //         if(ALUSrc == 1'b0)
    //             ALU_result = ReadData1-ReadData2;
    //         else ALU_result = ReadData1-imm32;
    //         if(ALU_result == 32'd0) zero = 1'b1;
    //         else zero = 1'b0;
    //     end
    //     else if(ALUOp == 2'b10)begin
    //         if(funct3 == 3'b111)begin
    //             if(ALUSrc == 1'b0)  
    //                 ALU_result = ReadData1 & ReadData2;
    //             else ALU_result = ReadData1 & imm32;
    //             if(ALU_result == 32'd0) zero = 1'b1;
    //             else zero = 1'b0;
    //          end
    //         else if(funct3 == 3'b110)begin
    //             if(ALUSrc == 1'b0)
    //                 ALU_result = ReadData1 | ReadData2;
    //             else ALU_result = ReadData1 | imm32;
    //             if(ALU_result == 32'd0) zero = 1'b1;
    //             else zero = 1'b0;
    //         end
    //         else begin
    //             if(funct7 == 7'b0000000)begin
    //                 if(ALUSrc == 1'b0)
    //                     ALU_result = ReadData1 + ReadData2;
    //                 else ALU_result = ReadData1 + imm32;
    //                 if(ALU_result == 32'd0) zero = 1'b1;
    //                 else zero = 1'b0;
    //             end
    //             else if(funct7 == 7'b0100000)begin
    //                 if(ALUSrc == 1'b0)
    //                     ALU_result = ReadData1 - ReadData2;
    //                 else ALU_result = ReadData1 - imm32;
    //                 if(ALU_result == 32'd0) zero = 1'b1;
    //                 else zero = 1'b0;
    //             end
    //         end
    //     end
    // end
    
    
    
endmodule
