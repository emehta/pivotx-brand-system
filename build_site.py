#!/usr/bin/env python3
# Generates every PivotX redesign subpage from one shared template set,
# matching the hand-authored index.html (color-blocked + spectral swirl system).
import json, html, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
INSIGHTS_SRC = "/private/tmp/claude-501/-Users-eshaanmehta-Documents-PivotX-Website/4365ec43-f31b-43d0-908d-ead7d8761f75/tasks/wvjx2akyk.output"

CONTACT = "info@pivotxadvisors.com"
LINKEDIN = "https://www.linkedin.com/company/pivotx-advisors/about/"
CAT_LABEL = {"genai": "GenAI", "ai": "AI", "operating-model": "Operating Model"}
THUMBS = ["thumb--orange", "thumb--indigo", "thumb--cobalt"]

URL_MAP = {
 "ai-is-raising-the-stakes-on-data-readiness":"https://pivotxadvisors.com/insights/genai/ai-is-raising-the-stakes-on-data-readiness/",
 "the-ceo-ai-stack-is-already-here-is-yours-working-for-you":"https://pivotxadvisors.com/insights/genai/the-ceo-ai-stack-is-already-here-is-yours-working-for-you/",
 "best-practices-for-successfully-using-ai-in-business":"https://pivotxadvisors.com/insights/operating-model/best-practices-for-successfully-using-ai-in-business/",
 "the-real-barrier-to-agentic-ai-still-isnt-tech-its-your-imagination":"https://pivotxadvisors.com/insights/operating-model/the-real-barrier-to-agentic-ai-still-isnt-tech-its-your-imagination/",
 "were-not-building-the-reusable-architectures-agentic-ai-needs":"https://pivotxadvisors.com/insights/genai/were-not-building-the-reusable-architectures-agentic-ai-needs/",
 "musings-of-a-data-enthusiast-will-we-really-need-data-lakes-in-the-future":"https://pivotxadvisors.com/insights/genai/musings-of-a-data-enthusiast-will-we-really-need-data-lakes-in-the-future/",
 "whats-old-is-new-again-ais-appetite-for-unstructured-data":"https://pivotxadvisors.com/insights/genai/whats-old-is-new-again-ais-appetite-for-unstructured-data-is-highlighting-systemic-quality-governance-and-compliance-failures/",
 "agentic-ai-isnt-magic-and-wont-cure-our-data-process-and-people-issues":"https://pivotxadvisors.com/insights/ai/agentic-ai-isnt-magic-and-wont-cure-our-data-process-and-people-issues/",
 "want-to-ensure-genai-success-first-fix-your-operating-models":"https://pivotxadvisors.com/insights/genai/want-to-ensure-genai-success-first-fix-your-operating-models/",
 "losing-control-of-shadow-ai-get-ready-to-democratize-ai-while-safeguarding-the-enterprise":"https://pivotxadvisors.com/insights/genai/losing-control-of-shadow-ai-get-ready-to-democratize-ai-while-safeguarding-the-enterprise/",
 "the-missing-ingredients-that-limit-genai-success-change-management-and-the-employee-journey":"https://pivotxadvisors.com/insights/genai/the-missing-ingredients-that-limit-genai-success-change-management-and-the-employee-journey/",
 "going-beyond-automation-the-power-of-combining-genai-with-intent":"https://pivotxadvisors.com/insights/genai/going-beyond-automation-the-power-of-combining-genai-with-intent/",
}

def esc(s):
    s = html.unescape(s or "")
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

LINKEDIN_SVG = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5a2.5 2.5 0 11-.02 5 2.5 2.5 0 01.02-5zM3 9h4v12H3zM9 9h3.8v1.7h.05c.53-1 1.83-2.05 3.77-2.05 4.03 0 4.78 2.65 4.78 6.1V21h-4v-5.4c0-1.29-.02-2.95-1.8-2.95-1.8 0-2.08 1.4-2.08 2.85V21H9z"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

def swirl(uid, seed, vb="0 0 1200 760"):
    parts = vb.split(); w, h = int(parts[2]), int(parts[3])
    return (f'<div class="swirl" aria-hidden="true"><svg viewBox="{vb}" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">'
            f'<defs><linearGradient id="sp{uid}" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="#2d0bce"/><stop offset=".3" stop-color="#160a78"/>'
            f'<stop offset=".52" stop-color="#0c0b10"/><stop offset=".76" stop-color="#f34100"/><stop offset="1" stop-color="#a82d00"/></linearGradient>'
            f'<filter id="sw{uid}" x="-30%" y="-30%" width="160%" height="160%">'
            f'<feTurbulence type="fractalNoise" baseFrequency="0.0055 0.0102" numOctaves="3" seed="{seed}" result="n"/>'
            f'<feDisplacementMap in="SourceGraphic" in2="n" scale="410" xChannelSelector="R" yChannelSelector="G"/>'
            f'<feGaussianBlur stdDeviation="14"/></filter></defs>'
            f'<rect width="{w}" height="{h}" fill="#0c0b10"/>'
            f'<g filter="url(#sw{uid})"><rect x="-120" y="-120" width="{w+240}" height="{h+240}" fill="url(#sp{uid})"/></g></svg></div>')

