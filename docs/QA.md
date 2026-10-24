# Verification report

Checked 24 October 2026. This report distinguishes automated controller/policy verification from native browser validation.

## Passed

- `node --check app.js` and `node --check engine.js`: syntax valid.
- `node --test tests/*.test.cjs`: **26/26 passed** (16 policy-engine tests, 10 controller/render-state tests).
- All seven views render in the controller harness without uncaught errors or undefined output.
- Tokyo recommendation is not rendered before a first choice; explore never accepts the job; explicit rejection, request-details and deferral branches produce distinct passport records.
- Current, exact action authorization is required for rejection; missing, stale or wrong-action approval fails.
- INR 200,000 blocks at INR 25,000. Editing to INR 200,000 changes BLOCK to REVIEW, then requires explicit approval. Confirmation-off cannot override consequential review. Approval cannot bypass an expired contract, bad recipient or cap violation.
- Third-party private information blocks; adding a fabricated consent field does not bypass the rule. The minimized request has a distinct payload and evaluation.
- Contracts, preference freshness, allowed recipients, enabled status and cap affect routing.
- Low-risk permitted routine action executes without interruption. Optional confirmation and lower limits can hold it.
- Passport records and contracts survive a simulated reload of the controller using the same stored data. Reset restores 47 seeded routines and the hidden first-stage recommendation.
- User text is escaped before HTML insertion. Corrupt persisted data falls back with a visible notice.
- No application fetch/API call, external fonts, trackers, model keys or runtime dependencies. Research links require an intentional click.
- ZIP integrity and byte comparison against the source assets pass. ZIP implementation contains only HTML, CSS and JavaScript. Favicon and diagrams are inline SVG markup inside HTML/JS.
- PDF has four A4 portrait pages: preserved official cover, exactly two body pages, one optional appendix. The revised case has **1,091 extracted words on the two main pages**, including headings, cards, diagrams, headers and footers; this is below 1,200.
- Body paragraphs use 9.25 pt (12.33 CSS px); other prose and annotations range from 10 to 12.93 CSS px. Cover and original corner branding were preserved from the supplied template. All four final PDF pages were rendered to PNG and visually inspected; a paragraph-heading parsing issue was repaired before the final render.

## Verification limits / candidate checks still required

- The authoring app's browser security policy blocked access to the local preview. Native browser interaction, screenshots, 375/768/1440 px layout, actual horizontal overflow, computed contrast, tab navigation and reduced-motion rendering remain **unverified**. CSS includes responsive breakpoints, focus styling, semantic forms and reduced-motion rules; these are implementation provisions, not passed browser checks.
- The controller harness uses a small DOM stub. It cannot prove browser-native form validation, modal focus behavior, real localStorage persistence, clipboard/download behavior or file-origin compatibility. Manually smoke-test the extracted ZIP before submission.
- No candidate walkthrough video was recorded. The supplied recording guide is a script, not a video.
- No participant study was conducted, no market demand was validated and no measured improvement is claimed.
- The GitHub integration could read the new repository but returned a permission error for writes. Publication uses the signed-in GitHub upload UI; repository file presence must be verified after the final commit.

## Short manual smoke test

1. Extract the ZIP into a fresh folder; open `index.html`. Check all navigation links.
2. Complete Tokyo with Explore → Reveal → Request details. Open the passport, copy/export and replay. Try rejection and deferral once.
3. Open finance, confirm the cap block, edit the financial cap to 200000, return, review and authorize the simulation.
4. Open privacy, reveal the dummy fields, use the minimized alternative, and inspect both new history records.
5. Refresh. Check contracts and history persist, then reset.
6. Test at 375, 768 and 1440 px. Check no page-level horizontal scrollbar, readable controls, keyboard focus and no obscured buttons. At narrow sizes the navigation intentionally scrolls horizontally within its own row.
7. Change expiry to 23 Oct 2040, remove a recipient, and pause a contract. Each should block its scenario. Restore defaults before recording.


## PDF editorial revision

The revised four-page document was rendered and every page visually inspected. Horizontal text bounds and vertical paragraph bounds passed. The original cover text and candidate details match the previous PDF exactly. The prototype and all application assets remain byte-for-byte unchanged. The revised case adds an editorial identity, distinct India/USA evidence cards, a Tokyo authority-boundary diagram, color-coded engine outcomes, selective principle emphasis, and a visible clickable prototype URL. All five PDF links (three research sources and two prototype links) were verified in the PDF annotations. No new study, scenario, metric or product outcome was introduced.
