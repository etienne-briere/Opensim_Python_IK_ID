# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 17:44:25 2024

@author: BRIERE Etienne
"""

     
    # =============================================================================
    # #---------------------[CREATION DU GRF_SETTINGS.XML avec OPENSIM]--------------
    #        
    # 
    #     # Créer un objet ExternalLoads
    #     external_loads  = opensim.ExternalLoads()
    #     print("ExternalLoads object created")
    # 
    #     
    #     # Première force externe (plateforme 1)
    #     external_force1 = opensim.ExternalForce()
    #     external_force1.setName("externalforce1")
    #     external_force1.set_applied_to_body("toes_l")
    #     external_force1.set_force_expressed_in_body("ground")
    #     external_force1.set_point_expressed_in_body("ground")
    #     external_force1.set_data_source_name('Data/'+name_mocap+'_GRF.mot')
    #     external_force1.setForceIdentifier("ground_force_v")
    #     external_force1.setPointIdentifier("ground_force_p")
    #     external_force1.setTorqueIdentifier("ground_torque")
    #     external_force1.appliesForce()
    #     external_force1.appliesTorque()
    #     print("First ExternalForce configured")
    # 
    #     # Ajouter la première force externe à l'objet ExternalLoads
    #     external_loads.adoptAndAppend(external_force1)
    #     print("First ExternalForce added to ExternalLoads")
    #     
    #     
    # 
    #     # Deuxième force externe (plateforme 2)
    #     external_force2 = opensim.ExternalForce()
    #     external_force2.setName("externalforce2")
    #     external_force2.set_applied_to_body("toes_r")
    #     external_force2.set_force_expressed_in_body("ground")
    #     external_force2.set_point_expressed_in_body("ground")
    #     external_force2.set_data_source_name('Data/'+name_mocap+'_GRF.mot')
    #     external_force2.setForceIdentifier("1_ground_force_v")
    #     external_force2.setPointIdentifier("1_ground_force_p")
    #     external_force2.setTorqueIdentifier("1_ground_torque")
    #     external_force2.appliesForce()
    #     external_force2.appliesTorque()
    #     print("Second ExternalForce configured")
    #  
    #     # Ajouter la deuxième force externe à l'objet ExternalLoads
    #     external_loads.adoptAndAppend(external_force2)
    #     print("Second ExternalForce added to ExternalLoads")
    #     
    # # =============================================================================
    # #     # Nettoyer (éviter les problèmes de mémoire)
    # #     del external_force1
    # #     del external_force2
    # # =============================================================================
    #     
    #     # Paramétrer le chemin vers les données GRF
    #     external_loads.setDataFileName('Data/'+name_mocap+'_GRF.mot')
    # 
    #     # Sauvegarder l'objet ExternalLoads dans un fichier XML
    #     external_loads.printToXML("GRF_settings.xml")
    #     print("ExternalLoads.xml saved")
    # 
    # =============================================================================
        