def head(title, desc):
    return (f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>{esc(title)}</title>\n<meta name="description" content="{esc(desc)}">\n'
            f'<link rel="icon" href="../assets/pivotx/mark-dark.svg">\n<link rel="stylesheet" href="styles.css?v=11">\n</head>\n<body>')

def nav():
    return f"""
<header class="nav">
  <div class="container nav-inner">
    <a class="brand" href="index.html" aria-label="PivotX Advisors home">
      <img class="mark" src="../assets/pivotx/mark-white.svg" alt="">
      <img class="word" src="../assets/pivotx/wordmark-white.svg" alt="PivotX Advisors">
    </a>
    <nav class="nav-links" aria-label="Primary">
      <a href="index.html#offerings">Offerings</a>
      <a href="index.html#about">About</a>
      <a href="index.html#method">Methodology</a>
      <a href="case-studies.html">Case Studies</a>
      <a href="data-journeys-aws.html">Partners</a>
      <a href="insights.html">Insights</a>
      <a href="index.html#contact">Contact</a>
    </nav>
    <div class="nav-cta">
      <a class="nav-icon" href="{LINKEDIN}" target="_blank" rel="noopener" aria-label="PivotX on LinkedIn">{LINKEDIN_SVG}</a>
      <a class="btn btn-primary" href="index.html#discovery">Free Discovery Session</a>
      <button class="nav-toggle" aria-label="Open menu" aria-expanded="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
    </div>
  </div>
</header>
<div class="scrim"></div>
<aside class="mobile-menu" aria-label="Mobile navigation">
  <button class="mobile-close" aria-label="Close menu"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
  <a href="index.html#offerings">Offerings</a><a href="index.html#about">About</a><a href="index.html#method">Methodology</a>
  <a href="case-studies.html">Case Studies</a><a href="data-journeys-aws.html">Partners</a><a href="insights.html">Insights</a>
  <a href="index.html#contact">Contact</a><a href="index.html#discovery" style="color:var(--orange)">Free Discovery Session &rarr;</a>
</aside>"""

def footer():
    return f"""
<footer class="footer" id="contact">
  <div class="container">
    <div class="footer-top">
      <div class="footer-brand">
        <div class="lock"><img class="mark" src="../assets/pivotx/mark-white.svg" alt=""><img class="word" src="../assets/pivotx/wordmark-white.svg" alt="PivotX Advisors"></div>
        <div class="cert-row">
          <div class="cert"><img src="../assets/logos/sdo.webp" alt="Supplier Diversity Office (SDO) Certified"></div>
          <div class="cert"><img src="../assets/logos/wbenc.webp" alt="WBENC Certified — Women's Business Enterprise"></div>
        </div>
      </div>
      <div class="footer-col"><h5>Explore</h5>
        <a href="index.html#offerings">Offerings</a><a href="index.html#method">Methodology</a><a href="case-studies.html">Case Studies</a><a href="data-journeys-aws.html">Partners</a><a href="insights.html">Insights</a></div>
      <div class="footer-col"><h5>Get in Touch</h5>
        <a href="mailto:{CONTACT}">{CONTACT}</a><a href="index.html#discovery">Free Discovery Session</a><a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a></div>
      <div class="footer-col"><h5>Newsletter</h5>
        <form class="newsletter-form" data-demo><input type="email" placeholder="Email ID (Work ID)" aria-label="Email" required><button class="btn btn-primary" type="submit">Subscribe</button></form>
        <div class="footer-social" style="margin-top:18px"><a href="{LINKEDIN}" target="_blank" rel="noopener" aria-label="LinkedIn">{LINKEDIN_SVG}</a></div>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; PivotX Advisors LLC, <span data-year>2026</span></span>
      <div class="legal"><a href="privacy-policy.html">Privacy Policy</a><a href="mailto:{CONTACT}">{CONTACT}</a></div>
    </div>
  </div>
</footer>
<script src="app.js?v=11"></script>
</body>
</html>"""

def page_head(eyebrow, h1_html, lead, uid=None, seed=None, extra=""):
    eb = (f'<span class="eyebrow">{esc(eyebrow)}</span>\n    ' if eyebrow else '<span class="tick"></span>\n    ')
    ld = f'<p class="lead">{esc(lead)}</p>\n    ' if lead else ''
    return f"""
<section class="page-head">
  <div class="container">
    {eb}<h1>{h1_html}</h1>
    {ld}{extra}
  </div>
</section>"""

# ----------------------------------------------------------- block render
def render_blocks(blocks):
    out = []
    for b in blocks:
        t = b.get("type")
        if t == "p": out.append(f"<p>{esc(b.get('text',''))}</p>")
        elif t == "h2": out.append(f"<h2>{esc(b.get('text',''))}</h2>")
        elif t == "h3": out.append(f"<h3>{esc(b.get('text',''))}</h3>")
        elif t == "quote": out.append(f"<blockquote>{esc(b.get('text',''))}</blockquote>")
        elif t in ("ul", "ol"):
            lis = "".join(f"<li>{esc(i)}</li>" for i in (b.get("items") or []))
            out.append(f"<{t}>{lis}</{t}>")
    return "\n      ".join(out)

