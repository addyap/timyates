# Tim Yates

Personal site for Tim Yates, financial adviser on the Côte d'Azur (The Spectrum IFA Group).

Live at https://timyates.vercel.app (Vercel deploys every push to main).

Plain HTML and CSS, no framework.

- Text for articles and FAQ: `tools/content.py`
- Page template, home page and footer: `tools/build.py`
- Rebuild after any change: `python3 tools/build.py`. This includes any change in `assets/`: the build stamps every asset link with `?v=<hash>`, and `vercel.json` lets browsers cache those for a year, so an edited file that isn't rebuilt never reaches returning visitors.
- Preview: `python3 -m http.server 4321`, then open http://localhost:4321

Open questions before launch: `docs/CHECK-WITH-TIM.md`.
