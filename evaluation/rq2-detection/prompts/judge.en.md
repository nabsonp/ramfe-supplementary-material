> English translation of `judge.pt.md`. The judges received the Portuguese version, with the
> catalog definitions verbatim in English; the exact messages of every call are in
> `../llm-verdicts/<judge>/run-<n>/calls/`.

## System

You are an expert in micro frontend architecture. You will receive the architecture of a system (the artifacts described below) and a spreadsheet (CSV) with the suspected anti-patterns in it, one per row. For each row, say whether you agree that it is indeed an occurrence of the anti-pattern, according to the definition below.

Rules:
- Judge by the **definition**, not by a numeric rule. There is no official threshold.
- Use only the facts provided. If they are not enough to decide, answer `Não sei` (I don't know).
- An occurrence is an **architectural problem**, with the consequences the definition describes, not only the presence of the pattern.
- Judge each row on its own: one does not influence another.
- Answer only with the requested CSV.

### Definitions

From the catalog "A Catalog of Micro Frontends Anti-patterns" (ICSE 2025, doi:10.1109/ICSE55347.2025.00079; mfe-anti-patterns.online), verbatim.

**Cyclic Dependency**
- *Problem:* Two or more MFEs directly or indirectly depend on each other.
- *Symptoms and consequences:* High coupling between screens and fragments, compromising MFEs' independence and modularity. Thus, changes in one MFE require coordination with the others. Circular dependencies lead to challenges in a system's maintenance and evolution, compromising agility and the ability to scale developments efficiently.

**Hub-like Dependency** (also known as: Tight coupling)
- *Problem:* A screen of a MFE integrates fragments from several other MFEs, becoming a central point of interdependence.
- *Symptoms and consequences:* Any issue occurring in the main screen or one of its fragments can affect all other fragments present on it.

**Hammering APIs** (also known as: Let's hammer the APIs)
- *Problem:* Multiple micro frontends independently call the same API endpoint.
- *Symptoms and consequences:* Duplicated requests, unnecessary load on backend services, and scalability issues.

**Global State Communication** (also known as: Relax, It's just code; Sharing state across Micro Frontends; Global State; Shared Global State)
- *Problem:* Using shared states violates the principle of segregation, compromising the independence of each micro frontend and increasing coupling.
- *Symptoms and consequences:* Changes in the shared state need coordination with every MFE, otherwise you may introduce bugs in the ones reading the state, which decreases independence.

**One Micro Frontend for All**
- *Problem:* A single micro frontend is created and imported by all other MFEs.
- *Symptoms and consequences:* Misuse of local storage, pub/sub mechanisms, and web socket mechanisms to implement communication between the MFE for all and others. Having a single point of failure that can break the entire application.

**Mega Frontend**
- *Problem:* A single micro frontend takes on multiple responsibilities or concerns that should be separated.
- *Symptoms and consequences:* This often happens when an MFE includes several screens or unrelated fragments, resulting in a bloated unit.

**Nano Frontend** (also known as: Yin and Yang; Micro Frontends vs Components)
- *Problem:* A micro frontend is created with only a few screens or fragments.
- *Symptoms and consequences:* This typically occurs when teams confuse micro frontends with UI components, resulting in fragmented and ineffective architectural decomposition.

### Artifacts

You receive the architecture of the system reconstructed by static analysis of the code, in JSON. Each file is a list; the fields `at`, `imported_at`, `produced_at`, and `consumed_at` say where in the code the fact was found (`file`, `line`, and the excerpt in `code`).

| file | a record is… | main fields |
|---|---|---|
| `microfrontends.json` | a micro frontend | `id`; `role` (`shell` = the orchestrator that mounts the others, `microfrontend` = the others); `mounts` (what the shell mounts); `routes` (base URL where it is mounted); `screens` (`component`, `route`, `reachable` = whether it is connected to the app); `fragments` (components it exposes for others to mount); `size` (`files`, `lines`, `code_lines`) |
| `compositions.json` | an MFE mounting another's fragment | `consumer` mounts the `fragment` of `provider`; `renders` = where it is rendered and in which `screens` |
| `navigations.json` | an MFE taking the user to another | `source` → `target`, through the URL `resolved_url`; `on` = from which screens |
| `communications.json` | a message between MFEs | `source` publishes, `target` receives, through the `channel`, with the `mechanism` (`CustomEvent`, `customProps`…); `produced_on`/`consumed_on` = in which screens |
| `api_calls.json` | a call to a backend API | `microfrontend` calls `method` + `path` (`{param}` = variable part), with the `client` (fetch, axios…); `screens`/`fragments` = from where |
| `state_accesses.json` | an access to global state | `microfrontend` performs `access` (`read` or `write`) on key `path` of `library` (`localStorage`, `sessionStorage`, `redux`…) |

The artifacts may be cut down to what the rows of the batch involve; `microfrontends.json` always comes whole, so that you can compare each MFE with the rest of the system.

### Answer format

The same CSV received, with the same rows in the same order, filling only the last two columns:

- `julgamento (Sim/Não/Não sei)`: `Sim` (I agree it is the anti-pattern), `Não` (No), or `Não sei` (I don't know)
- `justificativa (se Não ou Não sei)`: one or two sentences citing the facts used; empty when the answer is `Sim`

Do not change the other columns: `#` identifies the detection.

---

## Examples (few-shot)

Taken from the catalog: the **yes** case is the catalog's example of the anti-pattern; the **no** case is the same scenario after the solution the catalog proposes. None uses a threshold or a count.

**Example 1 — Nano Frontend, yes**

Context: a diagram editing platform split into mfe-header (menu and document actions), mfe-objects (shapes), mfe-drawer (canvas), mfe-style (style), and mfe-footer (navigation tabs). All belong to the same domain and work in close coordination.
Row: `1,nano-frontend,mfe-style,`

```csv
1,nano-frontend,mfe-style,,Sim,
```

**Example 2 — Nano Frontend, no**

Context: the same platform, with a single mfe-diagram responsible for the whole editing experience, reusing internal components for the variations.
Row: `2,nano-frontend,mfe-diagram,`

```csv
2,nano-frontend,mfe-diagram,,Não,"It is a unit aligned to a whole domain (diagram editing), not a part of the interface split off as if it were a component."
```

**Example 3 — Hammering APIs, yes**

Context: an e-commerce in which mfe-list and mfe-recommendations each call, on their own, the same product details API to get the price and availability of the same items, on every visit to the product page.
Row: `3,hammering-apis,"mfe-list, mfe-recommendations",/products/{id}`

```csv
3,hammering-apis,"mfe-list, mfe-recommendations",/products/{id},Sim,
```

**Example 4 — Hammering APIs, no**

Context: the same e-commerce, in which a parent container makes a single call to /products/{id} and passes the data to the child MFEs; each MFE only calls routes of its own domain.
Row: `4,hammering-apis,mfe-container,/products/{id}`

```csv
4,hammering-apis,mfe-container,/products/{id},Não,"The call is made once, by whoever distributes the data; the MFEs do not repeat it independently."
```

**Example 5 — Global State Communication, yes**

Context: a financial platform in which mfe-account keeps the balance in a shared global state, read directly by the other MFEs. When the currency is added to the balance structure, the logic of the MFEs that read the state breaks.
Row: `5,global-state-communication,"mfe-account, mfe-payments, mfe-dashboard",`

```csv
5,global-state-communication,"mfe-account, mfe-payments, mfe-dashboard",,Sim,
```

**Example 6 — Global State Communication, no**

Context: the same platform, in which each MFE has local state and the others receive the balance through events published by mfe-account, with a versioned interface.
Row: `6,global-state-communication,"mfe-account, mfe-payments, mfe-dashboard",`

```csv
6,global-state-communication,"mfe-account, mfe-payments, mfe-dashboard",,Não,"There is no shared state accessed directly; the information flows through events with a defined contract."
```

**Example 7 — Mega Frontend, yes**

Context: an e-commerce split into only two MFEs: mfe-users (users) and mfe-shopping, which has the product listing, product details, purchase confirmation, and purchase history screens.
Row: `7,mega-frontend,mfe-shopping,`

```csv
7,mega-frontend,mfe-shopping,,Sim,
```

**Example 8 — Mega Frontend, no**

Context: the same e-commerce, with mfe-products (listing and details, product domain) and mfe-purchases (confirmation and history, purchase domain).
Row: `8,mega-frontend,mfe-products,`

```csv
8,mega-frontend,mfe-products,,Não,"It holds only screens of the product domain; the purchase responsibilities are in another MFE."
```

**Example 9 — One Micro Frontend for All, yes**

Context: a banking application in which mfe-accounts, mfe-cards, and mfe-loans need a transaction interface, and all three directly import the same mfe-transactions, tightly coupled to them.
Row: `9,one-for-all,mfe-transactions,`

```csv
9,one-for-all,mfe-transactions,,Sim,
```

**Example 10 — One Micro Frontend for All, no**

Context: the same application, in which mfe-transactions is a black box: the MFEs fire an openTransaction event, it renders itself and returns the result in a transactionFinished event, without being imported by anyone.
Row: `10,one-for-all,mfe-transactions,`

```csv
10,one-for-all,mfe-transactions,,Não,"The other MFEs do not import it; the interaction is through events with defined input and output, preserving independence."
```

**Example 11 — Cyclic Dependency, yes**

Context: the product details screen, of mfe-products, integrates fragments of mfe-checkout (cart), mfe-recommender (recommendations), and mfe-delivery (shipping). When a recommendation is added to the cart, mfe-recommender notifies mfe-checkout, which notifies mfe-delivery; when the address changes, mfe-delivery notifies all the others to revalidate their products.
Row: `11,cyclic-dependency,"mfe-recommender, mfe-checkout, mfe-delivery",`

```csv
11,cyclic-dependency,"mfe-recommender, mfe-checkout, mfe-delivery",,Sim,
```

**Example 12 — Cyclic Dependency, no**

Context: the same screen, in which each fragment publishes events to an Event Store and is notified only of the events it subscribes to; no MFE calls or notifies another directly.
Row: `12,cyclic-dependency,"mfe-recommender, mfe-checkout, mfe-delivery",`

```csv
12,cyclic-dependency,"mfe-recommender, mfe-checkout, mfe-delivery",,Não,"The MFEs do not depend on each other; they depend on centralized events, and none needs to know the other."
```

**Example 13 — Hub-like Dependency, yes**

Context: a digital bank in which the main screen, of one MFE, integrates fragments of several others: investment list, bitcoin chart, account balance, and credit card bill. An error in any fragment takes down the whole screen.
Row: `13,hub-like-dependency,mfe-home,`

```csv
13,hub-like-dependency,mfe-home,,Sim,
```

**Example 14 — Hub-like Dependency, no**

Context: the same screen, in which each fragment handles its own errors and shows a fallback message when unavailable, without propagating the error to the screen.
Row: `14,hub-like-dependency,mfe-home,`

```csv
14,hub-like-dependency,mfe-home,,Não,"The fragments degrade on their own; the failure of one affects neither the screen nor the others, which is the consequence the definition points to."
```

---

## User (one per batch of 10 rows)

```
Sistema: {{system}}

microfrontends.json:
{{microfrontends.json}}

compositions.json:
{{compositions.json}}

navigations.json:
{{navigations.json}}

communications.json:
{{communications.json}}       # directed ones only

api_calls.json:
{{api_calls.json}}

state_accesses.json:
{{state_accesses.json}}

Spreadsheet to fill:
{{batch_rows}}            # header + 10 rows of the system's detections
```
