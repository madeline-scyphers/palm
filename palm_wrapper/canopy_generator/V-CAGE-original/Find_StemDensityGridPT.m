function [StemDensityGridPT]=Find_StemDensityGridPT(StemDensityTPHa,Dx,nxy,Dy)
% Calculate a rounded coarse mesh resolution (in integer mesh-point number)
% in which to place stems. 1 stem will be placed at each coarse mesh grid-cell
%
% Copyright: Gil Bohrer and Roni avissar, Duke University, 2006

StemDensityGridPT = 0;
i=1;
while i < nxy
    sizeHa = StemDensityTPHa/10000*Dx*Dy;
    if sizeHa*(i*i+(i+1)*(i+1))/2 >= 1 ;
        StemDensityGridPT = i;
        i=nxy;
    end
    i=i+1;
end

if StemDensityGridPT == 0
    StemDensityGridPT = nxy;
end

return