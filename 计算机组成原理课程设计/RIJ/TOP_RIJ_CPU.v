`timescale 1ns / 1ps

module TOP_RIJ_CPU(
    input rst,                      // 复位输入
    input clk_100MHz,               // 100MHz时钟输入
    input clk,                      // 时钟输入
    output ZF,                      // 零标志输出
    output OF,                      // 溢出标志输出
    output [31:0] F,                // ALU计算结果输出
    output [31:0] M_R_Data,         // 数据存储器读取数据输出
    output [31:0] PC                // 程序计数器输出
);
    wire Write_Reg;                 // 写寄存器使能信号
    wire [31:0] Inst_code;          // 指令代码
    wire [4:0] rs;                  // 源寄存器rs
    wire [4:0] rt;                  // 源寄存器rt
    wire [4:0] rd;                  // 目标寄存器rd
    wire [31:0] rs_data;            // 源寄存器rs的数据
    wire [31:0] rt_data;            // 源寄存器rt的数据
    wire [31:0] rd_data;            // 目标寄存器rd的数据
    wire [31:0] imm_data;           // 扩展后的立即数
    wire [15:0] imm;                // 立即数
    wire [1:0] w_r_s;               // 写寄存器选择信号
    wire imm_s;                     // 是否需要扩展立即数
    wire rt_imm_s;                  // B选择rt扩展imm
    wire Mem_Write;                 // 内存写使能信号
    wire [1:0] wr_data_s;           // 写数据选择信号
    wire [31:0] W_Addr;             // 写地址
    wire [31:0] W_Data;             // 写数据
    wire [31:0] R_Data_A;           // 源寄存器A的数据
    wire [31:0] R_Data_B;           // 源寄存器B的数据
    wire [31:0] F;                  // ALU计算结果
    wire [31:0] ALU_B;              // ALU的B端口
    wire [2:0] ALU_OP;              // ALU操作码
    wire [1:0] PC_s;                // 程序计数器选择信号
    wire [31:0] PC_new;             // 新的程序计数器值
    wire [31:0] PC;                 // 程序计数器
    wire [25:0] address;            // 内存地址

    // 实例化pc模块
    pc pc_connect_inst(clk, rst, PC_s, R_Data_A, imm_data, address, Inst_code, PC);  // 实例化一个名为pc_connect的pc模块

    // 实例化OP_YIMA模块
    OP_YIMA op(
        Inst_code, ALU_OP, rs, rt, rd, Write_Reg, imm, imm_s,
        rt_imm_s, Mem_Write, address, w_r_s, wr_data_s, PC_s, ZF
    );  // 实例化一个名为op的OP_YIMA模块

    assign W_Addr = (w_r_s[1]) ? 5'b11111 : ((w_r_s[0]) ? rt : rd);  // 根据写寄存器选择信号确定写地址

    assign imm_data = (imm_s) ? {{16{imm[15]}}, imm} : {{16{1'b0}}, imm};  // 根据是否需要扩展立即数进行立即数扩展

    // 实例化Register_file模块
    Register_file R_connect(
        rs, rt, W_Addr, Write_Reg, W_Data, clk, rst, R_Data_A, R_Data_B
    );  // 实例化一个名为R_connect的Register_file模块

    assign ALU_B = (rt_imm_s) ? imm_data : R_Data_B;  // 根据B选择信号确定ALU的B端口数据

    // 实例化ALU模块
    ALU ALU_connect(
        R_Data_A, ALU_B, F, ALU_OP, ZF, OF
    );  // 实例化一个名为ALU_connect的ALU模块

    // 实例化RAM_B模块
    RAM_B Data_Mem (
        .clka(clk_100MHz),           // 输入时钟
        .wea(Mem_Write),             // 写使能
        .addra(F[5:0]),              // 写地址
        .dina(R_Data_B),             // 写数据
        .douta(M_R_Data)             // 读数据
    );  // 实例化一个名为Data_Mem的RAM_B模块

    assign W_Data = (wr_data_s[1]) ? PC_new : ((wr_data_s[0]) ? M_R_Data : F);  // 根据写数据选择信号确定写数据

endmodule
