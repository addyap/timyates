#!/usr/bin/env python3
"""Builds the static site. Run from anywhere: python3 tools/build.py

Text for the blog and FAQ lives in tools/content.py. Shared header, footer
and page shell live here. Output is written to the repo root.
"""
import functools
import hashlib
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from content import POSTS, FAQ  # noqa: E402

# The live address. Change it when a custom domain is added; canonical links, share previews and the sitemap use it.
SITE = "https://timyates.vercel.app"

PHONE_OFFICE = "+33 (0)4 93 00 01 13"
PHONE_OFFICE_TEL = "+33493000113"
PHONE_MOBILE = "+33 (0)6 15 33 60 83"
PHONE_MOBILE_TEL = "+33615336083"
EMAIL = "tim.yates@spectrum-ifa.com"

NAV = [("/", "Home"), ("/#services", "How I help"), ("/#about", "About"), ("/blog/", "Articles"), ("/faq/", "FAQ")]


def esc(s):
    return html.escape(s, quote=True)


# Every /assets/ link carries ?v=<content hash>, so vercel.json can let browsers keep them for a year;
# a changed file gets a new hash and is fetched fresh.
ASSET_REF = re.compile(r'(?<=["( ])/assets/([\w.\-/]+?)(?:\?v=[0-9a-f]+)?(?=[") ])')


@functools.cache
def asset_hash(name):
    return hashlib.sha1((ROOT / "assets" / name).read_bytes()).hexdigest()[:8]


def version_assets(text):
    return ASSET_REF.sub(lambda m: f"/assets/{m.group(1)}?v={asset_hash(m.group(1))}", text)


def version_stylesheet():
    """Stamps the image links inside styles.css; run before anything hashes styles.css."""
    css = ROOT / "assets" / "styles.css"
    css.write_text(version_assets(css.read_text(encoding="utf-8")), encoding="utf-8")


def header(current):
    links = []
    for i, (href, label) in enumerate(NAV):
        cur = ' aria-current="page"' if href == current else ""
        links.append(f'<a href="{href}"{cur} style="--i:{i}">{label}</a>')
    links.append(f'<a class="btn" href="/#contact" style="--i:{len(NAV)}">Get in touch</a>')
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Tim Yates, home">
      <img src="/assets/tim-avatar.jpg" alt="" width="40" height="40">
      <div><strong>Tim Yates</strong><span>Financial adviser · Côte d'Azur</span></div>
    </a>
    <button class="menu-toggle" aria-expanded="false" aria-controls="nav" aria-label="Open menu"><span class="burger" aria-hidden="true"><span></span></span></button>
    <nav class="nav" id="nav" aria-label="Main">
      {' '.join(links)}
    </nav>
  </div>
</header>"""


FOOTER = f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <h3>Tim Yates</h3>
        <p>Founding partner of The Spectrum IFA Group. Helping English-speaking people in the south of France with investments, mortgages and tax-efficient planning.</p>
      </div>
      <div>
        <h3>Explore</h3>
        <ul>
          <li><a href="/blog/">Articles</a></li>
          <li><a href="/faq/">Questions and answers</a></li>
          <li><a href="https://spectrum-ifa.com/" rel="noopener">The Spectrum IFA Group</a></li>
        </ul>
        <a class="footer-mark" href="https://spectrum-ifa.com/" rel="noopener"><img src="/assets/spectrum-mark.png" alt="" width="34" height="34" loading="lazy"><span>Part of The Spectrum IFA Group</span></a>
      </div>
    </div>
    <div class="legal">
      <p>Tim Yates advises through TSG Insurance Services S.A.R.L., part of The Spectrum IFA Group. Office: Mediathel, 120 Route des Macarons, 06560 Valbonne, France.</p>
      <p>TSG Insurance Services S.A.R.L. is registered in Paris (RCS Paris B 447 609 108) as a <i lang="fr">société de courtage d'assurances</i>, ORIAS registration 07 025 332 (<a href="https://www.orias.fr/" rel="noopener">www.orias.fr</a>), and as a <i lang="fr">conseiller en investissements financiers</i> (CIF), reference E002440, member of ANACOFI-CIF, an association approved by the Autorité des Marchés Financiers (AMF).</p>
      <p>The articles and answers on this site are general information, not personal advice. Tax rules and rates change, and what suits one person may not suit another. Please get advice on your own situation before acting. The value of investments can fall as well as rise.</p>
      <p>© 2026 Tim Yates</p>
    </div>
  </div>
</footer>
<script src="/assets/site.js" defer></script>"""


