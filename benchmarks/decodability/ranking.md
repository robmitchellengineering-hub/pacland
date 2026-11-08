# Decodability deficit — ranking (most decodable first)

`D = 1 - (balanced_accuracy - chance)/(1 - chance)`, `chance = 1/n_classes`.
`D = 0` → the label is decodable to ceiling from the acoustic features; `D = 1` → at chance.

| # | species | label role | n | bal_acc | deficit |
|---|---------|------------|---|---------|---------|
| 1 | Dwarf mongoose (Helogale parvula) | referent (referent) | 144 | 1.000 | 0.000 |
| 2 | American crocodile (Crocodylus acutus) | context (context) | 88 | 0.843 | 0.236 |
| 3 | Prairie dog (Cynomys) | context (context) | 4138 | 0.718 | 0.423 |
| 4 | Macaque (4 species: Tonkean, crested, rhesus, Japanese) | context (context) | 2520 | 0.597 | 0.605 |
| 5 | Gryllus bimaculatus (two-spotted field cricket) | context (context) | 2955 | 0.482 | 0.647 |
| 6 | Manx shearwater (Puffinus puffinus) | context (context) | 508 | 0.651 | 0.698 |
| 7 | Little torrent frog (Amolops torrentis) | context (context) | 35 | 0.429 | 0.714 |
| 8 | Tungara frog (Engystomops pustulosus) | context (context) | 445 | 0.640 | 0.719 |
| 9 | Houbara bustard (Chlamydotis undulata) | context (context) | 478 | 0.502 | 0.747 |
| 10 | Phyllodytes luteolus (tree frog) | context (context) | 39 | 0.614 | 0.771 |
| 11 | Meerkat (Suricata suricatta) | context (context) | 2237 | 0.245 | 0.906 |
| 12 | Loxodonta africana (African savannah elephant) | context (context) | 1918 | 0.114 | 0.959 |
| 13 | Long-clawed shrew (Sorex unguiculatus) | context (context) | 4243 | 0.142 | 0.981 |
| 14 | Dendropsophus minutus (lesser treefrog) | context (context) | 2890 | 0.339 | 0.992 |
| 15 | Loxodonta africana (African savannah elephant) | referent (referent) | 625 | 0.009 | 1.000 |

_Constraint labels (species / dialect / call-type) and sequence corpora are reported in `results.json`, not ranked here as deficits._
