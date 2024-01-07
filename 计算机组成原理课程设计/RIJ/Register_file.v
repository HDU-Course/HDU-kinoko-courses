module Register_file(R_Addr_A, R_Addr_B, W_Addr, Write_Reg, W_Data, Clk, Reset, R_Data_A, R_Data_B);
  input [4:0] R_Addr_A;     // 读取地址A
  input [4:0] R_Addr_B;     // 读取地址B
  input [4:0] W_Addr;       // 写入地址
  input Write_Reg;         // 写使能信号
  input [31:0] W_Data;     // 写入数据
  input Clk;              // 时钟信号
  input Reset;           // 复位信号
  output [31:0] R_Data_A; // 读取数据A
  output [31:0] R_Data_B; // 读取数据B
  reg [31:0] REG_Files[0:31]; // 寄存器文件，32个32位寄存器
  reg [5:0] i;             // 循环计数器

  // 初始化寄存器文件
  initial begin
    for (i = 0; i <= 31; i = i + 1)
      REG_Files[i] = 0;
  end

  // 连接读取数据输出
  assign R_Data_A = REG_Files[R_Addr_A];
  assign R_Data_B = REG_Files[R_Addr_B];

  // 在时钟上升沿或复位上升沿时执行操作
  always @(posedge Clk or posedge Reset) begin
    if (Reset) begin
      // 复位时将寄存器文件清零
      for (i = 0; i <= 31; i = i + 1)
        REG_Files[i] <= 0;
    end
    else begin
      // 当写使能信号为高且写入地址不为零时，执行写入操作
      if (Write_Reg && W_Addr != 0)
        REG_Files[W_Addr] <= W_Data;
    end
  end
endmodule
