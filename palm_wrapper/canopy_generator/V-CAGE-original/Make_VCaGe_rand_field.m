function[lambda] = Make_VCaGe_rand_field(X,Y,nx,ny,Dx,Dy,AcF)
%[lambda] = Make_VCaGe_rand_field(X,Y,nx,ny,Dx,Dy,L,AcF)
%
% Generated a random phase, cyclic, 2-D field using FFT and an
% autocorrelation matrix
% Copyright: Gil Bohrer and Roni avissar, Duke University, 2006
%
% Input :
% X - meshed field of east-west coordinates (matrix[ny,nx]) 
% Y - meshed field of south-north coordinates (matrix[ny,nx])
% nx - # x grid points (integer)
% ny - # y grid points (integer)
% Dx - size [m] of x grid spacing (real)
% Dy - size [m] of x grid spacing (real)
% AcF - meshed field of auto-correlation function (matrix[ny,nx])
%
% Output:
% lambda - a random phase, cyclic, 2-D field


%Fourier trasnform the autocorrelation function
ZF=fft2(AcF);
%convert to real
ZF2=abs(ZF);

%generate random phase matrix from uniform [0,1] to uniform [-pi,pi]
R=pi*2*(rand(ny,nx)-0.5);
%compute complex amplitudes from real with random phase
ZF3 = ZF2.*exp(i*R);
%inverse transform
Z2=ifft2(ZF3);
%make real
lambda=abs(Z2);

return