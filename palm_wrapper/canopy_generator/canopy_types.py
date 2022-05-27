from dataclasses import dataclass, field

import numpy as np
from scipy import interpolate

from .utils import calculate_autocorrelation_function


@dataclass
class CanopyType:
    stand_density: int
    taper_profile: np.ndarray
    z_taper: np.ndarray
    breast_height_ind: int
    HDBHpar: np.ndarray
    LAI: np.ndarray
    zlai: np.ndarray
    avgH: float
    sigH: float
    sig_control: float

    avg_lai: float
    sig_lai: float
    avg_flux: float
    sig_flux: float
    avg_albedo: float
    sig_albedo: float
    bowen_ratio: float
    sig_bowen: float

    autocorrelation_length: float

    AcF: np.ndarray = field(init=False)
    LAD: np.ndarray = field(init=False)
    CSProfile: np.ndarray = field(init=False)
    zcm: np.ndarray = field(init=False)

    def __post_init__(self):
        self.sig_lai = self.sig_lai * (self.sigH / self.sig_control)
        self.sig_flux = self.sig_flux * (self.sigH / self.sig_control)
        self.sig_albedo = self.sig_albedo * (self.sigH / self.sig_control)
        self.sig_bowen = self.sig_bowen * (self.sigH / self.sig_control)

    def set_lad(self, mean_lai, zlad, dz):
        lad = interpolate.interp1d(np.arange(0, self.LAI.size * dz, dz), self.LAI)(zlad)
        self.lad = (lad / lad.sum()) * mean_lai

    def normalize_lai(self, canopytopCM, zcm):
        self.LAI = self.LAI / self.LAI.sum()
        lencm = np.ceil(max(self.zlai) * 100) / canopytopCM
        self.LADcm = interpolate.interp1d((self.zlai / lencm), self.LAI)(zcm)
        self.LAD = self.LADcm / sum(self.LADcm)

    def calculate_autocorrelation_function(self, nx, ny, Dx, Dy):
        self.AcF = calculate_autocorrelation_function(nx, ny, Dx, Dy, self.autocorrelation_length)

    def calculate_csprofile(self, canopytopCM, zcm):
        self.taper_profile = self.taper_profile / self.taper_profile[self.breast_height_ind]
        lencm = np.ceil(self.z_taper.max() * 100) / canopytopCM
        self.CSProfile = interpolate.interp1d((self.z_taper / lencm), self.taper_profile)(zcm)

    def export(self):
        return (
            self.CSProfile,
            self.HDBHpar,
            self.LAD,
            self.zcm,
            self.avg_lai,
            self.avgH,
            self.sig_lai,
            self.sigH,
            self.avg_flux,
            self.sig_flux,
            self.avg_albedo,
            self.sig_albedo,
            self.bowen_ratio,
            self.sig_bowen,
            self.stand_density,
            self.AcF,
        )


@dataclass
class Canopy:
    canopy_types: dict


duke_loblolly_pine = CanopyType(
    stand_density=1733,
    taper_profile=np.array(
        [
            0.0065882,
            0.0065882,
            0.0054559,
            0.0043235,
            0.0035000,
            0.0026765,
            0.0019559,
            0.0012353,
            0.0010294,
            0.0008235,
            0.0000000,
        ]
    ),
    z_taper=np.array([0, 1.72, 3.44, 5.16, 6.88, 8.6, 10.32, 12.04, 13.76, 15.48, 17.2]),
    breast_height_ind=1,
    HDBHpar=np.array([0.967, 1.854, 1.0]),
    LAI=np.array(
        [
            0.0,
            0.007114,
            0.010536,
            0.010461,
            0.022015,
            0.030084,
            0.046287,
            0.228772,
            0.091491,
            0.407698,
            0.099484,
            0.023835,
            0.014457,
            0.003917,
            0.003848,
            0.0,
        ]
    ),
    zlai=np.arange(0, 16),
    avgH=14.88,  # mean Height to canopy top , Duke forest, heather McCarthy, measured in 100 trees apr-2002
    sigH=2.053,
    sig_control=2.053,
    avg_lai=2.543,  # the mean LAI !Duke forest, heather McCarthy, measured 6 ring plots 2001
    sig_lai=0.227,
    avg_flux=202.25,
    sig_flux=10.0,
    avg_albedo=0.1,
    sig_albedo=0.0005,
    bowen_ratio=1.91,
    sig_bowen=0.23,
    autocorrelation_length=5.77,  # canopy scale autocorrelation length, mean crown radius
)


grass_pitch = CanopyType(
    stand_density=10_000,
    taper_profile=np.array([1.00, 0.00, 0.00, 0.00, 0.00, 0.00]),
    z_taper=np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5]),
    breast_height_ind=0,
    HDBHpar=np.array([0.967, 1.854, 1.0]),
    LAI=np.array([0.1, 0.2, 0.2, 0.35, 0.15, 0.0]),
    zlai=np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5]),
    avgH=0.3,
    sigH=0.05,
    sig_control=0.05,
    avg_lai=0.5,
    sig_lai=0.01,
    avg_flux=202.25,
    sig_flux=0.0001,
    avg_albedo=0.218,
    sig_albedo=0.0005,
    bowen_ratio=2.72,
    sig_bowen=0.08,
    autocorrelation_length=0.5,  # canopy scale autocorrelation length, mean crown radius
)


