import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from astropy.constants import c


columns = ['phase','VRA','VRB','E']
data = pd.read_csv('kepler_song.out',skiprows=1,names=columns,sep=' ')

def ascii_spec(filename):
    a = np.genfromtxt(filename,delimiter = '  ')
    w = a[:,0]
    f = a[:,-1]
    return w,f


cvel = c.to('km/s').value
def shift(wvl,flux,v):
    wlprime = wvl * (1.0 + v / cvel)
    nflux = interp1d(wlprime, flux, bounds_error=False, fill_value=1)(wvl)
    return nflux
#fijamos d,t1*,t2*

wb,fb = ascii_spec('./T300g380.asc')
#len(wb)
#len(fb)
fb=fb[wb<7000]
wb=wb[wb<7000]

wa,fa = ascii_spec('./T350g370.asc')
fa=fa[wa<7000]
wa=wa[wa<7000]



d=0.78
fa = fa*d
fb = fb*(1-d)
ticker = 0
H = [(4090,4120),(4330,4350),(4850,4875),(6550,6580)]
HeI = [(4018,4035),(4382,4398),(4465,4480),(5868,5886)]
HeII = [(4190,4210),(4535,4550),(4680,4697),(5400,5423)]
H_labels = ['Hδ', 'Hγ', 'Hβ', 'Hα']
HeI_labels = ['HeI+II4026','HeI4388','HeI4471','HeI5875']
HeII_labels = ['HeII4200','HeII4542','HeII4686','HeII5412']
for av,bv in zip(data['VRA'][:100],data['VRB'][:100]):
    fig2,axs = plt.subplots(4,4,sharey='row',figsize=plt.figaspect(0.75),
                        gridspec_kw={"hspace":0.5, 'wspace': 0.05})
    fb_s=shift(wb,fa,bv)
    fa_s=shift(wa,fb,av)
    if len(fb_s) > len(fa_s):
        arr_len = len(fa_s)
    else: arr_len = len(fb_s)
    w1=wa
    fa_s = fa_s[:arr_len]
    fb_s = fb_s[:arr_len]
    f1=fa_s[:arr_len]+fb_s[:arr_len]+np.random.normal(0,0.002,arr_len)
    
    for i,region in enumerate(H):
        axs[0,i].plot(w1,f1,linewidth=0.5,color= '#BC48EE')
        axs[0,i].plot(w1,fa_s+d+0.01,'--',linewidth=0.5,color= '#BC4822',alpha=0.7)
        axs[0,i].plot(w1,fb_s+(1-d)+0.01,'--',linewidth=0.5,color= '#332089',alpha=0.7) #plot models
        axs[0,i].set_title(H_labels[i],fontsize='xx-small')
        axs[0,i].set_xticks(range(H[i][0],H[i][1], 20))
        axs[0,i].tick_params(labelsize=5)
#        axs[0,i].plot(ww,ff,'gray',alpha=0.5)              #plot spec 0.5 opacity
        axs[0,i].set_xlim(region)                          #plot region
        axs[0,i].set_ylim(0.56,1.05)

    for i,region in enumerate(HeI):
        axs[1,i].plot(w1,f1,linewidth=0.5,color= '#BC48EE')
        axs[1,i].plot(w1,fa_s+d+0.01,'--',linewidth=0.5,color= '#BC4822',alpha=0.7)
        axs[1,i].plot(w1,fb_s+(1-d)+0.01,'--',linewidth=0.5,color= '#332089',alpha=0.7) #plot models
        axs[1,i].set_title(HeI_labels[i],fontsize='xx-small')
        axs[1,i].set_xticks(range(HeI[i][0],HeI[i][1], 10))
        axs[1,i].tick_params(labelsize=5)

        axs[1,i].set_xlim(region)
        axs[1,i].set_ylim(0.73,1.05)

    for i,region in enumerate(HeII):
        axs[2,i].plot(w1,f1,linewidth=0.5,color= '#BC48EE')
        axs[2,i].plot(w1,fa_s+d+0.01,'--',linewidth=0.5,color= '#BC4822',alpha=0.7)
        axs[2,i].plot(w1,fb_s+(1-d)+0.01,'--',linewidth=0.5,color= '#332089',alpha=0.7) #plot models
        axs[2,i].set_title(HeII_labels[i],fontsize='xx-small' )
#        axs[2,i].plot(ww,ff,'gray',alpha=0.5)
        axs[2,i].set_xticks(range(HeII[i][0],HeII[i][1], 15))
        axs[2,i].tick_params(labelsize=5)

        axs[2,i].set_xlim(region)
        axs[2,i].set_ylim(0.78,1.05)

    #Draw orbit
    for ax in axs[3,:]:
        ax.tick_params(labelsize=5)
    axs[3,-1].set_title('Velocidades Radiales vs fase',fontsize='xx-small' )
#        axs[2,i].plot(ww,ff,'gray',alpha=0.5)
    axs[3,-1].plot(data['phase'],data['VRA'],linewidth=0.3)
    axs[3,-1].scatter(data['phase'][ticker],av,c='b',s=0.5)
    axs[3,-1].plot(data['phase'],data['VRB'],linewidth=0.3)
    axs[3,-1].scatter(data['phase'][ticker],bv,c='r',s=0.5)
    
    if (ticker < 50):
        axs[3,-1].scatter(data['phase'][ticker]+1,av,c='b',s=0.5)
        axs[3,-1].scatter(data['phase'][ticker]+1,bv,c='r',s=0.5)
    #Save Plot
    plt.savefig('sp_'+str(data['phase'][ticker])+'.png',dpi=800)
    ticker += 1
    #Clear RAM
    plt.close()
