function [CSProfile, HDBHpar, LADcm,zcm, avg, avgH, sig, sigH, avgF, sigF, avgAlb, sigAlb, Bowen, sigBowen, StandDencity, AcF]=...
    ForestCanopy_data(ptype, nx, Dx, ny, Dy)
%[CSProfile, LADcm,zcm, avg, avgH, sig, sigH, StandDencity, AcFp]=ForestCanopy_data(ptype,canopytopCM, nx, Dx, ny, Dy)
%
% Copyright: Gil Bohrer and Roni avissar, Duke University, 2006
% User defined function that returns the normalized parameters of the
% canopy. This function gets a canopy code (patch type code) and return the
% appropriate parameters. The example here includes the data of Pine stand
% in the FACE site in Duke Forest in Dec/2001, and an arbitrary grass
% patch.
%
% Input 
% ptype - code for patch type (integer)
% nx, Dx, ny, Dy - grid mesh dimensions (integer)
%
% Output
% CSProfile - normalized (m^2 / DBH / m ) vertical profile at the normalized heights zcm
% LADcm - normalized (Tot LAI / m ) vertical profile at the normalized heights zcm
% zcm - normalized heights [m/m].
% avg - observed mean total (ground accumulated) LAI [m^2 leaf/m^2 ground]
% avgH - observed mean canopy top height [m] 
% sig - std of avg
% sigH - std of sigH
% StandDencity - number of stems / hectare 
% AcFp - autocorrelation function of canopy structure

canopytopCM=100;   %number of intervals in normalized LAD profile - The normalized profile is 1 m high, and therefore, canopytopCM=100 defines the profile every 1 cm.
zcm= double([0:canopytopCM])/double(canopytopCM); % normalized 0-1 [m] heights in 1 cm intervals
LADcm = zeros(canopytopCM+1,1)';

% example for 2 different canopy patches
if ptype==1 % 1=Duke forest loblolly pine December 2001, 
    StandDencity = 1733; %tree/ha
    TaperFunction = ([0.0065882 0.0065882 0.0054559 0.0043235 0.0035000 ...
        0.0026765 0.0019559 0.0012353 0.0010294 0.0008235 0.0000000]); %vertical profile of stem cross-sectional area [m^2] in observed points
    zvol = ([0 1.72 3.44 5.16 6.88 8.6 10.32 12.04 13.76 15.48 17.2]); %stem diameter measurement heights [m] in TaperFunction 
    DBHind = 2; %position in zvol vector of breast height
    HDBHpar = [0.967 1.854 1.0]; %[b1 b0 b00] b1,b0 are allometric parameters from Naidu et al 98 can j for res, Table 3
                                    %regression parameters of the function: log10(height[cm])=b1*log10(DBH[cm])+b0
                                    % b00 is used to cancel out non woody vegetation (i.e. make grass stems = 0)
                                    
    LAI =([0.0 0.007114 0.010536 0.010461 0.022015 0.030084 0.046287 0.228772 0.091491...  
            0.407698 0.099484, 0.023835 0.014457 0.003917 0.003848 0.0]);%vertical profile of LAI in observed points
    zlai =(0:15);     %measurement heights of points in LAI 
   
    avgH = 14.88; %mean Height to canopy top , Duke forest, heather McCarthy, measured in 100 trees apr-2002
    sigH = 2.053; %std of heights
    
    sigControl = 2.053;
    avg = 2.543; %the mean LAI !Duke forest, heather McCarthy, measured 6 ring plots 2001
    sig = 0.227*(sigH/sigControl); %LAI standard deviation
    
    avgF = 202.25 ;%mean total flux
    sigF = 10.0*(sigH/sigControl)  ;
    
    avgAlb= 0.1 ;%mean albedo
    sigAlb = 0.0005*(sigH/sigControl);
    
    Bowen = 1.91; %measured sensible/latent heat flux ratio
    sigBowen = 0.23*(sigH/sigControl) ; %std of bowen ratio
    
    %normalize LAI into LAD
    LAI = LAI/sum(LAI);
    lencm = double(ceil(max(zlai)*100))/double(canopytopCM);
    LADcm = interp1((zlai/lencm),LAI,zcm); 
    LADcm=LADcm/sum(LADcm);
    
    %calculate autocorrelation function, in this case - length-scale
    %derived, could be replaced by processed autocorrelation from an image or map
    L = 5.77; % canopy scale autocorrelation length, mean crown radius
    x=[-(nx-1)/2:(nx-1)/2]*Dx;  
    y=[-(ny-1)/2:(ny-1)/2]*Dy;
    [X,Y] = meshgrid(x,y);
    AcF=exp(-(1/L)*(X.^2+Y.^2).^0.5);
