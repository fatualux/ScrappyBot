# ScrappyBot


Questo progetto è nato per realizzare un robot basato su Raspberry Pi 4B.

Il ramo [legacy](https://gitlab.com/fatualux/ScrappyBot/-/tree/legacy?ref_type=heads#scrappybot) è il vecchio codice, dedicato alla versione "motorizzata" del robot, mentre il ramo main è dedicato alla versione "statica", con un focus sulle funzionalità di controllo e notifica tramite Bot Telegram.

[![License](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)

### RMBot.py

E' un piccolo Telegram Bot, e dipende da Motion (https://motion-project.github.io). Permette di avviare/fermare il motion detection, catturare istantanee, cancellare tutti i media presenti nel path specificato in motion.conf, controllare i movimenti del robot e la sua velocità, acquisire brevi registrazioni audio/video.

### REyeBot.py

Va inserito nella config di Motion (nel mio caso, on_picture_save /usr/bin/python /path/to/REyebot.py).

Invia all'amministratore del sistema le istantanee e i video acquisiti da Motion, e una breve registrazione audio quando rileva movimento.

Dopo l'invio, cancella tutti i file multimediali.

Motion deve essere correttamente configurato affinché funzioni (target e filename, soglie di attivazione, abilitazione istantanee e video preview).

### tgSend.py

Contiene le funzioni necessarie all'esecuzione degli script precedentemente descritti.

### streamCam.Py

Avvia l'anteprima della PICam e la rende disponibile all'IP locale del Raspberry (porta 8080) nel browser di qualsiasi periferica connessa alla rete locale.
