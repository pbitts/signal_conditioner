# -*- coding: utf-8 -*-
# Author: Pedro Bittencourt
# Repository: https://github.com/pbitts/signal_conditioner

import numpy as np
from random import choice

class Conditioner:
  def __init__(self, desired_output_signal: list = [5.0, 0.0], input_signal_rms: list = [220.0, -220.0], max_tries: int = 80000 ):
    
    input_signal_peak: np.darray = np.multiply(input_signal_rms,np.sqrt(2))

    #Get list of commercial resistors
    resistors: list = [10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82]
    unds: list = [1, 10, 100, 1000, 10000, 100000, 1000000 ]
    self.commercial_resistors = []
    for resistor in resistors:
      self.commercial_resistors: np.darray = np.concatenate((self.commercial_resistors, np.multiply(unds,resistor)))
    
    ideal_reqca_value = self.get_reqca_ideal_value(max(desired_output_signal), max(input_signal_peak))

    #Calculates the Vout of the circuit havind random resistors' values from the
    #commercial values list ( self.commercial_resistors)
    #if the values matches the vout desired ( as close as possible) it chooses it as
    #a possibility. The loop keeps going for the number of time
    #defined at the variable max_tries
    possibility: int = 0
    self.chosen_circuits: list = []
    for i in range(max_tries):
      r1: float = choice(self.commercial_resistors)
      r2: float = r1
      r3: float =  choice(self.commercial_resistors)
      reqca_value: float = self.get_reqca_analysis(r1, r2, r3)
      cc_value: float = self.get_cc_analysis(r1, r2, r3, desired_output_signal[0])
      vout: list = self.get_final_output(cc_value, reqca_value, input_signal_peak)    

      if ideal_reqca_value >= reqca_value and (max(vout) >= 0.90*max(desired_output_signal) ) \
                                    and (min(vout) >= 0.04*min(desired_output_signal)) :
        chosen_circuit = {'possibility': possibility, 
                          'r1':float(r1), 'r2':float(r2), 'r3':float(r3), 
                          'vout_max': float(max(vout)),
                          'vout_min': float(min(vout))
                          }
        #Having a unique possibility of circuit, stores in the self.chosen_circuits list
        if not chosen_circuit in self.chosen_circuits:
          self.chosen_circuits.append(chosen_circuit)
          possibility += 1

  def get_parallel (self, ra: float, rb: float):
    '''Calculates the parallel equivalent resistor of two resistors'''
    return (ra*rb/(ra+rb))

  def get_reqca_analysis (self, r1: float, r2: float, r3: float):
    '''Calculates de equivalent resistor considering a CA analysis'''
    r1pr2 = self.get_parallel (r1,r2)
    vout_ca = (r1pr2/(r3+r1pr2))
    return vout_ca

  def get_cc_analysis(self, r1: float, r2: float, r3: float, cc_signal: float):
    '''Calculates the Vout from the CC analysis'''
    r3pr2 = self.get_parallel(r3,r2)
    vout_cc = (r3pr2)/(r1+r3pr2)*cc_signal
    return vout_cc

  def get_reqca_ideal_value(self, cc_signal: float, ca_signal: float):
    '''Calculates the ideal value for the equivalent resistor of the CA analysis'''
    return (cc_signal/2)/ca_signal

  def get_final_output(self, cc_value: float, ca_value: float, input_signal_peak: float):
    '''After having calculated CA and CC analysis, returns the final Output from the conditioner circuit'''
    vout = [0.0, 0.0]
    vout[0] = cc_value + ca_value*input_signal_peak[0]
    vout[1] = cc_value + ca_value*input_signal_peak[1]
    return vout
