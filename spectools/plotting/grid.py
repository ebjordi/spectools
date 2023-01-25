import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from astropy.constants import c
from spectools.utils import *
from orbit import Orbit

# fijamos d,t1*,t2*
def main(
    A="../T300g380.asc",
    B="../T350g370.asc",
    d=0.78,
    regions1=None,
    regions2=None,
    regions3=None,
    N = 100,
    **kwargs):
    wb, fb = ascii_spec(B)
    # len(wb)
    # len(fb)
    fb = fb[wb < 7000]
    wb = wb[wb < 7000]

    wa, fa = ascii_spec(A)
    fa = fa[wa < 7000]
    wa = wa[wa < 7000]

    orb = Orbit.from_linspace(N, e=.734628,omega=126.314, K1= 108.311,K2=-192.327,gamma = 0.)

    d = 0.78
    fa = fa * d
    fb = fb * (1 - d)
    ticker = 0
    H = [(4090, 4120), (4330, 4350), (4850, 4875), (6550, 6580)]
    HeI = [(4018, 4035), (4382, 4398), (4465, 4480), (5868, 5886)]
    HeII = [(4190, 4210), (4535, 4550), (4680, 4697), (5400, 5423)]
    H_labels = ["Hδ", "Hγ", "Hβ", "Hα"]
    HeI_labels = ["HeI+II4026", "HeI4388", "HeI4471", "HeI5875"]
    HeII_labels = ["HeII4200", "HeII4542", "HeII4686", "HeII5412"]
    #aliases for ease of read
    a = 1
    phases = orb.phases
    theta = orb.theta
    r_1 = (a*(1-orb.e**2))/(1+orb.e*np.cos(orb.theta))
    r_2=(a*(1+orb.e**2))/(1+orb.e*np.cos(orb.theta))
    o = 0 #np.deg2rad(orb.omega)
    rb1 = value_to_rgb(orb.vr1)
    rb2 = value_to_rgb(orb.vr2)
    rv1 = orb.rv1
    rv2 = orb.rv2

    for v1,v2 in zip(orb.vr1,orb.vr2):
        fig2,axs = plt.subplots(4,4,sharey='row',figsize=plt.figaspect(0.75),
                            gridspec_kw={"hspace":0.5, 'wspace': 0.05})
        #subplot polar
        axs[3,0].remove()
        axs[3,1].remove()
        axs[3,2].remove()
        axs[3,0]=plt.subplot2grid((4,4), (3,0), rowspan=1, colspan=1,fig=fig2,polar=True)
        axs[3,1]=plt.subplot2grid((4,4), (3,1), rowspan=1, colspan=1,fig=fig2,polar=True)
        axs[3,2]=plt.subplot2grid((4,4), (3,2), rowspan=1, colspan=1,fig=fig2,polar=True)


        #sin ejes
        axs[3,0].set_xticks([])
        axs[3,0].set_yticks([])
        axs[3,1].set_xticks([])
        axs[3,1].set_yticks([])
        axs[3,2].set_xticks([])
        axs[3,2].set_yticks([])
        for ax in axs[3,:]:
            ax.sharey = None
            ax.tick_params(labelsize=5)

        #doppler segun v1,v2
        fb_s=shift(wb,fa,v2) #puedo hacer un dict para achicar esto
        fa_s=shift(wa,fb,v1) #y esto
        if len(fb_s) > len(fa_s):
            arr_len = len(fa_s)
        else: arr_len = len(fb_s)
        w1=wa
        fa_s = fa_s[:arr_len]
        fb_s = fb_s[:arr_len]
        f1 = fa_s[:arr_len]+fb_s[:arr_len]+np.random.normal(0,0.002,arr_len)

        for i,region in enumerate(H):
            axs[0,i].plot(w1,f1,linewidth=0.5,color= '#BC48EE')
            axs[0,i].plot(w1,fa_s+d+0.01,'--',linewidth=0.5,color= '#BC4822',alpha=0.7)
            axs[0,i].plot(w1,fb_s+(1-d)+0.01,'--',linewidth=0.5,color= '#332089',alpha=0.7) #plot models
            axs[0,i].set_title(H_labels[i],fontsize='xx-small')
            axs[0,i].set_xticks(range(H[i][0],H[i][1], 20))
            axs[0,i].tick_params(labelsize=5)
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
        axs[3,-1].set_title('velocidades radiales vs fase',fontsize='xx-small' )
        axs[3,-1].plot(phases,rv1,linewidth=0.3,c='b')
        axs[3,-1].plot(1+phases[:50],rv1[:50],linewidth=0.3,c='b')
        axs[3,-1].scatter(phases[ticker],v1,c='b',s=0.5)

        axs[3,-1].plot(phases,rv2,linewidth=0.3,c='r')
        axs[3,-1].plot(1+phases[:50],rv2[:50],linewidth=0.3,c='r')
        axs[3,-1].scatter(phases[ticker],v2,c='r',s=0.5)
        #plot orbit 1
        axs[3,0].plot(theta+o, r_1,c='k',alpha=0.5,lw=0.5)
        axs[3,0].scatter(theta[ticker]+o, r_1[ticker],s=3,c=rb1[ticker])
        #plot orbit 2
        axs[3,1].plot(theta+o+np.pi, r_2,c='k',alpha=0.5,lw=0.5)
        axs[3,1].scatter(theta[ticker]+np.pi+o, r_2[ticker],s=3,c=rb2[ticker])
        #plot both
        axs[3,2].plot(theta+o, r_1,c='k',alpha=0.5,lw=0.5)
        axs[3,2].plot(theta+o+np.pi, r_2,c='k',alpha=0.5,lw=0.5)

        axs[3,2].scatter(theta[ticker]+o, r_1[ticker],s=3,c=rb1[ticker])
        axs[3,2].scatter(theta[ticker]+np.pi+o, r_2[ticker],s=3,c=rb2[ticker])

        if (ticker < 50):
            axs[3,-1].scatter(1+phases[ticker],v1,c='b',s=0.5)
            axs[3,-1].scatter(1+phases[ticker],v2,c='r',s=0.5)


        #Save Plot
        plt.savefig(f'sp_or{ticker}.png',dpi=800)
        ticker += 1
        #Clear RAM
        plt.close()

    


def ratio(value,min_value=None,max_value=None):
    if min_value is None:
        min_value = np.min(value)
    if max_value is None:
        max_value = np.max(value)
    return (value - min_value) / (max_value - min_value)

def value_to_rgb(value,*args):
        rat = ratio(value,*args)
        r = (255 * np.ones_like(value) * (1.- rat)).astype(int)
        g = (255 * np.ones_like(value) * (1.-abs(2. * rat-1.))).astype(int)
        b = (255 * np.ones_like(value) * rat).astype(int)
#        rgbs = ["#{:02x}0000".format(ri) for ri in r]

        rgbs = ["#{:02x}00{:02x}".format(ri,gi,bi) for ri,gi,bi in zip(r,g,b)]
        return rgbs#"#{:02x}{:02x}".format(r,g,b)



if __name__ == '__main__':
    main()