elseif ptype==2 %arbitrary grass patch
    StandDencity = 10000 ; %tree/ha 
    DBHind = 1; %position in zvol vector of breast height. stem diameter below this height is assumed constant.
    TaperFunction=([1.00 0.00 0.00 0.00 0.00 0.00]); %vertical profile of stem diameter in observed points
    zvol=([0 0.1 0.2 0.3 0.4 0.5]);  %stem volume measurement heights in TaperFunction 
    HDBHpar = [1.0 0.0 0.0];
  
    LAI=([0.1 0.2 0.2 0.35 0.15 0.0]); %vertical profile of LAI in observed points
    zlai=([0 0.1 0.2 0.3 0.4 0.5]); %measurement heights of points in LAI 
 
    avgH=0.3; %mean Height
    sigH=0.05; %std of heights
    
    sigControl = 0.05;
    avg= 0.5; %the mean LAI 
    sig= 0.01*(sigH/sigControl) ; %LAI standard deviation
    
    avgF = 202.25 ;%mean total flux nov-dec % 307.13 mean tot flux Apr
    sigF = 1.0*(sigH/sigControl) ;
    avgAlb= 0.218 ;%mean albedo nov-dec %  0.192 mean albedo Apr
    sigAlb = 0.0001*(sigH/sigControl);
    
    Bowen=2.72; %AVG bowen ratio for december 2001 noontime, sunny days
    sigBowen = 0.08*(sigH/sigControl); %std of bowen ratio for december 2001 noontime, sunny days
    
    LAI = LAI/sum(LAI);
    lencm = double(ceil(max(zlai)*100))/double(canopytopCM);
    LADcm = interp1((zlai/lencm),LAI,zcm); 
    LADcm=LADcm/sum(LADcm);
    L = 0.5;
    x=[-(nx-1)/2:(nx-1)/2]*Dx;  
    y=[-(ny-1)/2:(ny-1)/2]*Dy;
    [X,Y] = meshgrid(x,y);
    AcF=exp(-(1/L)*(X.^2+Y.^2).^0.5); %synthetic autocorrelation function. Could be replaced by an observed auto-correlation function, or patch type map
elseif ptype==4 %hardwood duke forest march-april
    StandDencity = 937; %tree/ha
    zvol = ([0 1.72 2*3.44 2*5.16 2*6.88 2*8.6 2*10.32 2*12.04 2*13.76 2*15.48 2*17.2]); %height points for TAPER FUNCTION (based on pine*2)
    DBHind = 2; %position in zvol vector of breast height
    HDBHpar = [0.7538 2.254 1.0]; %[b1 b0 gil-extra-normalization] Chris Oishi "FACE hadwood data.xls"
    TaperFunction = ([0.0065882 0.0065882 0.0054559 0.0043235 0.0035000 ...
        0.0026765 0.0019559 0.0012353 0.0010294 0.0008235 0.0000000]);
    zlai=([0.0 1.0 3.1 5.0 6.75 8.6 10.4 12.3 14.2 16.0 17.8 19.7 21.6 23.4 26.2 27.0 28.8 30.7 32.5]);
    LAI=([0.0 0.0394 0.0245 0.0173 0.0114 0.0109 0.0213 0.0295 0.0314 0.0300 ...
          0.0353 0.0427 0.0679 0.0654 0.0537 0.0283 0.0135 0.0110 0.0]);
   
    avgH= 24.06+0.25*24.06; %mean Height
    sigH= 0;% 3.79; %std of heights
    
    sigControl = 3.79;
    avg= 2.950; %the mean LAI 
    sig= 0.257*(sigH/sigControl); %LAI standard deviation
    
    avgF = 350.9 ;%for 1 patch simulations % 365.48 for 2 patchs;%mean total flux
    sigF = 10.0*(sigH/sigControl) ;
    
    avgAlb= 0.2; % for 1 patch simulations 0.139 for 2 patchs ;%mean albedo
    sigAlb = 0.0005*(sigH/sigControl);
   
    Bowen = 1.25; %apr 18 2002
    sigBowen = 0.16*(sigH/sigControl); %apr 18 2002
    
    LAI = LAI/sum(LAI);
    lencm = double(ceil(max(zlai)*100))/double(canopytopCM);
    LADcm = interp1((zlai/lencm),LAI,zcm); 
    LADcm=LADcm/sum(LADcm);
    
    L = 6.5337;
    x=[-(nx-1)/2:(nx-1)/2]*Dx;  
    y=[-(ny-1)/2:(ny-1)/2]*Dy;
    [X,Y] = meshgrid(x,y);
    AcF=exp(-(1/L)*(X.^2+Y.^2).^0.5);
    