def page(path, title, description, body, current, extra_head="", body_class=""):
    canonical = f'<link rel="canonical" href="{SITE}{path}">' if SITE else ""
    og_url = f'<meta property="og:url" content="{SITE}{path}">' if SITE else ""
    # The hero photo is a CSS background, so preload it or it waits for the stylesheet;
    # normal priority, so it never holds up the stylesheet itself
    preload = ('<link rel="preload" as="image" href="/assets/tim-cutout.webp" imagesrcset="/assets/tim-cutout-sm.webp 600w, /assets/tim-cutout.webp 1040w" imagesizes="(min-width: 901px) 520px, 300px" type="image/webp" fetchpriority="high">\n'
               '<link rel="preload" as="image" href="/assets/riviera.webp" type="image/webp" media="(min-width: 901px)">\n'
               '<link rel="preload" as="image" href="/assets/riviera-sm.webp" type="image/webp" media="(max-width: 900px)">') if path == "/" else ""
    out = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
{canonical}
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
{og_url}
<meta property="og:image" content="{SITE}/assets/tim-yates.jpg">
<meta name="theme-color" content="#0c2a3c">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.jpg">
<script>document.documentElement.classList.add("js")</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500&family=Inter:wght@400;600&display=swap" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500&family=Inter:wght@400;600&display=swap"></noscript>
<link rel="stylesheet" href="/assets/styles.css">
{preload}
{extra_head}
</head>
<body class="{body_class}">
{header(current)}
<main id="main">
{body}
</main>
{FOOTER}
</body>
</html>
"""
    out = version_assets("\n".join(line for line in out.split("\n") if line.strip() != ""))
    target = ROOT / path.lstrip("/")
    if path.endswith("/"):
        target = target / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out, encoding="utf-8")
    return path


def jsonld(data):
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def contact_band():
    return f"""<section class="contact-band" id="contact" data-reveal="band">
  <div class="wrap contact-grid">
    <div data-reveal="head">
      <p class="eyebrow">Get in touch</p>
      <h2>Let's have a conversation</h2>
      <p>Tell me a little about where you are now and what you'd like to sort out: a property purchase, savings you're not sure what to do with, or a move to France. I'll tell you honestly whether I can help, and if I can't, who can.</p>
      <p>I meet clients at the office in Valbonne, around the Var and Alpes-Maritimes, or by video call wherever you are.</p>
      <div class="band-cta">
        <a class="btn btn-sun" href="mailto:{EMAIL}?subject=A%20first%20conversation">Book a conversation <span aria-hidden="true">→</span></a>
        <a class="hero-link" href="tel:{PHONE_MOBILE_TEL}">or call {PHONE_MOBILE}</a>
      </div>
    </div>
    <ul class="contact-list" data-reveal="stagger" style="--d:200ms">
      <li><span>Mobile</span><a href="tel:{PHONE_MOBILE_TEL}">{PHONE_MOBILE}</a></li>
      <li><span>Office</span><a href="tel:{PHONE_OFFICE_TEL}">{PHONE_OFFICE}</a></li>
      <li><span>Email</span><a href="mailto:{EMAIL}">{EMAIL}</a></li>
      <li><span>Office address</span>Mediathel, 120 Route des Macarons<br>06560 Valbonne, France</li>
    </ul>
  </div>
</section>"""


def post_card(p, feature=False):
    cls = "post-card feature" if feature else "post-card"
    return f"""<a class="{cls}" href="/blog/{p['slug']}/">
  <span class="tag">{esc(p['tag'])}</span>
  <h3 style="view-transition-name:post-{p['slug']}">{esc(p['title'])}</h3>
  <p>{esc(p['summary'])}</p>
  <span class="meta">{p['minutes']} min read</span>
