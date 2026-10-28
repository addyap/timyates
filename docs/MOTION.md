# Motion system

**Idea: the tide at dusk.** The site's story is calm: your money settled, your life here unhurried. Motion should feel like the sea at golden hour: things rise and settle, never bounce, never rush. Two recurring motifs come from the hero:

- **Rising.** Content enters upwards, the way the sun rises in the hero and the portrait rises into its arch.
- **The gold hairline.** The horizon line draws across in the hero; the same line draws in front of every section label, across the top of the contact band, and as the progress line in "How it works".

Code: tokens and components in `assets/styles.css` (section "Motion system"), behaviour in `assets/site.js`. Markup hooks are `data-reveal` attributes written by `tools/build.py`.

## Principles

1. **Every movement explains something.** Reveals show reading order. The process line shows progress. Hover shows what's clickable. If an animation explains nothing, cut it.
2. **One focal movement per screen.** Never two things competing.
3. **Enter slowly, leave quickly.** Exits take about 60% of the entrance time.
4. **Once only.** Reveals play the first time something appears, never again on scroll back.
5. **Reading text stays still.** Article bodies and FAQ answers never animate in while being read.
6. **Cheap properties only.** `transform`, `opacity` and `clip-path`. Never animate layout, width, top or shadows on large areas.
7. **Content never depends on motion.** No JavaScript, a failed script, or reduced motion all show the full page.

## Tokens

| Token | Value | Use |
|---|---|---|
| `--ease-settle` | `cubic-bezier(.16, 1, .3, 1)` | Default entrance. Fast start, long soft landing |
| `--ease-soft` | `cubic-bezier(.2, .7, .2, 1)` | Hover, UI that responds to the user |
| `--ease-draw` | `cubic-bezier(.65, 0, .35, 1)` | Lines drawing across |
| `--ease-exit` | `cubic-bezier(.4, 0, 1, 1)` | Things leaving |
| `--dur-press` | `120ms` | Button press |
| `--dur-hover` | `220ms` | Hover, colour, small state changes |
| `--dur-ui` | `340ms` | Menus, FAQ answers, page transitions |
| `--dur-reveal` | `800ms` | Scroll reveals |
| `--dur-title` | `1000ms` | Headline wipes |
| `--dur-scene` | `1400ms` | Hero scene, hairline draws |
| `--stagger` | `70ms` | Gap between items in a group (max 6 items staggered, so a group finishes within ~1.2s) |
| `--rise` | `24px` | Reveal travel distance (12px for small elements) |

## Loading sequences

**Home (hero), total about 1.2s to fully readable:**

| Time | What |
|---|---|
| 0ms | Sky fades in (1.4s), sun rises 70px into place (2s) |
| 100ms | Horizon hairline draws outward from the sun (1.4s, draw) |
| 150ms | Eyebrow rises |
| 200ms | Portrait wipes up into the arch (clip-path, 1.4s) |
| 250 / 400ms | Headline lines slide up out of their masks |
| 600ms | Lead paragraph rises |
| 750ms | Buttons rise |
| 800ms+ | Arch outline, name card and proof strip fade in |

**Inner pages:** the page header reveals at load: eyebrow hairline draws (0ms), heading wipes up (80ms), intro rises (160ms). Under 1s.

**Article pages:** the title doesn't animate, because it morphs from the card the visitor clicked (see page transitions). Only the eyebrow and byline reveal.

## Text reveals

- **Headlines (`h1`, `h2` in a reveal group):** a mask wipe. `clip-path: inset(0 0 100% 0)` to `inset(0)`, together with a rise of 0.35em, over `--dur-title` with `--ease-settle`. It feels like type rising from behind the horizon, without splitting words into spans (screen readers read the heading normally).
- **Body text and labels:** fade and rise `--rise` over `--dur-reveal`.
- **Section labels (eyebrows):** the gold hairline before the label draws from 0 to full width (`scaleX`, `--ease-draw`), then the text fades in.

## Image transitions

- **Hero portrait:** wipes up into the arch (clip-path) while rising 30px.
- **Utility `data-reveal="image"`:** for any future photo. The frame wipes up (`clip-path`) while the image inside settles from `scale(1.08)` to 1 over 1.2s. Use it for at most one image per screen.
- **Logos and avatars:** plain fade. Logos should never perform.

## Parallax

Only in the hero, and only as one layer: the scene drifts at 30% of scroll speed, the sun sinks into the sea at 35%, and the hero copy fades out over the first 75% of the hero's height. No parallax anywhere else: on a financial adviser's site, moving content below the fold reads as gimmick, and it costs battery on phones.

## Scroll-triggered animations

One `IntersectionObserver` (threshold 0.15, bottom margin -8% so things reveal slightly after they enter). Each element is revealed once, then unobserved.

