#!/usr/bin/env python
# coding: utf-8

# # X-ray tube design 

# In[22]:


from __future__ import print_function, division, absolute_import
import spekpy as sp
from matplotlib import pyplot as plt 


# # Parameter Setting

# Physics =                                                                    
# casim (spekpy version 2), kqp (high accuracy), spekcalc(software spekcalc), spekpy-v1(spekpy version 1)
# mu_data_source = pene(default) or nist

# In[46]:


# Tube potential in kV (default: 100)
kvp = 200 
# Exposure set to 2 mAs (default: 1)
mas = 17.8 
# Anode angle in degrees (default: 12)
th = 30 
# Spectrum bin width in keV (default: 0.5)
dk = 1
# Legacy physics mode rather than default (default: "spekpy-v1")
physics = "kqp" 
# Penelope mu/mu_en data rather than NIST/XCOM (default: "nist")
mu_data_source = "nist" 
# The anode target material 
targ = 'W'
# Point-of-interest is at a focus-to-detector-distance of 75 cm (default: 100)
z = 8.4
# Point-of-interest displaced 5 cm towards cathode in anode-cathode direction (default: 0)
x = 0
# Point-of-interest displaced -5 cm in orthogonal direction (right-hand-rule is applicable) (default: 0)
y = 0
# Whether the bremsstrahlung portion of spectrum is retained (default: True)
brem = True 
# Whether the characteristic portion of spectrum is retained (default: True)
char = True
# Whether path-length through extrinsic filtration varies with x, y (default: True)
obli = True 
# Optional fraction to shift the energy bins (-0.5 ~ 0.5)
shift = -0.5


# In[47]:


# Generate unfiltered spectrum
s = sp.Spek(kvp=kvp, th=th, dk=dk, physics=physics, mu_data_source=mu_data_source,
    x=x, y=y, z=z, mas=mas, brem=brem, char=char, obli=obli,targ=targ, shift=shift)

# Filter the spectrum
s.filter('Be',2), s.filter('Cu',0.5)

s.summarize(mode='full')


# # Get spectrum

# In[48]:


# 1. mid-bin, fluence, fluence is differential in energy no sigma 
# Get energy value array and differential fluence arrays (retrun value at bin-edges)
karr, spkarr = s.get_spectrum(edges=True,flu=True,diff=True,sig=None)

# 2. mid-bin ,energy fluence, energy fluence is differential in energy, no sigma
# Get energy values array and differential energy fluence arrays (return value at bin-edges)
karr1, spkarr1 = s.get_spectrum(edges=True,flu=False,diff=True,sig=None)

# 3. mid-bin, fluence, fluence 
# Get energy values array and fluence arrays (return values at bin-edges)
# diff = faluse (fluence, # per cm2 per bin) / (energy fluence # per cm2 per KeV)
karr2, spkarr2 = s.get_spectrum(edges=True,flu=True,diff=False)


# # Plot Spectrum

# In[49]:


fig1, axs1 = plt.subplots()
fig2, axs2 = plt.subplots()
fig3, axs3 = plt.subplots()

axs1.set_title('200 kV Energy spectrum (Fluence)')
axs2.set_title('Differential energy fluence spectrum (flu=False)')
axs3.set_title('Fluence spectrum (diff=False)')

# Plot fluence spectrum, fluence (# per cm2)
axs1.plot(karr , spkarr)
axs1.set(xlabel='Energy [keV]',ylabel='Fluence / mAs / unit energy [photons/cm2/mAs/keV]')

# Plot energy-fluence spectrum  (keV per cm2)
axs2.plot(karr1 , spkarr1)
axs2.set(xlabel='Energy [keV]',ylabel='Energy fluence / mAs / unit energy [photons/cm2/mAs]')

# plot fluence 
axs3.plot(karr2, spkarr2)
axs3.set(xlabel='Energy [keV]',ylabel='Fluence / mAs [photons/cm2/mAs]')

plt.show()


# # Export Spectrum

# Total 3 column <br>
# 
# First : mid-bin energies in KeV <br>
# Second : Total x-ray fluence (bremsstrahlung + characteristic) per KeV <br>
# Thrid : Characteristic x-ray fluence per KeV <br>

# In[50]:


# file append (.spk / .txt / .csv)
spek_name = '200Kev_spectrum_nist_heel.csv'
s.export_spectrum(spek_name, comment='200Kev,17.8mA,30degree,8.4,Bin 1 KeV,spekpy2, nist_heel')
s.summarize(mode ='full')


# In[ ]:





# In[ ]:


# For compatibility with Python2

