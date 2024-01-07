`timescale 1ns / 1ps

module TOP_LED(clk_100MHz, oclk, rst, SW, LED);
    input clk_100MHz;    // 输入时钟信号，频率为100MHz
    input oclk, rst;     // 输入时钟信号和复位信号
    input [3:0] SW;      // 4位开关输入
    output reg [7:0] LED;    // 8位LED输出

    wire rclk;           // 用于连接xiaodou模块的时钟信号
    wire ZF, OF;         // 用于连接TOP_RIJ_CPU模块的标志位
    wire [31:0] F;       // 用于连接TOP_RIJ_CPU模块的结果数据
    wire [31:0] M_R_Data; // 用于连接TOP_RIJ_CPU模块的内存读取数据
    wire [31:0] PC;      // 用于连接TOP_RIJ_CPU模块的程序计数器

    // 实例化xiaodou模块
    xiaodou doudong(clk_100MHz, oclk, rclk);  // 实例化一个名为doudong的xiaodou模块

    // 实例化TOP_RIJ_CPU模块
    TOP_RIJ_CPU(rst, clk_100MHz, rclk, ZF, OF, F, M_R_Data, PC);  // 实例化一个名为TOP_RIJ_CPU的模块

    always @(*)
    begin
        case (SW)  // 根据开关输入SW的值进行不同的操作
            4'b0000: LED = F[7:0];     // 当SW为0000时，LED显示F的低8位
            4'b0001: LED = F[15:8];    // 当SW为0001时，LED显示F的8位到15位
            4'b0010: LED = F[23:16];   // 当SW为0010时，LED显示F的16位到23位
            4'b0011: LED = F[31:24];   // 当SW为0011时，LED显示F的24位到31位
            4'b0100: LED = M_R_Data[7:0];   // 当SW为0100时，LED显示M_R_Data的低8位
            4'b0101: LED = M_R_Data[15:8];  // 当SW为0101时，LED显示M_R_Data的8位到15位
            4'b0110: LED = M_R_Data[23:16]; // 当SW为0110时，LED显示M_R_Data的16位到23位
            4'b0111: LED = M_R_Data[31:24]; // 当SW为0111时，LED显示M_R_Data的24位到31位
            4'b1000: begin   // 当SW为1000时
                LED[7:2] = 0;   // LED的高6位清零
                LED[1] = OF;    // LED的第7位设置为OF标志位
                LED[0] = ZF;    // LED的最低位设置为ZF标志位
            end
            4'b1100: LED = PC[7:0];    // 当SW为1100时，LED显示PC的低8位
            4'b1101: LED = PC[15:8];   // 当SW为1101时，LED显示PC的8位到15位
            4'b1110: LED = PC[23:16];  // 当SW为1110时，LED显示PC的16位到23位
            4'b1111: LED = PC[31:24];  // 当SW为1111时，LED显示PC的24位到31位
            default: LED = 0;   // 默认情况下，LED显示全0
        endcase
    end
endmodule
