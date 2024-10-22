# Opensim easy processing with Python
Ce script a été réalisé via l'API d'Opensim dans l'objectif de simplifier le lancement du process des outils de mise à l'échelle du modèle (Scale Model), de cinématique inverse (Inverse Kinematics) et de dynamique inverse (Inverse Dynamics) pour de nombreux essais et sujets (normalement applicables dans l'interface OpenSim). 

## Configuration de votre environnement de script Python 
Le package "opensim" est disponible sous différentes versions de python. Il est conseillé d'utiliser Conda pour créer et utiliser un nouvel environnement. Après ouverture du Powershell Anaconda, utilisez les commandes suivantes pour créer et activer un nouvel environnement Conda. 
```bash
$ conda create -n opensim_scripting python=3.11 numpy
$ conda activate opensim_scripting
```
`opensim_scripting` : nom de votre environnement (modifiable)

**Pour en savoir plus :** https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/pages/53085346/Scripting+in+Python.

## Création des dossiers préalables 
- Créer un dossier avec le nom de votre projet, à l'intérieur dupliquer le dossier `Dossiers_prealables_vides` ce sera plus simple.
- Il doit contenir :
  * Un dossier `Calibrations`
    + comprenant un dossier pour chaque sujet `Sujet_n` avec à l'interieur le .C3D de la calibration réalisée
  * Un dossier `Data`
    + comprenant le(s) dossier(s) `Sujet_n` avec à l'interieur les .C3D des différents essais
  * Un dossier `outputs`
    + comprenant le(s) dossier(s) `Sujet_n` vide(s)
    + dossier regroupant les résultats de la modélisation pour chaque sujet à chaque essai
  * Un dossier `Geometry`
    +  meshs des segments corporels en .VTP qui servent à concevoir le modèle
  * Un dossier `python`
    + Scripts des fonctions (.py) utilisées  par le code principal
      
  * Un fichier `Model.osim` : modèle à mettre à l'échelle
    + dupliquer le fichier `Model.osim` 
  * Des fichiers `_Settings.xml` : paramétrage de chaque outil d’OpenSim
    + `Scale_Settings_empty.xml` : paramètres standards pour la mise à l'échelle 
    + `IK_Settings_empty.xml` : paramètres standards pour la cinématique inverse
    + `ID_Settings_empty.xml` : paramètres standards pour la dynamique inverse
    + `GRF_Settings_empty.xml` : paramètres standards pour l'application des forces externes
   
## Paramètres d'entrée lors du lancement du script
1. Masse(s) sujet(s) en kg
2. Rotation sur x, y, z entre MOCAP et OPENSIM (en degré)
3. Localisation de l'application des forces externes (pied droit/gauche)
4. Choix du paramétrage des différents outils (Scale Model, IK, ID)
 
## Quelques conseils/limites d'utilisation du script
- Choix du paramétrage des outils est le même pour tous les sujets
- Fonctionne seulement si essais comportent 2 plateformes de force
- Fonctionne qu'importe le nombre de sujets
- Fonctionne qu'importe le nombre d'essais/sujet (même si nombre d'essais différent entre sujet)

## Utilisation du script principal 
1. Lancer le script `IK_ID_with_opensim.py` dans le dossier `python`
2. Suivre les paramètres d'entrée indiqués
3. Le traitement peut prendre un certain temps en fonction du nombre de données à traiter
4. En sortie :
   - Nouveau modèle mis à l'échelle .osim
   - Nouveaux fichiers `_settings.xml` en fonction des choix de paramétrage des outils
   - Dans `outputs` : résultats de IK en .mot et de ID en .sto pour chaque sujet
     

   



    
  


   
      
