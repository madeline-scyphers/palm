function [DBH]=Get_DBH(patch,HDBHpar, Height, nx,Dx, ny,Dy, StandDenc, numpatch)
%[DBH]=Get_DBH(patch,HDBHpar, Height, nx,Dx, ny,Dy, StandDenc, numpatch)
%
% Copyright: Gil Bohrer and Roni avissar, Duke University, 2006
% Calculate stem locations and scale DBH for each stem based on canopy
% height and allometric relationship between height and stem diameter and
% breast height (DBH). Assumes the stem is under the tallest part of a subsection of the
% canopy that represent a tree. These subsections are uniformly meshed (on a coarser mesh than the canopy domain) and
% are approximately based on stand density.
%
% Input
% patch - patch-type map (integer matrix [ny,nx])
% HDBHpar - Patch specific allometric parameters to fit height and DBH (real matrix [numpatch,3])
% Height - canopy top heights map (real matrix [ny,nx])
% nx,Dx,ny,Dy - mesh dimensions (integer)
% StandDenc - stand density Trees/Hectare (real vector [numpatch])
% numpatch - # patch-types (integer)
%
% Output
% DBH - map of DBH [m] (real matrix [ny,nx]). DBH=0 where there is no stem.


DBH=zeros(ny,nx);
for i = 1:numpatch
 
    cjxmax=1;
    cjymax=1;
    [StemDensityGridPT]=Find_StemDensityGridPT(StandDenc(i),Dx,min(ny,nx),Dy);
    for ix = 1:(floor(nx/StemDensityGridPT)+1)
        for iy = 1:(floor(ny/StemDensityGridPT)+1)
            maxH=0;
            emptyind=1;
            for jx= 1: StemDensityGridPT
                cjx = (ix-1)*StemDensityGridPT+jx;
                if cjx <= length(Height(1,:))
                    for jy=1:StemDensityGridPT
                        cjy =(iy-1)*StemDensityGridPT+jy;
                        if cjy <= length(Height(:,1)) & patch(cjy,cjx)==i
                            emptyind=0;
                            if Height(cjy,cjx) > maxH
                                maxH = Height(cjy,cjx);
                                cjxmax = cjx;
                                cjymax = cjy;
                            end
                        end
                    end
                end
            end
            if emptyind == 0
                %scale DBH with Height, based on Naidu et al 98 can j for res - this function should be replaced
                %if the user has another observed allometric indication of stem diameter 
                DBH(cjymax,cjxmax) =(StandDenc(i)/10000*StemDensityGridPT^2)*HDBHpar(i,3)*(10^((log10(Height(cjymax,cjxmax)*100)-HDBHpar(i,2))/HDBHpar(i,1))/100);
            end
        end
    end
                    
end

return