def excerpt_blocks(blocks, n=6):
    chosen = blocks[:n]
    while len(chosen) < len(blocks) and chosen and chosen[-1].get("type") in ("h2", "h3"):
        chosen = blocks[:len(chosen)+1]
    return chosen

def first_text(a):
    if a.get("dek"): return a["dek"]
    for b in a.get("blocks", []):
        if b.get("type") == "p" and b.get("text"): return b["text"]
        if b.get("type") in ("ul", "ol") and b.get("items"): return b["items"][0]
    return ""

def trim(s, n=150):
    s = html.unescape(s or "").strip()
    if len(s) <= n: return s
    return s[:n].rsplit(" ", 1)[0] + "…"

def write(name, content):
    with open(os.path.join(OUT, name), "w") as f: f.write(content)
    print("wrote", name)

def insight_filename(slug): return f"insight-{slug}.html"

def related_cards(items, hrefs, labels, dates, n=3):
    cards = []
    for it, href, lab, dt in list(zip(items, hrefs, labels, dates))[:n]:
        cards.append(f"""<a class="ins-card" href="{href}">
        <div class="ins-meta"><span class="ins-cat">{esc(lab)}</span> {esc(dt)}</div>
        <h3>{esc(it)}</h3>
        <span class="more">Read</span>
      </a>""")
    return "\n".join(cards)

# ----------------------------------------------------------- insight pages
def build_insight_page(a, idx, arts):
    slug = a["slug"]; cat = a.get("category", "genai"); label = CAT_LABEL.get(cat, cat.title())
    title = a.get("title", ""); date = a.get("date", ""); read = a.get("readMins", "")
    thumb = THUMBS[idx % len(THUMBS)]
    dek = a.get("dek", "")
    blocks = [b for b in excerpt_blocks(a.get("blocks", []), 6) if not (b.get("type") == "p" and b.get("text") == dek)]
    body = (f'<p class="lead" style="color:var(--text)">{esc(dek)}</p>\n      ' if dek else "") + render_blocks(blocks)
    src = URL_MAP.get(slug, "https://pivotxadvisors.com/insights/")
    rel = [arts[(idx+k) % len(arts)] for k in range(1, 4)]
    rel_html = related_cards([r.get("title","") for r in rel], [insight_filename(r["slug"]) for r in rel],
                             [CAT_LABEL.get(r.get("category"), r.get("category","").title()) for r in rel], [r.get("date","") for r in rel])
    meta = f'<span class="ins-cat">{label}</span> · {esc(date)}' + (f' · {esc(read)} read' if read else "")
    return head(f"{title} — PivotX : Advisory for Data Monetization", trim(first_text(a), 155)) + nav() + f"""
<section class="article-hero">
  <div class="container">
    <div class="crumbs"><a href="index.html">Home</a> / <a href="insights.html">Insights</a> / <span>{label}</span></div>
    <h1 class="article-title">{esc(title)}</h1>
    <div class="article-meta">{meta}</div>
    <div class="article-banner {thumb}"><img class="mk" src="../assets/pivotx/mark-white.svg" alt=""></div>
  </div>
</section>
<article class="container">
  <div class="prose">
      {body}
      <div class="readon">
        <div class="k">Design preview</div>
        <p style="color:var(--dim);margin-bottom:18px">This redesign preview shows the opening of the article. Read the full piece on the live PivotX Insights site.</p>
        <a class="btn btn-outline" href="{src}" target="_blank" rel="noopener">Continue reading on pivotxadvisors.com {ARROW}</a>
      </div>
  </div>
  <div class="article-foot"><span>Published on PivotX Insights</span><span>·</span><a href="mailto:{CONTACT}">{CONTACT}</a></div>
  <section class="sec-sm"><span class="eyebrow">More insights</span><div class="grid-3" style="margin-top:24px">{rel_html}</div></section>
</article>""" + footer()

