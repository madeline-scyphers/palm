
import json
from dataclasses import dataclass
import math

import holoviews as hv
import matplotlib.pyplot as plt
import numpy as np
import panel as pn
import param
import scipy.io
import xarray as xr
from holoviews.operation.datashader import regrid
from scipy import stats

from utils import pad_along_axis

from parameters import (

    time_slice,
    x_slice,
    y_slice,
    z_delta_s0_values,
    z_slice,
    DW,
    dZ,
)

# # %%
# z_delta_s0_values = np.arange(0, 30).tolist()

# # %%
# z_lad_values = np.arange(0, 15).tolist()

hv.extension('bokeh')
pn.extension(sizing_mode="stretch_width")




@dataclass
class ConfigTracker:
    job_name: str
    domain_x: int
    domain_y: int
    plot_x: int
    plot_y: int
    house_domain_fraction: int
    trees_domain_fraction: int
    run_time: int
    dis_spatiotemporal_mean: float
    sweep_perc: float 
    delta_s0_bounds_perc: float
    
    

@dataclass
class AnalyzeRun:
    data_path_3d: str
    data_path_lad: str
    run_config: str
    canopy_csv: str
    canopy_height_units: int = 9
    
    @property
    def one_pt_5_canopy_height(self):
        one_pt_5_canopy_height = int((
            self.canopy_height_units + 1  # +1 because python indexes from 0
        ) * 1.5 )
        return np.arange(0, one_pt_5_canopy_height)

    def substantiate_config_tracker(self):
        self.load_data_sets()
        
        dis_spatiotemporal_mean = self.get_deposition()
        
        DS0 = self.get_delta_s0()
        sweep_perc = self.calc_sweep_perc(DS0)
        delta_s0_bounds_perc = self.calc_DS0_bounds_perc(DS0)
        
        with open(self.run_config, "r") as f:
            cfg= json.load(f)
        config_tracker = ConfigTracker(
            job_name=cfg["job_name"],
            domain_x=cfg["domain"]["x"],
            domain_y=cfg["domain"]["y"],
            plot_x=cfg["plot_size"]["x"],
            plot_y=cfg["plot_size"]["y"],
            house_domain_fraction=cfg["house"]["domain_fraction"],
            trees_domain_fraction=cfg["trees"]["domain_fraction"],
            dis_spatiotemporal_mean=dis_spatiotemporal_mean,
            sweep_perc=sweep_perc,
            delta_s0_bounds_perc=delta_s0_bounds_perc,
            run_time = cfg["output_end_time"] - cfg["output_start_time"]
        )
        self.config_tracker = config_tracker
        return config_tracker

    def load_data_sets(self):
        self.ds_lad = xr.open_dataset(self.data_path_lad)
        self.ds_3d = xr.open_dataset(self.data_path_3d)
        self.ds_3d = self.ds_3d.drop_isel(zu_3d=0, zw_3d=0)  # nan value
        self.ds_3d = self.ds_3d.reset_index(["zu_3d", "zw_3d"])

    def get_lad_values(self, z_dim, t_dim):
        lad = self.ds_lad.lad.values
        lad = pad_along_axis(lad, z_dim, axis=0)
        lad = lad[np.newaxis, ...]
        return np.tile(lad, reps=(t_dim, 1, 1, 1))

    def get_deposition(self):
        lad = self.get_lad_values(self.ds_3d.zu_3d.size, self.ds_3d.time.size)
        u_bar = np.sqrt(np.square(self.ds_3d.u.values) + np.square(self.ds_3d.v.values))

        
        DR = u_bar[:lad.shape[0], :lad.shape[1], :lad.shape[2], :lad.shape[3]] * lad
        DRVsTime = np.nanmean(DR, axis=(x_slice, y_slice))
        tot_deposition = np.nansum(DRVsTime, axis=None) / dZ

        dis_spatiotemporal_mean = (self.canopy_height_units * dZ) * tot_deposition / (self.ds_3d.time.size * self.ds_3d.x.size * self.ds_3d.y.size * (self.canopy_height_units * dZ)) 

        return dis_spatiotemporal_mean

        
    def calc_temp_spac_means(self):
        TempSpacMeanU = self.ds_3d.u.sum(dim=["xu", "y", "time"]) / (self.ds_3d.x.size * self.ds_3d.y.size * self.ds_3d.time.size)
        TempSpacMeanV = self.ds_3d.v.sum(dim=["x", "yv", "time"]) / (self.ds_3d.x.size * self.ds_3d.y.size * self.ds_3d.time.size)
        return TempSpacMeanU, TempSpacMeanV

    def calc_temp_spac_can_means(self):
        canopy_loc = np.genfromtxt(self.canopy_csv, delimiter=',', dtype="int8")
        
        tiled_canopy = np.tile(canopy_loc, reps=(self.ds_3d.time.size, self.ds_3d.zw_3d.size, 1, 1))
        
        u_canopy = (self.ds_3d.u.values * tiled_canopy)
        v_canopy = (self.ds_3d.v.values * tiled_canopy)
        w_canopy = (self.ds_3d.w.values * tiled_canopy)
        

        # TempSpacCanMeanU = xr.DataArray((np.nansum(u_canopy, (time_slice, x_slice, y_slice))
        #                     / (self.ds_3d.x.size * self.ds_3d.y.size * self.ds_3d.time.size)
        #                     ), dims=["zu_3d"])

        # TempSpacCanMeanV = xr.DataArray((np.nansum(v_canopy, (time_slice, x_slice, y_slice))
        #                     / (self.ds_3d.x.size * self.ds_3d.y.size * self.ds_3d.time.size)
        #                     ), dims=["zu_3d"])
        
        TempSpacCanMeanW = xr.DataArray((np.nansum(w_canopy, (time_slice, x_slice, y_slice))
                        / (self.ds_3d.x.size * self.ds_3d.y.size * self.ds_3d.time.size)
                        ), dims=["zw_3d"])

        return TempSpacCanMeanW
        # return TempSpacCanMeanU, TempSpacCanMeanV, TempSpacCanMeanW



    def calc_vtr(self, TempSpacMeanU, TempSpacMeanV):
        theta = np.arctan2(TempSpacMeanU[self.canopy_height_units], TempSpacMeanV[self.canopy_height_units])

        u = (-self.ds_3d.u.isel(zu_3d=self.one_pt_5_canopy_height) * np.sin(theta)).values
        v = (self.ds_3d.v.isel(zu_3d=self.one_pt_5_canopy_height) * np.cos(theta)).values
        vtr = u + v  # work around to get around memory error with numpy (in place operation takes way less memory)
        return vtr

    def calc_mean_temp_and_space_vtr(self, vtr):
        MeanTempvtr = np.squeeze(np.nansum(vtr, time_slice)) / self.ds_3d.time.size
        MeanTempSpacvtr = MeanTempvtr.mean((x_slice - 1, y_slice - 1))  # time slice removed (slice 0), all slices go down
        return MeanTempvtr, MeanTempSpacvtr

    def calc_vp_and_wp(self, vtr, MeanTempSpacvtr, TempSpacCanMeanW):
        vp = vtr - np.expand_dims(MeanTempSpacvtr[self.one_pt_5_canopy_height], axis=(0, 2, 3))
        wp = (self.ds_3d.w.isel(zw_3d=self.one_pt_5_canopy_height) - TempSpacCanMeanW.isel(zw_3d=self.one_pt_5_canopy_height)).values

        return vp, wp

    @staticmethod
    def calc_Q2_Q4(vp, wp):
        Q2 = (vp<0) & (wp>0)
        Q4 = (vp>0) & (wp<0)
        
        return Q2, Q4

    @staticmethod
    def calc_sweep_and_eject_sum(Q2, Q4):
        SweepSum = np.nansum(Q4, time_slice)
        EjectSum = np.nansum(Q2, time_slice)
        
        return SweepSum, EjectSum


    def calc_all_sweeps_and_ejects(self, vp, wp, Q2, Q4):
        Sweeps = np.zeros(self.ds_3d.w.isel(zw_3d=self.one_pt_5_canopy_height).shape)
        Eject = np.zeros(self.ds_3d.w.isel(zw_3d=self.one_pt_5_canopy_height).shape)

        Sweeps[Q4] = vp[Q4] * wp[Q4]
        Eject[Q2] =  vp[Q2] * wp[Q2]
        Allvw = vp * wp
        
        return Sweeps, Eject, Allvw


    # def sum_over_chunks(arr, chunk_size, axis_to_sum):  # TODO this doesn't change the outcome value at all
    #     axes = len(arr.shape)
    #     reshapers = (arr.shape[axis] for axis in range(axes) if axis != axis_to_sum)
    #     return arr.reshape(-1, chunk_size, *reshapers).sum(1)
        


    def calc_delta_s0(self, Sweeps, SweepSum, Eject, EjectSum, Allvw):
        with np.errstate(divide='ignore', invalid='ignore'):
            DS0 = (
                ((np.nansum(Sweeps, time_slice) / SweepSum ) - (np.nansum(Eject, time_slice) / EjectSum))
                / 
                (np.nansum(Allvw, axis=time_slice) / self.ds_3d.time.size))
        return DS0


    def get_delta_s0(self):
        TempSpacMeanU, TempSpacMeanV = self.calc_temp_spac_means()
        TempSpacCanMeanW = self.calc_temp_spac_can_means()
        vtr = self.calc_vtr(TempSpacMeanU, TempSpacMeanV)
        MeanTempvtr, MeanTempSpacvtr = self.calc_mean_temp_and_space_vtr(vtr)
        vp, wp = self.calc_vp_and_wp(vtr, MeanTempSpacvtr, TempSpacCanMeanW)
        Q2, Q4 = self.calc_Q2_Q4(vp, wp)
        SweepSum, EjectSum = self.calc_sweep_and_eject_sum(Q2, Q4)
        Sweeps, Eject, Allvw = self.calc_all_sweeps_and_ejects(vp, wp, Q2, Q4)
        
        DS0 = self.calc_delta_s0(Sweeps, SweepSum, Eject, EjectSum, Allvw)
        
        print((DS0[(DS0 >= -1) & (DS0 <= 1)].size) / DS0.size)
        
        return DS0

    def calc_sweep_perc(self, DS0):
        sw_count = (DS0[self.one_pt_5_canopy_height, ...] > 0).sum(axis=None)
        ej_count = (DS0[self.one_pt_5_canopy_height, ...] < 0).sum(axis=None)
        n_grid = math.prod(DS0[self.one_pt_5_canopy_height, ...].shape)
        
        return sw_count / n_grid

    @staticmethod
    def calc_DS0_bounds_perc(DS0):
        return (DS0[(DS0 >= -1) & (DS0 <= 1)].size) / DS0.size

