# -*- coding: utf-8 -*-
"""
Objectif de ce script : Lancer le process des outils Scale Model, Inverse Kinematics, 
Inverse Dynamics pour de nombreux essais et sujets (normalement applicables dans OpenSim)

DOSSIERS A CREER :
    - Dossier "Calibrations" : sous-dossiers de chaque sujet 
    avec le .C3D de la calibration (ou pose static)
    - Dossier "Data" : sous-dossiers de chaque sujet
    avec .C3D des essais à traiter
    - Dossier "outputs" : sous-dossiers de chaque sujet
    vides
    - Dossier "Geometry" : mesh (en .VTP) pour modèle
    - Dossier "python" :  "code.py" et "fonctions.py"

FICHIERS A CREER : 
    - "Model.osim" : modèle à mettre à l'échelle
    - "Scaled_Settings_empty.xml" : paramètres standards Scale Model
    - "IK_Settings_empty.xml" : paramètres standards Inverse Kinematics
    - "ID_Settings_empty.xml" : paramètres standards Inverse Dynamics
    - "GRF_Settings_empty.xml" : paramètres standards des forces externes
    
PARAMETRES D'ENTREES LORS DU LANCEMENT DU SCRIPT :
   - Masse(s) sujet(s) en kg
   - Rotation sur x, y, z entre MOCAP et OPENSIM (°)
   - Localisation de l'application des forces externes (pied droit/gauche)
   - Choix du paramétrage des différents outils (Scale Model, IK, ID)

CONDITIONS D'UTILISATION DU CODE :
    - Choix du paramétrage des outils est le même pour tous les sujets
    - Fonctionne seulement si essais comportent 2 PFFS
    - Fonctionne qu'importe le nombre de sujets
    - Fonctionne qu'importe le nombre d'essais/sujet (même si nbr différent entre sujet)

"""

# LIBRAIRIES
import opensim
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

# Supprimer les messages [info]
opensim.Logger.setLevelString('Warn')  # Pour n'afficher que les avertissements et les erreurs


# =============================================================================
#                               PARAMETRES DE SORTIE
# =============================================================================

# Liste vide des chemins des fichiers de calib pour chaque sujet
list_path_calib_transform = []

# Dictionnaire vide des chemins des fichiers de mocap pour chaque sujet 
dict_path_mocap_transform = {}

# Dictionnaire vide des noms des fihciers mocap.c3d pour chaque sujet
dict_mocap_transform = {}

# Distionnaire vide des chemins vers les mocap.c3d de chaque sujet
dict_path_mocap_c3d = {}

# Liste des chemins de sortie des IDResults
list_path_IDResults =[]

# Dict des chemins des IDResults pour chaque sujet
dict_path_IDResults = {}

# Liste du nombre de mocap par sujet
list_nb_mocap = []



# =============================================================================
#                               PARAMETRES D'ENTREE
# =============================================================================


# Fichier du modèle .osim (du laboratoire M2S)
model = "M2S_model_complet.osim"
print()
print ('Modèle unscaled :', model)
print()

# Liste des sujets (sous-dossiers)
subfolders_sujet = os.listdir('Calibrations')
list_sujet = [d for d in subfolders_sujet if os.path.isdir(os.path.join('Calibrations', d))]
nb_sujets = len(list_sujet)



#--------------------------[CHOIX DES PARAMETRES D'ENTREE]---------------------

# CHOIX MASSE SUJET
list_masse = []
## |BOUCLE SUJET|
for i_sujet in range (nb_sujets):
    sujet = list_sujet[i_sujet]
    
    ## Entrer masse sujet(s) 
    masse_sujet = float(input(f"Entrez masse [{sujet}] (kg) : "))
    
    ## Liste et nombre de masse
    list_masse.append(masse_sujet)
    nb_masses = len(list_masse)
print()   
    
# CHOIX ROTATION MOCAP -> OPENSIM 
## => Rotations sur x(q1) y(q2) z(q3) en degrés (par défaut : -90, 0, 0)
q1 = int(input("Entrez la rotation mocap -> opensim sur x (°): "))
q2 = int(input("Entrez la rotation mocap -> opensim sur y (°): "))
q3 = int(input("Entrez la rotation mocap -> opensim sur z (°): "))
print()


