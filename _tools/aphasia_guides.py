"""Generates the Omilía aphasia guides under /omilia/aphasia-guides/.

Run from the repo root:  python3 _tools/aphasia_guides.py

Shared nav, styles and footer are copied from omilia/index.html so the
guides stay in sync with the app page. Folders starting with "_" are not
published by GitHub Pages.

These are health-related pages: keep claims conservative, keep the
"not medical advice" note, and have new articles reviewed before publishing.
"""
import datetime
import json
import os
import re
from html import escape

BASE = 'https://happypathapps.co'
GUIDES = '/omilia/aphasia-guides/'
APP_STORE = 'https://apps.apple.com/us/app/aphasia-speech-therapy-omil%C3%ADa/id1602156122'
THERAPIST_STORE = 'https://apps.apple.com/us/app/slps-omil%C3%ADa-therapist/id6736846216'

om = open('omilia/index.html', encoding='utf-8').read()
base_css = om[om.index('<style>') + len('<style>'):om.index('  /* ══════════════════════════════════════')]
footer_css = om[om.index('  /* Footer */'):om.index('  /* ─── RESPONSIVE ─── */')]
nav_html = om[om.index('<nav id="navbar">'):om.index('</nav>') + len('</nav>')]
nav_html = nav_html.replace('<a href="/omilia/" class="active">', '<a href="/omilia/">')
footer_html = om[om.index('<div class="om-footer">'):om.index('<script>', om.index('<div class="om-footer">'))].rstrip()
footer_html = footer_html.replace('<a href="/">Home</a>', '<a href="/">Home</a>\n      <a href="/omilia/">Omilía</a>', 1)
script_html = om[om.index('<script>', om.index('<div class="om-footer">')):om.rindex('</script>') + len('</script>')]

APPLE_SVG = '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'

