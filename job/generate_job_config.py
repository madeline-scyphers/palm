job_config = r"""
!-------------------------------------------------------------------------------
!-- INITIALIZATION PARAMETER NAMELIST
!   Documentation: https://palm.muk.uni-hannover.de/trac/wiki/doc/app/inipar
!-------------------------------------------------------------------------------
&initialization_parameters
!
!-- grid parameters
!-------------------------------------------------------------------------------
    nx                         = {domain_x},  ! Number of gridboxes in x-direction (nx+1)
    ny                         = {domain_y},  ! Number of gridboxes in y-direction (ny+1)
    nz                         = 192,  ! Number of gridboxes in z-direction (nz)

    dx                         = 5.0, ! Size of single gridbox in x-direction
    dy                         = 5.0, ! Size of single gridbox in y-direction
    dz                         = 5.0, ! Size of single gridbox in z-direction

    topography                 = 'read_from_file',              !Read Topography
    topography_grid_convention = 'cell_center', !Points in file are defined at the center of the cell

!
!-- initialization
!-------------------------------------------------------------------------------
    initializing_actions       = 'set_constant_profiles', ! initial conditions

    ug_surface                 = 0.0, ! u-comp of geostrophic wind at surface
    vg_surface                 = 4.0, ! v-comp of geostrophic wind at surface

    roughness_length           = 0.49, ! Roughnes Length

    pt_surface                 = 295.45, ! initial surface potential temp

    pt_vertical_gradient       = -0.01,0.094,1.0,  ! piecewise temp gradients
    pt_vertical_gradient_level =  0.0,75.0,400.0,  ! height level of temp gradients


!
!-- boundary conditions
!-------------------------------------------------------------------------------
    surface_heatflux           = 0.011697, ! sensible heat flux at the bottom surface
    surface_waterflux          = 0.015597, ! latent heat flux at the bottom surface

    bc_pt_b                    = 'neumann', ! required with surface_heatflux
    bc_uv_t                    = 'neumann',
    bc_q_b                     = 'neumann',
    bc_s_b                     = 'neumann',

    passive_scalar             = .T.  !To activate the scalar flux
    surface_scalarflux         = 0.0, !It should be input even if it is 0.0 for the wall_scalarflux be active
    !wall_scalarflux            = 0.0,0.0,0.0,1.0,0.0, !It is in kg m-1 s-2.

!
!-- numerics
!-------------------------------------------------------------------------------
    fft_method                 = 'temperton-algorithm',   ! build-in fft method

/ ! end of initialization parameter namelist

!-------------------------------------------------------------------------------
!-- RUNTIME PARAMETER NAMELIST
!   Documentation: https://palm.muk.uni-hannover.de/trac/wiki/doc/app/d3par
!-------------------------------------------------------------------------------
&runtime_parameters
!
!-- run steering
!-------------------------------------------------------------------------------
    end_time                   = 1800.0, ! simulation time of the 3D model

    !create_disturbances        = .TRUE., ! randomly perturbate horiz. velocity
    !dt_disturb                 = 1500.0,  ! interval for random perturbations
    !disturbance_energy_limit   = 0.01,   ! upper limit for perturbation energy

    !data_output_2d_on_each_pe  = .FALSE., ! don't do 2D output on each MPI rank

!
!-- data output
!-------------------------------------------------------------------------------
    netcdf_data_format         = 2, ! use NetCDF3 64 bit offset
                                    ! Options:
                                    ! 1 	netCDF classic format (filesize limited to 2GB)
                                    ! 2 	netCDF 64-bit-offset format (large file support, but single variable still limited to 2GB)
                                    ! 3 	netCDF-4 (HDF5) format (files can be as large as file system supports; unlimited variable size), without parallel I/O support
                                    ! 4 	netCDF-4 format, but with NF90_CLASSIC_MODEL bit set (some new features of netCDF4 are not available), without parallel I/O support
                                    ! 5 	same as 3, but with parallel I/O support
                                    ! 6 	same as 4, but with parallel I/O support 


    dt_run_control             = 0.0,    ! output interval for run control
    dt_data_output             = 5.0,   ! output interval for general data
    !skip_time_data_output      = 23400.0, ! time interval skipped before output starts
    !dt_do2d_xy                = 100.0,  ! output interval for xy data
    !dt_do2d_xz                = 100.0,  ! output interval for xz data
    !dt_do2d_yz                = 100.0,  ! output interval for yz data

    data_output                = 'theta', 'v', 'w', 'u', 's'

    !section_xy                = 0,1,2,3,4,5,6,7,8,9,10,11,12,13,15, ! grid index for 2D XY cross sections
    !section_yz                = 180,190,200,210,220,230,240, ! grid index for 2D YZ cross sections
    !section_xz                = 250,260,270,280,290,300,310,320, ! grid index for 2D XZ cross sections

/ ! end of runtime parameter namelist

&user_parameters

            !user_module_enabled        = .T.,

            !Canopy1_edge_south         = 960,
            !Canopy1_edge_north         = 1225,
            !Canopy1_edge_left          = 450,
            !Canopy1_edge_right         = 760,

            !Canopy2_edge_south         = 1225,
            !Canopy2_edge_north         = 1405,
            !Canopy2_edge_left          = 60,
            !Canopy2_edge_right         = 450,


/

&plant_canopy_parameters

          canopy_mode                  = 'read_from_file',		!For defining the canopy shape 
          canopy_drag_coeff            = 0.15,				!This is the drag coeffecient. 0.15 is the typical value used			
          cthf                         = 0.011697,			!Average heat flux that is prescribed at the top of the plant canopy
          lad_surface                  = 0.02,			!Surface value of the leaf area density (in m2/m3)
          lad_vertical_gradient        = 0.003,0.0085,0.014,-0.011,      !Gradient(s) of the leaf area density (in m2/m4)
          lad_vertical_gradient_level  = 0.0, 5.0, 10.0, 15.0,		!Height level from which on the gradient of the leaf area density defined by lad_vertical_gradient is effective (in m)	
          pch_index                    = 4,   	   	     	  	!Grid point index (w-grid) of the upper boundary of the plant canopy layer
          leaf_scalar_exch_coeff       = 1.0,				!Scalar exchange coefficient for a "bulk" leaf (dimensionless)

/
"""


def generate_job_config(config: dict):
    job_cfg = job_config.format(domain_x=config["domain"]["x"], domain_y=config["domain"]["y"])
    return job_cfg
    # job_config_path = JOBS_PATH / "INPUT" / config["job_name"]
    # with open(job_config_path, "w") as f:
    #     f.write(job_cfg)
