import glob
import matplotlib.pyplot as plt
import h5py
import numpy as n
import stuffr
import scipy.constants as c

fl=glob.glob("lace_il/pprof*.h5")
fl.sort()

h=h5py.File(fl[0],"r")
pprof=h["power"][()]
n_rg=len(pprof)
h.close()

S=n.zeros([n_rg,len(fl)])

uts=[]
for i in range(len(fl)):
    print(i)
    h=h5py.File(fl[i],"r")
    p=h["power"][()]
    S[:,i]=p
    uts.append(stuffr.unix2date(h["ut"][()]))
    h.close()
    
# from rtg_def_v.m
r0=1e-6*(1034-720)*c.c/2.0/1e3

rg=n.arange(1656)*3e-6*c.c/2.0/1e3 + r0

print(S.shape)

S[S<0]=1e-3
#plt.imshow(10.0*n.log10(S[::-1,:]),vmin=20,vmax=90)
#plt.colorbar()
#plt.show()
plt.figure(figsize=(8*2,6*2))
plt.pcolormesh(uts,rg,10.0*n.log10(S),vmin=60,vmax=90)
plt.title("Raw power (dB)")
plt.xlabel("Time (UT)")
plt.ylabel("Height (km)")
plt.ylim([150,250])
plt.colorbar()
plt.tight_layout()
plt.savefig("pwr.png")
plt.show()