</a>"""


# The first two are Tim's core work and lead the list.
SERVICES = [
    ("Assurance vie and investments",
     "France's favourite savings wrapper, and often the most tax-efficient home for your savings once you live here. I help you choose, structure and keep it under review.",
     "/blog/assurance-vie-explained/"),
    ("Mortgages in France",
     "Through Spectrum International Mortgages, which I run, I find the right French mortgage for your purchase and guide you through a process that works differently from the UK.",
     "/blog/buying-a-home-in-france-with-a-mortgage/"),
    ("Asset-backed mortgages",
     "Borrow against an investment portfolio instead of selling it. Useful for larger purchases, and for buyers whose income doesn't fit a French bank's usual boxes.",
     "/blog/asset-backed-mortgages/"),
    ("Moving to France",
     "Becoming French tax resident changes how your savings, ISAs and pensions are taxed. The best time to plan is before you arrive.",
     "/blog/moving-to-france-money-checklist/"),
    ("UK pensions in France",
     "What happens to your pensions when you're French resident, how they're taxed, and what your options are for drawing them.",
     "/faq/#pensions"),
    ("Protection and health cover",
     "With colleagues across Spectrum, I can help with life insurance and private health cover alongside your other planning.",
     "/faq/#insurance"),
]


def build_home():
    services = "\n".join(
        f'<li class="svc-item{" svc-lead" if i < 2 else ""}"><a href="{href}">'
        f'<span class="svc-num">{i + 1:02d}</span><span class="svc-title">{esc(t)}</span>'
        f'<span class="svc-desc">{esc(d)}</span><span class="svc-arrow" aria-hidden="true">→</span></a></li>'
        for i, (t, d, href) in enumerate(SERVICES)
    )
    latest = "\n".join(post_card(p) for p in POSTS[:3])
    person = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": "Tim Yates",
        "jobTitle": "Financial adviser",
        "worksFor": {"@type": "Organization", "name": "The Spectrum IFA Group", "url": "https://spectrum-ifa.com/"},
        "email": EMAIL,
        "telephone": PHONE_MOBILE_TEL,
        "address": {"@type": "PostalAddress", "streetAddress": "Mediathel, 120 Route des Macarons", "postalCode": "06560", "addressLocality": "Valbonne", "addressCountry": "FR"},
        "alumniOf": "University of Liverpool",
    }
    body = f"""<section class="hero" aria-labelledby="hero-title">
  <div class="scene" aria-hidden="true">
    <div class="sky"></div>
    <div class="sun"><span></span></div>
    <svg class="ridge far" viewBox="0 0 1440 140" preserveAspectRatio="none"><path d="M0 140V96l70-10 60-22 50 12 70-30 60 18 80-26 70 22 90-6 90 18 100-14 90-24 70 14 80-20 90 26 110 10 160 18v54z"/></svg>
    <svg class="ridge near" viewBox="0 0 1440 140" preserveAspectRatio="none"><path d="M0 140V82l48-6 42-30 34 16 46-40 40 28 52-34 44 30 60-12 58 30 72-6 66 22 90 8 120 16 160 4 200 6 308-2v54z"/></svg>
    <div class="sea"><div class="glitter"></div></div>
    <div class="horizon"></div>
    <div class="grain"></div>
  </div>
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="hero-eyebrow">Financial adviser on the Côte d'Azur</p>
      <h1 id="hero-title"><span class="line"><span>Your life on the Riviera,</span></span> <span class="line"><span><em>financially in order.</em></span></span></h1>
      <p class="hero-lead">I'm Tim Yates. I help English-speaking people invest tax-efficiently, finance the home they want and settle with confidence in the south of France.</p>
      <div class="hero-cta">
        <a class="btn btn-sun" href="#contact">Book a conversation <span aria-hidden="true">→</span></a>
        <a class="hero-link" href="#services">See how I help</a>
      </div>
    </div>
    <figure class="portrait">
      <div class="portrait-glow" aria-hidden="true"></div>
      <img class="portrait-img" src="/assets/tim-cutout.webp" srcset="/assets/tim-cutout-sm.webp 600w, /assets/tim-cutout.webp 1040w" sizes="(min-width: 901px) 520px, 300px" alt="Portrait of Tim Yates" width="1040" height="1560" fetchpriority="high">
    </figure>
  </div>
  <ul class="hero-proof wrap">
    <li><strong>Since 1994</strong> an expatriate himself</li>
    <li><strong>Founding partner</strong> of The Spectrum IFA Group</li>
    <li><strong>Regulated in France</strong> ORIAS · ANACOFI-CIF</li>
  </ul>