PAGE_CSS = """
  /* ══════════════════════════════════════
     APHASIA GUIDES
     ══════════════════════════════════════ */
  .ag-hero {
    position: relative; overflow: hidden; padding: 130px 32px 64px;
    background: linear-gradient(180deg, #F7FBFF 0%, var(--blue-50) 70%, #FFFFFF 100%);
  }
  .ag-hero-inner { max-width: 820px; margin: 0 auto; }
  .ag-crumbs { display: flex; flex-wrap: wrap; gap: 6px; font-size: 0.9rem; color: var(--slate); margin-bottom: 22px; }
  .ag-crumbs a { color: var(--slate); text-decoration: none; }
  .ag-crumbs a:hover { color: var(--navy); text-decoration: underline; }
  .ag-hero h1 { font-size: clamp(2.2rem, 5vw, 3.3rem); font-weight: 800; line-height: 1.06; color: var(--night); letter-spacing: -1px; }
  .ag-lede { font-size: 1.18rem; color: var(--slate); line-height: 1.7; margin-top: 20px; }
  .ag-meta { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; margin-top: 22px; font-size: 0.92rem; color: var(--slate); }
  .ag-meta img { width: 28px; height: 28px; border-radius: 7px; }
  .ag-meta strong { color: var(--night); }

  .ag-body { padding: 32px 32px 90px; }
  .ag-article { max-width: 760px; margin: 0 auto; font-size: 1.1rem; line-height: 1.78; color: var(--ink); }
  .ag-article h2 { font-size: 1.75rem; color: var(--night); margin: 50px 0 14px; letter-spacing: -0.3px; line-height: 1.2; }
  .ag-article h3 { font-size: 1.22rem; color: var(--night); margin: 30px 0 6px; }
  .ag-article p { margin-top: 14px; }
  .ag-article ul, .ag-article ol { margin: 14px 0 0 22px; }
  .ag-article li { margin-top: 8px; }
  .ag-article strong { color: var(--night); }
  .ag-article a { color: var(--blue); font-weight: 600; text-underline-offset: 3px; }
  .ag-note {
    margin-top: 24px; padding: 16px 20px; border-radius: 16px;
    background: var(--blue-50); border-left: 4px solid var(--blue); font-size: 1rem;
  }
  .ag-note p:first-child { margin-top: 0; }
  .ag-note.warn { background: #FFF5F3; border-left-color: var(--coral); }
  .ag-toc { margin-top: 28px; padding: 20px 24px; border: 1px solid #DCEBFF; border-radius: 16px; background: white; }
  .ag-toc strong { display: block; margin-bottom: 4px; }
  .ag-toc ol { margin-top: 6px; }
  .ag-toc li { margin-top: 4px; font-size: 1rem; }
  .ag-try { margin-top: 12px; padding: 14px 18px; border-radius: 14px; background: #F7FBFF; border: 1px dashed #BFDBFE; font-size: 1rem; }
  .ag-try p:first-child { margin-top: 0; }

  .ag-faq details { border-bottom: 1px solid #DCEBFF; padding: 16px 0; }
  .ag-faq summary { cursor: pointer; font-weight: 700; color: var(--night); list-style: none; display: flex; justify-content: space-between; gap: 16px; }
  .ag-faq summary::-webkit-details-marker { display: none; }
  .ag-faq summary::after { content: '+'; color: var(--blue); font-size: 1.3rem; line-height: 1; }
  .ag-faq details[open] summary::after { content: '\\2212'; }
  .ag-faq details p { margin-top: 10px; }

  .ag-cta {
    margin: 56px auto 0; max-width: 760px; padding: 34px; border-radius: 24px; text-align: center;
    background: var(--navy); color: white; position: relative; overflow: hidden;
  }
  .ag-cta::before {
    content: ''; position: absolute; inset: 0;
    background: radial-gradient(circle at 15% 20%, rgba(10,221,24,0.25), transparent 50%),
                radial-gradient(circle at 85% 90%, rgba(61,141,244,0.35), transparent 55%);
  }
  .ag-cta > * { position: relative; }
  .ag-cta img.icon { width: 64px; height: 64px; border-radius: 15px; }
  .ag-cta h2 { color: white; font-size: 1.7rem; margin-top: 14px; }
  .ag-cta p { color: rgba(255,255,255,0.75); margin-top: 10px; line-height: 1.6; }
  .ag-cta .badges { display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 16px; margin-top: 22px; }
  .ag-cta .store-badge { border-color: rgba(255,255,255,0.4); }
  .ag-cta .therapist { color: white; font-weight: 600; text-decoration: underline; text-underline-offset: 3px; }

  .ag-disclaimer { max-width: 760px; margin: 40px auto 0; font-size: 0.9rem; color: var(--slate); line-height: 1.6; }

  @media (max-width: 600px) {
    .nav-inner { padding: 12px 20px; }
    .ag-hero { padding: 104px 16px 44px; }
    .ag-body { padding: 24px 16px 64px; }
    .ag-cta { padding: 26px 20px; }
  }
"""

# ─────────────────────────── content ───────────────────────────

