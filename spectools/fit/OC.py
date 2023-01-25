import numpy as np
from utils import cut_resample
from typing import Union
from astropy.constants import c
from orbit import Orbit
from spectools import utils
from concurrent.futures import ThreadPoolExecutor, as_completed
import concurrent

def main():
    wo,fo=utils.open_file('HD37043_20170408_201940_M_V85000.fits')
    fo = fo[0]

    A = 'T350g370.asc'
    B = 'T300g380.asc'
    v1=-100
    v2=300

    w1, fa_s, fb_s = utils.open_shift(A,B,v1,v2,b=7000)

    dils = [0.6,0.65,0.7,0.75,0.8,0.85]
    lines=[(4080,4112),(4330,4346),(4845,4875),(4019,4035),(5868,5885),(4682,4693),(4197,4203),(4537,4543),(4682,4686),(5400,5417)]
    #Esto son etiquetas para el mapa de color

    labels_y = [str(d) for d in dils]
    labels_x = [str(l) for l in lines]

    tests = OC_dils(w1,fa_s,fb_s,wo,fo,dils,lines)#OC_dils_parallel(w1,fa_s,fb_s,wo,fo,dils,lines)
    print(tests)
    return


def OC_dils(w_model :  np.array, f_model_a :  np.array, f_model_b :  np.array,
            w_object :  np.array, f_object :  np.array, dilutions :  Union[list,np.array], regions :  Union[list,np.array]):

    #Hacemos una matriz de (O-C)**2 donde las filas son dilusion y las columnas regiones que pasamos como argumento
    region_oc = np.ndarray((len(dilutions),len(regions)))
    for i,d in enumerate(dilutions):
        fa_ = f_model_a * d
        fb_ = f_model_b * (1-d)
        f1 = fa_+fb_
        for j,ab in enumerate(regions):
            a,b=ab
            x,y,y_model = cut_resample(w_model,f1,w_object,f_object,a,b)
            region_oc[i][j] = (np.square(y-y_model) / y_model).sum()
    return region_oc

def OC_dils_parallel(w_model : np.array, f_model_a : np.array, f_model_b : np.array,
                    w_object : np.array, f_object : np.array, dilutions : Union[list,np.array], regions : Union[list,np.array]):

    region_oc = np.ndarray((len(dilutions),len(regions)))
    with ThreadPoolExecutor() as executor:
        futures = {}
        for i,d in enumerate(dilutions):
            fa_ = f_model_a * d
            fb_ = f_model_b * (1-d)
            f1 = fa_+fb_
            future = executor.submit(calculate_OC,f1,w_model,f_object,w_object,regions,i,region_oc)
            futures[future] = i
    for future in concurrent.futures.as_completed(futures):
        i = futures[future]
        try:
            region_oc[i] = future.result()
        except Exception as e:
            print(f'{i} generated an exception: {e}')
    return region_oc

def calculate_OC(f1,w_model,f_object,w_object,regions,i,region_oc):
    for j,ab in enumerate(regions):
        a,b=ab
        x,y,y_model = cut_resample(w_model,f1,w_object,f_object,a,b)
        region_oc[i][j] = (np.square(y-y_model) / y_model).sum()
    return region_oc[i]


if __name__ == '__main__':
    main()
