# -*- coding: utf-8 -*-
# Author: Pedro Bittencourt
# Repository: https://github.com/pbitts/signal_conditioner

import numpy as np
from random import choice

class Conditioner:
  def __init__(self, desired_output_signal: list = [5.0, 0.0], input_signal_rms: list = [220.0, -220.0], max_tries: int = 80000 ):
    
    input_signal_peak: np.darray = np.multiply(input_signal_rms,np.sqrt(2))

    resistors: list = [10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 33, 36, 39, 43, 47, 51, 56, 62, 68, 75, 82]
    unds: list = [1, 10, 100, 1000, 10000, 100000, 1000000 ]
    self.commercial_resistors = []
    for resistor in resistors:
      self.commercial_resistors: np.darray = np.concatenate((self.commercial_resistors, np.multiply(unds,resistor)))
    
    print('Finding best resistors values for conditioning...')
    print('Output signal desired: ', desired_output_signal, ' v')
    print('Input signal: ', input_signal_peak, ' v')
    ideal_reqca_value = self.get_reqca_ideal_value(max(desired_output_signal), max(input_signal_peak))
    print('Ideal REQ CA value: ', ideal_reqca_value)
    possibility = 0
    self.chosen_circuits = []
    for i in range(max_tries):
      r1 = choice(self.commercial_resistors)
      r2 = r1
      r3 =  choice(self.commercial_resistors)
      reqca_value = self.get_reqca_analysis(r1, r2, r3, input_signal_peak[0])
      cc_value = self.get_cc_analysis(r1, r2, r3, desired_output_signal[0])
      vout = self.get_final_output(cc_value, reqca_value, input_signal_peak)    

      if ideal_reqca_value >= reqca_value and (max(vout) >= 0.90*max(desired_output_signal) ) \
                                    and (min(vout) >= 0.04*min(desired_output_signal)) :
        chosen_circuit = {'possibility': possibility, 
                          'r1':float(r1), 'r2':float(r2), 'r3':float(r3), 
                          'vout_max': float(max(vout)),
                          'vout_min': float(min(vout))
                          }
        if not chosen_circuit in self.chosen_circuits:
          self.chosen_circuits.append(chosen_circuit)
          possibility += 1

    for circuit in self.chosen_circuits:
      print(f'\n--------Circuit possibility {circuit["possibility"]}-------------'
            f'\nChosen resistors:\nr1: {circuit["r1"]} ohms\nr2: {circuit["r2"]} ohms\nr3: {circuit["r3"]} ohms'
            f'\nFinal Output: {circuit["vout_max"]} volts | {circuit["vout_min"]} volts ')

      

  def get_parallel (self, ra, rb):
    return (ra*rb/(ra+rb))

  def get_reqca_analysis (self, r1, r2, r3, ca_signal):
    r1pr2 = self.get_parallel (r1,r2)
    vout_ca = (r1pr2/(r3+r1pr2))
    return vout_ca

  def get_cc_analysis(self, r1,r2,r3,cc_signal):
    r3pr2 = self.get_parallel(r3,r2)
    vout_cc = (r3pr2)/(r1+r3pr2)*cc_signal
    return vout_cc

  def get_reqca_ideal_value(self, cc_signal, ca_signal):
    return (cc_signal/2)/ca_signal

  def get_final_output(self, cc_value, ca_value, input_signal_peak):
    vout = [0.0, 0.0]
    vout[0] = cc_value + ca_value*input_signal_peak[0]
    vout[1] = cc_value + ca_value*input_signal_peak[1]
    return vout


Conditioner(desired_output_signal=[5.0,0.0], input_signal_rms = [220.0, -220.0], max_tries=8000)