ARTICLES = [
dict(
    slug='word-finding-exercises',
    updated='2026-10-21',
    title='Word-Finding Exercises for Aphasia: 8 to Try at Home',
    h1='Word-finding exercises for aphasia: 8 to try at home',
    desc='Simple word-finding exercises for people with aphasia and their caregivers, with cueing tips, how to practice at home, and when to involve a speech therapist.',
    lede='You know exactly what you want to say, but the word won&rsquo;t come. That&rsquo;s one of the most common &mdash; and most frustrating &mdash; parts of aphasia. The good news: word-finding is a skill you can practice. Here are eight exercises you can do at home, plus tips for caregivers who want to help.',
    toc=[('what', 'What word-finding difficulty is'), ('before', 'Before you start'), ('exercises', 'Eight exercises to try'),
         ('caregivers', 'How caregivers can help'), ('omilia', 'How Omilía can help'), ('faq', 'FAQ')],
    body="""
<h2 id="what">What is word-finding difficulty?</h2>
<p>Word-finding difficulty &mdash; also called <strong>anomia</strong> &mdash; is trouble coming up with the right word, especially names for people, places and things. It can feel like a constant &ldquo;tip of the tongue&rdquo; moment. Someone might:</p>
<ul>
  <li>pause for a long time searching for a word,</li>
  <li>use a related word instead (&ldquo;fork&rdquo; for &ldquo;spoon&rdquo;),</li>
  <li>describe the thing instead of naming it (&ldquo;the thing you drink coffee from&rdquo;), or</li>
  <li>use a general word like &ldquo;thing&rdquo; or &ldquo;stuff.&rdquo;</li>
</ul>
<p>Word-finding problems show up in nearly every type of aphasia, whether it follows a stroke, a brain injury or another condition. When it&rsquo;s the main symptom, it&rsquo;s sometimes called <em>anomic aphasia</em>.</p>

<h2 id="before">Before you start</h2>
<ul>
  <li><strong>Check in with your speech-language pathologist (SLP).</strong> They can tell you which exercises fit your goals and how hard to make them.</li>
  <li><strong>Keep sessions short and regular.</strong> Ten to twenty focused minutes most days usually beats one long, tiring session a week.</li>
  <li><strong>Aim for success.</strong> Practice should be challenging but doable. If most attempts end in frustration, make it easier.</li>
  <li><strong>Use words that matter.</strong> Family names, favorite foods and places you go are more useful &mdash; and more motivating &mdash; than random vocabulary.</li>
  <li><strong>Stop when tired.</strong> Fatigue makes word-finding harder. It&rsquo;s fine to end on a good attempt and come back later.</li>
</ul>

<h2 id="exercises">Eight word-finding exercises to try</h2>

<h3>1. Picture naming with cues</h3>
<p>Look at a picture of an everyday object and try to name it. If the word doesn&rsquo;t come, a helper gives cues, starting with the smallest hint and only giving more if needed:</p>
<ol>
  <li><strong>Meaning cue:</strong> &ldquo;You use it to eat soup.&rdquo;</li>
  <li><strong>Sentence cue:</strong> &ldquo;Pass me the salt and the pepper and a&hellip;&rdquo;</li>
  <li><strong>First-sound cue:</strong> &ldquo;It starts with &lsquo;sp&hellip;&rsquo;.&rdquo;</li>
  <li><strong>Say it together</strong>, then try to say it alone.</li>
</ol>
<div class="ag-try"><p><strong>Try it:</strong> pick 10 pictures of things in your kitchen. Name each one, then try the whole set again later in the day.</p></div>

<h3>2. Describe it: features first</h3>
<p>Instead of jumping straight to the name, talk about the object&rsquo;s features: <em>What group does it belong to? What is it used for? Where would you find it? What does it look like? What does it remind you of?</em> Thinking through these features often brings the word with it. SLPs use a structured version of this called <strong>semantic feature analysis</strong>, which is one of the most studied word-finding techniques.</p>
<div class="ag-try"><p><strong>Try it:</strong> for &ldquo;apple&rdquo; &mdash; it&rsquo;s a fruit, you eat it, it grows on trees, it&rsquo;s red or green, it&rsquo;s crunchy. Then say the word.</p></div>

<h3>3. Category naming</h3>
<p>Set a timer for one minute and name as many things as you can in a category: animals, foods, clothing, things in a bathroom. Write down the count and try to beat it another day.</p>

<h3>4. Finish the sentence</h3>
<p>Familiar phrases give the brain a running start. A helper says the beginning and you finish it: &ldquo;You brush your&hellip; <em>teeth</em>.&rdquo; &ldquo;Bread and&hellip; <em>butter</em>.&rdquo; &ldquo;Salt and&hellip; <em>pepper</em>.&rdquo;</p>

<h3>5. Talk around the word</h3>
<p>Sometimes the most useful skill in a real conversation is getting your meaning across even when the exact word won&rsquo;t come. Practice describing things without naming them: &ldquo;the big yellow vehicle that takes kids to school.&rdquo; This strategy is called <strong>circumlocution</strong>, and it keeps conversations moving.</p>

<h3>6. Write it, draw it or gesture it</h3>
<p>For some people, writing the first letter, sketching the object or acting out how it&rsquo;s used helps the spoken word come. Even when it doesn&rsquo;t, it&rsquo;s another way to communicate.</p>

<h3>7. Say it, then use it</h3>
<p>Once you find a word, use it right away in a short sentence: &ldquo;Spoon. I need a spoon.&rdquo; Using new words in context helps them stick, and it&rsquo;s closer to how words are used in real conversation.</p>

<h3>8. Build a personal word list</h3>
<p>Make a list &mdash; or a deck of photo cards &mdash; of the words that matter most in daily life: the names of family members, pets, medications, favorite places and foods. Practice these first; they&rsquo;re the ones you&rsquo;ll use every day.</p>

<h2 id="caregivers">How caregivers can help</h2>
<ul>
  <li><strong>Give time.</strong> Wait a little longer than feels natural before stepping in. Many words arrive after a pause.</li>
  <li><strong>Offer cues, not answers.</strong> Start with a small hint, like what the thing is used for, before giving the first sound or the whole word.</li>
  <li><strong>Ask what they prefer.</strong> Some people want you to supply the word quickly; others want to find it themselves. Ask, and respect the answer.</li>
  <li><strong>Keep it relaxed.</strong> Practice works best when it doesn&rsquo;t feel like a test. Avoid quizzing during stressful moments or in front of others.</li>
  <li><strong>Celebrate effort.</strong> Every attempt is practice, and small wins add up.</li>
</ul>
<p>For everyday conversation tips beyond practice time, see our guide on <a href="/omilia/aphasia-guides/communication-tips/">how to communicate with someone who has aphasia</a>.</p>

<h2 id="omilia">How Omilía can help</h2>
<p>Omilía is an aphasia speech therapy app built to make daily practice simple. Several of its exercises focus on word-finding:</p>
<ul>
  <li><strong>Speak:</strong> press, hold and say what you see in a picture.</li>
  <li><strong>Describe:</strong> put what you see into your own words.</li>
  <li><strong>Write and Draw:</strong> handwrite the word with hints when you need them, or sketch it to help recall.</li>
  <li><strong>Make-your-own flash cards:</strong> add the words and photos that matter most &mdash; family, pets, favorite places &mdash; and practice them every day.</li>
</ul>
<p>Each day starts with a fresh plan, exercises adjust in difficulty as you improve, and if you work with a speech therapist, they can assign homework and see your progress through the <a href="/omilia/#therapists">Omilía Therapist</a> app.</p>

<div class="ag-note warn"><p><strong>Important:</strong> new or suddenly worse trouble speaking or understanding can be a sign of a stroke. Call 911 or your local emergency number right away.</p></div>
""",
    faq=[
        ('Can word-finding improve years after a stroke?',
         'Many people keep making progress for months and even years after a stroke, especially with regular practice. Progress is different for everyone, so a speech-language pathologist is the best person to set realistic goals.'),
        ('How often should you practice word-finding exercises?',
         'Short, regular sessions tend to work best, such as 10 to 20 minutes on most days. Your speech-language pathologist can recommend a schedule that fits your goals and energy levels.'),
        ('Is anomia the same as aphasia?',
         'Not exactly. Anomia means difficulty finding words, and it is a symptom of almost every type of aphasia. When word-finding difficulty is the main symptom, it is sometimes called anomic aphasia.'),
        ('Should I finish sentences for someone with aphasia?',
         'Give them time first, and offer small hints before giving the whole word. Preferences differ, so ask the person whether they want help finding words and how much.'),
        ('Are word-finding apps a replacement for speech therapy?',
         'No. Apps like Omilía are designed to support practice at home between sessions, not to replace a speech-language pathologist.'),
    ],
),
dict(
    slug='communication-tips',
    updated='2026-10-21',
    title='How to Communicate With Someone Who Has Aphasia',
    h1='How to communicate with someone who has aphasia',
    desc='Practical communication tips for families and caregivers of people with aphasia: how to talk, listen, use gestures and pictures, and keep conversations going.',
    lede='When someone you love has aphasia, everyday conversation can suddenly feel hard for both of you. A few simple changes in how you talk and listen can make a big difference. Here&rsquo;s a practical guide for family members, friends and caregivers.',
    toc=[('what', 'What aphasia is &mdash; and isn&rsquo;t'), ('talking', 'Tips for talking'), ('listening', 'Tips for listening'),
         ('tools', 'Tools that help'), ('yourself', 'Taking care of yourself'), ('omilia', 'How Omil&iacute;a can help'), ('faq', 'FAQ')],
    body="""
<h2 id="what">What aphasia is &mdash; and isn&rsquo;t</h2>
<p>Aphasia is a language disorder. It most often follows a stroke or brain injury, and it can affect speaking, understanding, reading and writing in different ways for different people.</p>
<p>The most important thing to remember: <strong>aphasia affects language, not intelligence.</strong> The person still has their thoughts, opinions, memories and personality. They just have trouble getting words in or out. Treating them as the capable adult they are is the foundation of every tip below.</p>

<h2 id="talking">Tips for talking</h2>
<h3>Set up the conversation</h3>
<ul>
  <li><strong>Get their attention first.</strong> Say their name, make eye contact, and face them.</li>
  <li><strong>Cut background noise.</strong> Turn off the TV or move somewhere quieter. Distractions make understanding much harder.</li>
  <li><strong>One conversation at a time.</strong> Group conversations move fast. In a group, slow the pace and make room for them to join in.</li>
</ul>
<h3>Keep it clear</h3>
<ul>
  <li><strong>Use short, simple sentences</strong> with one idea at a time.</li>
  <li><strong>Slow down a little</strong> and pause between ideas &mdash; but keep a natural rhythm.</li>
  <li><strong>Don&rsquo;t raise your voice.</strong> Aphasia isn&rsquo;t a hearing problem. Speaking louder doesn&rsquo;t help and can feel patronizing.</li>
  <li><strong>Use a normal adult tone.</strong> Avoid talking down or speaking as if they aren&rsquo;t there.</li>
</ul>
<h3>Make it easier to answer</h3>
<ul>
  <li><strong>Ask yes/no questions</strong> when you need a clear answer: &ldquo;Do you want coffee?&rdquo;</li>
  <li><strong>Offer choices:</strong> &ldquo;Coffee or tea?&rdquo; &mdash; and show the options if you can.</li>
  <li><strong>Add gestures, pictures and written key words.</strong> Pointing, showing a photo or writing one key word down can make your message much easier to understand.</li>
</ul>

<h2 id="listening">Tips for listening</h2>
<ul>
  <li><strong>Give time.</strong> Wait patiently while they search for words. Silence is okay.</li>
  <li><strong>Accept every way of communicating.</strong> Gestures, pointing, drawing, writing and facial expressions all count.</li>
  <li><strong>Ask before you help.</strong> Some people want you to suggest the word; others want to find it themselves. Ask what they prefer.</li>
  <li><strong>Check that you understood.</strong> Repeat back what you think they meant: &ldquo;So you want to call your sister?&rdquo;</li>
  <li><strong>Don&rsquo;t pretend to understand.</strong> It&rsquo;s better to say &ldquo;I&rsquo;m not getting it yet &mdash; let&rsquo;s try another way&rdquo; than to nod along.</li>
  <li><strong>Focus on the message, not mistakes.</strong> Correcting every wrong word is discouraging. What matters is understanding each other.</li>
  <li><strong>Take a break if it&rsquo;s not working.</strong> Frustration is normal. Come back to it later.</li>
</ul>

<h2 id="tools">Tools that help</h2>
<ul>
  <li><strong>A communication notebook or board</strong> with photos and key words: family names, places, foods, feelings, and common needs like &ldquo;tired,&rdquo; &ldquo;pain&rdquo; or &ldquo;bathroom.&rdquo;</li>
  <li><strong>A calendar and a map</strong> to point to when talking about times and places.</li>
  <li><strong>A rating scale</strong> (1&ndash;10, or simple faces) for questions like &ldquo;How&rsquo;s your pain today?&rdquo;</li>
  <li><strong>Paper and a pen</strong> close by, for writing or drawing key words.</li>
  <li><strong>Photos on a phone or tablet</strong> to show people, places and things you want to talk about.</li>
</ul>
<p>A speech-language pathologist (SLP) can help you build these tools around the person&rsquo;s strengths, and can coach the whole family on communication strategies.</p>

<h2 id="yourself">Taking care of yourself</h2>
<p>Supporting someone with aphasia is meaningful &mdash; and tiring. Caregivers need support too:</p>
<ul>
  <li><strong>Ask the SLP to include you</strong> in sessions or give you strategies to use at home.</li>
  <li><strong>Find a support group.</strong> Aphasia and stroke support groups, in person or online, connect you with families who understand.</li>
  <li><strong>Share the load.</strong> Let other family members and friends learn the same communication tips so it doesn&rsquo;t all fall on you.</li>
  <li><strong>Take breaks</strong> without guilt.</li>
</ul>

<h2 id="omilia">How Omil&iacute;a can help</h2>
<p>Omil&iacute;a is an aphasia speech therapy app built for home practice. For families, it offers a daily plan you can sit down and do together, with progress you can actually see. You can make your own flash cards with the photos and words that matter most &mdash; family names, pets, favorite places &mdash; which double as a simple communication tool. And if your loved one works with a speech therapist, the therapist can assign homework and follow progress through <a href="/omilia/#therapists">Omil&iacute;a Therapist</a>.</p>
<p>Looking for practice ideas? See our guide to <a href="/omilia/aphasia-guides/word-finding-exercises/">word-finding exercises for aphasia</a>.</p>

<div class="ag-note warn"><p><strong>Important:</strong> new or suddenly worse trouble speaking or understanding can be a sign of a stroke. Call 911 or your local emergency number right away.</p></div>
""",
    faq=[
        ('Does aphasia affect intelligence?',
         'No. Aphasia affects language, not intelligence. People with aphasia keep their thoughts, memories, opinions and personality, even when finding or understanding words is hard.'),
        ('Should I speak louder to someone with aphasia?',
         'No, unless they also have hearing loss. Speaking slowly and clearly, with short sentences, helps much more than speaking louder.'),
        ('Is it okay to finish sentences for someone with aphasia?',
         'Give them time first, and ask what they prefer. Some people welcome a suggested word, while others want to find it themselves.'),
        ('What is a communication board for aphasia?',
         'A communication board or notebook has pictures and key words, such as family names, places, foods and common needs, that a person with aphasia can point to when words are hard to find.'),
        ('Where can caregivers of people with aphasia find support?',
         'A speech-language pathologist is a good first stop for strategies. Aphasia and stroke support groups, in person or online, can also connect caregivers with others who understand.'),
    ],
),
]