# Tube potential in kV (default: 100)
kvp = 200 
# Exposure set to 2 mAs (default: 1)
mas = 17.8 
# Anode angle in degrees (default: 12)
th = 30 
# Spectrum bin width in keV (default: 0.5)
dk = 1
# Legacy physics mode rather than default (default: "spekpy-v1")
physics = "kqp" 
# Penelope mu/mu_en data rather than NIST/XCOM (default: "nist")
mu_data_source = "nist" 
# The anode target material 
targ = 'W'
# Point-of-interest is at a focus-to-detector-distance of 75 cm (default: 100)
z = 8.4
# Point-of-interest displaced 5 cm towards cathode in anode-cathode direction (default: 0)
x = 3
# Point-of-interest displaced -5 cm in orthogonal direction (right-hand-rule is applicable) (default: 0)
y = 0
# Whether the bremsstrahlung portion of spectrum is retained (default: True)
brem = True 
# Whether the characteristic portion of spectrum is retained (default: True)
char = True
# Whether path-length through extrinsic filtration varies with x, y (default: True)
obli = True 
# Optional fraction to shift the energy bins (-0.5 ~ 0.5)
shift = -0.5

# Generate unfiltered spectrum
s = sp.Spek(kvp=kvp, th=th, dk=dk, physics=physics, mu_data_source=mu_data_source,
    x=x, y=y, z=z, mas=mas, brem=brem, char=char, obli=obli,targ=targ, shift=shift)

# Filter the spectrum
s.filter('Be',2), s.filter('Cu',0.5)

k = s.get_kerma()

s.summarize(mode='full')

n=301
xarr=np.zeros([n])
darr=np.zeros([n])
for i in range(n):
  x=-10.0+0.1*float(i)
  xarr[i]=x
  darr[i]=k

plt.plot(xarr, darr)
plt.xlabel('x [cm]')
plt.ylabel('Air kerma @ 1 m per mAs [uGy]')
plt.title('A line profile of air kerma')
plt.suptitle('Anode heel-effect, r-sq effect and path-length (in filter) included', y = 0.16, x= 0.53, fontsize=10)
plt.show()


# In[89]:


# Tube potential in kV (default: 100)
kvp = 200 
# Exposure set to 2 mAs (default: 1)
mas = 17.8 
# Anode angle in degrees (default: 12)
th = 30 
# Spectrum bin width in keV (default: 0.5)
dk = 1
# Legacy physics mode rather than default (default: "spekpy-v1")
physics = "kqp" 
# Penelope mu/mu_en data rather than NIST/XCOM (default: "nist")
mu_data_source = "nist" 
# The anode target material 
targ = 'W'
# Point-of-interest is at a focus-to-detector-distance of 75 cm (default: 100)
z = 8.4
# Point-of-interest displaced 5 cm towards cathode in anode-cathode direction (default: 0)
x = 0
# Point-of-interest displaced -5 cm in orthogonal direction (right-hand-rule is applicable) (default: 0)
y = 0
# Whether the bremsstrahlung portion of spectrum is retained (default: True)
brem = True 
# Whether the characteristic portion of spectrum is retained (default: True)
char = True
# Whether path-length through extrinsic filtration varies with x, y (default: True)
obli = True 
# Optional fraction to shift the energy bins (-0.5 ~ 0.5)
shift = -0.5

s = sp.Spek(kvp=kvp, th=th, dk=dk, physics=physics, mu_data_source=mu_data_source,
    x=x, y=y, z=z, mas=mas, brem=brem, char=char, obli=obli,targ=targ, shift=shift)
# Filter the spectrum
s.filter('Be',2), s.filter('Cu',0.5)


# In[90]:


n=501
xarr=np.zeros([n])
darr=np.zeros([n])
for i in range(n):
  x=-10.0+0.1*float(i)
  xarr[i]=x
  s_new = sp.Spek(kvp=kvp, th=th, dk=dk, physics=physics, mu_data_source=mu_data_source,
                 z=8.4, mas=mas, brem=brem, char=char, obli=obli, targ=targ, shift=shift)
  s_new.filter('Be', 2).filter('Cu', 0.5)
  darr[i] = s_new.get_kerma()

plt.plot(xarr, darr)
plt.xlabel('x [cm]')
plt.ylabel('Air kerma @ 1 m per mAs [uGy]')
plt.title('A line profile of air kerma')
plt.suptitle('Anode heel-effect, r-sq effect and path-length (in filter) included', y = 0.16, x= 0.53, fontsize=10)
plt.show()


# In[ ]:





# In[ ]:




