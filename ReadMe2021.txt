fDocument de transisiton - Défi bisbille des galaxies (Défi Gentec-EO) - Jeux photoniques - Édition 2021
Dernière modification par Jérémi Lesage le 07-01-22

Matériel:

- Ordinateur avec prise USB-3.0
- Câble d'alimentation de l'ordinateur
- Trousse Gentec-EO avec clé USB et caméra Beamage avec câble USB
- Pointeur laser avec piles de rechange
- VI LabVIEW disponible dans le Google Drive des Jeux photoniques

Protocole:

- Sur le site internet de LabVIEW, télécharger gratuitement « LabVIEW Community » (la version payante de LabVIEW fonctionne aussi)

- Sur le site internet de Gentec-EO, télécharger « Beamage-Installer-V1.02.04.exe » sous l'onglet « BEAMAGE » (la version est peut-être différente)
  (Lien pour le téléchargement: https://www.gentec-eo.com/resources/download-center?DownloadCenterParamViewModel.DocumentTypes=0&DownloadCenterParamViewModel.Lang=en&DownloadCenterParamViewModel.IsUserFromChina=False#page:1)
- Cliquer sur « Installer tout » et suivre la procédure d'installation, puis redémarrer l'ordinateur
- Lancer l'application « PC-Beamage »

# LA PROCHAINE ÉTAPE N'EST PEUT-ÊTRE PAS NÉCESSAIRE SI LE PILOTE EST AUTOMATIQUEMENT INSTALLÉ AVEC L'EXÉCUTABLE BEAMAGE
- Brancher la clé USB fournie par Gentec-EO
- Extraire tout du dossier compressé
- Exécuter le pilote USB qui se trouve dsans « USB Drivers » afin de pouvoir connecter la caméra à l'ordinateur

- Brancher la caméra à l'ordinateur
- Lancer l'application « PC-Beamage » si ce n'est pas déjà fait
- Appuyer sur « Connect » afin de connecter la caméra (bouton rond en haut à gauche)
- Dans la fenêtre du programme, sous l'onglet « Setup », dans « Pixel Addressing » cocher « Decimate 2x2 » et dans « ADC Level » cocher « 10 bit »
- Dans la fenêtre « Advanced », sous l'onglet « Pipeline », cliquer sur « LabVIEW » afin de connecter l'application PC-Beamage à L'application LabVIEW
- Appuyer sur « Start Capture » afin de débuter l'aquisition
- Pointer le laser dans la caméra afin de vérifier que l'aquisition fonctionne (un pic d'intensité devrait apparaître à l'écran)

- Dans le Google Drive des Jeux photoniques, télécharger le dossier compressé « Défi Gentec-EO » et extraire tout
- Ouvrir le fichier « DéfiGentecEO.vi » avec LabVIEW
- Appuyer sur « Run » afin de débuter une partie (en s'assurant de démarrer préalablement l'aquisition sur l'application PC-Beamage)
- Pointer le laser dans la caméra et détruire les vaisseaux
- S'amuser :)
 

------------------------------------------------------------------------------------------------------------------------

Downloader le dossier : https://drive.google.com/drive/folders/1HpwH1RNlUmcR1B5gHtB0RaP4ZLxdS0TR?usp=sharing
et le placer dans src/engine


Ajouter à .vscode :
"env": {
    "PYTHONPATH": "${workspaceFolder}"
}
et exécuter en mode déboggage avec le launch.json

Pour download les packages :
pip install -r requirements.txt