# ----------------------------------------------------------- case studies (full)
CASE_STUDIES = [
 {"file":"case-study-procurement.html","thumb":"thumb--orange","label":"Procurement · AI","date":"28 Aug 2025","read":"3 mins",
  "title":"Turning Fortune 500 Manual Procurement Challenges into Value Through AI",
  "dek":"In today's data-driven economy, procurement leaders are tasked with more than just cost control – they're expected to drive agility, resilience, and efficiency. But for many enterprise procurement teams, legacy processes, siloed systems, and manual workflows often bog down operations.",
  "blocks":[
   {"type":"p","text":"This is especially true for large organizations, where procurement often lives in the shadows – deemed a necessary function but rarely a technology investment priority. However, with the rise of AI and automation, there's an unprecedented opportunity to elevate procurement from its back-office reputation to a front-line value creator."},
   {"type":"p","text":"This was the ambition of the procurement office of a Fortune 500 digital innovator that recently partnered with PivotX. The team was overwhelmed with high volumes of unstructured data from invoices and purchase orders and overly reliant on manual processes. Using our I2V (Idea to Value) Framework and AI, PivotX transformed multiple areas of core functions from reactive to proactive while unlocking speed, precision, and strategic insight."},
   {"type":"h2","text":"Accelerating Procurement Intake with AI-Driven Simplicity"},
   {"type":"p","text":"The intake process was a friction point – heavily manual, slow, and unclear. Turn-around times were lengthy and required multiple follow-ups, and the team lacked visibility after requests were submitted."},
   {"type":"p","text":"PivotX introduced an AI-powered conversational agent that could interpret user intent and automatically structure procurement intake submissions. By guiding requesters through a smart, conversational interface, the agent dramatically simplified the front-end experience."},
   {"type":"quote","text":"The result was full lifecycle visibility with control, where manual data handling dropped significantly and intake time shrank from weeks to hours, saving $300K."},
   {"type":"h2","text":"Smart PO Creation Through Contract-Aware Automation"},
   {"type":"p","text":"Creating purchase orders was very manual – from reviewing Master Purchase Agreements (MSPAs) and Statements of Work (SOWs) to rekeying information into forms. This not only delayed procurement cycles but also introduced errors and compliance risks."},
   {"type":"p","text":"PivotX deployed Agentic AI to automate PO creation. The system intelligently extracts key terms from contracts, validates them against sourcing policies, and auto-fills PO templates with precision."},
   {"type":"quote","text":"The Agentic solution accelerated PO cycle times while sharply reducing errors and compliance gaps, enabling the team to take on higher value tasks while benefiting from both speed and accuracy with an estimated $365K in savings."},
   {"type":"h2","text":"Intelligent Invoice Validation & Cashflow Optimization"},
   {"type":"p","text":"Invoice validation was another manual, time-consuming process that saw significant inconsistencies in payment terms and data formats. Delays and premature payments were impacting cash flow and working capital."},
   {"type":"p","text":"The PivotX team applied AI to help the team ingest and analyze unstructured invoice data in real time. By automating the description and payment term comparisons across large volumes of documents, the system was able to quickly flag discrepancies and potential risks for human review."},
   {"type":"quote","text":"With AI driving the process with near real-time validation, the team saw a significant reduction in premature payments and improved working capital preservation."},
   {"type":"h2","text":"AI-Assisted Vendor Vetting for ESG Compliance"},
   {"type":"p","text":"Due diligence for ESG compliance had been a lengthy and manually intensive process. With growing regulatory and reputational pressures, the organization needed a faster, more reliable approach to vendor risk management."},
   {"type":"p","text":"PivotX leveraged LLM-driven search to automate ESG risk identification. By scanning and citing credible sources, the AI flagged potential vendor violations – helping the team make better decisions, faster."},
   {"type":"quote","text":"The team can now vet vendors at scale without sacrificing thoroughness – building a more responsible, risk-aware supply network where ESG review cycles went from 10 days to under 10 hours, with an estimated $250K in cost avoidance!"},
   {"type":"h2","text":"AI Has Opened the Door for Procurement to Lead"},
   {"type":"p","text":"Procurement has long been underserved and forgotten in the digital transformation conversation. But with AI and automation, the function can confidently innovate while aligning with corporate IT aspirations. PivotX's solutions are modular, scalable, and capable of delivering immediate impact without disrupting existing systems. By embracing AI and automation, procurement teams can shake off manual burdens and quickly move to a more agile, data-driven, and resilient future."},
  ]},
 {"file":"case-study-healthcare-chatbot.html","thumb":"thumb--cobalt","label":"Healthcare · GenAI","date":"14 Jul 2025","read":"3 mins",
  "title":"ChatBot for On Demand Virtual Healthcare Provider",
  "dek":"Our client partners with cancer providers to deliver on-demand, technology-enabled virtual care, enhancing the practice of oncology while transforming the patient's experience.",
  "blocks":[
   {"type":"p","text":"The need for these types of services is rapidly growing in the United States. There is a significant provider shortage that is being exacerbated by two coinciding trends: an aging population who need more care, and an aging workforce nearing retirement. Together these are driving high burnout rates in both oncologists and the front-line care teams who support them."},
   {"type":"ul","items":[
     "A 2023 survey revealed that “59% of oncologists reported symptoms of burnout, a significant increase from 34% in 2013.”",
     "ASCO projects “a shortage of over 2,200 oncologists by the end of 2025,” which will be especially acute in rural areas, where the percentage of practicing oncologists has declined from 11.2% in 2021 to 10% in 2023."]},
   {"type":"p","text":"The team had started using a third-party chatbot to help address these challenges. Through a chat experience, more patients could benefit from quicker access to relevant information while care teams would be able to prioritize patient needs."},
   {"type":"p","text":"While the first version proved valuable, the care team wanted to uplevel the chatbot's capabilities and bring the solution in house."},
   {"type":"p","text":"PivotX was initially engaged to understand the role that the existing chatbot was playing for both cancer patients and the caregiving teams. By taking a human-centric data-as-a-product approach, the team identified multiple additional needs and capabilities that, along with partners, were designed into an upgraded chat experience. Enhancements included a more robust natural language conversation flow for patients delivered through SMS RCS (Rich Communication Services) leveraging Microsoft Azure CLU, which enables:"},
   {"type":"ul","items":[
     "A guided pathway to identifying symptoms based on responses and severity signals",
     "More personalized interactions based on context (e.g., day, time of day), initial input and awareness based on previous conversations",
     "A wider range of content such as images, videos and interactive elements, delivered based on the clinical pathway identified during the chat"]},
   {"type":"p","text":"Additional enhancement included chat summarization for care providers and patients, so each future interaction is based on the latest information. The summarization capabilities were activated using Azure OpenAI Services."},
   {"type":"p","text":"These enhancements worked hand in hand to improve patient care and practitioner effectiveness. The enhanced natural language experience has helped guide patients to more accurately describe what their exact issues are, so the information provided is more useful. The summarization capability has saved valuable time when assessing a patient's status to determine when direct intervention is needed, helping care givers prioritize the most acute cases for quicker action."},
   {"type":"p","text":"One example is how the chatbot can now provide more detailed and accurate information about diet. Cancer patients often have questions about their diet due to therapy-related nausea or reactions to specific foods. In the past a nurse practitioner had to read an entire chat before following up manually via email with relevant diet articles and information."},
   {"type":"p","text":"Today, chat interactions prompt more detailed responses about current conditions and patient history. These responses enable the chatbot to directly provide information on what the patient can eat and what they should avoid, along with links to relevant articles so the patient can immediately revise their diet."},
   {"type":"p","text":"Closing this timing gap can have a huge positive impact on patient outcomes. Nutrition plays a vital role in cancer patient success, helping them withstand the immediate effects of chemotherapy and keeping their strength up during a treatment cycle. Now through the enhanced version of the chatbot, more patients can get the information they need right away, and the nurse practitioners can follow up with patients to assess progress at regular intervals."},
   {"type":"p","text":"This level of information and interaction fits the client's vision of how it wants to use AI, which is a human + technology experience. The chatbot is not replacing nurse practitioner interactions. Instead, it is creating the conditions for greater impact while scaling the organization's ability to serve more patients more effectively, spending valuable practitioner time on the most acute cases and needs."},
  ]},
 {"file":"case-study-financial-reporting.html","thumb":"thumb--indigo","label":"Finance · Automation","date":"14 Jul 2025","read":"3 mins",
  "title":"Streamlining and Automating Financial System Reporting",
  "dek":"The client is a multi-billion-dollar collection of hundreds of discreet businesses, which often are organized into practice areas. In one practice area there are four distinct operating companies.",
  "blocks":[
   {"type":"p","text":"Historically each of these organizations has operated its own P&L and ERP system to capture individual business unit financial data. What has been lacking is a single system of record to automatically consolidate the required financial data to understand and report on the entire entity or execute financial data reconciliation with the general ledger."},
   {"type":"p","text":"Because of this, much of the month and quarter end reporting was still happening manually. Different teams were extracting data and readjusting codes in the ERP system for consistency by hand. Team members reported that it took most of the month to complete all this work, while still keeping core financial operations up and running."},
   {"type":"p","text":"The practice area lead organization was looking to eliminate costs and time associated with calibrating this data so they could manage these business units from a one P&L vantage point, while also freeing up team member time and resources to focus on more value-added tasks."},
   {"type":"p","text":"Pivot X was engaged to support reconciliation and variance analysis for things like actual vs AOP/budget, actual vs forecast and YoY actuals comparisons across the entities as a first step in a journey to fully automating the consolidation of financial reporting across the four business units. Access to the relevant files of each entity was provided, along with a master Hyperion file, which contained all the aggregated data across various teams, departments, and account code hierarchies."},
   {"type":"p","text":"Also, the variance analysis is actual vs AOP/budget, actual vs forecast and YoY actuals comparison. This exercise is done during the financial close period after the financial consolidation."},
   {"type":"p","text":"PivotX leveraged its unique I2I (Idea to Implementation) prototype driven methodology to rapidly prototype an automated solution. The solution leveraged real world data to drive a better understanding of the needs and data issues, providing end users a way to address their immediate pain areas and quickly become advocates for extending the roadmap for a larger solution set."},
   {"type":"p","text":"PivotX first worked to transform and consolidate the data, which enabled the automatic aggregation comparison between the unit details and the aggregated Hyperion file. This allowed teams to confidently compare their month-to-month forecasts for gap analysis and reconciliation. This effort is also informing the bi-annual operation planning cycle, allowing teams to compare monthly performance against stated forecasts."},
   {"type":"p","text":"The key to the project was to first fully understand the business requirements before engaging with the data, applying a change management mindset that aligns stakeholder needs with expected outcomes. In less than two weeks the PivotX team was able to normalize the data, implement transformation rules, and execute the engineering needed to stand up the solution."},
   {"type":"p","text":"The rapid pace and project agility was enabled in part by the team's Data and AI Programming Framework, where full-stack data/AI engineers deploy strategic use of GenAI and LLMs to cocreate and execute transformations."},
   {"type":"p","text":"Once the initial data transformation and automation work was complete, the PivotX team leveraged the files from various systems such as Oracle and Hyperion. This data was landed into Google Cloud Platform in BigQuery, from which the reconciliation processes are being automated."},
   {"type":"p","text":"With the initial data foundation in place, the organization is looking to PivotX to help enable data governance, data observability and a data catalog alongside the infrastructure, with the configuration taking place through Google Catalog in combination with Pentaho."},
   {"type":"p","text":"The solution, built out and delivered in less than two months, drove significant cross-team involvement and has become the foundation for the lead practice organization's finance data product with its own future roadmap. For example, the team has discussed with PivotX the potential of creating a business user interface where finance team members easily adjust new codes and entities every month. And while Finance is the first functional area to benefit from this application, due to early cross function stakeholder involvement additional corporate functions such as Audit are eager to participate in plans for onboarding their areas in rapid succession."},
  ]},
]

def build_case_study(cs):
    body = f'<p class="lead" style="color:var(--text)">{esc(cs["dek"])}</p>\n      ' + render_blocks(cs["blocks"])
    others = [c for c in CASE_STUDIES if c["file"] != cs["file"]]
    rel_html = related_cards([c["title"] for c in others], [c["file"] for c in others],
                             [c["label"] for c in others], [c["date"] for c in others])
    return head(f"{cs['title']} — PivotX : Advisory for Data Monetization", trim(cs["dek"], 155)) + nav() + f"""
<section class="article-hero">
  <div class="container">
    <div class="crumbs"><a href="index.html">Home</a> / <a href="case-studies.html">Case Studies</a> / <span>{esc(cs['label'])}</span></div>
    <h1 class="article-title">{esc(cs['title'])}</h1>
    <div class="article-meta"><span class="ins-cat">{esc(cs['label'])}</span> · {esc(cs['date'])} · {esc(cs['read'])} read</div>
    <div class="article-banner {cs['thumb']}"><img class="mk" src="../assets/pivotx/mark-white.svg" alt=""></div>
  </div>
</section>
<article class="container">
  <div class="prose">
      {body}
  </div>
  <div class="article-foot"><span>PivotX Advisors case study</span><span>·</span><a href="mailto:{CONTACT}">{CONTACT}</a></div>
  <section class="sec-sm"><span class="eyebrow">More case studies</span><div class="grid-3" style="margin-top:24px">{rel_html}</div></section>
</article>""" + footer()