duke_hardwood_winter = CanopyType(
    stand_density=937,
    taper_profile=np.array(
        [
            0.0065882,
            0.0065882,
            0.0054559,
            0.0043235,
            0.0035000,
            0.0026765,
            0.0019559,
            0.0012353,
            0.0010294,
            0.0008235,
            0.0000000,
        ]
    ),
    z_taper=np.array(
        [0, 1.72, 2 * 3.44, 2 * 5.16, 2 * 6.88, 2 * 8.6, 2 * 10.32, 2 * 12.04, 2 * 13.76, 2 * 15.48, 2 * 17.2]
    ),
    breast_height_ind=1,
    HDBHpar=np.array([0.7538, 2.254, 1.0]),
    LAI=np.array(
        [
            0.0,
            0.0394,
            0.0245,
            0.0173,
            0.0114,
            0.0109,
            0.0213,
            0.0295,
            0.0314,
            0.0300,
            0.0353,
            0.0427,
            0.0679,
            0.0654,
            0.0537,
            0.0283,
            0.0135,
            0.0110,
            0.0,
        ]
    ),
    zlai=np.array(
        [0.0, 1.0, 3.1, 5.0, 6.75, 8.6, 10.4, 12.3, 14.2, 16.0, 17.8, 19.7, 21.6, 23.4, 26.2, 27.0, 28.8, 30.7, 32.5]
    ),
    avgH=24.06,
    sigH=1,
    sig_control=3.79,
    avg_lai=1.372,
    sig_lai=0.135,
    avg_flux=225,
    sig_flux=10,
    avg_albedo=0.2,
    sig_albedo=0.0005,
    bowen_ratio=15.25,
    sig_bowen=0.25,
    autocorrelation_length=6.5337,  # canopy scale autocorrelation length, mean crown radius
)


duke_hardwood_spring = CanopyType(
    stand_density=937,
    taper_profile=np.array(
        [
            0.0065882,
            0.0065882,
            0.0054559,
            0.0043235,
            0.0035000,
            0.0026765,
            0.0019559,
            0.0012353,
            0.0010294,
            0.0008235,
            0.0000000,
        ]
    ),
    z_taper=np.array(
        [0, 1.72, 2 * 3.44, 2 * 5.16, 2 * 6.88, 2 * 8.6, 2 * 10.32, 2 * 12.04, 2 * 13.76, 2 * 15.48, 2 * 17.2]
    ),
    breast_height_ind=1,
    HDBHpar=np.array([0.7538, 2.254, 1.0]),
    LAI=np.array(
        [
            0.0,
            0.0394,
            0.0245,
            0.0173,
            0.0114,
            0.0109,
            0.0213,
            0.0295,
            0.0314,
            0.0300,
            0.0353,
            0.0427,
            0.0679,
            0.0654,
            0.0537,
            0.0283,
            0.0135,
            0.0110,
            0.0,
        ]
    ),
    zlai=np.array(
        [0.0, 1.0, 3.1, 5.0, 6.75, 8.6, 10.4, 12.3, 14.2, 16.0, 17.8, 19.7, 21.6, 23.4, 26.2, 27.0, 28.8, 30.7, 32.5]
    ),
    avgH=24.06,
    sigH=1,
    sig_control=3.79,
    avg_lai=2.950,
    sig_lai=0.257,
    avg_flux=350.9,
    sig_flux=10,
    avg_albedo=0.2,
    sig_albedo=0.0005,
    bowen_ratio=1.25,
    sig_bowen=0.16,
    autocorrelation_length=6.5337,  # canopy scale autocorrelation length, mean crown radius
)

canopy_map = {1: duke_loblolly_pine, 2: grass_pitch, 3: duke_hardwood_winter, 4: duke_hardwood_spring}


def ForestCanopy_data(ptype, nx, Dx, ny, Dy, mean_lai, zlad, dz) -> CanopyType:
    """
    [CSProfile, LADcm,zcm, avg, avgH, sig, sigH, StandDencity, AcFp]=ForestCanopy_data(ptype,canopytopCM, nx, Dx, ny, Dy)

    Copyright: Gil Bohrer and Roni avissar, Duke University, 2006
    User defined function that returns the normalized parameters of the
    canopy. This function gets a canopy code (patch type code) and return the
    appropriate parameters. The example here includes the data of Pine stand
    in the FACE site in Duke Forest in Dec/2001, and an arbitrary grass
    patch.

    Input
        ptype - code for patch type (integer)
        nx, Dx, ny, Dy - grid mesh dimensions (integer)

    Output
        CSProfile - normalized (m^2 / DBH / m ) vertical profile at the normalized heights zcm
        LADcm - normalized (Tot LAI / m ) vertical profile at the normalized heights zcm
        zcm - normalized heights [m/m].
        avg - observed mean total (ground accumulated) LAI [m^2 leaf/m^2 ground]
        avgH - observed mean canopy top height [m]
        sig - std of avg
        sigH - std of sigH
        StandDencity - number of stems / hectare
        AcFp - autocorrelation function of canopy structure

    """
    canopytopCM = 100  # number of intervals in normalized LAD profile - The normalized profile is 1 m high, and therefore, canopytopCM=100 defines the profile every 1 cm.
    zcm = np.arange(0, canopytopCM + 1) / canopytopCM  # normalized 0-1 [m] heights in 1 cm intervals
    LADcm = np.zeros((canopytopCM + 1, 1)).T

    canopy_type = canopy_map[ptype]

    canopy_type.zcm = zcm
    canopy_type.normalize_lai(canopytopCM=canopytopCM, zcm=zcm)
    canopy_type.calculate_autocorrelation_function(nx=nx, ny=ny, Dx=Dx, Dy=Dy)
    canopy_type.calculate_csprofile(canopytopCM=canopytopCM, zcm=zcm)
    canopy_type.set_lad(mean_lai, zlad, dz)
    return canopy_type
