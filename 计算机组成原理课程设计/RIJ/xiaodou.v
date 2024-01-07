module xiaodou(
    input clk_100MHz,
    input BTN,
    output reg BTN_Out
    );
    reg BTN1,BTN2;          // 定义两个寄存器BTN1和BTN2
    wire BTN_Down;          // 定义一个线BTN_Down
    reg [21:0] cnt;         // 定义一个寄存器cnt，宽度为22位
    reg BTN_20ms_1,BTN_20ms_2;  // 定义两个寄存器BTN_20ms_1和BTN_20ms_2
    wire BTN_Up;            // 定义一个线BTN_Up
    
    always @(posedge clk_100MHz)   // 时钟上升沿触发的始终块
    begin
        BTN1 <= BTN;         // 将输入BTN的值赋给BTN1
        BTN2 <= BTN1;        // 将BTN1的值赋给BTN2
    end
    
    assign BTN_Down = (~BTN2) && BTN1;   // 将(~BTN2)与BTN1进行与操作，并将结果赋给BTN_Down
    
    always @(posedge clk_100MHz)   // 时钟上升沿触发的始终块
    begin
        if (BTN_Down)   // 如果BTN_Down为真
        begin
            cnt <= 22'b0;   // 将cnt设置为22位的零
            BTN_Out <= 1'b1;   // 将BTN_Out设置为1
        end
        else
            cnt <= cnt + 1'b1;   // cnt加1
        if (cnt == 22'h20000)   // 如果cnt等于22'h20000
            BTN_20ms_1 <= BTN;   // 将BTN的值赋给BTN_20ms_1
        BTN_20ms_2 <= BTN_20ms_1;   // 将BTN_20ms_1的值赋给BTN_20ms_2
        if (BTN_Up)   // 如果BTN_Up为真
            BTN_Out <= 1'b0;   // 将BTN_Out设置为0
    end
    
    assign BTN_Up = BTN_20ms_2 && (~BTN_20ms_1);   // 将BTN_20ms_2与(~BTN_20ms_1)进行与操作，并将结果赋给BTN_Up
endmodule