elseif ptype==3 %hardwood duke forest nov-dec
    StandDencity = 937; %tree/ha
    zvol = ([0 1.72 2*3.44 2*5.16 2*6.88 2*8.6 2*10.32 2*12.04 2*13.76 2*15.48 2*17.2]); %height points for TAPER FUNCTION (based on pine*2)
    DBHind = 2; %position in zvol vector of breast height
    HDBHpar = [0.7538 2.254 1.0]; %[b1 b0 gil-extra-normalization] Chris Oishi "FACE hadwood data.xls"
    TaperFunction = ([0.0065882 0.0065882 0.0054559 0.0043235 0.0035000 ...
        0.0026765 0.0019559 0.0012353 0.0010294 0.0008235 0.0000000]);
    zlai=([0.0 1.0 3.1 5.0 6.75 8.6 10.4 12.3 14.2 16.0 17.8 19.7 21.6 23.4 26.2 27.0 28.8 30.7 32.5]);
    LAI=([0.0 0.0394 0.0245 0.0173 0.0114 0.0109 0.0213 0.0295 0.0314 0.0300 ...
          0.0353 0.0427 0.0679 0.0654 0.0537 0.0283 0.0135 0.0110 0.0]);
  
    avgH= 24.06; %mean Height
    sigH=  0; %3.79; %std of heights
    sigControl = 3.79;
    
    avg= 1.372; %the mean LAI 
    sig= 0.135*(sigH/sigControl); %LAI standard deviation
    
    avgF = 225;%232.58 ;%mean total flux
    sigF = 10.0*(sigH/sigControl) ;
    
    avgAlb= 0.2 ;%0.124 ;%mean albedo
    sigAlb = 0.0005*(sigH/sigControl);
   
    Bowen=15.25; %13.25 dec hardwood
    sigBowen = 0.25*(sigH/sigControl); %2.05 dec hardwood !Tot flx  180!156 !Nov hardwood 180
    
    LAI = LAI/sum(LAI);
    lencm = double(ceil(max(zlai)*100))/double(canopytopCM);
    LADcm = interp1((zlai/lencm),LAI,zcm); 
    LADcm=LADcm/sum(LADcm);
    
    L = 6.5337;
    x=[-(nx-1)/2:(nx-1)/2]*Dx;  
    y=[-(ny-1)/2:(ny-1)/2]*Dy;
    [X,Y] = meshgrid(x,y);
    AcF=exp(-(1/L)*(X.^2+Y.^2).^0.5);
  elseif ptype==17 %BCI 50 H
    StandDencity = 6000; %tree/ha
    zvol = ([0 1.72 2*3.44 2*5.16 2*6.88 2*8.6 2*10.32 2*12.04 2*13.76 2*15.48 2*17.2]); %height points for TAPER FUNCTION (based on pine*2)
    DBHind = 2; %position in zvol vector of breast height
    HDBHpar = [0.7538 2.254 1.0]; %[b1 b0 gil-extra-normalization] Chris Oishi "FACE hadwood data.xls"
    TaperFunction = ([0.0065882 0.0065882 0.0054559 0.0043235 0.0035000 ...
        0.0026765 0.0019559 0.0012353 0.0010294 0.0008235 0.0000000]);
    zlai=([0 1 3 5 7 9 11 13 15 17 19 21 23 25 27 29 31 33 35 37]);
    LAI=([0.0 0.022816683 0.066995499 0.059196721 0.026734183 0.039798298 0.036912367 ...
        0.082735363 0.078359437 0.08699766 0.019589859 0.014573452 0.003917972 ...
        0.003263962 0.015038233 0.00403354 0.066829447 0.215488451 0.156718874 0.0]);
   
    avgH= 35; %mean Height
    sigH= 2.113; %std of heights
    
    sigControl = sigH;
    avg= 5.43; %the mean LAI 
    sig= 0.81*(sigH/sigControl); %LAI standard deviation
    
    avgF = 350.9 ;%for 1 patch simulations % 365.48 for 2 patchs;%mean total flux
    sigF = 10.0*(sigH/sigControl) ;
    
    avgAlb= 0.2; % for 1 patch simulations 0.139 for 2 patchs ;%mean albedo
    sigAlb = 0.0005*(sigH/sigControl);
   
    Bowen = 1.25; %apr 18 2002
    sigBowen = 0.16*(sigH/sigControl); %apr 18 2002
    
    LAI = LAI/sum(LAI);
    lencm = double(ceil(max(zlai)*100))/double(canopytopCM);
    LADcm = interp1((zlai/lencm),LAI,zcm); 
    LADcm=LADcm/sum(LADcm);
    
    L = 37.037;
    x=[-(nx-1)/2:(nx-1)/2]*Dx;  
    y=[-(ny-1)/2:(ny-1)/2]*Dy;
    [X,Y] = meshgrid(x,y);
    AcF=exp(-(1/L)*(X.^2+Y.^2).^0.5);
     
end

TaperFunction=TaperFunction/TaperFunction(DBHind);
lencm = double(ceil(max(zvol)*100))/double(canopytopCM);
CSProfile = interp1((zvol/lencm),TaperFunction,zcm);
   
return

    
