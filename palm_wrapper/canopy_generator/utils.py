import numpy as np
from scipy.fft import fft2, ifft2
from scipy.stats import norm


def calculate_autocorrelation_function(nx, ny, Dx, Dy, L):
    x = np.arange(-(nx - 1) / 2, (nx - 1) / 2 + 1) * Dx
    y = np.arange(-(ny - 1) / 2, (ny - 1) / 2 + 1) * Dy
    X, Y = np.meshgrid(x, y, indexing="ij")

    AcF = np.exp(-(1 / L) * (X**2 + Y**2) ** 0.5)
    return AcF


def Find_StemDensityGridPT(StemDensityTPHa, Dx, nxy, Dy):
    """
    function [StemDensityGridPT]=Find_StemDensityGridPT(StemDensityTPHa,Dx,nxy,Dy)
    Calculate a rounded coarse mesh resolution (in integer mesh-point number)
    in which to place stems. 1 stem will be placed at each coarse mesh grid-cell

    Copyright: Gil Bohrer and Roni avissar, Duke University, 2006

    """
    StemDensityGridPT = 0
    i = 1
    while i < nxy:
        sizeHa = Dx * Dy * StemDensityTPHa / 10000
        if sizeHa * (i * i + (i + 1) * (i + 1)) / 2 >= 1:
            StemDensityGridPT = i
            i = nxy
        i = i + 1

    if StemDensityGridPT == 0:
        StemDensityGridPT = nxy

    return StemDensityGridPT


def get_stem_diam_and_breast_height(patch, HDBHpar, Height, nx, Dx, ny, Dy, StandDenc, numpatch):
    """
    Copyright: Gil Bohrer and Roni avissar, Duke University, 2006
    Calculate stem locations and scale DBH for each stem based on canopy
    height and allometric relationship between height and stem diameter and
    breast height (DBH). Assumes the stem is under the tallest part of a subsection of the
    canopy that represent a tree. These subsections are uniformly meshed (on a coarser mesh than the canopy domain) and
    are approximately based on stand density.

    Input
        patch - patch-type map (integer matrix [ny,nx])
        HDBHpar - Patch specific allometric parameters to fit height and DBH (real matrix [numpatch,3])
        Height - canopy top heights map (real matrix [ny,nx])
        nx,Dx,ny,Dy - mesh dimensions (integer)
        StandDenc - stand density Trees/Hectare (real vector [numpatch])
        numpatch - # patch-types (integer)

    Output
        DBH - map of DBH [m] (real matrix [ny,nx]). DBH=0 where there is no stem.
    """
    DBH = np.zeros((nx, ny))
    for i in range(numpatch):

        cjxmax = 1
        cjymax = 1
        StemDensityGridPT = Find_StemDensityGridPT(StandDenc[i], Dx, min(nx, ny), Dy)
        for ix in range(nx // StemDensityGridPT + 1):
            for iy in range(ny // StemDensityGridPT + 1):
                maxH = 0
                emptyind = 1
                for jx in range(StemDensityGridPT):
                    cjx = (ix - 1) * StemDensityGridPT + jx
                    if cjx <= len(Height[0, :]):
                        for jy in range(StemDensityGridPT):
                            cjy = (iy - 1) * StemDensityGridPT + jy
                            if cjy <= len(Height[:, 0]) and patch[cjx, cjy] == i:
                                emptyind = 0
                                if Height[cjx, cjy] > maxH:
                                    maxH = Height[cjx, cjy]
                                    cjxmax = cjx
                                    cjymax = cjy
                if emptyind == 0:
                    # scale DBH with Height, based on Naidu et al 98 can j for res - this function should be replaced
                    # if the user has another observed allometric indication of stem diameter
                    DBH[cjxmax, cjymax] = (
                        (StandDenc[i] / 10000 * StemDensityGridPT**2)
                        * HDBHpar[i, 2]
                        * (10 ** ((np.log10(Height[cjxmax, cjymax] * 100) - HDBHpar[i, 1]) / HDBHpar[i, 0]) / 100)
                    )

    return DBH


def Generate_PatchMap(patchtype, lambda_r, nx, ny, PatchCutOff, numpatch):
    """
    Apply histogram filter to a random regional level (inter-patch) random field to generate patchtype map.
    Copyright: Gil Bohrer and Roni avissar, Duke University, 2006

    Input :
        patchtype - patch types (vector[numpatch])
        lambda_r - a random regional level (inter-patch) random field (matrix[ny,nx])
        ny,nx - # grid-points on x,y, axes (integer)
        PatchCutOff - cumulative fraction of the area occupied by each patch type. Sorted at the same order as patchtype (vector[numpatch])
        numpatch - number of patch types

    Output
        patch - a map of patch type indexes. The actual patch types in this map (at point x,y) is given by patchtype(patch(y,x))"""

    patch = np.zeros(lambda_r.shape, dtype=np.int8) - 1
    # patch = - lambda_r / lambda_r
    # LAIvec = lambda_r.reshape((nx * ny, 1))
    LAIvec = lambda_r[~np.isnan(lambda_r)]
    values, bins = np.histogram(LAIvec, bins=100)
    N, Lx = values, bins  # TODO remove

    cumN = np.zeros(len(N) + 1)

    for j in range(1, len(N) + 1):
        cumN[j] = cumN[j - 1] + N[j - 1]

    norm_cdf = norm.cdf(values)

    cumN = cumN / cumN[len(N)]
    # figure(500); plot(Lx,(N-min(N))/(max(N)-min(N)),'-k',[0, Lx],cumN,'--k'),axis('tight')

    px = np.zeros(numpatch + 1)
    cumulat = 0
    h = 0
    dj = 1
    while dj < numpatch:
        cumulat = cumulat + N[h]
        if cumulat > (PatchCutOff[dj - 1] * len(LAIvec)):
            px[dj] = Lx[h]
            dj = dj + 1
        h = h + 1

    px[numpatch] = max(LAIvec)

    for i in range(numpatch):
        patchi = (lambda_r <= px[i + 1]) & (lambda_r > px[i])
        patch[patchi] = i

    return patch


def make_can_gen_rand_field(nx, ny, AcF, domain):
    """
    Generated a random phase, cyclic, 2-D field using FFT and an
    autocorrelation matrix
    Copyright: Gil Bohrer and Roni avissar, Duke University, 2006

    Input :
        X - meshed field of east-west coordinates (matrix[ny,nx])
        Y - meshed field of south-north coordinates (matrix[ny,nx])
        nx - # x grid points (integer)
        ny - # y grid points (integer)
        Dx - size [m] of x grid spacing (real)
        Dy - size [m] of x grid spacing (real)
        AcF - meshed field of auto-correlation function (matrix[ny,nx])

    Output:
        lambda - a random phase, cyclic, 2-D field
    """
    # Fourier trasnform the autocorrelation function
    ZF = fft2(AcF)
    # convert to real
    ZF2 = abs(ZF)

    # generate random phase matrix from uniform [0,1] to uniform [-pi,pi]
    R = 2 * np.pi * (np.random.rand(nx, ny) - 0.5)
    # compute complex amplitudes from real with random phase
    ZF3 = ZF2 * np.exp(1j * R)
    # inverse transform
    Z2 = ifft2(ZF3)
    # make real
    lambda_ = abs(Z2)

    # remove indexese not marked on domain
    lambda_ = lambda_ * domain
    return lambda_
