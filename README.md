# UNSCRIPTED

**Intelligence is not authority.**

A personal AI intent firewall, built for Flipkart APM '29, Prompt 1. By **Arkaprava Ghosh, IIT Madras**.

In 2040, an agent may know what you chose in 2036. That does not give it permission to decide for you today. UNSCRIPTED demonstrates a permission boundary: routine work proceeds inside scoped contracts; consequential actions need present intent; prohibited disclosures block.

## Start in under a minute

**No installation:** download [the prototype ZIP](submission/Arkaprava_Ghosh_IIT_Madras_Prototype.zip), extract it completely, and open `index.html` in a current desktop browser. The prototype uses only HTML, CSS, JavaScript with inline vector drawings. No network, API keys, login or build tools are needed.

For the most predictable browser-local persistence and clipboard behavior, serve the repository using Node 18 or newer:

```sh
node scripts/serve.cjs
```

Open **http://127.0.0.1:4173**. Stop the server with Ctrl+C. `npm start` is an equivalent convenience command. There are no npm dependencies to install.

When opened directly from a file, storage availability depends on browser settings and file origin behavior. The app falls back to an in-memory workspace and exposes JSON export; clipboard failure downloads the passport instead.

## Submission files

| File | Purpose |
| --- | --- |
| [Case PDF](submission/Arkaprava_Ghosh_IIT_Madras.pdf) | Preserved official cover with candidate details, two A4 portrait case pages, one optional reference appendix |
| [Prototype ZIP](submission/Arkaprava_Ghosh_IIT_Madras_Prototype.zip) | Buildless offline prototype; extract and open `index.html` |
| [Recording guide](docs/VIDEO_RECORDING_GUIDE.md) | A 2–3 minute walkthrough with exact clicks and narration |
| [Editable case](docs/CASE_DRAFT.md) | Source text for the two body pages |
| [Research register](docs/REFERENCES.md) | Primary-source links, populations and interpretation limits |
| [QA report](docs/QA.md) | Automated checks and explicit verification limits |
| [Submission checklist](docs/SUBMISSION_CHECKLIST.md) | Packaging, deadline and final candidate checks |

The official brief requires **a PDF plus at least one of a locally runnable HTML/CSS/JS ZIP or a screen recording of actual interactions**. A GitHub URL can hold those files; it is not itself a substitute for them. The supplied documents do not identify a submission portal.

## Try the three decisions

1. **Tokyo:** Enter Decision Room → choose independently → reveal the agent's proposed rejection → request details, explicitly authorize rejection, or defer. Exploring does not accept the job. A stale preference never auto-rejects it.
2. **Finance:** inspect the blocked INR 200,000 proposal → edit the INR 25,000 cap → save → return to Financial Boundary. A cap of INR 200,000 changes the route from BLOCK to REVIEW. Review and explicitly authorize a simulated investment, or decline.
3. **Privacy:** inspect a fictional friend's proposed exposure → reveal sample fields if useful → use a minimized planning request. The original private payload remains blocked; the generic alternative is evaluated separately.

**Decision Passports** exposes the rule IDs, source assumption, exact contract snapshot and authorization. Filter, search, expand, copy or export. **Reset demo** restores the contracts, first-choice flow and 47 seeded routine task records. Those 47 are illustrative history, not measured real-world use. The live queue counts unresolved scenario reviews; choosing “decide later” completes the demo review but leaves the underlying offer unresolved.

## Product decisions

- **Human first:** collect an unanchored first reaction before showing the agent recommendation. It is revisable and not a claim to know someone's “true” preferences.
- **Adaptive friction:** authorized, reversible routine tasks execute without interruption. High stakes and hard-to-reverse actions always need human review, even when an optional confirmation setting is off.
- **Hard privacy boundary:** a user's contract cannot manufacture verified consent for someone else's sensitive data. This prototype does not implement third-party consent collection.
- **One engine:** `engine.js` evaluates intent, authority, privacy and consequence for every scenario. `app.js` owns presentation and persisted workspace state.
- **Inspectability:** plain rule reasons and complete exported snapshots, without presenting editable local records as cryptographic attestations.

## Check and package

```sh
node --check app.js
node --check engine.js
node --test tests/*.test.cjs
```

The test suite uses only Node built-ins. `tests/workspace.test.cjs` exercises the real controller with a small DOM stub; it does not prove browser layout or native browser interaction correctness. See the QA report before recording.

Rebuild the ZIP with Python (standard library only):

```sh
python scripts/package_prototype.py
```

To regenerate the PDF, use Python with `reportlab` and `pypdf`, Windows Arial fonts, and the supplied official template:

```sh
python scripts/build_case.py --template "PATH/TO/Prompt 1 _ Case Submission _ Flipkart APM 2029 (2).pdf"
```

The revised PDF has **1,091 extracted words** across its two main pages, including headings, diagram labels, evidence cards and page furniture. Body paragraphs use **9.25 pt = 12.33 CSS px**. The official original cover and blank body pages are reused; no template is invented. The source template is read locally and not separately redistributed.

## Boundaries of this prototype

All agents, employers, services, actions, times and outcomes are fictional. No investment, job acceptance, rejection, email or private-data transfer occurs. The clock is fixed in October 2040; user-driven passport timestamps advance deterministically. The prototype has no live agent/model integration and no analytics or trackers. External research links open only when selected.

Contracts and passports live in localStorage on this browser/device. They are inspectable and editable, not secure against a user changing their browser data. A real product needs a trusted execution gateway, authenticated time-limited approval, durable audit storage and verified consent infrastructure. It cannot protect actions outside that enforcement boundary.

## Repository privacy

The case PDF and case-generation script contain the candidate's supplied contact details. This public repository includes those details at the candidate’s explicit request. The source FAQ sheet and master prompt are excluded. If reusing the project as a general public showcase, remove candidate details first.
