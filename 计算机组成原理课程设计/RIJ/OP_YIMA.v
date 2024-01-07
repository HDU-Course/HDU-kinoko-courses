`timescale 1ns / 1ps

module OP_YIMA(
    input [31:0] inst, // 输入的指令（32位）
    output reg [2:0] ALU_OP, // ALU 操作码（3位）
    output reg [4:0] rs, // rs 寄存器号（5位）
    output reg [4:0] rt, // rt 寄存器号（5位）
    output reg [4:0] rd, // rd 寄存器号（5位）
    output reg Write_Reg, // 写使能信号
    output reg [15:0] imm, // 立即数（16位）
    output reg imm_s, // 立即数选择信号
    output reg rt_imm_s, // rt 或立即数选择信号
    output reg Mem_Write, // 内存写使能信号
    output reg [25:0] address, // 地址（26位）
    output reg [1:0] w_r_s, // 写寄存器选择信号
    output reg [1:0] wr_data_s, // 写数据选择信号
    output reg [1:0] PC_s, // PC 选择信号
    input ZF // 零标志位
);
    always @(*)
    begin
        //----------R指令----------
        if (inst[31:26] == 6'b000000) // R 类指令
        begin
            rd = inst[15:11];
            rt = inst[20:16];
            rs = inst[25:21];
            wr_data_s = 2'b00;
            Mem_Write = 0;
            w_r_s = 2'b00;
            rt_imm_s = 0;
            case (inst[5:0])
                6'b100000: begin ALU_OP = 3'b100; Write_Reg = 1; PC_s = 2'b00; end // add
                6'b100010: begin ALU_OP = 3'b101; Write_Reg = 1; PC_s = 2'b00; end // subtract
                6'b100100: begin ALU_OP = 3'b000; Write_Reg = 1; PC_s = 2'b00; end // bitwise AND
                6'b100101: begin ALU_OP = 3'b001; Write_Reg = 1; PC_s = 2'b00; end // bitwise OR
                6'b100110: begin ALU_OP = 3'b010; Write_Reg = 1; PC_s = 2'b00; end // bitwise XOR
                6'b100111: begin ALU_OP = 3'b011; Write_Reg = 1; PC_s = 2'b00; end // bitwise NOR
                6'b101011: begin ALU_OP = 3'b110; Write_Reg = 1; PC_s = 2'b00; end // set less than
                6'b000100: begin ALU_OP = 3'b111; Write_Reg = 1; PC_s = 2'b00; end // branch on equal
                6'b001000: begin ALU_OP = 3'b100; Write_Reg = 0; PC_s = 2'b01; end // load word
            endcase
        end
        //---------I类指令-------
        if (inst[31:29] == 3'b001) // I 类指令
        begin
            imm = inst[15:0];
            rt = inst[20:16];
            rs = inst[25:21];
            Mem_Write = 0;
            rt_imm_s = 1;
            imm_s = 1;
            w_r_s = 2'b01;
            Write_Reg = 1;
            wr_data_s = 2'b00;
            case (inst[31:26])
                6'b001000: begin imm_s = 1; ALU_OP = 3'b100; end // add immediate
                6'b001100: begin imm_s = 0; ALU_OP = 3'b000; end // bitwise AND immediate
                6'b001110: begin imm_s = 0; ALU_OP = 3'b010; end // bitwise OR immediate
                6'b001011: begin imm_s = 0; ALU_OP = 3'b110; end // set less than immediate
            endcase
        end
        //--------I取/存指令------
        if ((inst[31:30] == 2'b10) && (inst[28:26] == 3'b011)) // I 类取/存指令
        begin
            imm = inst[15:0];
            rt = inst[20:16];
            rs = inst[25:21];
            rt_imm_s = 1;
            imm_s = 1;
            w_r_s = 2'b01;
            wr_data_s = 2'b01;
            PC_s = 2'b00;
            case (inst[31:26])
                6'b100011: begin Mem_Write = 0; Write_Reg = 1; ALU_OP = 3'b100; end // load word
                6'b101011: begin Mem_Write = 1; Write_Reg = 0; ALU_OP = 3'b100; end // store word
            endcase
        end
        //-----------I转移指令---------
        if (inst[31:27] == 5'b00010) // I 类转移指令
        begin
            imm = inst[15:0];
            rt = inst[20:16];
            rs = inst[25:21];
            case (inst[31:26])
                6'b000100: begin rt_imm_s = 0; ALU_OP = 3'b101; Write_Reg = 0; Mem_Write = 0; PC_s = (ZF ? 2'b10 : 2'b00); end // branch on equal zero
                6'b000101: begin rt_imm_s = 0; ALU_OP = 3'b101; Write_Reg = 0; Mem_Write = 0; PC_s = (ZF ? 2'b00 : 2'b10); end // branch on not equal zero
            endcase
        end
        //----------J转移指令----------
        if (inst[31:27] == 5'b00001) // J 类转移指令
        begin
            address = inst[25:0];
            case (inst[31:26])
                6'b000010: begin w_r_s = 2'b00; Write_Reg = 0; Mem_Write = 0; PC_s = 2'b11; end // jump
                6'b000011: begin w_r_s = 2'b10; wr_data_s = 2'b10; Write_Reg = 1; Mem_Write = 0; PC_s = 2'b11; end // jump and link
            endcase
        end
    end
endmodule