#--------------------------[CHOIX DES OPTIONS DU SCALE MODEL]------------------

# CHOIX DE L'APPLICATION 
choice_ScaleModel = input("Créer un modèle mis à l'échelle pour le(s) sujet(s) :\n1 - Oui\n2 - Non\n")
print()

if choice_ScaleModel == "1" :

    ## Choix de l'outil <ModelScaler> (mettre à l'échelle les segments en fonction de la calib) 
    choice_ModelScaler = input("Appliquer l'outil Model Scaler :\n1 - Oui\n2 - Non\n")
    print()
    
    if choice_ModelScaler == "1":
        choice_MS = True
        
        ### Choix de l'option pour préserver la masse lors de la distribution
        choice_preserve_mass = input("Preserve mass distribution :\n1 - Oui\n2 - Non\n")
        print()
        
    if choice_ModelScaler == "2":
        choice_MS = False
         
    
    ## SI NECESSAIRE : Fichier de sortie des mesures des segments mis à l'échelle
    if choice_ModelScaler == "1":
        choice_scalefactor = input("Souhaitez-vous les mesures des segments mis à l'échelle (Scale Factors):\n1 - Oui\n2 - Non\n")
        print()
    
    ## Choix de l'outil <MarkerPlacer> (ajuster le modèle en fonction des marqueurs)
    choice_MarkerPlacer = input("Appliquer l'outil Marker Placer :\n1 - Oui\n2 - Non\n")
    print()
    
    if choice_MarkerPlacer == "1":
        choice_MP = True
        
        ### SI NECESSAIRE : Ajouter un markerset
        choice_markerset = input("Ajouter un markerset (.xml) :\n1 - Oui\n2 - Non\n")
        print()
    
    if choice_MarkerPlacer == "2":
        choice_MP = False
        
        
    ## SI NECESSAIRE : Ajouter un markerset avec génération des marqueurs automatiques
    if choice_MarkerPlacer == "1":
        if choice_markerset == "1":
            markerset = input('Nom du fichier du markerset (name_markerset.xml) : ')
        
    if choice_MarkerPlacer =='1' :
        choice_markerset_calib = input("Souhaitez-vous un markerset (.xml) de la calibration :\n1 - Oui\n2 - Non\n")
        print()


#------------------------------[CHOIX DES OPTIONS DU IK]-----------------------

# CHOIX DE L'APPLICATION 
choice_IK = input("Lancer le processus de cinématique inverse :\n1 - Oui\n2 - Non\n")
print()


#------------------------------[CHOIX DES OPTIONS DU ID]-----------------------

# CHOIX DE L'APPLICATION 
choice_ID = input("Lancer le processus de dynamique inverse :\n1 - Oui\n2 - Non\n")
print()

if choice_ID == "1":
    
    ## CHOIX : Partie du corps sur laquelle s'exerce les forces externes
    choice_body_pff1 = input("Application de la force externe 1 (Pff 1) :\n1 - Pied droit\n2 - Pied gauche\n")
    choice_body_pff2 = input("Application de la force externe 2 (Pff 2) :\n1 - Pied droit\n2 - Pied gauche\n")

    ## Création des variables d'entrée en fonction des choix
    if choice_body_pff1 == "1":
        body_pff1 = 'toes_r'
    
    if choice_body_pff1 == "2":
        body_pff1 = 'toes_l'

    if choice_body_pff2 == "1":
        body_pff2 = 'toes_r'
    
    if choice_body_pff2 == "2":
        body_pff2 = 'toes_l'


#--------------------[FICHIERS DE CALIBRATION / SUJET (C3D)]-----------------

