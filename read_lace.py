#!/usr/bin/env python

import scipy.io as sio
import bz2
import matplotlib.pyplot as plt
import glob
import scipy.constants as c
import numpy as n
import stuffr

sample_rate=1e6/3.0


def read_lace_file(fn):
    # with vhf, both the ion line and the plasma line channel are recorded with a
    # 1/3 MHz sample-rate, which presumably corresponds to the transmit baud length
    # the interpulse period is 6144 microseconds
    # there are 1024 ipps in one file,
    # the transmit pulse length is 246 samples
    # there are 512 transmit samples
    # the plasmaline center frequency is UP 5, but it is -7.5 MHz, and yet we can see
    # plasma-lines in the data
    
    #"lace_zenith_1.0v_SW@vhf/20200318_13/06702271.mat.bz2"
    a=sio.loadmat(bz2.open(fn))
 #   print(a.keys())
    
    print(a["d_parbl"])
#    print(a["d_parbl"].shape)
    
    pl_freq=a["d_parbl"][0,46]
    print(pl_freq)
#    return
    
    print(a["d_raw"].shape)
    
    ut=a["d_parbl"][0,10]
    # tx samples
    #0 - 125951
    tx=a["d_raw"][0:125952]
    n_tx=int(len(tx)/512)
    print(n_tx)
    
    tx.shape=(512,246)

    # ion line
    il_echoes=a["d_raw"][125952:1822720]
    
    # plasma line
    #    1822720 - 3519487
    pl_echoes=a["d_raw"][1822720:3519488]


    n_ipp=1024
    n_samples=1657
    # start of tx in samples
    tx_start=74/3.0
    # microseconds
    ipp=6144
    # start of rx in samples
    start_sample=1108/3.0
    pl_echoes.shape=(n_ipp,n_samples)
    il_echoes.shape=(n_ipp,n_samples)    

    sync_time = 8544
    
    #print(len(echoes)/512)

    range_km=c.c*(n.arange(n_samples)+start_sample)/sample_rate/2.0/1e3
    times=n.arange(n_ipp)*ipp/1e6

    dB=10.0*n.log10(n.abs(il_echoes)**2.0)
    dB=dB-n.nanmedian(dB)
    plt.subplot(121)
    plt.pcolormesh(range_km,times,dB,vmin=-3,vmax=12)
    plt.title("ion line\n%s"%(stuffr.unix2datestr(ut)))
    plt.xlim([0,900])
    plt.colorbar()
    
    plt.subplot(122)
    dB=10.0*n.log10(n.abs(pl_echoes)**2.0)
    dB=dB-n.nanmedian(dB)
    plt.pcolormesh(range_km,times,dB,vmin=-3,vmax=12)
    plt.title("plasma line")
    plt.xlim([0,900])
    plt.colorbar()
    plt.tight_layout()
    plt.savefig("img-%d.png"%(ut))
    plt.close()
    plt.clf()



fl=glob.glob("/home/j/Downloads/lace_zenith_1.0v_SW@vhf/*/*.bz2")
fl.sort()
for f in fl:
    read_lace_file(f)
