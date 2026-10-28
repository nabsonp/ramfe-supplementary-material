# Omissions pointed out by the LLM judges, verified

The recall prompt (`../prompts/recall.en.md`) gave each judge the reconstructed architecture of a system (the reconstruction of 2026-10-15, `../../reconstruction-2026-10-15/`) and the MFAD detections, and asked for the occurrences missing from the list. An omission counted when it appeared in two of the three runs of a judge. We checked each one in the artifacts and in the source code before counting it as a false negative. The raw calls are in `calls/`.

| omission | judges (of 3) | verification |
|---|---|---|
| Nano Frontend: `micro-frontend-feed` (Insta-Graph) | 2 | **false negative.** One screen and 132 lines of code against a median of 126.5; it is left out only by the strict comparison with the median, while `micro-frontend-user` (121 lines) was detected |
| Cyclic Dependency: `planeacion_pendientes` ↔ `planeacion_seguimiento` (udistrital), through navigation | 3 | design decision: the rule does not count navigations, since going back and forth between screens is part of the product flow |
| Cyclic Dependency through communication between MFEs mounted side by side (udistrital: `core_mf_cliente` ↔ `inscripcion`, `plantillas_root` ↔ `auditoria`) | 1 | design decision: the rule only counts cycles within a screen |
| Cyclic Dependency through `localStorage:token` (Grupo-10-Pos-FIAP) | 1 | already detected as Global State Communication |
| Mega Frontend: `DEMIS-portal-disease` (gematik), `gigs-app` (topcoder-archive), `statement` (Grupo-10-Pos-FIAP), `ipd-frontend` (Bahmni) | 1 to 2 | design decision: the rule abstains in systems with fewer than eight MFEs, and these systems have two to five |
| Mega Frontend: `sga_cliente_inscripcion`, `gestion_contractual` (udistrital) | 1 | design decision: the rule requires both screens and lines of code above the fence, and their screens are not |
| Hub-like Dependency: `host` (fubaritico) | 1 | judge error: each fragment is mounted at a route of its own, not in a single screen |

The only false negative is the Nano Frontend of Insta-Graph, which yields the recall of 99% reported in the paper (137 true positives and one false negative).