# ----------------------------------------------------------- index pages
def build_case_studies_index():
    cards = "\n".join(f"""<a class="cs-card" href="{c['file']}">
        <div class="cs-thumb {c['thumb']}"><img class="mk" src="../assets/pivotx/mark-white.svg" alt=""><span class="label">{esc(c['label'])}</span></div>
        <div class="cs-body"><span class="date">{esc(c['date'])}</span><h3>{esc(c['title'])}</h3><p>{esc(trim(c['dek'],150))}</p><span class="more">Read</span></div>
      </a>""" for c in CASE_STUDIES)
    return (head("Case Studies — PivotX : Advisory for Data Monetization", "Real outcomes from PivotX data and AI engagements across procurement, healthcare, and finance.")
            + nav() + page_head("", "Case Studies", "")
            + f'\n<section class="sec sec--ink" style="padding-top:36px"><div class="container"><div class="grid-3">{cards}</div></div></section>'
            + footer())

def build_insights_index(arts):
    cards = []
    for i, a in enumerate(arts):
        cat = a.get("category", "genai")
        hidden = ' data-hidden style="display:none"' if i >= 9 else ''
        cards.append(f"""<a class="ins-card" data-cat="{cat}"{hidden} href="{insight_filename(a['slug'])}">
        <div class="ins-meta"><span class="ins-cat">{CAT_LABEL.get(cat,cat.title())}</span> {esc(a.get('date',''))}</div>
        <h3>{esc(a.get('title',''))}</h3><p>{esc(trim(first_text(a),148))}</p><span class="more">Read</span></a>""")
    loadmore = '<div style="text-align:center;margin-top:38px"><button class="btn btn-outline btn-lg" data-loadmore>Load More</button></div>' if len(arts) > 9 else ''
    return (head("Insights — PivotX : Advisory for Data Monetization", "Thinking on data, AI and GenAI from the PivotX Advisors team.")
            + nav() + page_head("", "Insights", "")
            + f"""
<section class="sec sec--ink" style="padding-top:36px"><div class="container">
  <div class="filter-row">
    <button class="filter-btn active" data-filter="all">All</button>
    <button class="filter-btn" data-filter="genai">GenAI</button>
    <button class="filter-btn" data-filter="ai">AI</button>
    <button class="filter-btn" data-filter="operating-model">Operating Model</button>
  </div>
  <div class="grid-3">{chr(10).join(cards)}</div>
  {loadmore}
</div></section>""" + footer())