# |BOUCLE SUJET|
for i_sujet in range (nb_sujets):
    sujet = list_sujet[i_sujet]
    
    ## Liste de tous les fichiers dans le dossier 
    fichier_calib = os.listdir(f'Calibrations/{sujet}')
    
    ## Filtrer pour ne garder que le fichier avec l'extension .c3d (.trc pour l'instant)
    calib = [f for f in fichier_calib if f.endswith('.c3d')]
    
    ## Afficher le fichier de calib/static traité
    print (f'Fichier de calibration [{sujet}] : ', calib[0])
    print()
    
    ## Chemin du fichier de calib (C3D)
    path_calib_c3d = os.path.join(f'Calibrations\\{sujet}', calib[0])


    #-----------------------[CONVERTION CALIB.C3D --> CALIB.TRC]---------------

    ## Chemin du fichier .TRC de sortie 
    path_calib_trc = os.path.join(f'Calibrations\\{sujet}', calib[0][:-4]+'.trc')
    
    ## Convertion à l'aide de la fonction 'convert_c3d_to_trc'
    fct.convert_c3d_to_trc(path_calib_c3d, path_calib_trc)
    print()


    #-------------------------[PIVOTER LES DONNEES DU CALIB.TRC]---------------

    ## Matrice de rotation MOCAP -> OPENSIM  
    Rop = fct.transfo_cap_to_opensim(q1,q2,q3)
    
    ## Chemin vers le fichier .trc transformé
    path_calib_transform = path_calib_trc[:-4]+'_transformed.trc'
    list_path_calib_transform.append(path_calib_transform)
    
    ## Lire les données du fichier .trc
    header, data = fct.read_trc(path_calib_trc)
    
    ## Appliquer la rotation
    rotated_data = fct.rotate_data(data, Rop)
    
    ## Écrire les données modifiées dans un nouveau fichier .trc
    fct.write_trc(path_calib_transform, header, rotated_data)


    #-----------------------[LISTE DES FICHIERS DE MOCAP (C3D)]----------------

    ## Liste de tous les fichiers dans le répertoire
    fichiers_mocap = os.listdir(f'Data/{sujet}')

    ## Filtrer pour ne garder que les fichiers avec l'extension .c3d 
    list_mocap = [f for f in fichiers_mocap if f.endswith('.c3d')]
    nb_mocap = len(list_mocap)

    
    ## Ajout dans le dictionnaire
    dict_mocap_transform[sujet] = list_mocap
    
    ## Ajout dans la liste du nombre de mocap par sujet
    list_nb_mocap.append(nb_mocap)
    
    ## Affichage des fichiers traités
    print (f'Fichiers mocap [{sujet}] : ')
    for mocap in list_mocap :
        print (mocap)
    print()
    
    
    ## Listes des chemins vers les fichiers trouvés
    list_path_mocap_c3d =[]
    for mocap in list_mocap:
        list_path_mocap_c3d.append(os.path.join(f'Data\\{sujet}', mocap))
    
    ## Ajout dans le dictionnaire
    dict_path_mocap_c3d [sujet] = list_path_mocap_c3d

    #-----------------------[CONVERTION MOCAP.C3D --> MOCAP.TRC]---------------

    ## Listes vides des chemins des fichiers .TRC de sortie 
    list_path_mocap_trc =[]
    
    ## Listes vides des chemins des fichiers .TRC pivotés de sortie
    list_mocap_transform = []

    
    ## |BOUCLE MOCAP|
    for i_mocap in range(list_nb_mocap[i_sujet]):
        mocap = list_mocap[i_mocap]
       
        ## Chemin du fichier .TRC de sortie
        path_mocap_trc = os.path.join(f'Data\\{sujet}', list_mocap[i_mocap][:-4]+'.trc')
        
        ## Listes des chemins mocap.trc
        list_path_mocap_trc.append(path_mocap_trc)
    
        ## Convertion à l'aide de la fonction 'convert_c3d_to_trc'
        fct.convert_c3d_to_trc(list_path_mocap_c3d[i_mocap], path_mocap_trc)
        print()


        #----------------------[PIVOTER LES DONNEES DES MOCAP.TRC]-------------

        ## Chemin vers le fichier .TRC 
        path_mocap_trc = list_path_mocap_trc[i_mocap]
        
        ## Chemin vers le fichier .TRC transformé de sortie
        output_file_path = path_mocap_trc[:-4]+'_transformed.trc'
        list_mocap_transform.append(output_file_path)
        
        ## Ajouter les chemins de sortie au dictionnaire
        dict_path_mocap_transform[sujet] = list_mocap_transform

        ## Lire les données du fichier .TRC
        header, data = fct.read_trc(path_mocap_trc)
        
        ## Appliquer la rotation
        rotated_data = fct.rotate_data(data, Rop)
        
        ## Écrire les données modifiées dans un nouveau fichier .trc
        fct.write_trc(output_file_path, header, rotated_data)


