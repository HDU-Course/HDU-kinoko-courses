image = imread('test.jpg');
image_gray = rgb2gray(image);
fmean3 = ones(3,3);
fmean5 = ones(5,5);
fmean11 = ones(11,11);
fgaussian5_1 = fspecial('gaussian', 5, 1);
fgaussian7_05 = fspecial('gaussian', 7, 0.5);
fgaussian7_3 = fspecial('gaussian', 7, 3);
fsobelx = fspecial('sobel');
fsobely = fspecial('sobel')';
fprewittx = fspecial('prewitt');
flog = fspecial('log', 5, 1);
filtered_mean3 = imfilter(image_gray, fmean3);
filtered_mean5 = imfilter(image_gray, fmean5);
filtered_mean11 = imfilter(image_gray, fmean11);
filtered_gaussian5_1 = imfilter(image_gray, fgaussian5_1);
filtered_gaussian7_05 = imfilter(image_gray, fgaussian7_05);
filtered_gaussian7_3 = imfilter(image_gray, fgaussian7_3);
filtered_sobelx = imfilter(image_gray, fsobelx);
filtered_prewittx = imfilter(image_gray, fprewittx);
filtered_log = imfilter(image_gray, flog);

% a
figure;
subplot(3, 4, 1);
imshow(image_gray);
title('Original Image');

subplot(3, 4, 2);
imshow(filtered_mean3);
title('Mean 3x3');

subplot(3, 4, 3);
imshow(filtered_mean5);
title('Mean 5x5');

subplot(3, 4, 4);
imshow(filtered_mean11);
title('Mean 11x11');

subplot(3, 4, 5);
imshow(filtered_gaussian5_1);
title('Gaussian 5x5 s=1');

subplot(3, 4, 6);
imshow(filtered_gaussian7_05);
title('Gaussian 7x7 s=0.5');

subplot(3, 4, 7);
imshow(filtered_gaussian7_3);
title('Gaussian 7x7 s=3');

subplot(3, 4, 8);
imshow(filtered_sobelx);
title('Sobel X');

subplot(3, 4, 9);
imshow(filtered_prewittx);
title('Prewitt X');

subplot(3, 4, 10);
imshow(filtered_log);
title('Log');

% b
figure;

subplot(4, 3, 1);
freqz2(fmean3);
title('Mean 3x3');

subplot(4, 3, 2);
freqz2(fmean5);
title('Mean 5x5');

subplot(4, 3, 3);
freqz2(fmean11);
title('Mean 11x11');

subplot(4, 3, 4);
freqz2(fgaussian5_1);
title('Gaussian 5x5, σ=1');

subplot(4, 3, 5);
freqz2(fgaussian7_05);
title('Gaussian 7x7, σ=0.5');

subplot(4, 3, 6);
freqz2(fgaussian7_3);
title('Gaussian 7x7, σ=3');

subplot(4, 3, 7);
freqz2(fsobelx);
title('Sobel X');

subplot(4, 3, 8);
freqz2(fprewittx);
title('Prewitt X');

subplot(4, 3, 9);
freqz2(flog);
title('Log');

% 添加不同噪声并且使用不同边缘检测函数
% 添加不同类型的噪声
noisy_image_gaussian = imnoise(image_gray, 'gaussian', 0, 0.01);
noisy_image_salt_pepper = imnoise(image_gray, 'salt & pepper', 0.05);
noisy_image_poisson = imnoise(image_gray, 'poisson');
noisy_image_speckle = imnoise(image_gray, 'speckle', 0.02);

figure;
subplot(2, 3, 1);
imshow(image_gray);
title('Original Image');
subplot(2, 3, 2);
imshow(noisy_image_gaussian);
title('Gaussian Noise');
subplot(2, 3, 3);
imshow(noisy_image_salt_pepper);
title('Salt & Pepper Noise');
subplot(2, 3, 4);
imshow(noisy_image_speckle);
title('Speckle Noise');

% 边缘检测
edges_canny = edge(image_gray, 'canny');
edges_prewitt = edge(image_gray, 'prewitt');
edges_sobel = edge(image_gray, 'sobel');
edges_roberts = edge(image_gray, 'roberts');
edges_log = edge(image_gray, 'log');
% 显示原图和边缘检测结果
figure;
subplot(2, 3, 1);
imshow(image_gray)
title('Original Image');
subplot(2, 3, 2);
imshow(edges_canny)
title('Canny');
subplot(2, 3, 3);
imshow(edges_prewitt)
title('Prewitt');
subplot(2, 3, 4);
imshow(edges_sobel)
title('Sobel');
subplot(2, 3, 5);
imshow(edges_roberts)
title('Roberts');
subplot(2, 3, 6);
imshow(edges_log);
title('LOG');

% 显示直方图后设定阈值二值化
% 调整 threshold 的值来看看不同阈值对二值化结果的影响
img = imread('test.jpg');
figure;
subplot(2, 2, 1);
imshow(img);
title('Original Image');
subplot(2, 2, 2);
imhist(img);
title('Histogram');


img = imread('test.jpg');
subplot(2, 2, 1);
imshow(img);
title('Original Image');

img_gray = rgb2gray(img);
subplot(2, 2, 2);
imshow(img_gray);
title('Grayscale Image');

threshold = 100;
binary_img = imbinarize(img_gray, threshold/255);
subplot(2, 2, 3);
imshow(binary_img);
title('Binary Image (Threshold=100)');

threshold = 80;
binary_img_2 = imbinarize(img_gray, threshold/255);
subplot(2, 2, 4);
imshow(binary_img_2);
title('Binary Image (Threshold=80)');
