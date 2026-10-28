# What MFAD supports

MFAD reconstructs the architecture of a micro frontend (MFE) system from its source code, detects seven anti-patterns on the reconstructed model, and renders both as a self-contained HTML report. Every step is static: no step executes the analyzed code, reaches the network, or uses a language model, so the same input always yields the same output.

## Integration technologies

| technology | supported | how MFEs are found |
|---|---|---|
| single-spa | yes | `registerApplication` calls (object and positional forms), single-spa-layout (`<template id="single-spa-layout">`, `microfrontend-layout.html`, `constructRoutes` with an object literal), `APP_BASE_HREF` of single-spa-angular, and the lifecycle exports `bootstrap`/`mount`/`unmount` |
| Module Federation | yes | the federation call in the build configuration: `ModuleFederationPlugin` (webpack, Rspack), `federation` (Vite: `@originjs/vite-plugin-federation`, `@module-federation/vite`), `withModuleFederation` and `NxModuleFederationPlugin` (Nx), `moduleFederationPlugin` |
| OpenMRS 3 (`@openmrs/esm-framework`), Open edX (`@edx/frontend-platform`) | no | their MFEs are registered at runtime through the platform's own manifests; packages built on them are skipped with a warning, and a repository with nothing else is refused instead of reconstructed wrongly |
| qiankun, Garfish, Piral, Luigi, iframes, Web Components, server-side or edge composition | no | no extractor yet; a new technology needs only a new extractor, since the analysis and the report read the model |

## What is extracted

| element | recognized |
|---|---|
| **MFEs and shell** | one node per registered or federated unit, plus the orchestrator as a `shell` node that mounts the others; directory, entrypoint, base routes, and size (files, lines, code lines counted on the syntax tree) |
| **Screens** | React Router v5, v6, and v6.4+ (`<Route>`, data-router objects, `lazy`), @reach/router, and Angular Router (`component`, `loadComponent`, `loadChildren`, relative `path`, redirects excluded); without a router, the root component is the screen; screens record whether the app reaches them |
| **Fragments** | non-lifecycle named exports of a single-spa entrypoint; `exposes` entries of Module Federation |
| **Compositions** | imports of another MFE's fragment, JSX instantiations, single-spa parcels (`<Parcel config>`, `mountRootParcel`, `mountParcel`), static and dynamic (`import("remote/x")`) federated imports; each with the screens where it is rendered |
| **Navigations** | any expression that resolves to a route owned by another MFE (independent of the router API): literals, constants, template strings (`/movie/${id}` → `/movie/{param}`), concatenation, `.replace(":id", …)`; React Router `basename`; targets owned through another MFE's screens |
| **Communications** | `customProps` of single-spa registrations; `CustomEvent`, `BroadcastChannel`, cross-window `postMessage`; shared RxJS subjects; `mitt`, `eventemitter3`, `tiny-emitter`, `pubsub-js`; project-specific mechanisms declared in `.mfad/communication.yml`; shared global state as undirected edges |
| **API calls** | `fetch`, `XMLHttpRequest`, axios, ky, got, superagent, Angular `HttpClient`; URLs built with `new URL(path, base)`; project functions that wrap a client, followed in layers (URL parameter at any position, ternaries, suffixes after the endpoint); the screens and fragments that reach each call |
| **State accesses** | react-redux (including aliases such as `useAppSelector`), zustand, jotai, recoil, mobx, pinia; `localStorage` and `sessionStorage` reads and writes (including `clear()`), keys with runtime segments as `{param}`, and project functions that wrap them |
| **Shared code** | code of a package of the repository that an MFE imports counts for that MFE |
| **Provenance** | `manifest.json` records the schema and tool versions, the extractor, the date, and the commit and dirty state of every repository read |

Imports are resolved through relative paths and `tsconfig`/`jsconfig` `paths` and `baseUrl`. Test code (`*.spec.*`, `*.test.*`, `__tests__`, `__mocks__`, `cypress`, `e2e`) and code with no use are not read.

## Anti-pattern rules

| anti-pattern | condition |
|---|---|
| Cyclic Dependency | elementary cycle in the directed graph of compositions or communications within each screen, ignoring undirected edges |
| Hub-like Dependency | five or more distinct fragments rendered in the same screen |
| One Micro Frontend for All | connected to at least 90% of the other MFEs, in systems with five or more MFEs, excluding the shell and undirected edges |
| Hammering APIs | two or more MFEs call the same path |
| Global State Communication | two or more MFEs access the same state slice |
| Mega Frontend | screens and lines of code at or above Q3 + 1.5·IQR, in systems with at least eight MFEs |
| Nano Frontend | screens plus fragments at most five or at or below Q1 − 1.5·IQR, and lines of code below the median |

Each detection lists the MFEs involved, the source locations, the relationship that produced it, the values that support it, and a link to the catalog definition.

## Report

A single HTML file with no external dependency: one graph per question (overview, composition, navigation, communication, global state, backend, screens), a table for every element and detection with file and line, search, filters, and English and Portuguese texts.

## Not supported yet

| gap | effect |
|---|---|
| Vue Router and `.vue` files | Vue MFEs have no screens |
| Bundler aliases (`resolve.alias`, Vite `alias`) | imports through them are not followed |
| `activeWhen` functions of unknown shape | routes are taken from the literals inside them and flagged `opaque` |
| Navigation targets held in variables or read from runtime data | not resolved; a target read from a list literal in a `.map` is not resolved either |
| Routes declared in a project-specific object and mounted in a loop | screens are missed |
| `baseURL` and environment variables | API paths stay relative, so two services with the same path look the same |
| URLs read from class fields (`this.environment.X`) or from configuration files loaded at runtime | the call is not resolved |
| HTTP clients generated at build time (e.g., from an OpenAPI specification) | their calls are not extracted |
| GraphQL | all operations go to one endpoint, so Hammering APIs does not apply per operation |
| Redux writes (`dispatch`) | not extracted, since the call names the action, not the slice |
| `document.cookie` and properties of `window` | not treated as shared state |
| Events dispatched from scripts inside HTML or EJS templates | not read |
| Module Federation configuration built at runtime, `loadRemote`, remote URLs | not read; only the remote alias is recorded |
| Integrations with no trace in the code (iframes with runtime URLs, reverse-proxy routing, edge or server composition) | cannot be reconstructed statically |
| Coverage report | the output does not list what was left unresolved |
