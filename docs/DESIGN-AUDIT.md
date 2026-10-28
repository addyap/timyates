# Design audit (29 October 2026)

**Verdict.** The hero is distinctive: the dusk scene, the arch, the gold hairline. Below it, the site falls back on a standard template: equal card grids, flat beige page headers, a white header bar, and a contact section that's just a table of details. The identity starts strong and then fades out. The fix isn't more effects. It's carrying the hero's language (dusk navy, sun gold, hairlines, serif) through the rest of the site, and giving each section one clear job.

Ranked by visual impact × ease. ✅ = done in this pass.

## 1. Services are a generic card grid ✅
**What's wrong:** six identical boxes, each ending in "Read more", in a 4 + 2 layout that leaves half the bottom row empty. Every service has the same weight, though two of them (assurance vie and mortgages) are Tim's core work. On a phone it's 1,800px of boxes.
**Change:** an editorial numbered index, like a private bank's list of services. Hairline rows: number, serif title, one-line description, and an arrow. The two core services lead at a larger size. On hover a gold line sweeps under the row, the title shifts slightly, and the arrow fills.
**Why:** it reads as considered rather than templated, shows priority at a glance, and halves the length on a phone.

## 2. Header and buttons break the colour story ✅
**What's wrong:** a flat white bar sits on top of the dark hero, and the most important button is a muddy olive pill. The hero's button is sun gold, so the site has two competing "golds".
**Change:** the header floats transparently over dark openings (the home hero and the page headers) and turns solid once you scroll past them. One button system: sun gold on dark backgrounds, deep navy on light ones. Olive is kept only for small accents (labels, links).
**Why:** the first screen becomes a single composed image, and colour means the same thing everywhere.

## 3. The contact section doesn't ask for anything ✅
**What's wrong:** the moment meant to convert is a label-and-value table with no button, and the "Get in touch" label is olive on navy, which is hard to read.
**Change:** make it a closing scene that echoes the hero: a dusk glow rising from the horizon line, a gold label, and a clear "Book a conversation" button (an email with the subject filled in) plus "or call" with the mobile number. The details list stays, but quieter.
**Why:** every "Book a conversation" button on the site now ends in an action, not just a list.

## 4. Inner pages lose the identity ✅
**What's wrong:** Articles, FAQ and 404 open with a flat beige box and a white header, a different visual world from the home page.
**Change:** the page headers become miniature dusk scenes (navy, low sun glow, a hairline horizon, ivory serif heading), with the header floating over them.
**Why:** every page now feels like the same place.

## 5. Orphans and widows ✅
**What's wrong:** "France" alone on a line in two headings, "pace" alone, "France." alone in the hero. The blog grid has four articles in three columns, so one sits alone.
**Change:** balanced wrapping on headings and better paragraph wrapping (`text-wrap: balance` and `pretty`). The newest article becomes a full-width feature on the Articles page.
**Why:** this kind of ragged detail is what makes a site look unfinished.

## 6. Redundant elements and clutter ✅
- **Hero name card:** says "Tim Yates, founding partner", already in the headline paragraph and the proof strip below. Removed, so the arch reads as a clean frame.
- **Footer contact column:** repeats the contact details sitting directly above it. Removed. The footer becomes brand, links and the legal text.
- **Pill buttons under the articles:** "All articles" and "Questions and answers" as outlined pills. Replaced by one quiet "All articles →" text link.

## 7. About is a CV, not a person ✅
**What's wrong:** the qualifications list has the most visual weight; the human line is buried in paragraph one.
**Change:** pull the line "listen first, explain simply" out as a large serif quote. It's the brand promise in Tim's own voice.

## 8. Not done in this pass (lower impact or needs Tim)
- **Photography:** the only image is one studio headshot, used three times. A relaxed photo of Tim on the coast (Fréjus, the Estérel) would do more for "premium and personal" than any code. This is the biggest remaining gap.
- **Body typeface:** Inter is clean but generic. A more characterful sans would add polish; not worth the risk until the content settles.
- **Article pages:** good reading typography, but a plain template. A dusk header like the other pages, and pull quotes in the text, once Tim has reviewed the content.
- **Section rhythm:** every section has the same 80px padding. Varying it (tighter for lists, more air before About and Contact) would add pace. Partly addressed by the new layouts.