# =============================================================================
#                               SCALE MODEL
# =============================================================================


#-----[MODIFICATION DU FICHIER SCALE_SETTINGS (.xml) AVEC PACKAGE OPENSIM]-----

# CHOIX : Appliquer la mise à l'échelle
if choice_ScaleModel == "1" :

    # |BOUCLE SUJET|
    for i_sujet in range (nb_sujets):
        masse = list_masse[i_sujet]
        sujet = list_sujet[i_sujet]
        path_calib_transform = list_path_calib_transform[i_sujet]
        
        # Charger le fichier de configuration modifié (.xml) et l'associer à la classe "ScaleTool"
        scale_tool = opensim.ScaleTool('Scaled_Settings_empty.xml') # Setup avec ScaleFactors qui fonctionnent
        
        # Configurer la masse du sujet en kg
        scale_tool.setSubjectMass(masse)
        
        # Associer le modèle à la class "GenericModelMaker" 
        generic_model_maker = scale_tool.getGenericModelMaker()
        
        # Ajouter le fichier modèle qui doit être mis à l'échelle
        generic_model_maker.setModelFileName(model)
        
        
        
        ##----OUTIL {ModelScaler}----##
        
        # Associer le modèle à la class "ModelScaler"
        model_scaler = scale_tool.getModelScaler()
        
        # Appliquer l'otpion ModelScaler
        model_scaler.setApply(choice_MS)
        
        # Configurer le fichier de calibration
        model_scaler.setMarkerFileName(path_calib_transform)
        
        
        # Durée de la calib à l'aide de la fonction "get_trc_duration"
        duration = fct.get_trc_duration(path_calib_transform)
        
        
        # Changer les time range par la durée de la calib
        time_range = opensim.ArrayDouble()
        time_range.append(duration[0])
        time_range.append(duration[1])
        model_scaler.setTimeRange(time_range)
        
        # CHOIX : Préserver la distribution de masse 
        if choice_ModelScaler == "1":

            if choice_preserve_mass == "1":
                model_scaler.setPreserveMassDist(True)
            
            if choice_preserve_mass == "2":
                model_scaler.setPreserveMassDist(False)
        
        
        # Fichier de sortie du modèle mis à l'échelle
        model_scaler.setOutputModelFileName(f"Model_{sujet}.osim")
        
        if choice_ModelScaler == "1":

            if choice_scalefactor == "1":
                model_scaler.setOutputScaleFileName(f"scale_factors_{sujet}.trc") 
        
        
        #----OUTIL {MarkerPlacer}----##
        
        if choice_MarkerPlacer == "1":
            if choice_markerset == "1":    
                generic_model_maker.setMarkerSetFileName(markerset)
        
        
        # Associer le modèle à la class "MarkerPlacer"
        marker_placer = scale_tool.getMarkerPlacer()
        
        # SI NECESSAIRE : Appliquer l'otpion MarkerPlacer
        marker_placer.setApply(choice_MP)
        
        # Configurer la pose statique selon le fichier .trc de calibration (calib statique initiale)
        #marker_placer.setStaticPoseFileName(path_calib_transform)
        
        # Configurer la pose statique (orienté analyse mvt dynamique plutôt)
        marker_placer.setMarkerFileName(path_calib_transform)
        
        # Durée de la calib à l'aide de la fonction "get_trc_duration"
        duration = fct.get_trc_duration(path_calib_transform)   
        
        # Changer les time range par la durée de la calib
        time_range = opensim.ArrayDouble()
        time_range.append(duration[0])
        time_range.append(duration[1])
        marker_placer.setTimeRange(time_range)
        
        # Fichier de sortie du modèle mis à l'échelle
        marker_placer.setOutputModelFileName(f"Model_{sujet}.osim")
        
        # SI NECESSAIRE : Fichier de sortie du MarkerSet de la calibration 
        if choice_MarkerPlacer =='1' :

            if choice_markerset_calib == "1":
                marker_placer.setOutputMarkerFileName(f"MarkerSet_calib_{sujet}.xml")
        
        # =============================================================================
        #     # SI NECESSAIRE : Fichier de sortie de ??
        #     check_motion_filname = input("Souhaitez-vous un fichier (.mot) du réajustement de la mocap :\n1 - Oui\n2 - Non\n")
        #     print()
        #     
        #     if check_motion_filname == "1":
        #         marker_placer.setOutputMotionFileName("Motion_filname.mot")
        # =============================================================================
        
        print (f"GENERATION DU MODELE [{sujet}]")
        print()
        
        # Enregistrer le fichier XML modifié
        success = scale_tool.printToXML(f'Scaled_Settings_modified_{sujet}.xml')
        if success :
            print (f"-> Fichier <Scaled_Settings_modified_{sujet}.xml> sauvegardé.")
            if choice_ModelScaler == "1" and choice_scalefactor == "1":
                print(f'Fichier <scale_factors_{sujet}.trc> sauvegardé.')  
                
            if choice_MarkerPlacer == "1" and choice_markerset_calib == "1":
                print(f'-> Fichier <MarkerSet_calib_{sujet}.xml> sauvegardé.')
        print()
                
        
        
        #--------------------[GENERATION DU MODELE MIS A L'ECHELLE]--------------------
        
        # Exécuter le processus de mise à l'échelle
        success = scale_tool.run() 
        if success:
            print(f"La mise à l'échelle du modèle {sujet} a réussi avec ajustement du modèle aux marqueurs")
            print()
        else:
            print(f"La mise à l'échelle du modèle {sujet} a réussi mais n'a pas été ajusté aux marqueurs") # même si échoué le model_scale a été créé (juste comme le modèle est non ajusté aux marqueurs -> success = False) (A VERIFIER)
        

