# Grafico pseudo-archimate basato su cerchi concentrici
Serve implementare una nuova vista olistica dei diagrammi archimate, da pubblicare in Github Pages.

## premessa: modularizzazione dei dati di diagramma
- serve un refactoring delle pagine html contenute in /docs: ora i contenuti dei diagrammi archimate sono embedded nelle pagine stesse. Dato che si vuole riutilizzare gli stessi contenuti per la vista olistica, bisogna estrarre i dati dei diagrammi nelle pagine e spostarli in file esterni alle pagine; le pagine dovranno perciò attingere agli stessi dati per mostrare la rispettiva vista in archimate. Dal punto di vista di un utilizzatore esterno non devono notarsi cambiamenti.

## Vista concentrica olistica
- implementare una nuova pagina che mostri tutti i dati dei diagrammi archimate
- i layer archimate verranno mostrati come cerchi concentrici. Il cerchio più interno deve essere il Motivation Layer, il più esterno il Technology Layer. Il cerchio del Technology Layer ha una parte più interna e una parte più esterna: la parte più esterna deve contenere solamente "Technology Device"
- all'interno dei cerchi ci devono essere le rispettive box contenenti i caption (dovranno avere un caption di poche parole per risparmiare spazio - il mouseover mostrerà la caption completa)
- l'intero diagramma con le relazioni fra gli elementi deve essere un force directed graph, con i vincoli stretti che ogni elemento deve restare nella propria sezione di cerchio.
- clickando sopra un qualsiasi elemento: vengono evidenziati tutti gli elementi correlati direttamente ed indirettamente e vengono sbiaditi tutti gli altri
- l'intero diagramma deve essere zoomabile, prestando attenzione a nascondere le scritte se non sono più visibili o se si confondono per troppa sovrapposizione

------------------------------------------------

# Revisione 01
- le caption dei nodi nel grafo olistico sono troppo lunghe. Trova il modo di tenere una forma breve (es. rimuovi le parti di testo che sono fra parentesi. Inoltre, puoi andare a capo tra una parola e la successiva se il numero dei caratteri delle 2 parole supera i 10 caratteri).
- il mouseover funziona finché non si clicka sopra ad un elemento, poi non funziona più: correggere
- l'evidenziazione dei nodi indirettamente collegati al nodo selezionato deve essere ridimensionata; devi evidenziare solo:
  - il path che porta verso il layer Motivation e i nodi che sono compresi in questo path (percorso unico)
  - l'eventuale path che porta verso i technology device, comprendendo tutti i path ramificati (percorso ad albero)