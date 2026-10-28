# Manual decisions on the 31 candidate organizations

Step 5 of the mining: the first author read each candidate organization and decided whether it holds an MFE system with two or more MFEs (IC2/EC1). `guess` is the first reading of the organization; `included` is the final decision. The full record is in `results/organizations.csv`.

| organization | first reading | included | MFEs | integration | note |
|---|---|---|---|---|---|
| openedx | product | YES | 21 | none (route-level) | The same organization analyzed by a previous study (MIAPI). |
| gematik | product | YES | 7 | single-spa |  |
| openmrs | product | YES | 49 | single-spa |  |
| openedx-unsupported | product | YES | 9 | none (route-level) | From the Open edX organization (MIAPI), but a set of archived repositories. |
| edx | product | YES | 28 | none (route-level) | From the Open edX organization (MIAPI). |
| mandi-tech | POC | NO | 3 | — | Undergraduate project of two students. |
| pagopa | product | YES | 3 | module-federation | Also includes https://github.com/pagopa/selfcare-dashboard-frontend. |
| topcoder-archive | product | YES | 5 | single-spa |  |
| udistrital | product | YES | 63 | single-spa |  |
| Bahmni | product | YES | 10 | mixed: in-house loader + module-federation |  |
| Insta-Graph | product | YES | 5 | single-spa |  |
| LBHackney-IT | product | YES | 5 | single-spa |  |
| Tinkoff | framework | NO | - | — | microzord is an MFE framework they built. |
| aclue-de | POC | NO | 2 | — | Both repositories are described as the demo of a workshop: https://github.com/aclue-de/FrontendWorkshop. |
| fubaritico | product | YES | 5 | module-federation | The five MFEs are in one monorepo: https://github.com/fubaritico/vite-mf-monorepo-tmdb. |
| inab | product | NO | ? | — | States that OEB is an MFE system, but its repositories follow no naming pattern, so its MFEs could not be identified. |
| sihsalus | product | YES | 67 | single-spa | Monorepo: https://github.com/sihsalus/sihsalus-frontend/tree/main/packages/apps. |
| Grupo-10-Pos-FIAP | product | YES | 6 | single-spa | An academic project, but deployed in production for an existing bank, so it was considered a real system. |
| FIAP-Grupo-30 | POC | NO | — | — |  |
| micro-frontends-demo | examples | NO | — | — |  |
| piral-samples | examples | NO | — | — | Several MFE implementations, all of them examples. |
| react-microfrontends | examples | NO | — | — |  |
| smapiot | tool | NO | — | — | micro-frontends-state2023: website of the State of Micro Frontends 2023 survey. |
| collagejs | tool | NO | — | — |  |
| WJSoftware | tool | NO | — | — |  |
| nonblocking | tool | NO | — | — |  |
| Open-Microfrontends | tool | NO | — | — | A standard to document MFEs: https://open-microfrontends.org/getting-started/. |
| luigi-project | tool | NO | — | — | luigi is an MFE framework, and samples holds examples of its use. |
| micro-lc | tool | NO | — | — | micro-lc is a lightweight micro-frontend orchestrator. |
| namecheap | tool | NO | — | — |  |
| openmfp | tool | NO | — | — |  |
