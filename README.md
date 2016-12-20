## Introducció


## Com funciona

* El programa tres fitxers principals d'entrada: 
  * el fitxer català a traduir (que pot estar parcialment traduït)
  * el fitxer traduït en castellà
  * la memòria de traducció del projecte al qual pertany el fitxer català. Per exemple, la memòria del GIMP si és un fitxer del Git.
* El programa mira cada cadena del fitxer català a traduir i fa el següent procés:
  * Usant la cadena en anglès busca la traducció en castellà d'aquella cadena
  * Si la cadena té etiquetes (com ara <quote>) les reemplaça per MATCH-XX perquè l'Apertium no les tradueixi
  * Si hi ha text entre etiquetes (per exemple, <quote>Editar</quote/> busca la cadena a la memòria i la recupera d'allà (per assegurar consistència terminològica)
  * En l'Apertium per fer la traducció castellà -> català 
* A la traducció en català canviem de forma automàtica algunes coses que traduïm diferent de com les fa l'Apertium (grandària -> mida)
* Per últim, el programa mira si hi ha frases que hi ha a la memòria que són part de cadenes que hem traduït diferent i les afegeix com a comentari al PO perquè ho tinguem en compte al revisar.
* Finalment podem usar el cleanup.py per netejar els fuzzy no traduïts i els comentaris afegits per l'eina

L'objectiu és que llavors cal editar i revisar el fitxer català final. 

En les proves fetes es va entre 6 i 8 vegades més ràpid editant la traducció així que no fent-la des de zero de l'anglès. 

## Contacte

Contacte: Jordi Mas <jmas@softcatala.org>
