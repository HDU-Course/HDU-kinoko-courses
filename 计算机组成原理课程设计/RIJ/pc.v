`timescale 1ns / 1ps

module pc(
    input clk,                 // 时钟输入
    input rst,                 // 复位输入
    input [1:0] PC_s,          // 程序计数器选择信号
    input [31:0] R_Data_A,     // 寄存器数据输入
    input [31:0] imm_data,     // 立即数数据输入
    input [25:0] address,      // 地址输入
    output [31:0] Inst_code,   // 指令代码输出
    output [31:0] PC           // 程序计数器输出
);
    reg [31:0] PC;             // 程序计数器寄存器
    wire [31:0] PC_new;        // 新的程序计数器值

    initial
        PC <= 32'h00000000;   // 初始化程序计数器为全零

    // 实例化指令存储器模块 Inst_ROM
    Inst_ROM Inst_ROM1 (
        .clka(clk),            // 时钟输入
        .addra(PC[7:2]),       // 指令存储器地址输入（从程序计数器的[7:2]位获取）
        .douta(Inst_code)      // 指令代码输出
    );

    assign PC_new = PC + 4;    // 新的程序计数器值为当前值加4

    always @(negedge clk or posedge rst)  // 在时钟下降沿或复位上升沿触发
    begin
        if (rst)
            PC <= 32'h00000000;  // 复位时将程序计数器重置为全零
        else
        begin
            case (PC_s)          // 根据程序计数器选择信号进行不同的操作
                2'b00: PC <= PC_new;                             // 选择PC_new作为新的程序计数器值
                2'b01: PC <= R_Data_A;                            // 选择R_Data_A作为新的程序计数器值
                2'b10: PC <= PC_new + (imm_data << 2);            // 选择PC_new + (imm_data << 2)作为新的程序计数器值
                2'b11: PC <= {PC_new[31:28], address, 2'b00};      // 选择{PC_new[31:28], address, 2'b00}作为新的程序计数器值
            endcase
        end
    end
endmodule
