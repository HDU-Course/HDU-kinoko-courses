% 展示图像
image = imread('test.jpg');
imshow(image);

% 转变为灰度图
image_gray = rgb2gray(image);
imshow(image_gray);

% 显示直方图
histogram1 = imhist(image_gray);
figure;
bar(histogram1);

% a. 使用线性拉伸函数对灰度值进行拉伸
min_val = double(min(image_gray(:)));
max_val = double(max(image_gray(:)));
stretched_image = uint8((double(image_gray) - min_val) / (max_val - min_val) * 255);

% b. 计算图像值的出现概率
num_pixels = numel(stretched_image);
histogram = hist(double(stretched_image(:)), 256) / num_pixels;

% c. 计算图像值的累积分布函数(CDF)
cdf = cumsum(histogram);

% d. 使用通用直方图均衡化公式获得最终处理的图像
equalized_image = uint8(255 * cdf(stretched_image + 1));

% 显示原始图像和增强对比度后的图像
figure;
subplot(1, 2, 1);
imshow(stretched_image);
title('Stretched Image');

subplot(1, 2, 2);
imshow(equalized_image);
title('Histogram Equalized Image');