% 创建方形
img_square = zeros(100);
[rows, cols] = size(img_square);
center = [rows/2, cols/2];
side_length = 40;
square_top_left = center - side_length/2;
square_bottom_right = center + side_length/2;
img_square(square_top_left(1):square_bottom_right(1), square_top_left(2):square_bottom_right(2)) = 255;
figure;
imshow(uint8(img_square));

% 创建条纹线
line_width = 5;
line_spacing = 10;
for i = 1:line_width
    img_stripes(i:line_spacing:end,:) = 255;
end
figure;
imshow(uint8(img_stripes));

% 创建圆形
img_circle = zeros(100);
[rows, cols] = size(img_circle);
center = [rows/2, cols/2];
radius = 20;
for i = 1:rows
    for j = 1:cols
        if sqrt((i-center(1))^2 + (j-center(2))^2) <= radius
            img_circle(i, j) = 255;
        end
    end
end
figure;
imshow(uint8(img_circle));

% 创建矩形
img_rectangle = zeros(100);
[rows, cols] = size(img_rectangle);
rect_top = 30;
rect_bottom = 70;
rect_left = 20;
rect_right = 80;
img_rectangle(rect_top:rect_bottom, rect_left:rect_right) = 255;
figure;
imshow(uint8(img_rectangle));

% 创建三角形
img_triangle = zeros(100);
triangle_height = 30;
triangle_base = 40;
triangle_top = [50, 50];
for i = 1:rows
    for j = 1:cols
        if j >= triangle_top(2) - triangle_base/2 && j <= triangle_top(2) + triangle_base/2 && i >= triangle_top(1) && i <= triangle_top(1) + triangle_height - abs(j - triangle_top(2))
            img_triangle(i, j) = 255;
        end
    end
end
figure;
imshow(uint8(img_triangle));



% 对方形进行45°旋转
theta = 45;
tform = affine2d([cosd(theta) -sind(theta) 0; sind(theta) cosd(theta) 0; 0 0 1]);
img_rotated = imwarp(img_square, tform);
figure;
imshow(uint8(img_rotated));



% DCT 应用
RGB = imread('test.jpg');
I = im2gray(RGB);
J = dct2(I);
imshow(log(abs(J)), []);
colormap parula;
colorbar;


% IDCT 逆变换
RGB = imread('test.jpg');
I = rgb2gray(RGB);
J = dct2(I);
K = idct2(J);
figure;
imshow(uint8(K));
title('Reconstructed Image');


% 不同图像 DCT 对比
smooth_image = ones(100, 100) * 128;
verticle_stripes = repmat([0 255], 50, 50);
horizontal_stripes = repmat([0; 255], 50, 50);
checkboard = repmat([0 255; 255 0], 25, 25);
noise_image = uint8(rand(100, 100) * 255);



images = { smooth_image, verticle_stripes, horizontal_stripes, checkboard, noise_image};
titles = {'smooth', 'verticle', 'horizontal', 'checkboard', 'noise'};

figure;

for i = 1:length(images)
    I= images{i};
    J = dct2(I);
    
    subplot(length(images), 2, 2*i-1);
    imshow(I, []);
    title(titles{i});
    colormap(gca, gray);
    axis image;

    subplot(length(images), 2, 2*i-1);
    imshow(log(abs(J)), []);
    colormap(gca, parula);
    colorbar;
    title(['DCT of ', titles{i}]);
    axis image;
end