def build_aws():
    pains = [("Data Overload","Endless streams of structured and unstructured data that are increasingly difficult to manage."),
             ("Data Quality Gaps","Errors and inconsistencies creeping into your insights pipeline, causing delays and distrust."),
             ("Infrastructure Constraints","Soaring compute costs and resource limitations slowing down AI scalability."),
             ("Model Drift","Once-reliable AI models faltering post-deployment, jeopardizing decisions.")]
    pillars = [("SEE","Gain real-time, end-to-end insights across your data and AI ecosystems."),
               ("DO","Automate alerts and get intelligent recommendations to act swiftly."),
               ("WIN","Minimize costs, maximize ROI, and ensure regulatory compliance.")]
    stages = [("ASSESS","Measure your data readiness for AI and GenAI using AIrborne."),
              ("ESTABLISH","Build a robust foundation with DataOps, quality assurance, and observability."),
              ("ELEVATE","Optimize AI systems with MLOps and governance for peak performance."),
              ("ENRICH","Manage resources and costs efficiently through advanced FinOps strategies."),
              ("ACCELERATE","Achieve seamless operations with a fully functional Data & AI Control Tower.")]
    pains_html = "\n".join(f'<div class="card"><div class="kicker">0{i+1}</div><h3 style="font-family:var(--font-serif);font-size:clamp(20px,4.5vw,25px);margin:10px 0 8px">{esc(t)}</h3><p class="muted">{esc(d)}</p></div>' for i,(t,d) in enumerate(pains))
    pillars_html = "\n".join(f'<div class="pillar"><div class="pk">{esc(t)}</div><p>{esc(d)}</p></div>' for t,d in pillars)
    stages_html = "\n".join(f'<li><span class="pn">{i+1:02d}</span><span class="pt"><b style="color:var(--text);font-family:var(--font-cond);text-transform:uppercase;letter-spacing:.08em">{esc(t)}</b> &nbsp; {esc(d)}</span></li>' for i,(t,d) in enumerate(stages))
    cta = f'<div class="hero-cta" style="margin-top:30px"><a class="btn btn-primary btn-lg" href="index.html#discovery">Kickstart Your Journey {ARROW}</a><a class="btn btn-outline btn-lg" href="#stages">See the 5 Stages</a></div>'
    return (head("Data Journeys with AWS — PivotX : Advisory for Data Monetization", "The PivotX Data & AI Observability and Optimization Control Tower — your command center for trustworthy, scalable data and AI systems, powered by AWS.")
            + nav()
            + page_head("Powering Data Journeys with AWS",
                'Data &amp; AI Observability and<br>Optimization <span class="o">Control Tower</span>',
                "Your Command Center for Trustworthy and Scalable Data and AI Systems.", "Aws", 11, cta)
            + f"""
<section class="sec sec--ink">
  <div class="container">
    <div class="head reveal"><span class="eyebrow">The Problem</span><h2 class="display">A Growing Storm: The Data<br>and AI Confidence Crisis</h2>
      <p class="lead" style="margin-top:18px">Imagine this: your organization is scaling rapidly, but the very systems that power your insights — Data and AI — are under strain.</p></div>
    <div class="problem-grid reveal d1" style="margin-top:40px">{pains_html}</div>
  </div>
</section>
<section class="sec sec--indigo">
  <div class="container">
    <div class="head reveal"><span class="eyebrow">The Solution</span><h2 class="display">Meet the PivotX Control Tower</h2>
      <p class="lead" style="margin-top:18px">Built on AWS DataZone and AWS SageMaker, paired with GenAI intelligence — so you can SEE, DO, and WIN across the data and AI lifecycle.</p></div>
    <div class="pillars reveal d1" style="margin-top:40px">{pillars_html}</div>
  </div>
</section>
<section class="sec sec--ink" id="stages">
  <div class="container">
    <div class="method">
      <div class="reveal"><span class="eyebrow">The Journey</span><h2 class="display" style="margin:20px 0 16px">Five stages to a fully<br>operational Control Tower</h2>
        <p class="lead">We meet you where you are — from measuring readiness to running a fully functional Data &amp; AI Control Tower.</p>
        <div class="stage-rail"><span class="stage-pill">Assess</span><span class="stage-pill">Establish</span><span class="stage-pill">Elevate</span><span class="stage-pill">Enrich</span><span class="stage-pill">Accelerate</span></div></div>
      <ul class="principles reveal d1">{stages_html}</ul>
    </div>
  </div>
</section>
<section class="sec sec--orange bigstat">
  <img class="bigstat-mark" src="../assets/pivotx/mark-dark.svg" alt="" aria-hidden="true">
  <div class="container reveal" style="text-align:center">
    <img class="d2e-badge" src="../assets/logos/aws-d2e.webp" alt="Your AWS D2E (Data Driven Everything) Certified Partner" style="margin:0 auto 8px">
    <h2 class="display" style="margin:24px auto 14px;max-width:20ch;font-size:clamp(34px,5vw,66px)">PivotX Advisors is AWS D2E certified</h2>
    <p class="sub">D2E is an exclusive invite-only program, with only 32 partners certified as of mid-2024. AWS D2E focuses on helping customers move faster and with greater precision in their data-centric journey.</p>
    <a class="btn btn-primary btn-lg" style="margin-top:28px" href="index.html#discovery">Contact us today to kickstart your journey {ARROW}</a>
  </div>
</section>""" + footer())

