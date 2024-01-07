`timescale 1ns / 1ps

module test;

    // 输入
    reg rst;                    // 复位信号，用于将系统置于初始状态
    reg clk_100MHz;             // 100MHz 时钟信号，用于驱动模块
    reg clk;                    // 时钟信号，用于时序控制

    // 输出
    wire ZF;                    // 零标志位，用于表示运算结果是否为零
    wire OF;                    // 溢出标志位，用于表示运算是否发生溢出
    wire [31:0] F;              // F 寄存器，32 位数据
    wire [31:0] M_R_Data;       // M_R_Data 寄存器，32 位数据
    wire [31:0] PC;             // PC 寄存器，32 位数据

    // 实例化被测试的模块（UUT）
    TOP_RIJ_CPU uut (
        .rst(rst), 
        .clk_100MHz(clk_100MHz), 
        .clk(clk), 
        .ZF(ZF), 
        .OF(OF), 
        .F(F), 
        .M_R_Data(M_R_Data), 
        .PC(PC)
    );

    initial begin
        // 初始化输入信号
        rst = 0;                // 将复位信号初始化为低电平
        clk_100MHz = 0;         // 将 100MHz 时钟信号初始化为低电平
        clk = 0;                // 将时钟信号初始化为低电平

        #100;                   // 等待全局复位完成，持续 100ns

        // 在这里添加刺激信号
        forever begin
            #2;                // 延时 2ns
            clk = ~clk;        // 时钟信号取反，实现时钟的上升沿和下降沿切换
            #10;               // 延时 10ns
            clk_100MHz = ~clk_100MHz;  // 100MHz 时钟信号取反，实现时钟的上升沿和下降沿切换
        end
    end
      
endmodule
