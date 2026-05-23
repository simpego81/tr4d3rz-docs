# Holistic view

## mouse over
- ~~ho notato che alcuni path non vengono evidenziati ad es. nel technology device "Android powerful". Occorre clickare sopra il nodo per visualizzare il path, mentre in altri nodi basta solo passarci sopra col mouse~~
- **✅ FIXED (2026-05-17)**: Aggiunto `pointer-events: none` al testo così gli eventi del mouse passano attraverso le caption e raggiungono il circle sottostante. Ora l'hover funziona su tutti i nodi.

## caption
- ~~le caption sono tornate ad essere troppo lunghe e quindi fanno confusione grafica in quanto si sovrappongono le scritte~~
- **✅ FIXED (2026-05-17)**: Implementate abbreviazioni aggressive + limite 2 parole + soglia 10 caratteri. La maggior parte delle caption ora sta su una sola linea. Esempi:
  - "Application Component" → "App Comp"
  - "Evolution Service" → "Evo Svc"
  - "Niche Discovery" → "Niche Disc"
  
**Vedi**: `holistic_view_feedback_fixes.md` per dettagli completi delle fix.