| Hook | Behaviour |
|---|---|
| `data-reveal="up"` | Element fades and rises |
| `data-reveal="head"` | Children reveal in sequence (`--stagger`); eyebrow hairline draws, heading wipes |
| `data-reveal="stagger"` | Children rise one after another (cards, contact rows) |
| `data-reveal="image"` | Image wipe (see above) |
| `data-reveal="band"` | Contact band: gold hairline draws across its top edge, echoing the hero horizon |

`style="--d: 120ms"` on an element adds a delay, used to let a second column follow the first.

## Pinned section: "How it works"

The only pinned moment, because it's the only place where the order matters.

- **Desktop (1024px and wider):** the heading column sticks (`position: sticky; top: 140px`) while the three steps scroll past on the right. This is native sticky positioning, not scroll-jacking: scroll speed is never altered.
- **The progress line:** a vertical 1px track down the steps, with a gold fill that grows (`scaleY`) as you scroll through the list. Its value comes from one rAF-throttled scroll handler.
- **Step markers:** each number's circle fills gold when that step passes 60% of the screen height (`--dur-hover`).
- **Phones:** same vertical list and line, no sticky column.
- **Reduced motion:** the line shows full and every marker is lit.

## Hover states and micro-interactions

| Element | Interaction | Spec |
|---|---|---|
| Buttons | Hover | Lift 2px, shadow deepens, arrow nudges 4px right. `--dur-hover`, `--ease-soft` |
| Buttons | Press | `scale(.98)`, `--dur-press` |
| Cards (services, articles) | Hover | Lift 4px, border turns gold, soft shadow. "Read more" underline draws left to right |
| Nav links | Hover | Gold underline draws from the left (`scaleX`), retracts to the right on leave |
| Contact links (dark band) | Hover | Underline draws, as nav |
| Header | Scroll | After 8px, a hairline shadow appears (`--dur-hover`) so the header separates from the content |
| Mobile menu | Open | Panel fades and drops 12px (`--dur-ui`), links follow 35ms apart. Label swaps Menu/Close |
| FAQ | Open | Plus turns to minus (vertical bar rotates 90° and fades); answer height eases open and shut where the browser supports animating to `auto` (Chrome 131+); elsewhere it opens instantly. The answer text rises 8px |
| Article | Scroll | 2px gold reading-progress bar along the top edge of the window |
| Hero portrait | Pointer | Arch tilts up to 7°, warm light follows the pointer. Fine pointers only, never on touch |
| Focus | Keyboard | Focus rings appear instantly. Never animated, never delayed |

## Transitions between pages

Cross-document View Transitions (`@view-transition { navigation: auto; }`), supported in Chrome, Edge and Safari 18.2+. Other browsers navigate normally.

- **Default:** the old page fades out (180ms, `--ease-exit`); the new page fades in while rising 12px (`--dur-ui`, `--ease-settle`).
- **The header doesn't move:** it has its own `view-transition-name`, so it stays perfectly still across pages.
- **Article cards morph into the article:** each card title and its article heading share a `view-transition-name` (`post-<slug>`), so the title glides and grows into place (`--dur-ui` + 100ms).

## Transitions between sections

Sections alternate warm paper and sand backgrounds, with no animated dividers. Continuity comes from the hairline: each section opens with its label's line drawing, and the contact band opens with a full-width line, the same as the hero horizon.

## Reduced motion

With `prefers-reduced-motion: reduce`:

- All reveals are shown immediately, with no transforms.
- The hero is a still image of the scene: no sun rise, shimmer, tilt or scroll drift.
- Page transitions are off.
- Hover lifts are off; colour changes stay.
- The process line is full and every step is lit.

## No JavaScript

A tiny inline script adds `class="js"` to `<html>` before the stylesheet applies. Every "hidden before reveal" style is scoped to `.js`, so without JavaScript the whole page shows normally. If `IntersectionObserver` is missing, everything is revealed at once.

## Performance budget

- Motion JavaScript under 4 KB, no libraries.
- No layout-triggering properties animated. `will-change` only on the hero scene and the water shimmer.
- Scroll handlers are passive and throttled with `requestAnimationFrame`.
- Observers stop watching elements once revealed.
- Target: 60fps on a mid-range Android phone with 4x CPU slowdown in DevTools.

## Testing checklist

- [ ] Desktop Chrome and Safari, iPhone Safari, Android Chrome.
- [ ] macOS "Reduce motion" on: everything visible, nothing moves.
- [ ] JavaScript disabled: full content visible.
- [ ] Keyboard only: focus visible at every step, menu and FAQ usable.
- [ ] Card-to-article morph in Chrome; plain navigation in Firefox.
- [ ] Performance panel: no long frames while scrolling the home page.