</section>

<section id="services">
  <div class="wrap">
    <div class="section-head" data-reveal="head">
      <p class="eyebrow">How I help</p>
      <h2>Your money, arranged for life in France</h2>
      <p class="muted">French tax, French banks and French paperwork follow their own logic. I've lived as an expatriate since 1994, so I know what it's like to work it out from the other side.</p>
    </div>
    <ol class="svc" data-reveal="stagger">
{services}
    </ol>
  </div>
</section>

<section class="alt process">
  <div class="wrap process-grid">
    <div class="process-head" data-reveal="head">
      <p class="eyebrow">How it works</p>
      <h2>Simple, and at your pace</h2>
      <p class="muted">No jargon and no pressure. You decide how fast we go, and nothing happens until you're comfortable with it.</p>
    </div>
    <ol class="steps" data-steps>
      <li data-reveal="up"><h3>A first conversation</h3><p>We talk about where you are, what you want, and what's worrying you. In person or by video, in plain English.</p></li>
      <li data-reveal="up"><h3>A clear recommendation</h3><p>I look at the whole picture and set out what I suggest, why, and what it costs, in writing, before you commit to anything.</p></li>
      <li data-reveal="up"><h3>Ongoing support</h3><p>Lives change and so do the rules. I keep your plan under review and I'm on the end of the phone when you need me.</p></li>
    </ol>
  </div>
</section>

<section id="about">
  <div class="wrap about">
    <div data-reveal="head">
      <p class="eyebrow">About me</p>
      <h2>An expatriate since 1994, and still enjoying it</h2>
      <blockquote class="pull">Listen first. Explain simply. That's most of what good advice is.</blockquote>
    </div>
    <div class="about-creds" data-reveal="up">
      <ul class="creds">
        <li>BA (Hons) Geography, University of Liverpool</li>
        <li>Postgraduate Diploma in Marketing (DipM), Member of the Chartered Institute of Marketing</li>
        <li>Member of the Chartered Insurance Institute, Certificate in Financial Planning</li>
        <li>Co-gérant, Spectrum International Mortgages SARL</li>
      </ul>
      <img class="spectrum-logo" src="/assets/spectrum-logo.webp" alt="The Spectrum IFA Group, International Financial Advisers" width="480" height="223" loading="lazy">
    </div>
    <div class="about-text" data-reveal="up" style="--d:160ms">
      <p>Before financial services I spent my career in marketing and business development in the healthcare and pharmaceutical industry, where the job was always to understand what people really needed before offering anything.</p>
      <p>I'm a founding partner of The Spectrum IFA Group, which advises English-speaking clients across Europe, and I run Spectrum International Mortgages, the group's mortgage brokerage. My work centres on assurance vie, tax-efficient wealth management, and finding the right mortgage for each property purchase in France, including asset-backed lending.</p>
      <p>I live in Fréjus. When I'm not working you'll find me skiing in the Alps or diving in the Mediterranean.</p>
      <div class="btn-row"><a class="btn" href="#contact">Get in touch</a></div>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <div class="section-head split" data-reveal="head">
      <p class="eyebrow">Articles</p>
      <h2>Straight answers on money in France</h2>
      <a class="link-arrow" href="/blog/">All articles <span aria-hidden="true">→</span></a>
    </div>
    <div class="post-list rail" data-reveal="stagger">
{latest}
    </div>
  </div>
</section>

{contact_band()}"""
    return page("/", "Tim Yates | Financial adviser on the Côte d'Azur",
                "Tim Yates helps English-speaking people in the south of France with assurance vie, tax-efficient investments, French mortgages and planning a move to France.",
                body, "/", jsonld(person), body_class="dark-top")


def build_blog():
    cards = "\n".join(post_card(p, feature=(i == 0)) for i, p in enumerate(POSTS))
    body = f"""<div class="page-head">
  <div class="wrap" data-reveal="head">
    <p class="eyebrow">Articles</p>
    <h1>Money and life in France</h1>
    <p>Plain-English guides to the questions I'm asked most: saving, borrowing and settling in the south of France.</p>
  </div>
