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

    
    Phi1Psi1=np.matrix([[Phi[0,1]*Psi[1,0], Phi[0,1]*Psi[1,1] ], [Phi[1,1]*Psi[1,0], Phi[1,1]*Psi[1,1] ]])
    
    Omega_plus=Phi[:,0]+np.exp(-2*lambda_*d)*np.dot(Phi1Psi1,Omega_moins)/(Psi[0,0]*Omega_moins[0]+Psi[0,1]*Omega_moins[1])
    
    Omega_plus=Phi[:,0]+np.exp(-2*lambda_*d)*Phi[:,1].dot(Psi[1,:]).dot(Omega_moins)/(Psi[0,:].dot(Omega_moins))
    
    Xi=np.exp(-lambda_*d)/np.dot(Psi[0,:],Omega_moins);
    
    return (Omega_plus,Xi)



#def  Transfert_Solid(Omega_moins,omega,k_x,lambda,mu,rho,d)
#
#
#    P=lambda+2*mu;  
#    delta_P=omega*sqrt(rho/(P));
#    delta_s=omega*sqrt(rho/(mu));
#
#    beta_P=sqrt(delta_P^2-k_x^2);
#    beta_s=sqrt(delta_s^2-k_x^2);
#
#    alpha_P=-j*lambda*delta_P^2-j*2*mu*beta_P^2;
#    alpha_s= 2*j*mu*beta_s*k_x;
#
#    V_0=np.matrix([1j*beta_P,-1j*beta_P,1j*beta_s,-1j*beta_s]);
#
#    Phi_0[0,0)=-2*j*mu*beta_P*k_x;
#    Phi_0[0,1)=2*j*mu*beta_P*k_x;
#    Phi_0[0,2)=j*mu*(beta_s^2-k_x^2);
#    Phi_0[0,3)=j*mu*(beta_s^2-k_x^2);
#
#    Phi_0[1,0)= beta_P;
#    Phi_0[1,1)=-beta_P;
#    Phi_0[1,2)= k_x;
#    Phi_0[1,3)= k_x;
#
#    Phi_0[2,0)=alpha_P;
#    Phi_0[2,1)=alpha_P;
#    Phi_0[2,2)=-alpha_s;
#    Phi_0[2,3)=alpha_s;
#
#    Phi_0[3,0)=k_x;
#    Phi_0[3,1)=k_x;
#    Phi_0[3,2)=-beta_s;
#    Phi_0[3,3)=beta_s;
#
#
#    [a,indice]=sort((real(V_0)));
#
#    for i_m=in range(0,3)
#        Phi(:,i_m)=Phi_0(:,indice(4+1-i_m));
#        V(i_m,i_m)=V_0(indice(4+1-i_m),indice(4+1-i_m));
#
#    lambda=diag(V);
#
#    Phi_inv=inv(Phi);
#
#    Phi_1=Phi(:,1);
#    Psi_1=Phi_inv(1,:);
#
#    A_1=Phi_1*Psi_1;
#    alpha_prime=Phi*diag([0 1 exp((lambda(3)-lambda(2))*d) exp((lambda(4)-lambda(2))*d)])*Phi_inv;
#
#
#    temp=Psi_1*Omega_moins;
#
#    A=temp(1);
#    B=temp(2);
#
#
#    temp=zeros(2,2);
#    temp(1,1)= exp((lambda(2)-lambda(1))*d)/A;
#    temp(2,1)=0;
#
#    temp(1,2)=-B/A;
#    temp(2,2)=1;
#
#    Omega_plus=[Phi_1 0*Phi_1]+alpha_prime*Omega_moins*temp;
#
#    Xi=temp*exp(-lambda(2)*d);