# ZPlot = 3
# X1 = 0
# _, Y2, X2 = DS0.shape
# Y1 = 0
# x = np.arange(X1, X2) * .25
# y = np.arange(Y1, Y2) * .25


# class Delta_s0(param.Parameterized):
#     z_plot = param.Integer(0, bounds=(min(z_delta_s0_values), max(z_delta_s0_values)))
#     clim_l = param.Number(-1.0, bounds=(-5.0, 0))
#     clim_r = param.Number(1.0, bounds=(0, 5.0))
    
#     def view(self):
#         delta_s0 = DS0[self.z_plot, :, :]
#         img = hv.HeatMap((y, x, np.swapaxes(delta_s0, 0, 1))).opts(
#             hv.opts.HeatMap(tools=['hover'], cmap='bkr', colorbar=True, toolbar='above', 
#                                                                 clim=(self.clim_l, self.clim_r)
#                                                                )
#         )
# #         img = regrid(img, interpolation='bilinear' ).opts(width=1200)
#         return img


# plot = Delta_s0()
# pn.Column(plot.param, plot.view)


# plot = Delta_s0()
# pn.Column(plot.param, plot.view)

# # %%
# plt.imshow(a, cmap='hot', interpolation='nearest')

# # %%
# kw = dict(z_plot=(0,5))
# pn.Row(pn.interact(plot_delta_s0, **kw, ), width=900)

# # %%

# harvest = np.array([[0.8, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
#                     [2.4, 0.0, 4.0, 1.0, 2.7, 0.0, 0.0],
#                     [1.1, 2.4, 0.8, 4.3, 1.9, 4.4, 0.0],
#                     [0.6, 0.0, 0.3, 0.0, 3.1, 0.0, 0.0],
#                     [0.7, 1.7, 0.6, 2.6, 2.2, 6.2, 0.0],
#                     [1.3, 1.2, 0.0, 0.0, 0.0, 3.2, 5.1],
#                     [0.1, 2.0, 0.0, 1.4, 0.0, 1.9, 6.3]])

# # %%
# delta_s0.shape

# # %%
# width = 30
# height = 15

# delta_s0 = DS0[0, :, :]

# fig, ax = plt.subplots(figsize=(width, height))
# im = ax.imshow(np.swapaxes(delta_s0, 0, 1), 
#                vmin=-1, vmax=1, 
#                interpolation="bilinear")

# # fig.set_size_inches(10, 5.5)     # set a suitable size
# plt.show()

# # %%
# np.swapaxes(np.array([[1,2,3,4]]), 0, 1)

# # %%


# # %%
# mean_var["MeanVar"].shape


