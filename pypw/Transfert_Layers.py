#! /usr/bin/env python
# -*- coding:utf8 -*-
#
# transfert_layers.py
#
# This file is part of pypw, a software distributed under the MIT license.
# For any question, please contact one of the authors cited below.
#
# Copyright (c) 2017
# 	Olivier Dazel <olivier.dazel@univ-lemans.fr>
# 	Mathieu Gaborit <gaborit@kth.se>
# 	Peter Göransson <pege@kth.se>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#

import numpy as np
from numpy.lib.scimath import *


def Transfert_Fluid(Omega_moins,omega,k_x,K_eq,rho_eq,d):

    delta=omega*sqrt(rho_eq/K_eq)
    # Eigenvalue of the State Matrix (the other one is -lambda_)
    lambda_=-sqrt(k_x**2-delta**2)
    # Matrix of eigenvectors , Eq (A10) in JAP 2013 corrected    
    Phi=np.matrix([[-lambda_/(rho_eq*omega**2),lambda_/(rho_eq*omega**2)],[1,1]])
    # Inverse of Phi (analytical)    
    Psi=(rho_eq*omega**2/(2*lambda_))*np.matrix([[-1,lambda_/(rho_eq*omega**2)],[1,lambda_/(rho_eq*omega**2)]])

    
    Omega_plus=Phi[:,0]+np.exp(-2*lambda_*d)*Phi[:,1].dot(Psi[1,:]).dot(Omega_moins)/(Psi[0,:].dot(Omega_moins))
    
    Xi=np.exp(-lambda_*d)/np.dot(Psi[0,:],Omega_moins);
    
    return (Omega_plus,Xi)


def Transfert_PEM(Omega_moins,omega,k_x,Mat,d):
    return 0
    




def Transfert_Elastic(Omega_moins,omega,k_x,Mat,d):
    
    
    
#    print(Mat.lambda_)
#    print(Mat.mu)
#    print(k_x)
#
#    print(Mat.lambda__)
    
    
    
    P_mat=Mat.lambda_+2*Mat.mu  
    delta_p=omega*sqrt(Mat.rho/P_mat)
    delta_s=omega*sqrt(Mat.rho/Mat.mu)

    beta_p=sqrt(delta_p**2-k_x**2)
    beta_s=sqrt(delta_s**2-k_x**2)

    alpha_p=-1j*Mat.lambda_*delta_p**2-1j*2*Mat.mu*beta_p**2
    alpha_s= 2j*Mat.mu*beta_s*k_x
    
#    print(alpha_p)
#    print(alpha_s)
#

    Phi_0=np.zeros((4,4),dtype=np.complex);
    Phi_0[0,0]=-2*1j*Mat.mu*beta_p*k_x
    Phi_0[0,1]=2*1j*Mat.mu*beta_p*k_x
    Phi_0[0,2]=1j*Mat.mu*(beta_s**2-k_x**2)
    Phi_0[0,3]=1j*Mat.mu*(beta_s**2-k_x**2)
    
    Phi_0[1,0]= beta_p
    Phi_0[1,1]=-beta_p
    Phi_0[1,2]= k_x
    Phi_0[1,3]= k_x

    Phi_0[2,0]=alpha_p
    Phi_0[2,1]=alpha_p
    Phi_0[2,2]=-alpha_s
    Phi_0[2,3]=alpha_s

    Phi_0[3,0]=k_x
    Phi_0[3,1]=k_x
    Phi_0[3,2]=-beta_s
    Phi_0[3,3]=beta_s
    
    
    V_0=np.array([1j*beta_p,-1j*beta_p,1j*beta_s,-1j*beta_s])
    
#    print("V_0")
#    print(V_0)
    
    index=np.argsort(V_0.real)
#    print("index=")
#    print(index)
     
    Phi=np.zeros((4,4),dtype=np.complex);
    lambda_=np.zeros((4),dtype=np.complex);


    for i_m in range(0,4):
        Phi[:,i_m]=Phi_0[:,index[3-i_m]]
        lambda_[i_m]=V_0[index[3-i_m]]
    
#    print("lambda_")
#    print(lambda_)
    
#    print(dfssdf)

    Phi_inv=np.linalg.inv(Phi)

#    print("Phi_1=")
#    print(Phi[:,0])     
    
    #A_1=np.outer(Phi[:,0],Phi_inv[0,:])
    
    Lambda=np.diag([0,1,np.exp((lambda_[2]-lambda_[1])*d),np.exp((lambda_[3]-lambda_[1])*d)])
#    print("Lambda=")
#    print(Lambda)
 

    alpha_prime=Phi.dot(Lambda).dot(Phi_inv)
#    print("alpha_prime") 
#    print(alpha_prime)    
#
#
    temp=np.matmul(Phi_inv[0,:],Omega_moins)
#    print("temp=")
#    print(temp)

#
    A=temp[0]
    B=temp[1]
    
    temp=np.zeros((2,2),dtype=np.complex);  
 
#    print("np.exp((lambda_[1]-lambda_[0])*d)")
#
#    print(np.exp((lambda_[1]-lambda_[0])*d))
#    print("A")
#
#    print(A)

    
    temp[0,0]=np.exp((lambda_[1]-lambda_[0])*d)/A
    temp[0,1]=-B/A
    temp[1,1]=1
    
#    print("temp=")
#    print(temp)
    
    
    Omega_plus=alpha_prime.dot(Omega_moins).dot(temp)
    Omega_plus[:,0]+=Phi[:,0]

#    print("Omega_plus")
#    print(Omega_plus)    
    
#    Omega_plus=Omega_plus.dot(temp)
#    print("Omega_plus")
#    print(Omega_plus)

    
    #print(Omega_plus)

    Xi=temp*np.exp(-lambda_[1]*d)
    
    return (Omega_plus,Xi)
