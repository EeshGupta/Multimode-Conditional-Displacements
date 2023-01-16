# Imports  -----------------------------------------------------------------------------

#%matplotlib inline
import os
import sys
import inspect
import numpy as np
from scipy.special import factorial
import h5py

#data_path = '/data'     ... data path specified later
#data_path
#initial_pulse = '../pulses/example_pulses/transmon_cat_initial_pulse.h5'
from h5py import File
import matplotlib.pyplot as plt
from pylab import*
from qutip import*

from scipy import interpolate
font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 18}

matplotlib.rc('font', **font)

from quantum_optimal_control.helper_functions.grape_functions import *
from quantum_optimal_control.main_grape.grape import Grape
from quantum_optimal_control import*

from circle_grape_v3 import *
#----------------------------------------------------------------------------------------

# 3D MM2 parameters

# chi = Peak splitting MHz
chis = 2*array([-33.1962, -0.8676]) 
kappas  = array([0,0]) # kHz
transmon_levels = 2

# Circle grape class
mode = 0
mode_levels = 2
chi,kappa = chis[mode]*1e-6,kappas[mode]*1e-6
circle_grape_params = {"chis":[chi],"kappas":[kappa],"alpha":30.0,"delta_c":-0.01}

op = multimode_circle_grape_optimal_control(mode_state_num = mode_levels,
                                            number_of_modes = 1,hparams = circle_grape_params,add_disp_kerr=False)
data_path = ''

states_forbidden_list = []
total_time = 5000.0
steps  = 500  #number of points over the total time where amplitudes will be specified

convergence = {'rate': 0.01, 'update_step': 10, 'max_iterations': 100,
               'conv_target': 3e-4, 'learning_rate_decay': 500.0}


reg_coeffs = {'dwdt': 0.1, 'd2wdt2': 1.0e-3, 'forbid_dressed': False,
               'states_forbidden_list':states_forbidden_list,
               'forbidden_coeff_list': [1.0*steps] * len(states_forbidden_list)}



initial_guess = None

ss = op.run_optimal_control(state_transfer = True, initial_states = [0], target_states = [1], 
                        total_time = total_time, steps = steps,max_amp = 1e-2, 
                        taylor_terms = None,is_dressed=False, 
                        convergence = convergence, reg_coeffs =  reg_coeffs,
                        plot_only_g = True,
                        states_forbidden_list = states_forbidden_list,initial_guess = initial_guess, 
                        file_name="g0_to_g1_circlgrape", data_path=data_path, save = True)

