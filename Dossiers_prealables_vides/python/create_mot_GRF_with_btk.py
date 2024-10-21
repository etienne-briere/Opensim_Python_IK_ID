# -*- coding: utf-8 -*-
"""
Created on Thu May 23 21:47:30 2024

@author: BRIERE Etienne
"""

# LIBRAIRIES
import btk
import numpy as np
import os
import sys 

# Importer le script "fonction" du dossier <python>
## Chemin absolu actuel
current_dir = os.getcwd()

## Ajouter le script des fonctions au chemin de recherche des modules
dossier_python = os.path.abspath(current_dir + '/python')
sys.path.append(dossier_python)

## Importer le script des fonctions
import fonctions as fct

# PARAMETRES D'ENTREE
filnameC3D = 'Data/S1/s1s2_saut_h0_0001_cut.c3d'
q1 = -90
q2 = 0
q3 = 0
fout = 'Data/S1/s1s2_saut_h0_0001_cut_GRF.mot'
masse = 64

# TRAITEMENT DU FICHIER .C3D

## Lecture du fichier .c3d
reader = btk.btkAcquisitionFileReader()
reader.SetFilename(filnameC3D)
reader.Update()
acq = reader.GetOutput()

## Extraction des frames de la mocap (utilité ??)
nb_frames_mocap = acq.GetPointFrameNumber() 

## Extraction des frames de capture des PFFs
nb_frames_pff = acq.GetAnalogFrameNumber()

## Fréquence d'acquisition des plateformes (Hz)
freq_analog = acq.GetAnalogFrequency() 

## Fréquence d'acquisition de la mocap (Hz)
freq_mocap = acq.GetPointFrequency()


# RECUPERATION DES INFORMATIONS D'UN MARQUEUR DU PIED

## Extraire les données des marqueurs
markers = acq.GetPoints()

## Parcourir les marqueurs et récupérer leurs positions
marker_positions = {}
for i in range(markers.GetItemNumber()):
    marker = markers.GetItem(i)
    label = marker.GetLabel()
    data = marker.GetValues()  # positions des marqueurs sur chaque frame
    marker_positions[label] = data

## Positions du marqueur RTOE
RTOE_position = marker_positions['RTOE']

## Récupérer moment où RTOE est au plus haut 
where_zmax_RTOE = np.where(RTOE_position[:,2]==max(RTOE_position[:,2]))[0][0]



# RECUPERATION DES INFORMATIONS DES PFF

## Tableau des résultats final vide
#data_results_final = np.zeros([nb_frames_mocap, 19])
data_results_final = np.empty((nb_frames_mocap, 19))*np.nan  

## Création du tableau data_results vide 
coeff = freq_analog/freq_mocap 
#data_results = np.zeros([int(nb_frames_pff/coeff), 6]) # 6 = nb_channels
data_results = np.empty((int(nb_frames_pff/coeff), 6))*np.nan 

## Liste vide des labels des channels
list_labels = []

## Obtenir les plateformes de force
force_platforms = btk.btkForcePlatformsExtractor()
force_platforms.SetInput(acq)
force_platforms.Update()

## Outil pour accéder à la class "btkForcePlatformCollection"
platform_collection = force_platforms.GetOutput()

## Nombre de PFF
nb_pf = platform_collection.GetItemNumber()