# ─────────────────────────── rendering ───────────────────────────

def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s)


def render(a):
    path = f'{GUIDES}{a["slug"]}/'
    url = BASE + path
    og = BASE + '/omilia/images/og.jpg'
    ld = [
        {"@context": "https://schema.org", "@type": "Article", "headline": strip_tags(a['h1']), "description": a['desc'],
         "image": og, "datePublished": a['updated'], "dateModified": a['updated'],
         "author": {"@type": "Organization", "name": "Omilía by Happy Path Apps", "url": BASE + '/omilia/'},
         "publisher": {"@type": "Organization", "name": "Happy Path Apps", "logo": {"@type": "ImageObject", "url": BASE + '/images/logo.png'}},
         "about": {"@type": "MedicalCondition", "name": "Aphasia"},
         "mainEntityOfPage": url},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Omilía", "item": BASE + '/omilia/'},
            {"@type": "ListItem", "position": 2, "name": strip_tags(a['h1']), "item": url}]},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in a['faq']]},
    ]
    toc = ''.join(f'<li><a href="#{i}">{label}</a></li>' for i, label in a['toc'])
    faq = '\n'.join(f'<details><summary>{escape(q)}</summary><p>{escape(ans)}</p></details>' for q, ans in a['faq'])
    tags = [
        f'<title>{escape(a["title"])}</title>',
        f'<meta name="description" content="{escape(a["desc"])}">',
        f'<link rel="canonical" href="{url}">',
        '<link rel="icon" type="image/png" href="/omilia/images/omilia-icon.png">',
        '<meta name="apple-itunes-app" content="app-id=1602156122">',
        '<meta property="og:type" content="article">',
        '<meta property="og:site_name" content="Happy Path Apps">',
        f'<meta property="og:title" content="{escape(a["title"])}">',
        f'<meta property="og:description" content="{escape(a["desc"])}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{og}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{escape(a["title"])}">',
        f'<meta name="twitter:description" content="{escape(a["desc"])}">',
        f'<meta name="twitter:image" content="{og}">',
    ] + ['<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + '</script>' for d in ld]
    html = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n' + '\n'.join(tags) + '\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@400;600;700;800&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">\n'
            '<style>' + base_css + footer_css + PAGE_CSS + '</style>\n</head>\n<body>\n\n' + nav_html + f"""

<section class="ag-hero">
  <div class="ag-hero-inner fade-up">
    <div class="ag-crumbs" role="navigation" aria-label="Breadcrumb"><a href="/omilia/">Omil&iacute;a</a> <span>/</span> <span>Aphasia guides</span></div>
    <h1>{a['h1']}</h1>
    <p class="ag-lede">{a['lede']}</p>
    <div class="ag-meta"><img src="/omilia/images/omilia-icon.png" alt=""><span>By the <strong>Omil&iacute;a</strong> team</span><span>&middot;</span><span>Updated {datetime.date.fromisoformat(a['updated']).strftime('%B %-d, %Y')}</span></div>
  </div>
</section>

<section class="ag-body">
  <article class="ag-article">
    <div class="ag-toc"><strong>In this guide</strong><ol>{toc}</ol></div>
{a['body']}
    <h2 id="faq">Frequently asked questions</h2>
    <div class="ag-faq">
{faq}
    </div>
  </article>

  <div class="ag-cta fade-up">
    <img class="icon" src="/omilia/images/omilia-icon.png" alt="">
    <h2>Practice a little every day</h2>
    <p>Omil&iacute;a gives you a fresh plan of speech therapy exercises each day, with big clear pictures and encouragement after every answer. Try it free for 7 days.</p>
    <div class="badges">
      <a href="{APP_STORE}" target="_blank" rel="noopener" class="store-badge" aria-label="Download Omilía on the App Store">{APPLE_SVG}<span class="store-badge-text"><small>Download on the</small><strong>App Store</strong></span></a>
      <a class="therapist" href="/omilia/#therapists">Speech therapist? See Omil&iacute;a Therapist &rarr;</a>
    </div>
  </div>

  <p class="ag-disclaimer">This guide is for general education and isn&rsquo;t medical advice. Every person&rsquo;s recovery is different &mdash; work with a licensed speech-language pathologist on a plan that&rsquo;s right for you.</p>
</section>

""" + footer_html + '\n\n' + script_html + '\n</body>\n</html>\n')
    out = path.strip('/') + '/index.html'
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(html)
    print('wrote', out)


if __name__ == '__main__':
    for a in ARTICLES:
        render(a)