# =============================================================================
#                             CINEMATIQUE INVERSE (IK)
# =============================================================================

# CHOIX : Appliquer la cinématique inverse
if choice_IK == "1":


    # |BOUCLE SUJET|
    for i_sujet in range (nb_sujets):
        sujet = list_sujet[i_sujet]
        
       # list_path_IKResults = [] # -> à supprimer
        
        print()
        print(f'PROCESSUS DE CINEMATIQUE INVERSE [{sujet}]')
        print()
        
        # Charger le modèle mis à l'échelle
        scaled_model = opensim.Model(f"Model_{sujet}.osim") 
        
        # Création de l'outil de cinématique inverse
        ik_tool = opensim.InverseKinematicsTool('IK_Settings_empty.xml')
        
        # Paramétrer le modèle sur lequel est appliqué IK
        ik_tool.setModel(scaled_model)
    
    
    #------[MODIFICATION DU FICHIER IK_SETTINGS (.xml) AVEC PACKAGE OPENSIM]-------
    
    
        # |BOUCLE MOCAP|
        for i_mocap in range(list_nb_mocap[i_sujet]) :
            path_mocap = dict_path_mocap_transform[sujet][i_mocap]
            name_mocap = dict_mocap_transform [sujet][i_mocap][:-4] # [:-4] pour supprimer le .trc
    
