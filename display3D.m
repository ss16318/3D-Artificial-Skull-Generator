
clear all;
close all;

im1 = load('Test.mat');     %note the model and test files are too large to upload to GitHub
im2 = load('model.mat');

im1 = im1.image;
im2 = im2.image;

im1 = im1 > 1000; %converts to a binary array
im2 = im2 > 1000; %converts to a binary array

spacing = 4;
im1 = im1(1:spacing:end , 1:spacing:end , 1:spacing:end ); %take every 64th pixel
im2 = im2(1:spacing:end , 1:spacing:end , 1:spacing:end ); %take every 64th pixel

[x1 y1 z1] = ind2sub(size(im1), find(im1)); %converts indices to coordinates
[x2 y2 z2] = ind2sub(size(im2), find(im2)); %converts indices to coordinates

figure;
plot3(y1, z1, x1, '.', 'MarkerSize' , 2); %displays in 3D
hold on;
plot3(y2, z2, x2, '.', 'MarkerSize' , 2); %displays in 3D
title('Artificial & Real Skulls')
legend('Artificial Skull (red)' , 'Real Skull (blue)')






