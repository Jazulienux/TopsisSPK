# -*- coding: utf-8 -*-
"""TopsisSPK.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WvG-FPcgUpcF3RcZRa3-cBUmrtVK6q3K
"""

import numpy as np
import math

class Topsis:
  def __init__(self,bobot,alternatif,code,desc_alt):
    self.desc_alt = desc_alt
    self.alternatif = alternatif
    self.rank_alt = np.zeros((self.alternatif.shape[0],1),dtype=float)
    self.bobot = bobot
    self.ideal_positif = np.zeros((self.bobot.shape[0],1),dtype=float)
    self.ideal_negatif = np.zeros((self.bobot.shape[0],1),dtype=float)
    self.ed_positif = np.zeros((self.alternatif.shape[0],1),dtype=float)
    self.ed_negatif = np.zeros((self.alternatif.shape[0],1),dtype=float)
    self.res_norm = np.zeros((self.alternatif.shape[0],self.alternatif.shape[1]),dtype=float)
    self.matrix_skor_norm = np.zeros((self.alternatif.shape[0],self.alternatif.shape[1]),dtype=float)
    self.code = code
    self.nomr_kriteria()
  
  def nomr_kriteria(self):
    self.alternatif = self.alternatif.T
    self.res_norm = self.res_norm.T
    for i in range(0,self.alternatif.shape[0]):
      for j in range(0,self.alternatif.shape[1]):
        self.res_norm[i,j] = self.alternatif[i,j] / math.sqrt(np.sum(self.alternatif[i]** 2))
        
    self.alternatif = self.alternatif.T
    self.norm_matrix_kali_bobot()
  
  def norm_matrix_kali_bobot(self):
    self.matrix_skor_norm = self.matrix_skor_norm.T
    for i in range(0,self.matrix_skor_norm.shape[0]):
      self.matrix_skor_norm[i] = self.res_norm[i] * self.bobot[i]

    self.get_idx_code()

  def get_idx_code(self):
    cost = np.where(self.code == "Cost")
    ben = np.where(self.code == "Benefit")
    cost = np.asarray(cost)
    ben = np.asarray(ben)
    self.get_ideal_matrix(cost,ben)
  
  def get_ideal_matrix(self,cost,ben):
    for i in range(0,ben.shape[0]):
      for j in range(0,ben.shape[1]):
        self.ideal_positif[ben[i,j]] = np.max(self.matrix_skor_norm[ben[i,j]])
        self.ideal_negatif[ben[i,j]] = np.min(self.matrix_skor_norm[ben[i,j]])
    
    for i in range(0,cost.shape[0]):
      for j in range(0,cost.shape[1]):
        self.ideal_positif[cost[i,j]] = np.min(self.matrix_skor_norm[cost[i,j]])
        self.ideal_negatif[cost[i,j]] = np.max(self.matrix_skor_norm[cost[i,j]])
        
    self.get_euqlidiance_distance()
  
  def get_euqlidiance_distance(self):
    self.matrix_skor_norm = self.matrix_skor_norm.T
    self.res_norm = self.res_norm.T
    
    ed_pos = np.zeros((self.alternatif.shape[0],self.alternatif.shape[1]),dtype=float)
    ed_neg = np.zeros((self.alternatif.shape[0],self.alternatif.shape[1]),dtype=float)
    for i in range(0,self.matrix_skor_norm.shape[0]):
      for j in  range(0,self.matrix_skor_norm.shape[1]):
        ed_pos[i,j] = (self.ideal_positif[j] - self.matrix_skor_norm[i,j]) ** 2
        ed_neg[i,j] = (self.ideal_negatif[j] - self.matrix_skor_norm[i,j]) ** 2

    for i in range(0,ed_pos.shape[0]):
      val_pos = np.sum(ed_pos[i])
      val_neg = np.sum(ed_neg[i])
      val_pos = math.sqrt(val_pos)
      val_neg = math.sqrt(val_neg)
      self.ed_positif[i] = val_pos
      self.ed_negatif[i] = val_neg
      
    self.ranking()

  def ranking(self):
    for i in range(0,self.rank_alt.shape[0]):
      self.rank_alt[i] = self.ed_negatif[i] / (self.ed_negatif[i] + self.ed_positif[i])

    
    new_rank = np.array([[0,""]]*self.rank_alt.shape[0])
    for i in range (0,new_rank.shape[0]):
        new_rank[i][0] = self.rank_alt[i][0]
        new_rank[i][1] = self.desc_alt[i][0]

    print("Bobot\n")
    print(self.bobot)
    print("-----------------------------------------------\n")

    print("Rentang Skor Alt dan Kriteria\n")
    print(self.alternatif)
    print("-----------------------------------------------\n")

    print("Normalisasi Kriteria\n")

    print(self.res_norm)
    print("-----------------------------------------------\n")

    print("Matriks Skor Normalisasi Terbobot\n")
    print(self.matrix_skor_norm)
    print("-----------------------------------------------\n")

    print("Matriks Ideal Positif\n")
    print(self.ideal_positif)
    print("-----------------------------------------------\n")

    print("Matriks Ideal Negatif\n")
    print(self.ideal_negatif)
    print("-----------------------------------------------\n")

    print("Euqlidiance Positif\n")
    print(self.ed_positif)
    print("-----------------------------------------------\n")

    print("Euqlidiance Negatif\n")
    print(self.ed_negatif)
    print("-----------------------------------------------\n")

    print("Ranking Before Sort\n")
    print(new_rank)
    print("-----------------------------------------------\n")

    print("Ranking After Sort\n")
    sort_rank = new_rank[new_rank[:,0].argsort()[::-1]]
    print(sort_rank)
    print("-----------------------------------------------\n")

if __name__ == '__main__' :
  try:
    bobot = np.array([3,2,2,2,1])
    alternatif = np.array([[2,4,2,3,3],[4,1,5,5,3],[3,2,1,4,4]])
    code = np.array(["Benefit","Cost","Cost","Cost","Benefit"])
    desc_alt = np.array([["Apartemen 1"],["Apartemen 2"],["Apartemen 3"]])
    topsis = Topsis(bobot,alternatif,code,desc_alt)
  except Exception as e:
    print(e)