# =============================================================================
#             print()
#             print(f'PROCESSUS DE CINEMATIQUE INVERSE [{sujet}]')
#             print()
# =============================================================================
            
            ## Ajouter le fichier TRC de la mocap
            ik_tool.setMarkerDataFileName(path_mocap)
        
            ## Durée de la mocap
            duration = fct.get_trc_duration(path_mocap)
        
            ## Spécifier le début et la fin de l'analyse
            ik_tool.setStartTime(duration[0])  # Début de l'analyse (en secondes)
            ik_tool.setEndTime(duration[1])  # Fin de l'analyse (en secondes)
        
            ## Chemin du fichier MOT de sortie 
            ik_tool.setOutputMotionFileName(f"outputs/{sujet}/IK_Results_{sujet}_{name_mocap}.mot")
            IKResults_filname = ik_tool.getOutputMotionFileName()
            
            # Ajout des chemins IKResults de sortie dans la liste (utilité ?)
            #list_path_IKResults.append (IKResults_filname) --> supprimer 
            
            #dict_path_IKResults [sujet] = list_path_IKResults  --> supprimer
    
            
            
    #---------------------------[GENERATION DES IK_RESULTS.MOT]--------------------
    
            ## Exécuter le processus de cinématique inverse
            success = ik_tool.run()
            if success:
                print(f"-> Fichier <IK_Results_{sujet}_{name_mocap}> enregistré dans <outputs/{sujet}>")        
            else:
                print("La cinématique inverse de <IK_Results_{sujet}_{name_mocap}> a échoué") 
        
            ## Enregsitrer le fichier XML modifié
            ik_tool.printToXML(f'IK_Settings_modified_{sujet}.xml')
            if  name_mocap ==  dict_mocap_transform [sujet][-1][:-4] :
                print (f"-> Fichier <IK_Settings_modified_{sujet}.xml> sauvegardé.")
         
        


# =============================================================================
#                               DYNAMIQUE INVERSE (ID)
# =============================================================================