## | BOUCLE PFF|
for i_pf in range(nb_pf):
    
    ## Création de l'outil pour accéder aux infos de la PFF
    platform_tools = platform_collection.GetItem(i_pf)
    
    ## Type de la PFF (Type 2 = 6 channels (FX, FY, FZ, MX, MY, MZ))
    type_platform = platform_tools.GetType()
    
    ## Nombre de channels de la pff (Fx, Fy, Fz, Mx, My, Mz)
    nb_channels = platform_tools.GetChannelNumber()
    
    ## |BOUCLE CHANNEL|
    for i_channel in range(nb_channels):
        
        ## Création de l'outil Channel
        channels_tools = platform_tools.GetChannels()
        
        ## Création l'outil pour accéder aux infos du channel cible
        channel_item_tools = channels_tools.GetItem(i_channel)
        
        ## Obtenir le nom du label du channel 
        label = channel_item_tools.GetLabel() 
        print(f"Platform {i_pf+1}")
        print(f"Type: {type_platform}")
        print()
        print(f"Channels {i_channel+1}: {label}")
        
        ## Ajout des labels dans la liste
        list_labels.append(label)
        
        ## Essai random pour obtenir le nombre de données pour créer tab_tps
        FX = acq.GetAnalog(list_labels[0]) 
        Fx = FX.GetValues()
    
        ## Création du tableau de temps
        nb_lignes = Fx.shape [0]
        tps_total = nb_lignes/freq_analog
        tab_tps = np.linspace(0, tps_total, nb_frames_mocap)
        
        ## Ajout de la colonne de temps dans le data_results_final
        data_results_final[:,0] = tab_tps
    
    
        # EXTRACTION DES FORCES ET MOMENTS DE FORCES 

        ## Définir les labels        
        label = list_labels[i_channel]
        
        ## SI NECESSAIRE : Supprimer les suffixes "1" et "2" des labels de la liste 
        if label[-1]==1 or label[-1]==2 :
            label = label [:-1]
            DATA_channel = acq.GetAnalog(label+str(i_pf+1))

        print(label)
        
        ## Recupération des valeurs du channel (Fx, Fy, Fz, Mx, My, Mz)
        DATA_channel = acq.GetAnalog(label)
        
        data_channel = DATA_channel.GetValues()/masse
        print(data_channel)
        
        ## freq_analog --> freq_mocap
        data_channel_cut = data_channel[::int(coeff), :]

        
        ## Importation des data dans le data_results
        data_results[:,i_channel] = data_channel_cut[:,0]
        
      
    ## SI NECESSAIRE : Inverser signe de l'axe z 
    #data_results[:, 2] = -data_results[:, 2] # a voir avec diane !??
      
    ## Si force non remise à zéro --> Ajouter la force négative de la phase vol
    if data_results[where_zmax_RTOE,2]<-10 :
    
        ### Trouver la valeur sur z minimale 
        negative_force = max(data_results[:, 2])
        
        ## Trouver la ligne du tableau correspondante
        row_where = np.where (data_results[:, 2]==negative_force)[0][0]
        
        ## Récupérer x, y, z et ajouter ces valeurs à toutes les lignes
        value_fx_fy_fz_min = data_results[row_where, 0:3]
        
        data_results[:,0:3]=data_results[:,0:3]+abs(value_fx_fy_fz_min)
    
    
    ## Changement de l'unité des moments de force (N.mm en N.m)
    ### Obtenir les numéros des colonnes des moments de force
    Moment_force_col = [3,4,5]
    
    ### Convertir les Mf en N.m
    #data_results[:, Moment_force_col] = data_results[:, Moment_force_col]/1000

    ## Importation des data dans le data_results_final (à voir pour essayer de placer exactement comme le .mot de nicolas)
    if i_pf == 0 :
        data_results_final[:,1:7]  = data_results[:,0:6] 
    if i_pf == 1 :
        data_results_final[:,7:13] = data_results[:,0:6] 
   
    
   
    # PASSAGE DES Fx Fy Fz ET CoP DANS LE REPERE CAPTURE

    ## Création de la matrice de la PFF

    ### Création de l'outil pour accéder aux infos de la PFF 
    platform_tools = platform_collection.GetItem(i_pf)
    
    ### Origine de la PFF
    origin = platform_tools.GetOrigin()
    
    ### Aplatir le tableau en (3,)
    origin = origin.ravel()

    ### Tableau de la position des coins de la PFF
    corners = platform_tools.GetCorners()
    print(f"Platform {i_pf+1}")
    print("Corners:")
    for corner in corners:
        print(f"  {corner}")
    print()

    ### Vecteur x du repère 
    x = ((corners[:,3]-corners[:,0])/2)-((corners[:,1]-corners[:,2])/2)
    x = x/fct.norme(x)

    ### Vecteur y du repère 
    y = ((corners[:,0]-corners[:,1])/2)-((corners[:,2]-corners[:,3])/2)
    y = y/fct.norme(y)
    
    ### Vecteur z du repère
    z = np.cross(x,y)
    z = z/fct.norme(z)

    ### Produit vectoriel pour s'assurer de l'orthogonalité du repère 
    y = np.cross(z,x)

    ### Matrice du repère plateforme
    Rplatform = np.array([x,y,z]) 


    ### |BOUCLE FRAME|
    nb_frames = data_channel.shape[0]
    for i_frame in range (nb_frames_mocap):
        
        
        ### Données 3D de la force à chaque image (Fx, Fy, Fz)
        data_F = data_results[i_frame, 0:3]

        ### Données 3D du moment de force à chaque image (Mx, My, Mz)
        data_Mp = data_results[i_frame, 3:6]
        
        ## Convertir les Mf en N.m
        data_Mp = data_Mp/1000

        ### Passage de F dans le repère de capture
        F = Rplatform@data_F

        ### Passage de Mp (moment de force) dans le repère capture
        Mp = Rplatform@data_Mp
        
        ### Replacer Mp à l'origine du repère mocap (??)
        M0 = Mp + np.cross(origin, F)
        
        
        # PASSAGE DES VARIABLES DANS LE REPERE OPENSIM
        
        ## Matrice de tranformation dans le repère opensim (-90° sur x normalement)
        Rop = fct.transfo_cap_to_opensim(q1, q2, q3)
        
        ## Calcul du CoP dans le repère plateforme
        CoP = np.cross(data_F,data_Mp/fct.norme(data_F**2)) 
        
        ## Point sur l'axe avec z = 0
        CoP = CoP - (CoP[2]/data_F[2])*data_F
        
        ## Passage du CoP dans le repère capture 
        CoP0 = origin + Rplatform@CoP
        
        ## Passage des variables dans le repère Opensim
        F = Rop@F
        M0 = Rop@M0
        CoP0 = Rop@CoP0
        
        ## Importation dans le data_results_final (tableau dans le même ordre que le .mot --> Fx1, Fy1, Fz1, CoPx1, CoPy1, CoPz1, Fx2, Fy2, Fz2, CoPx2, CoPy2, CoPz2, Mx1, My1, Mz1, Mx2, My2, Mz2)
        if i_pf == 0 :
            data_results_final[i_frame,1:4] = F
            data_results_final[i_frame,13:16] = M0
            data_results_final[i_frame,4:7] = CoP0
        
        if i_pf == 1 :
            data_results_final[i_frame,7:10] = F
            data_results_final[i_frame,16:] = M0
            data_results_final[i_frame,10:13] = CoP0
        


