installation:

python3 setup.py install

========================================================

usage: latex2tei.py [-h] -t  -x  -s  [-g]

optional arguments:
  -h, --help  show this help message and exit
  -t          -t <file tex>
  -x          -x <file xml>
  -s          -s <sigla>
  -g          -g [0/1] 0) disable seg 1) enable seg)

========================================================
es.

con seg disabilitato

latex2tei.py -t A_019_testo_lavoro.tex -x A_019_testo_lavoro.xml -s  K -g 0

oppure, utilizzando il valore di default 0 per seg, g può essere omesso

latex2tei.py -t A_019_testo_lavoro.tex -x A_019_testo_lavoro.xml -s  K

con seg abilitato

latex2tei.py -t A_019_testo_lavoro.tex -x A_019_testo_lavoro.xml -s  K -g 1

=========================================================

installazione  e lancio dell'applicazione

1) aapriretermminale

2) scegliere un directory

3) verificare disponibilità pythom3
       dgitare python3 o python
       se si dgita python verificare laversione difigatnod python --version
       deve essere successiva a 3.5

4)  utilizzar quindi il comando python3 o python se quest'ultimomo è alla versione 3.5 o successive

5)  esplodere latex2tei.zip

6)  digitare python3 setup.py install o
      python setup.py inslall ( se python è alla versione 3)
              
7)  Il comando latex2tei.py  è dispèonibile in qualsiasi directory

8) Se non funziona verifcare che la variabile PYTHONPATH sia settataa correttamente
   La dir dove è stato salvato latex2tei.py deve esseere fra le dire  settatte
   in PYTGONPATH
   
9) Se NON funziona controllare la versione windows, controllare PYTHONPATH

ALTENATIVA A  python3 setpup.py install

10) Volendo si puà salvare late2tei.py in una qualsiasi dire ed 
    eseguire i seguenti passi:
    a) entrare (col termnale) nella sir dove si è salvato latex2tei.py
    b) digitare latex2tei.py con le opzioni indicate in README
    
========================================================
NB
i nome dei parametri NON devono avere spazi bianchi
========================================================
    
 es.

K è la sigla scelta per reneder univoci gli id nel mansocritto.
    
latex2tei.py -t A_019_testo_lavoro.tex -x A_019_testo_lavoro.xml -s  K
  
 per una gestione pià ordinata:
 
 dalla dir di lavoroe creare le direectory
 
 makddir tex
 makdir xml
 
 spostare in tex i file latex e digiater per ogni scritto:

latex2tei.py -t tex/A_019_testo_lavoro.tex -x xml/A_019_testo_lavoro.xml -s  K