# CHOIX : Appliquer la cinématique inverse
if choice_ID == "1":

    # |BOUCLE SUJET|
    for i_sujet in range (nb_sujets):
        sujet = list_sujet[i_sujet]
        masse = list_masse[i_sujet]

        
        print()
        print(f'PROCESSUS DYNAMIQUE INVERSE [{sujet}]')
        print()
    
        # Charger le modèle mis à l'échelle
        scaled_model = opensim.Model(f"Model_{sujet}.osim")
    
        # Création de l'outil de dynamique inverse
        id_tool = opensim.InverseDynamicsTool('ID_Settings_empty.xml')
        
        ## Liste de tous les fichiers dans le répertoire
        fichier_IKResults = os.listdir(f'outputs/{sujet}')

        ## Filtrer pour ne garder que les fichiers avec l'extension .mot
        list_IKResults = [f for f in fichier_IKResults if f.endswith('.mot')]
        
        ## Listes des chemins vers les fichiers IKResults
        list_path_IKResults =[]
        
        for IKResult in list_IKResults :
            list_path_IKResults.append(os.path.join(f'outputs\\{sujet}', IKResult))
    
    
    #------[MODIFICATION DU FICHIER IK_SETTINGS (.xml) AVEC PACKAGE OPENSIM]-------
    
        # Paramétrer le modèle sur lequel est appliqué ID
        id_tool.setModel(scaled_model)    
        
        # Paramétrer le chemin du modèle mis à l'échelle dans le settings.xml (ne marche pas sans la fonction SetModel())
        id_tool.setModelFileName(f"Model_{sujet}.osim") 
        
        # Dossier de sortie 
        id_tool.set_results_directory (f'outputs/{sujet}') 
        
    
        # |BOUCLE MOCAP|
        for i_mocap in range(list_nb_mocap[i_sujet]) :
            path_c3d = dict_path_mocap_c3d [sujet][i_mocap]
            path_mocap = dict_path_mocap_transform[sujet][i_mocap]
            name_mocap = dict_mocap_transform [sujet][i_mocap][:-4] # [:-4] pour supprimer le .c3d
            
            print(f'Process <{name_mocap}> du [{sujet}]')
        
            ## Ajouter le fichier IKResults 
            # id_tool.setCoordinatesFileName(dict_path_IKResults[sujet][i_mocap])
            id_tool.setCoordinatesFileName(list_path_IKResults[i_mocap])
        
        
            ## Durée de la mocap
            duration = fct.get_trc_duration(path_mocap)
        
            ## Spécifier le début et la fin de l'analyse
            id_tool.setStartTime(duration[0])  # Début de l'analyse (en secondes)
            id_tool.setEndTime(duration[1])  # Fin de l'analyse (en secondes)
            
            ## Filtre de fréquence passe-bas () 
            id_tool.setLowpassCutoffFrequency(6) # PAR DEFAUT
            
            ## Créer le fichier GRF.mot 
            fct.create_mot_grf(path_c3d, q1, q2, q3, f'Data/{sujet}/{name_mocap}_GRF.mot', masse) 
            
            
        #-----------------------[MODIFICATION DU GRF_SETTINGS.XML]-----------------
        
            import xml.etree.ElementTree as ET
        
            # Charger le fichier XML
            tree = ET.parse('GRF_Settings_empty.xml')
            root = tree.getroot()
        
              
            # Mettre à jour le filname d'entrée des 3 composantes des PFFs
            for elem in root.iter('datafile'): 
                elem.text = f'Data/{sujet}/{name_mocap}_GRF.mot'
        
            
            # Elément tout en haut du xml
            root.findall(".") # test
            
            # Elément en dessous
            root.findall("./") # test
            
            # Elément encore en dessous
            root.findall(".//ExternalForce/[@name='externalforce_0']/applied_to_body")
          
            # Mettre à jour l'application de la force de chaque pf sur la partie du corps
            ## pour pff 1
            for body_elem in root.findall(".//ExternalForce/[@name='externalforce1']/applied_to_body"):  
                body_elem.text = body_pff1
                
            ## pour pff 2
            for body_elem in root.findall(".//ExternalForce/[@name='externalforce2']/applied_to_body"):  
                body_elem.text = body_pff2
        
        
            # Mettre à jour le chemin vers les données de Force pour chaque PFF
            ## pour PFF 1
            for body_elem in root.findall(".//ExternalForce/[@name='externalforce1']/data_source_name"):  
                body_elem.text = f'{name_mocap}_GRF.mot'
                
            ## pour PFF 2
            for body_elem in root.findall(".//ExternalForce/[@name='externalforce2']/data_source_name"):  
                body_elem.text = f'{name_mocap}_GRF.mot'
        
            # Sauvegarder les modifications dans un nouveau fichier XML
            tree.write(f'GRF_Settings_modified_{sujet}.xml')
    
            # Paramétrer le fichier GRF_Settings.xml
            id_tool.setExternalLoadsFileName(f'GRF_Settings_modified_{sujet}.xml')
            
            ## Chemin du fichier de sortie ID_Results.sto
            id_tool.setOutputGenForceFileName(f"ID_Results_{sujet}_{name_mocap}.sto")
            
            ## Enregsitrer le fichier XML modifié
            id_tool.printToXML(f'ID_Settings_modified_{sujet}.xml')
            if  path_mocap ==  list_mocap_transform[-1] :
                print (f"-> Fichier <ID_Settings_modified_{sujet}.xml> sauvegardé.")
    
    
    #---------------------------[GENERATION DES ID_RESULTS.STO]--------------------
    
            ## Exécuter le processus de dynamique inverse
            success = id_tool.run()
            if success:
                print(f"-> Fichier <ID_Results_{sujet} {name_mocap}> enregistré dans <outputs/{sujet}>") 
                print()
            else:
                print(f"La dynamique inverse de <ID_Results_{sujet} {name_mocap}> a échoué") 
        
        
            ## Ajout des chemins IKResults de sortie dans la liste
            list_path_IDResults.append (id_tool.getOutputGenForceFileName())
        
            # Ajout dans le dictionnaire des IDResults
            dict_path_IDResults [sujet] = list_path_IDResults[i_sujet]




# =============================================================================
# # A FAIRE :
#   # Problème de l'inversion sur l'axe z, impacte également les MF ?
#   # Ajouter un choix pour éviter d'avoir a lancer le processus de conversion en.trc si on a déjà les fichiers
# =============================================================================