</div>
<section>
  <div class="wrap">
    <div class="post-list" data-reveal="stagger">
{cards}
    </div>
  </div>
</section>
{contact_band()}"""
    paths = [page("/blog/", "Articles | Tim Yates, financial adviser", "Plain-English guides to assurance vie, French mortgages and moving to France, by financial adviser Tim Yates.", body, "/blog/", body_class="dark-top")]
    for p in POSTS:
        art = {
            "@context": "https://schema.org", "@type": "Article", "headline": p["title"],
            "description": p["summary"], "datePublished": p["date"],
            "author": {"@type": "Person", "name": "Tim Yates"},
        }
        body = f"""<div class="read-progress" aria-hidden="true"></div>
<article class="article">
  <div class="wrap narrow">
    <header class="article-head" data-reveal="head">
      <p class="crumbs"><a href="/">Home</a> / <a href="/blog/">Articles</a></p>
      <p class="eyebrow">{esc(p['tag'])}</p>
      <h1 data-vt style="view-transition-name:post-{p['slug']}">{esc(p['title'])}</h1>
      <p class="meta">By Tim Yates · {p['minutes']} min read</p>
    </header>
    <div class="prose">
{p['body']}
    </div>
    <div class="note"><strong>General information, not advice.</strong> This article explains how things generally work. Rules and rates change, and the right answer depends on your circumstances, so please talk to me before acting on it.</div>
    <div class="author-box">
      <img src="/assets/tim-avatar.jpg" alt="" width="72" height="72" loading="lazy">
      <p><strong>Tim Yates</strong> is a founding partner of The Spectrum IFA Group, based on the Côte d'Azur. <a href="/#contact">Get in touch</a></p>
    </div>
  </div>
</article>
{contact_band()}"""
        paths.append(page(f"/blog/{p['slug']}/", f"{p.get('seo_title', p['title'])} | Tim Yates", p["summary"], body, "/blog/", jsonld(art)))
    return paths


def build_faq():
    groups = []
    entities = []
    for g in FAQ:
        items = "\n".join(
            f'<details><summary>{esc(q)}</summary><div class="answer">{a}</div></details>' for q, a in g["items"]
        )
        groups.append(f'<div class="faq-group" id="{g["id"]}" data-reveal="up"><h2>{esc(g["title"])}</h2>\n{items}\n</div>')
        for q, a in g["items"]:
            entities.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}
    body = f"""<div class="page-head">
  <div class="wrap" data-reveal="head">
    <p class="eyebrow">Questions and answers</p>
    <h1>What people ask me</h1>
    <p>Short answers to common questions about investing, borrowing and living in France. If yours isn't here, just ask.</p>
  </div>
</div>
<section>
  <div class="wrap narrow">
{chr(10).join(groups)}
    <div class="note"><strong>General information, not advice.</strong> These answers explain how things generally work. Rules and rates change, so please get advice on your own situation.</div>
  </div>
</section>
{contact_band()}"""
    return page("/faq/", "Questions and answers | Tim Yates, financial adviser",
                "Answers to common questions about assurance vie, French mortgages, UK pensions and ISAs in France, and working with Tim Yates.",
                body, "/faq/", jsonld(data), body_class="dark-top")


def build_404():
    body = """<div class="page-head"><div class="wrap" data-reveal="head">
  <p class="eyebrow">Page not found</p>
  <h1>That page isn't here</h1>
  <p>It may have moved. Try the <a href="/">home page</a>, the <a href="/blog/">articles</a> or the <a href="/faq/">questions and answers</a>.</p>
</div></div>"""
    page("/404.html", "Page not found | Tim Yates", "Page not found.", body, "", body_class="dark-top")


def build_meta(paths):
    robots = "User-agent: *\nAllow: /\n"
    if SITE:
        robots += f"\nSitemap: {SITE}/sitemap.xml\n"
        urls = "\n".join(f"  <url><loc>{SITE}{p}</loc></url>" for p in paths)
        (ROOT / "sitemap.xml").write_text(
            f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n',
            encoding="utf-8")
    (ROOT / "robots.txt").write_text(robots, encoding="utf-8")


if __name__ == "__main__":
    version_stylesheet()
    paths = [build_home(), *build_blog(), build_faq()]
    build_404()
    build_meta(paths)
    print(f"Built {len(paths)} pages")