# ECRIRE LES DONNEES DANS UN FICHIER .MOT

# Variables d'entrée
nrow = nb_frames_mocap
ncols = data_results_final.shape[1]
list_labels_mot = ['time', 'ground_force_vx', 'ground_force_vy', 'ground_force_vz', 'ground_force_px', 'ground_force_py', 'ground_force_pz',
               '1_ground_force_vx', '1_ground_force_vy', '1_ground_force_vz', '1_ground_force_px', '1_ground_force_py', '1_ground_force_pz',
               'ground_torque_x','ground_torque_y','ground_torque_z', '1_ground_torque_x','1_ground_torque_y','1_ground_torque_z']



# Ouvrir le fichier en mode écriture
with open(fout, 'w') as f:
    # Écrire l'en-tête
    f.write("name\t{}\n".format(fout))
    f.write("datacolumns\t{}\n".format(ncols))
    f.write("datarows\t{}\n".format(nb_frames_mocap))
    f.write("range\t0.0\t{}\n".format(nb_frames_mocap / freq_mocap))
    f.write("endheader\n\n")
    
   # Écrire le label 'time'
    f.write('{}\t'.format(list_labels_mot[0]).rjust(21))

    # Écrire les autres labels
    for i in range(1, ncols):
        f.write('{}\t'.format(list_labels_mot[i]).rjust(21))
    
    # Ajouter une nouvelle ligne après les labels
    f.write('\n')

    # Écrire les données
    for row in data_results_final :
        for item in row:
            f.write('{:.8f}\t'.format(item).rjust(21))
        f.write('\n')

print("Conversion réussie ! Le fichier <" + fout+"> a été créé.")