PRIVACY_BODY = """
<article class="container">
  <div class="prose">
    <p>At PivotX Advisors (&ldquo;we,&rdquo; &ldquo;our,&rdquo; or &ldquo;us&rdquo;), we are committed to protecting the privacy and security of your personal data. This Privacy Policy outlines how we process personal data collected through our LinkedIn lead generation forms, in compliance with applicable data protection laws and industry standards.</p>
    <h2>1. General Information</h2>
    <p>PivotX Advisors is responsible for all data processing activities related to LinkedIn lead generation forms. This privacy statement details the collection, use, and protection of your personal data when you engage with our LinkedIn advertisements and lead generation forms.</p>
    <h2>2. Collection and Use of Personal Data</h2>
    <h3>2.1 Data Collection</h3>
    <p>We collect personal data that you voluntarily provide when completing our LinkedIn lead generation forms. This may include, but is not limited to, your name, email address, job title, and company name. We also collect anonymous data related to the usage of our lead generation forms to help us analyze the performance of our advertising campaigns on LinkedIn.</p>
    <h3>2.2 Purpose of Data Collection</h3>
    <p>The personal data collected through our lead generation forms will be used solely for the purposes described in the respective forms. These purposes may include:</p>
    <ul><li>Contacting you with relevant information about our services or products.</li><li>Providing you with customized content and offers.</li><li>Fulfilling requests or inquiries made through the form.</li></ul>
    <h3>2.3 Data Usage for Analytics</h3>
    <p>To improve our advertising efforts, PivotX Advisors collects anonymized data on the usage of our lead generation forms. This data helps us understand how users interact with our forms and ads on LinkedIn, enabling us to refine and optimize our campaigns.</p>
    <h3>2.4 Data Retention</h3>
    <p>Your personal data will be retained only for as long as necessary to fulfill the purposes for which it was collected or to comply with legal and regulatory obligations. Periodically, your data may be archived or stored as part of our backup processes.</p>
    <h2>3. Data Security</h2>
    <p>We have implemented appropriate technical and organizational security measures to protect your personal data against unauthorized access, alteration, disclosure, or destruction. These measures include, but are not limited to, encryption, access controls, and secure data storage.</p>
    <h2>4. Sharing and Disclosure of Personal Data</h2>
    <p>PivotX Advisors does not sell, rent, or trade your personal data to third parties. Your personal data may only be shared with third-party service providers who assist us in operating our services or conducting our business, and these providers are required to maintain the confidentiality and security of your data in compliance with applicable laws.</p>
    <h2>5. Your Data Rights</h2>
    <p>You have several rights concerning your personal data collected via LinkedIn lead generation forms:</p>
    <h3>5.1 Right to Be Informed</h3><p>You have the right to be informed about the personal data we collect and how we use it.</p>
    <h3>5.2 Right to Access</h3><p>You can request access to the personal data we hold about you.</p>
    <h3>5.3 Right to Rectification</h3><p>You have the right to request correction of any inaccurate or incomplete personal data.</p>
    <h3>5.4 Right to Erasure</h3><p>You can request the deletion of your personal data when it is no longer necessary for the purposes for which it was collected or when you withdraw your consent.</p>
    <h3>5.5 Right to Restrict Processing</h3><p>You may request that we restrict the processing of your data under certain conditions.</p>
    <h3>5.6 Right to Data Portability</h3><p>You have the right to receive your personal data in a structured, commonly used, and machine-readable format, and to transmit that data to another controller where technically feasible.</p>
    <h3>5.7 Right to Object</h3><p>You can object to the processing of your personal data for certain purposes, including direct marketing.</p>
    <h3>5.8 Right to Withdraw Consent</h3><p>If the processing of your personal data is based on consent, you have the right to withdraw that consent at any time.</p>
    <h3>5.9 Right to Lodge a Complaint</h3><p>You have the right to lodge a complaint with a supervisory authority if you believe that your data protection rights have been violated.</p>
    <h2>6. Contact Us</h2>
    <p>If you have any questions or concerns about this Privacy Policy or wish to exercise any of your rights, please contact us via email: <a href="mailto:%CONTACT%">%CONTACT%</a></p>
    <h2>7. Changes to This Privacy Policy</h2>
    <p>We may update this Privacy Policy from time to time to reflect changes in our practices, technologies, legal requirements, or other factors. Any updates will be posted on this page with a new &ldquo;Last Updated&rdquo; date. We encourage you to review this Privacy Policy periodically to stay informed about how we are protecting your data.</p>
  </div>
</article>"""

def build_privacy():
    ph = page_head("", "Privacy Policy", "",
                   extra='<p class="muted" style="font-family:var(--font-mono);font-size:13px;margin-top:6px">Last Updated: 03, Sep 2024</p>')
    # remove empty lead paragraph
    ph = ph.replace('<p class="lead"></p>', '')
    return head("Privacy Policy — PivotX : Advisory for Data Monetization", "PivotX Advisors privacy policy for personal data collected through LinkedIn lead generation forms.") + nav() + ph + PRIVACY_BODY.replace("%CONTACT%", CONTACT) + footer()

def main():
    arts = json.load(open(INSIGHTS_SRC))["result"]
    for i, a in enumerate(arts): write(insight_filename(a["slug"]), build_insight_page(a, i, arts))
    for cs in CASE_STUDIES: write(cs["file"], build_case_study(cs))
    write("case-studies.html", build_case_studies_index())
    write("insights.html", build_insights_index(arts))
    write("data-journeys-aws.html", build_aws())
    write("privacy-policy.html", build_privacy())
    print("done:", len(arts)+len(CASE_STUDIES)+4, "pages")

if __name__ == "__main__":
    main()
