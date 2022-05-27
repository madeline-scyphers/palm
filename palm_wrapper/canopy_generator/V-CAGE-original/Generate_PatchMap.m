function [patch]=Generate_PatchMap(patchtype,lambda_r,ny,nx,PatchCutOff,numpatch)
%[patch]=Generate_PatchMap(patchtype,lambda_r,ny,nx,PatchCutOff)
%
%% Copyright: Gil Bohrer and Roni avissar, Duke University, 2006
%Apply histogram filter to a random regional level (inter-patch) random field to generate patchtype map.
%
% Input : 
% patchtype - patch types (vector[numpatch])
% lambda_r - a random regional level (inter-patch) random field (matrix[ny,nx])
% ny,nx - # grid-points on x,y, axes (integer)
% PatchCutOff - cumulative fraction of the area occupied by each patch type. Sorted at the same order as patchtype (vector[numpatch])  
% numpatch - number of patch types
%
% Output
% patch - a map of patch type indexes. The actual patch types in this map (at point x,y) is given by patchtype(patch(y,x)) 


patch=zeros(size(lambda_r));
LAIvec=reshape(lambda_r,[nx*ny 1]);
[N,Lx]=hist(LAIvec,100);

cumN = zeros(1,length(N)+1);
for j=2:length(N)+1
    cumN(j) = cumN(j-1)+N(j-1);
end
cumN = cumN/cumN(length(N)+1);
figure(500); plot(Lx,(N-min(N))/(max(N)-min(N)),'-k',[0, Lx],cumN,'--k'),axis('tight')

px=zeros(numpatch+1,1);
cumulat=0;
h=0;
dj=1;
while dj<numpatch
    h=h+1;
    cumulat=cumulat+N(h);
    if cumulat>PatchCutOff(dj)*nx*ny
        px(dj+1)=Lx(h);
        dj=dj+1;
    end
end
px(numpatch+1)=max(LAIvec);

for i = 1:numpatch
    patchi=find(lambda_r <= px(i+1) & lambda_r > px(i));
    patch(patchi)=i;           
end

return



