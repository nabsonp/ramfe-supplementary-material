# Assessment of the MFAD detections: guide for the practitioners

English translation of the guide the practitioners received (in Portuguese). Links to the shared folders and the contact channel are omitted.

1. Download all the MFAD outputs from the shared folder. There is one HTML report per system (`../../../systems/<system>/report.html`); open it in the browser.
2. Open the spreadsheet of detections.
3. Fill in the "About you" tab, the first one of the spreadsheet (`profiles.csv`).
4. Analyze each architecture individually. Each tab after the first is a system, and each row is an MFAD detection. In the judgment column, mark:
   - **Yes** (*Sim*): you agree with the detection;
   - **No** (*Não*): you disagree;
   - **I don't know** (*Não sei*): you do not know whether you agree or not.
5. Do not know the anti-pattern? Click its name in the spreadsheet, or "Reference" in the detection details of the HTML report: it opens the definition in the catalog of micro frontend anti-patterns.
6. **Hammering APIs:** the row gathers all the shared routes of the system (up to 116, in udistrital). Choose at least 5 routes at random, check each one, and answer according to what you find.
7. Justify every No or I don't know answer in the last column.
8. Use the MFAD extraction (the HTML report of the system) as the basis and, if needed, the code of the micro frontends:

| tab | code | where the micro frontends are |
|---|---|---|
| Bahmni | github.com/Bahmni | `*-frontend` repositories |
| Grupo-10-Pos-FIAP | github.com/Grupo-10-Pos-FIAP | `cortex-bank-*` repositories |
| Insta-Graph | github.com/Insta-Graph | `micro-frontend-*` repositories |
| LBHackney-IT | github.com/LBHackney-IT | `mtfh-*` repositories |
| fubaritico | vite-mf-monorepo-tmdb | one repository |
| gematik | github.com/gematik | `DEMIS-portal-*` repositories |
| topcoder-archive | github.com/topcoder-archive | `micro-frontends-*` repositories |
| udistrital | github.com/udistrital | `*_mf` repositories |

The spreadsheet the practitioners received also had a tab for a ninth system, diego-coronado, which was later removed from the study because it was not selected through the organization step of the mining and served to calibrate a threshold of the protocol. Its rows are not part of `answers.csv`.
