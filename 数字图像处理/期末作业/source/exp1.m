% 读取图像文件
rgb = imread('./test.jpg');

% 提取RGB三个通道
rgb_r = rgb(:,:,1);
rgb_g = rgb(:,:,2);
rgb_b = rgb(:,:,3);

% 获取图像的尺寸
[n, m] = size(rgb);
% 创建与RGB图像相同尺寸的零矩阵
zero = zeros(n, m/3);

% 生成分离后的R、G、B通道图像
R = cat(3, rgb_r, zero, zero);
G = cat(3, zero, rgb_g, zero);
B = cat(3, zero, zero, rgb_b);

% 显示R、G、B通道图像
figure;
subplot(2,2,1), imshow(R), title('R Component');
subplot(2,2,2), imshow(G), title('G Component');
subplot(2,2,3), imshow(B), title('B Component');
subplot(2,2,4), imshow(rgb), title('RGB Component');

% 计算YUV颜色空间
Y = 0.299 * rgb_r + 0.587 * rgb_g + 0.114 * rgb_b;
U = -0.14713 * rgb_r - 0.288886 * rgb_g + 0.436 * rgb_b;
V = 0.615 * rgb_r - 0.51499 * rgb_g - 0.10001 * rgb_b;
YUV = cat(3, Y, U, V);

% 计算YCbCr颜色空间
Cb = -0.168736 * rgb_r - 0.331264 * rgb_g + 0.5 * rgb_b + 0.5;
Cr = 0.5 * rgb_r - 0.418688 * rgb_g - 0.081312 * rgb_b + 0.5;
YCbCr = cat(3, Y, Cb, Cr);

% 显示YUV和YCbCr图像
figure;
subplot(1,2,1), imshow(YUV), title('YUV');
subplot(1,2,2), imshow(YCbCr), title('YCbCr');