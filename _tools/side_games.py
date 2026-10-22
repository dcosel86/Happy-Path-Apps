"""Generates the golf side-game rules pages under /onlyBirdies/golf-side-games/.

Run from the repo root:  python3 _tools/side_games.py

Shared nav, styles and footer are copied from onlyBirdies/index.html so the
pages stay in sync with the app page. Folders starting with "_" are not
published by GitHub Pages.
"""
import json
import os
import re
from html import escape

BASE = 'https://happypathapps.co'
HUB = '/onlyBirdies/golf-side-games/'
APP_STORE = 'https://apps.apple.com/us/app/onlybirdies-golf-scorecard/id6749419654'
PLAY = 'https://play.google.com/store/apps/details?id=com.happypathapps.golfpad'
UPDATED = '2026-10-21'

ob = open('onlyBirdies/index.html', encoding='utf-8').read()
base_css = ob[ob.index('<style>') + len('<style>'):ob.index('  /* ══════════════════════════════════════\n     ONLYBIRDIES PAGE')]
footer_css = ob[ob.index('  /* Footer */'):ob.index('  /* ─── RESPONSIVE ─── */')]
nav_html = ob[ob.index('<nav id="navbar">'):ob.index('</nav>') + len('</nav>')]
nav_html = nav_html.replace('<a href="/onlyBirdies/" class="active">', '<a href="/onlyBirdies/">')
footer_html = ob[ob.index('<div class="ob-footer">'):ob.index('<script>')].rstrip()
footer_html = footer_html.replace('<a href="privacy-policy.html">', '<a href="/onlyBirdies/privacy-policy.html">')
footer_html = footer_html.replace('<a href="/">Home</a>', '<a href="/">Home</a>\n      <a href="/onlyBirdies/">OnlyBirdies</a>')
script_html = ob[ob.index('<script>', ob.index('<div class="ob-footer">')):ob.rindex('</script>') + len('</script>')]

APPLE_SVG = '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'
PLAY_SVG = '<svg viewBox="0 0 512 512" aria-hidden="true" style="width:26px;height:28px;"><path d="M325.3 234.3L104.6 13l280.8 161.2-60.1 60.1zM47 0C34 6.8 25.3 19.2 25.3 35.3v441.3c0 16.1 8.7 28.5 21.7 35.3l256.6-256L47 0zm425.2 225.6l-58.9-34.1-65.7 64.5 65.7 64.5 60.1-34.1c18-14.3 18-46.5-1.2-60.8zM104.6 499l280.8-161.2-60.1-60.1L104.6 499z"/></svg>'
BADGES = (f'<a href="{APP_STORE}" target="_blank" rel="noopener" class="store-badge" aria-label="Download OnlyBirdies on the App Store">{APPLE_SVG}'
          '<span class="store-badge-text"><small>Download on the</small><strong>App Store</strong></span></a>\n'
          f'        <a href="{PLAY}" target="_blank" rel="noopener" class="store-badge" aria-label="Get OnlyBirdies on Google Play">{PLAY_SVG}'
          '<span class="store-badge-text"><small>Get it on</small><strong>Google Play</strong></span></a>')

PAGE_CSS = """
  /* ══════════════════════════════════════
     SIDE GAME GUIDES
     ══════════════════════════════════════ */
  .sg-hero {
    position: relative; overflow: hidden; padding: 130px 32px 70px;
    background: linear-gradient(180deg, #F8FCF6 0%, var(--green-50) 70%, #FFFFFF 100%);
  }
  .sg-hero-inner { max-width: 860px; margin: 0 auto; }
  .sg-crumbs { display: flex; flex-wrap: wrap; gap: 6px; font-size: 0.9rem; color: var(--slate); margin-bottom: 22px; }
  .sg-crumbs a { color: var(--slate); text-decoration: none; }
  .sg-crumbs a:hover { color: var(--forest); text-decoration: underline; }
  .sg-hero-title { display: flex; align-items: center; gap: 18px; }
  .sg-hero-title img { width: 64px; height: 64px; border-radius: 50%; flex-shrink: 0; box-shadow: 0 8px 24px rgba(14,59,12,0.15); }
  .sg-hero h1 { font-size: clamp(2.2rem, 5vw, 3.4rem); font-weight: 800; line-height: 1.05; color: var(--night); letter-spacing: -1px; }
  .sg-lede { font-size: 1.18rem; color: var(--slate); line-height: 1.7; margin-top: 20px; }
  .sg-facts { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-top: 30px; }
  .sg-fact { background: white; border: 1px solid var(--green-100); border-radius: 16px; padding: 14px 16px; }
  .sg-fact small { display: block; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.8px; text-transform: uppercase; color: var(--slate); }
  .sg-fact strong { display: block; margin-top: 4px; color: var(--night); font-size: 1rem; }

  .sg-body { padding: 40px 32px 90px; }
  .sg-article { max-width: 760px; margin: 0 auto; font-size: 1.08rem; line-height: 1.75; color: var(--ink); }
  .sg-article h2 { font-size: 1.75rem; color: var(--night); margin: 48px 0 14px; letter-spacing: -0.3px; }
  .sg-article h3 { font-size: 1.2rem; color: var(--night); margin: 28px 0 8px; }
  .sg-article p { margin-top: 14px; }
  .sg-article ul, .sg-article ol { margin: 14px 0 0 22px; }
  .sg-article li { margin-top: 8px; }
  .sg-article strong { color: var(--night); }
  .sg-article a { color: var(--forest); font-weight: 600; text-decoration-color: rgba(14,59,12,0.3); text-underline-offset: 3px; }
  .sg-article a:hover { text-decoration-color: currentColor; }
  .sg-table-wrap { overflow-x: auto; margin-top: 20px; border: 1px solid var(--green-100); border-radius: 16px; }
  .sg-article table { width: 100%; border-collapse: collapse; font-size: 0.98rem; }
  .sg-article th, .sg-article td { padding: 11px 14px; text-align: left; border-bottom: 1px solid var(--green-100); white-space: nowrap; }
  .sg-article th { background: var(--green-50); color: var(--night); font-weight: 700; }
  .sg-article tr:last-child td { border-bottom: none; }
  .sg-article td.win { color: var(--forest); font-weight: 700; }
  .sg-callout {
    margin-top: 24px; padding: 18px 22px; border-radius: 16px;
    background: var(--green-50); border-left: 4px solid var(--green);
  }
  .sg-callout p:first-child { margin-top: 0; }

  .sg-faq details { border-bottom: 1px solid var(--green-100); padding: 16px 0; }
  .sg-faq summary { cursor: pointer; font-weight: 700; color: var(--night); list-style: none; display: flex; justify-content: space-between; gap: 16px; }
  .sg-faq summary::-webkit-details-marker { display: none; }
  .sg-faq summary::after { content: '+'; color: var(--green); font-size: 1.3rem; line-height: 1; }
  .sg-faq details[open] summary::after { content: '\\2212'; }
  .sg-faq details p { margin-top: 10px; }

  .sg-cta {
    margin: 56px auto 0; max-width: 760px; padding: 34px; border-radius: 24px; text-align: center;
    background: var(--night); color: white; position: relative; overflow: hidden;
  }
  .sg-cta::before {
    content: ''; position: absolute; inset: 0;
    background: radial-gradient(circle at 15% 20%, rgba(76,187,60,0.35), transparent 50%);
  }
  .sg-cta > * { position: relative; }
  .sg-cta img.icon { width: 64px; height: 64px; border-radius: 15px; }
  .sg-cta h2 { color: white; font-size: 1.7rem; margin-top: 14px; }
  .sg-cta p { color: rgba(255,255,255,0.72); margin-top: 10px; line-height: 1.6; }
  .sg-cta .badges { display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; margin-top: 22px; }

  .sg-more { padding: 80px 32px 100px; background: var(--green-50); }
  .sg-more-inner { max-width: 1100px; margin: 0 auto; }
  .sg-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 16px; margin-top: 32px; }
  .sg-card {
    display: block; background: white; border: 1px solid var(--green-100); border-radius: var(--radius);
    padding: 24px; text-decoration: none; color: inherit; transition: transform 0.25s, box-shadow 0.25s;
  }
  a.sg-card:hover { transform: translateY(-4px); box-shadow: 0 12px 30px rgba(14,59,12,0.1); }
  .sg-card img { width: 52px; height: 52px; border-radius: 50%; }
  .sg-card h3 { font-size: 1.15rem; color: var(--night); margin-top: 12px; }
  .sg-card p { font-size: 0.93rem; color: var(--slate); line-height: 1.55; margin-top: 6px; }
  .sg-card .go { display: inline-block; margin-top: 12px; font-weight: 700; font-size: 0.9rem; color: var(--forest); }
  .sg-card.soon { background: transparent; border-style: dashed; }
  .sg-card.soon .go { color: var(--slate); font-weight: 600; }

  @media (max-width: 760px) {
    .sg-facts { grid-template-columns: repeat(2, 1fr); }
  }
  @media (max-width: 600px) {
    .nav-inner { padding: 12px 20px; }
    .sg-hero { padding: 104px 16px 48px; }
    .sg-body { padding: 28px 16px 64px; }
    .sg-more { padding: 56px 16px 72px; }
    .sg-cta { padding: 26px 20px; }
    .sg-hero-title img { width: 52px; height: 52px; }
  }
"""

# ─────────────────────────── content ───────────────────────────

GAMES = [
    dict(slug='nassau', name='Nassau', icon='game-nassau.jpg',
         short='Three bets in one: the front nine, the back nine and the full 18.'),
    dict(slug='skins', name='Skins', icon='game-skins.jpg',
         short='Win a hole outright to take the skin. Ties carry the pot to the next hole.'),
    dict(slug='wolf', name='Wolf', icon='game-wolf.jpg',
         short='A rotating Wolf picks a partner after each drive, or goes it alone for double.'),
    dict(slug='vegas', name='Vegas', icon='game-vegas.jpg',
         short='Two-player teams pair their scores into a two-digit number. Lowest number wins.'),
    dict(slug='snake', name='Snake', icon='game-snake.jpg',
         short='Three-putt and you hold the snake. Whoever holds it at the end pays up.'),
    dict(slug='nine-point', name='9-Point', icon='game-nine-point.jpg',
         short='Three players split nine points on every hole based on their scores.'),
    dict(slug='dots', name='Dots', icon='game-dots.jpg',
         short='Earn points for birdies, sandies, greenies and other good shots.'),
]
WRITTEN = {g['slug'] for g in GAMES}

ARTICLES = {}

ARTICLES['nassau'] = dict(
    title='Nassau Golf Bet: Rules, Scoring & Examples',
    h1='How to play a Nassau in golf',
    desc='Nassau golf bet rules explained: three bets on the front nine, back nine and full 18, how presses work, and a worked $5 Nassau example.',
    lede='The Nassau is the most popular bet in golf. It splits one round into three separate bets — the front nine, the back nine and the overall 18 — so a bad start never takes you out of the game.',
    facts=[('Players', '2, or two teams of 2'), ('Format', 'Match play or stroke play'), ('Bets', '3 per round'), ('Difficulty', 'Easy')],
    body="""
<h2>How a Nassau works</h2>
<p>A Nassau is really three bets played at the same time, each for the same stake:</p>
<ol>
  <li><strong>The front nine</strong> &mdash; holes 1&ndash;9.</li>
  <li><strong>The back nine</strong> &mdash; holes 10&ndash;18.</li>
  <li><strong>The overall</strong> &mdash; all 18 holes.</li>
</ol>
<p>A &ldquo;$5 Nassau&rdquo; means $5 on each of the three bets, so the most you can win or lose (before any presses) is $15. You&rsquo;ll also hear it called &ldquo;5-5-5.&rdquo; Some groups weight the overall higher, like $5-$5-$10.</p>
<p>Most Nassaus are played as <strong>match play</strong>: you win, lose or tie each hole, and whoever wins more holes in a segment wins that bet. You can also play it as <strong>stroke play</strong>, where the lowest total score for each nine (and for the 18) wins.</p>

<h2>Scoring a match-play Nassau</h2>
<p>In match play, the score is kept as how many holes one player is &ldquo;up.&rdquo; Win a hole and you go 1 up; lose the next and you&rsquo;re back to all square (&ldquo;AS&rdquo;). A segment ends when one player is up by more holes than remain, or when the last hole of that segment is played.</p>
<div class="sg-callout"><p><strong>Tip:</strong> The overall isn&rsquo;t a separate match you track from scratch &mdash; it&rsquo;s simply the running total of holes won across all 18. If you win the front 2 up and lose the back 1 down, you win the overall 1 up.</p></div>

<h2>A worked example: $5 Nassau</h2>
<p>David and Joe play a $5 match-play Nassau.</p>
<div class="sg-table-wrap"><table>
  <thead><tr><th>Bet</th><th>Result</th><th>Winner</th><th>Payout</th></tr></thead>
  <tbody>
    <tr><td>Front nine</td><td>David wins 2 up</td><td class="win">David</td><td>Joe pays $5</td></tr>
    <tr><td>Back nine</td><td>Joe wins 1 up</td><td class="win">Joe</td><td>David pays $5</td></tr>
    <tr><td>Overall 18</td><td>David wins 1 up (2 &minus; 1)</td><td class="win">David</td><td>Joe pays $5</td></tr>
    <tr><td><strong>Net</strong></td><td></td><td></td><td><strong>Joe owes David $5</strong></td></tr>
  </tbody>
</table></div>

<h2>Presses</h2>
<p>A <strong>press</strong> is a new side bet that starts mid-segment, usually offered by the player who&rsquo;s losing. It covers the remaining holes of that nine and is worth the same stake as the original bet. Presses are what turn a friendly $5 Nassau into a real game.</p>
<ul>
  <li><strong>Manual press:</strong> the player who is down can call a press at any time (some groups only allow it once you&rsquo;re 2 down).</li>
  <li><strong>Automatic press (&ldquo;2-down auto&rdquo;):</strong> a new bet starts automatically whenever a player falls 2 holes behind in any active bet.</li>
  <li><strong>Pressing a press:</strong> if you fall 2 down in a press, it can be pressed again &mdash; agree on a limit before you tee off.</li>
</ul>
<p><strong>Example:</strong> Joe is 2 down after hole 5 and presses. A new $5 bet covers holes 6&ndash;9. Joe wins three of those four holes, so he wins the press even though he still loses the front nine overall.</p>

<h2>Playing a Nassau with handicaps</h2>
<p>For a fair game between players of different abilities, use net scores. Take the difference between the two players&rsquo; course handicaps; the higher-handicap player gets that many strokes, applied on the hardest holes by handicap index (the &ldquo;HCP&rdquo; row on the scorecard).</p>

<h2>Four-ball Nassau</h2>
<p>With four players, split into two teams of two and play best ball: each team takes its lower score on every hole. Everything else &mdash; front, back, overall and presses &mdash; works the same way.</p>
""",
    faq=[
        ('How much is a $5 Nassau?', 'A $5 Nassau is three $5 bets: front nine, back nine and overall. Without presses, the most you can win or lose is $15.'),
        ('Is the overall bet a separate match?', 'No. The overall is decided by the total holes won over all 18. If you win the front 2 up and lose the back 1 down, you win the overall 1 up.'),
        ('What happens if a Nassau bet is tied?', 'A tied segment is a push: nobody pays for that bet. Some groups play extra holes to settle the overall, but most just call it even.'),
        ('What is a press in a Nassau?', 'A press is a new bet, for the same stake, that starts partway through a nine and runs to the end of it. It is usually called by the player who is losing, often once they are 2 holes down.'),
        ('Why is it called a Nassau?', 'The format is widely credited to the Nassau Country Club on Long Island, New York, around the turn of the 20th century.'),
    ],
)

ARTICLES['skins'] = dict(
    title='Skins Golf Game: Rules, Carryovers & Payouts',
    h1='How to play Skins in golf',
    desc='Skins golf game rules explained: winning a hole outright, how carryovers work, how to pay out, and a worked four-player example.',
    lede='Skins turns every hole into its own prize. Make the lowest score on a hole, all by yourself, and you win the skin. Tie, and the skin carries over &mdash; so one great hole late in the round can win a pile of them.',
    facts=[('Players', '2 to 4+ (best with 3&ndash;4)'), ('Format', 'Hole by hole'), ('Bets', '18 skins, one per hole'), ('Difficulty', 'Easy')],
    body="""
<h2>How Skins works</h2>
<p>Every hole is worth one skin. To win it, you need the <strong>lowest score on the hole outright</strong> &mdash; no ties. If two or more players share the low score, nobody wins that skin.</p>
<p>Before the round, agree on what a skin is worth. In OnlyBirdies, as in many groups, a skin is worth the stake from <strong>each</strong> other player: in a $5 skins game with four players, winning one skin earns you $15 ($5 from each of the other three).</p>

<h2>Carryovers</h2>
<p>When a hole is tied, the skin usually <strong>carries over</strong> to the next hole. The next outright winner takes every skin that has built up. Carryovers are what make Skins exciting: three tied holes in a row means the fourth hole is worth four skins.</p>
<p>If you&rsquo;d rather keep things small, play <strong>without carryovers</strong> &mdash; a tied hole&rsquo;s skin simply disappears.</p>

<h2>A worked example: $5 skins, four players</h2>
<p>Anne, Ben, Cal and Dev play $5 skins with carryovers. Here are the first five holes:</p>
<div class="sg-table-wrap"><table>
  <thead><tr><th>Hole</th><th>Anne</th><th>Ben</th><th>Cal</th><th>Dev</th><th>Result</th></tr></thead>
  <tbody>
    <tr><td>1</td><td>4</td><td>4</td><td>5</td><td>5</td><td>Tie &mdash; 1 skin carries</td></tr>
    <tr><td>2</td><td class="win">3</td><td>4</td><td>4</td><td>5</td><td>Anne wins 2 skins</td></tr>
    <tr><td>3</td><td>4</td><td>4</td><td>4</td><td>4</td><td>Tie &mdash; 1 skin carries</td></tr>
    <tr><td>4</td><td>4</td><td class="win">3</td><td>4</td><td>4</td><td>Ben wins 2 skins</td></tr>
    <tr><td>5</td><td>5</td><td>5</td><td class="win">4</td><td>5</td><td>Cal wins 1 skin</td></tr>
  </tbody>
</table></div>
<p>Each skin pays its winner $5 from each of the other three players. After five holes:</p>
<div class="sg-table-wrap"><table>
  <thead><tr><th>Player</th><th>Skins</th><th>Won</th><th>Paid out</th><th>Net</th></tr></thead>
  <tbody>
    <tr><td>Anne</td><td>2</td><td>+$30</td><td>&minus;$15 (Ben 2, Cal 1)</td><td class="win">+$15</td></tr>
    <tr><td>Ben</td><td>2</td><td>+$30</td><td>&minus;$15 (Anne 2, Cal 1)</td><td class="win">+$15</td></tr>
    <tr><td>Cal</td><td>1</td><td>+$15</td><td>&minus;$20 (Anne 2, Ben 2)</td><td>&minus;$5</td></tr>
    <tr><td>Dev</td><td>0</td><td>$0</td><td>&minus;$25 (all 5 skins)</td><td>&minus;$25</td></tr>
  </tbody>
</table></div>
<p>The nets add up to zero, which is a handy way to check your math.</p>

<h2>What if the last hole ties?</h2>
<p>Decide this before you tee off. The common options are:</p>
<ul>
  <li><strong>Play it off</strong> on extra holes until someone wins outright.</li>
  <li><strong>Split</strong> the carried skins evenly among the players who tied on 18.</li>
  <li><strong>Let them go</strong> &mdash; nobody wins the leftover skins.</li>
</ul>

<h2>Popular variations</h2>
<h3>Net skins</h3>
<p>Players get handicap strokes on the hardest holes, so a bogey with a stroke can beat a par. Net skins keeps the game fair for mixed groups.</p>
<h3>Validated skins</h3>
<p>To claim a skin you have to &ldquo;validate&rdquo; it by tying or winning the next hole. This rewards consistency and stops one lucky hole from winning everything.</p>
<h3>Pot skins</h3>
<p>Instead of paying per skin, everyone puts the same amount in a pot. At the end, the pot is divided by the total number of skins won, and each player collects for the skins they hold. This is common in large groups and club events.</p>
""",
    faq=[
        ('Do you need to win a hole outright to win a skin?', 'Yes. A skin goes only to the player with the lowest score on the hole by themselves. If the low score is tied, nobody wins it and it usually carries over.'),
        ('How do carryovers work in skins?', 'When a hole is tied, its skin is added to the next hole. The next player to win a hole outright collects every skin that has built up.'),
        ('How do you pay out skins?', 'Most groups pay each skin winner the agreed stake from every other player. In a $5 game with four players, one skin is worth $15 to the winner. Pot skins is the other common method.'),
        ('What happens if the 18th hole is tied in skins?', 'Agree before the round: play extra holes, split the carried skins among the tied players, or let them go unclaimed.'),
        ('Can you play skins with handicaps?', 'Yes. In net skins, players receive strokes on the hardest holes by handicap index, and skins are decided on net scores.'),
    ],
)

ARTICLES['wolf'] = dict(
    title='Wolf Golf Game: Rules, Points & Strategy',
    h1='How to play Wolf in golf',
    desc='Wolf golf game rules explained: the rotating Wolf, picking a partner after each drive, Lone Wolf and Blind Wolf, points scoring and a worked example.',
    lede='Wolf is the four-player game that makes every tee shot matter. Each hole, one player is the Wolf and decides &mdash; drive by drive &mdash; whether to pick a partner or take on the other three alone.',
    facts=[('Players', '4 (best)'), ('Format', 'Best ball, hole by hole'), ('Scoring', 'Points'), ('Difficulty', 'Medium')],
    body="""
<h2>How Wolf works</h2>
<ol>
  <li><strong>Set the order.</strong> On the first tee, decide a hitting order (a ball toss works). That order rotates each hole, and the Wolf rotates with it, so everyone is the Wolf about four times through 16 holes.</li>
  <li><strong>The Wolf watches the drives.</strong> In the most common version, the Wolf tees off first and then watches the other three hit in order.</li>
  <li><strong>Pick a partner &mdash; right away.</strong> After each player&rsquo;s drive, the Wolf must decide immediately whether that player is their partner. Pass on someone and you can&rsquo;t go back to them.</li>
  <li><strong>Or go Lone Wolf.</strong> If the Wolf passes on everyone, they play the hole alone against the other three, for bigger points.</li>
  <li><strong>Play best ball.</strong> Each side uses its best score on the hole. Lower best ball wins the hole; a tie means no points.</li>
</ol>

<h2>Lone Wolf and Blind Wolf</h2>
<p><strong>Lone Wolf:</strong> the Wolf decides to play alone after seeing the drives. Their single score has to beat the best of the other three.</p>
<p><strong>Blind Wolf:</strong> the Wolf declares they&rsquo;re going alone <em>before anyone tees off</em> &mdash; including themselves. It&rsquo;s the boldest call in the game and pays the most. OnlyBirdies shows when the current Wolf has gone blind right at the top of the scorecard.</p>

<h2>Scoring Wolf with points</h2>
<p>Groups use a lot of different point systems. Here&rsquo;s a popular one:</p>
<div class="sg-table-wrap"><table>
  <thead><tr><th>Outcome</th><th>Points</th></tr></thead>
  <tbody>
    <tr><td>Wolf and partner win the hole</td><td>2 points each to the Wolf and partner</td></tr>
    <tr><td>The other two win the hole</td><td>3 points each to the two opponents</td></tr>
    <tr><td>Lone Wolf wins the hole</td><td>4 points to the Wolf</td></tr>
    <tr><td>Lone Wolf loses the hole</td><td>1 point each to the three opponents</td></tr>
    <tr><td>Blind Wolf wins / loses</td><td>Usually double the Lone Wolf points</td></tr>
    <tr><td>Hole is tied</td><td>No points (some groups carry them over)</td></tr>
  </tbody>
</table></div>
<p>At the end of the round, points are settled at an agreed value. A common way is to pay the difference: if you finish with 14 points and a friend has 9, they owe you 5 points&rsquo; worth.</p>

<h2>A worked example</h2>
<p>On hole 3, Cal is the Wolf. He hits a good drive, then watches: Anne pulls hers into the trees (pass), Ben hits it 280 down the middle &mdash; &ldquo;Ben, you&rsquo;re with me.&rdquo; Dev is now on Anne&rsquo;s side.</p>
<div class="sg-table-wrap"><table>
  <thead><tr><th>Team</th><th>Scores</th><th>Best ball</th><th>Points</th></tr></thead>
  <tbody>
    <tr><td>Cal (Wolf) &amp; Ben</td><td>5, 4</td><td class="win">4</td><td>+2 each</td></tr>
    <tr><td>Anne &amp; Dev</td><td>6, 5</td><td>5</td><td>0</td></tr>
  </tbody>
</table></div>
<p>On hole 4, Dev is the Wolf. Nobody hits a great drive, so Dev goes Lone Wolf and makes a 4. The best of the other three is a 5. Dev takes 4 points.</p>

<h2>The last two holes</h2>
<p>With four players, 16 holes gives everyone four turns as the Wolf. For holes 17 and 18, the most common rule is that <strong>the player in last place becomes the Wolf</strong> &mdash; a chance to catch up.</p>

<h2>Strategy tips</h2>
<ul>
  <li><strong>Don&rsquo;t grab the first good drive automatically.</strong> If the last player to hit is your group&rsquo;s best golfer, it can pay to wait &mdash; but you risk ending up with nobody.</li>
  <li><strong>Go Lone Wolf on your strong holes.</strong> A short par 3 you play well is the best place to go alone.</li>
  <li><strong>Save Blind Wolf for when you&rsquo;re behind.</strong> It&rsquo;s a big swing, best used late when you need points.</li>
</ul>
""",
    faq=[
        ('How many players do you need for Wolf?', 'Wolf is designed for four players. There are three- and five-player versions, but the rotation and points work best with four.'),
        ('Does the Wolf hit first or last?', 'It varies by group. In the most common version the Wolf tees off first and then watches the other three drives before choosing. Some groups have the Wolf hit last instead.'),
        ('What is a Lone Wolf?', 'A Lone Wolf is when the Wolf passes on every partner and plays the hole alone against the other three, for more points if they win.'),
        ('What is a Blind Wolf?', 'A Blind Wolf is when the Wolf announces they are going alone before anyone tees off on the hole. It is the riskiest call and usually pays double a Lone Wolf.'),
        ('Who is the Wolf on 17 and 18?', 'A common rule is that the player in last place is the Wolf on the final two holes, giving them a chance to catch up.'),
    ],
)

ARTICLES['vegas'] = dict(
    title='Vegas Golf Game: Rules, Scoring & Birdie Flips',
    h1='How to play Vegas in golf',
    desc='Las Vegas golf game rules explained: pairing team scores into two-digit numbers, birdie flips, how points add up, and a worked example.',
    lede='Vegas (or Las Vegas) is a fast-moving team game for a foursome. Each team turns its two scores into a two-digit number, and the lower number wins the difference in points &mdash; so the swings can get big in a hurry.',
    facts=[('Players', '4, in two teams of 2'), ('Format', 'Team, hole by hole'), ('Scoring', 'Points'), ('Difficulty', 'Medium')],
    body="""
<h2>How Vegas works</h2>
<ol>
  <li><strong>Split into two teams of two.</strong> Partners can stay the same all round or rotate every six holes so everyone plays with everyone.</li>
  <li><strong>Make your team number.</strong> On each hole, put the two scores together with the <strong>lower score first</strong>. A 4 and a 5 make <strong>45</strong>; a 3 and a 6 make <strong>36</strong>.</li>
  <li><strong>Lower number wins.</strong> The team with the lower number wins the difference in points. 45 against 56 is an 11-point hole.</li>
  <li><strong>Settle up at the end.</strong> Add up each team&rsquo;s points and pay the difference at an agreed value per point.</li>
</ol>
<div class="sg-callout"><p><strong>Keep the stakes small.</strong> Points add up fast in Vegas &mdash; a single hole can swing 30 points or more &mdash; so most groups play for dimes or quarters a point, or set a cap per hole.</p></div>

<h2>The birdie flip</h2>
<p>The rule that makes Vegas famous: if a player makes a <strong>birdie</strong>, the <em>other</em> team&rsquo;s number is flipped so the higher score goes first. That turns a 45 into a 54 and makes the birdie worth a lot more.</p>
<p>Many groups also flip for an eagle (some double it), and agree that a birdie only flips if the other team didn&rsquo;t make one too.</p>

<h2>Scores of 10 or more</h2>
<p>If a player makes double digits, the usual rule is that the big number goes first: a 4 and a 10 become <strong>104</strong>, not 410. Some groups cap a blow-up hole at double par to keep things friendly.</p>

<h2>A worked example</h2>
<p>Anne &amp; Ben play Cal &amp; Dev for 10 cents a point.</p>
<div class="sg-table-wrap"><table>
  <thead><tr><th>Hole</th><th>Anne &amp; Ben</th><th>Cal &amp; Dev</th><th>Result</th></tr></thead>
  <tbody>
    <tr><td>1</td><td>4, 5 &rarr; <strong>45</strong></td><td>5, 6 &rarr; <strong>56</strong></td><td class="win">Anne &amp; Ben +11</td></tr>
    <tr><td>2</td><td>4, 4 &rarr; <strong>44</strong></td><td>4, 5 &rarr; <strong>45</strong></td><td class="win">Anne &amp; Ben +1</td></tr>
    <tr><td>3</td><td>5, 6 &rarr; flipped to <strong>65</strong></td><td>3 (birdie), 5 &rarr; <strong>35</strong></td><td class="win">Cal &amp; Dev +30</td></tr>
  </tbody>
</table></div>
<p>After three holes Cal &amp; Dev lead 30 to 12, or 18 points. At 10 cents a point, that&rsquo;s $1.80 &mdash; usually split so each player on the losing team pays their opponent 90 cents.</p>

<h2>Variations</h2>
<ul>
  <li><strong>Rotating partners:</strong> switch teams after holes 6 and 12 so nobody is stuck with the same partner.</li>
  <li><strong>Net Vegas:</strong> apply handicap strokes before building the numbers.</li>
  <li><strong>No flips:</strong> skip the birdie rule for a calmer game.</li>
</ul>
""",
    faq=[
        ('How do you make a team number in Vegas golf?', 'Put the two partners’ scores together with the lower score first. A 4 and a 5 make 45. The lower team number wins the hole by the difference.'),
        ('What is the birdie flip in Vegas?', 'If a player makes a birdie, the other team’s number is reversed so the higher score comes first. A 45 becomes a 54, which makes the birdie worth more points.'),
        ('What happens if someone scores 10 or more in Vegas?', 'The usual rule is that the double-digit score goes first, so a 4 and a 10 make 104. Some groups cap scores at double par instead.'),
        ('How much should you play Vegas for?', 'Because points add up quickly, most groups play for small stakes like 10 or 25 cents a point, or cap the points on any one hole.'),
    ],
)

ARTICLES['snake'] = dict(
    title='Snake Golf Game: Rules for the 3-Putt Bet',
    h1='How to play Snake in golf',
    desc='Snake golf game rules explained: how the snake passes on every three-putt, who pays at the end, popular variations and a worked example.',
    lede='Snake is the side game for the greens. Three-putt and you&rsquo;re holding the snake. It moves to the next player who three-putts &mdash; and whoever is stuck with it at the end of the round pays up.',
    facts=[('Players', '2 to 4+'), ('Format', 'Putting only'), ('Bets', '1 snake per round'), ('Difficulty', 'Easy')],
    body="""
<h2>How Snake works</h2>
<ol>
  <li><strong>Agree on the stake</strong> before the round &mdash; say $5.</li>
  <li><strong>The first player to three-putt</strong> (or worse) takes the snake.</li>
  <li><strong>The snake moves</strong> to whoever three-putts next. If the player holding it three-putts again, they just keep it.</li>
  <li><strong>Whoever holds the snake after the 18th hole</strong> pays the stake to each of the other players.</li>
</ol>
<p>If nobody three-putts all day, nobody pays &mdash; a nice bonus for a group that putted well.</p>

<h2>A worked example: $5 snake</h2>
<div class="sg-table-wrap"><table>
  <thead><tr><th>Hole</th><th>What happened</th><th>Who holds the snake</th></tr></thead>
  <tbody>
    <tr><td>3</td><td>Ben three-putts</td><td>Ben</td></tr>
    <tr><td>8</td><td>Anne three-putts</td><td>Anne</td></tr>
    <tr><td>14</td><td>Ben three-putts again</td><td>Ben</td></tr>
    <tr><td>18</td><td>Everyone two-putts</td><td class="win">Ben is stuck with it</td></tr>
  </tbody>
</table></div>
<p>In a four-player game, Ben pays $5 to each of the other three players: $15 in all.</p>

<h2>Variations</h2>
<h3>Growing snake</h3>
<p>The snake gets more expensive every time it moves &mdash; for example, it starts at $1 and adds $1 for each three-putt. Late-round three-putts become very costly.</p>
<h3>Front and back snakes</h3>
<p>Play a separate snake on each nine, so a bad putting stretch early doesn&rsquo;t decide the whole day.</p>
<h3>What counts as a putt</h3>
<p>Agree whether strokes from the fringe count. Most groups only count strokes taken with the ball on the green.</p>
""",
    faq=[
        ('Who pays in the snake golf game?', 'The player holding the snake after the last hole pays the agreed stake to each of the other players.'),
        ('Does a four-putt count in snake?', 'Yes. Any three-putt or worse passes the snake to that player.'),
        ('What if nobody three-putts?', 'If nobody three-putts during the round, nobody takes the snake and nobody pays.'),
        ('Do putts from the fringe count in snake?', 'Agree before the round. Most groups only count strokes taken with the ball on the putting green.'),
    ],
)

ARTICLES['nine-point'] = dict(
    title='9-Point Golf Game (Nines): Rules & Scoring',
    h1='How to play 9-Point (Nines) in golf',
    desc='9-Point golf game rules explained: how three players split nine points on every hole, how ties are scored, how to settle up, and a worked example.',
    lede='9-Point, also called Nines, is the classic game for a threesome. Every hole is worth nine points, split between the three players based on their scores, so you&rsquo;re always playing for something.',
    facts=[('Players', '3'), ('Format', 'Hole by hole'), ('Points', '9 per hole, 162 per round'), ('Difficulty', 'Easy')],
    body="""
<h2>How 9-Point works</h2>
<p>On every hole, the three players split nine points:</p>
<div class="sg-table-wrap"><table>
  <thead><tr><th>Result on the hole</th><th>Points</th></tr></thead>
  <tbody>
    <tr><td>Three different scores</td><td>Low 5, middle 3, high 1</td></tr>
    <tr><td>Two tie for low</td><td>4 and 4, the other player 1</td></tr>
    <tr><td>Two tie for high</td><td>Low 5, the other two 2 each</td></tr>
    <tr><td>All three tie</td><td>3 each</td></tr>
  </tbody>
</table></div>
<p>Every hole hands out exactly nine points, so 18 holes hand out 162 &mdash; an average of 54 per player.</p>

<h2>Settling up</h2>
<p>The simplest way is to compare each player to the average of 54. If you finish above it, you collect the difference; below it, you pay. At $1 a point:</p>
<div class="sg-table-wrap"><table>
  <thead><tr><th>Player</th><th>Points</th><th>vs. 54</th><th>Result</th></tr></thead>
  <tbody>
    <tr><td>Anne</td><td>70</td><td>+16</td><td class="win">Wins $16</td></tr>
    <tr><td>Ben</td><td>52</td><td>&minus;2</td><td>Pays $2</td></tr>
    <tr><td>Cal</td><td>40</td><td>&minus;14</td><td>Pays $14</td></tr>
  </tbody>
</table></div>
<p>The results add up to zero: Ben and Cal&rsquo;s $16 covers Anne&rsquo;s winnings.</p>

<h2>A hole-by-hole example</h2>
<div class="sg-table-wrap"><table>
  <thead><tr><th>Hole</th><th>Anne</th><th>Ben</th><th>Cal</th><th>Points (A / B / C)</th></tr></thead>
  <tbody>
    <tr><td>1</td><td>4</td><td>5</td><td>6</td><td>5 / 3 / 1</td></tr>
    <tr><td>2</td><td>4</td><td>4</td><td>5</td><td>4 / 4 / 1</td></tr>
    <tr><td>3</td><td>3</td><td>5</td><td>5</td><td>5 / 2 / 2</td></tr>
    <tr><td>4</td><td>5</td><td>5</td><td>5</td><td>3 / 3 / 3</td></tr>
  </tbody>
</table></div>

<h2>Variations</h2>
<ul>
  <li><strong>Net 9-Point:</strong> use handicap strokes on the hardest holes.</li>
  <li><strong>Birdie bonus:</strong> some groups give a sweep (all nine points) to an outright birdie.</li>
  <li><strong>Four players:</strong> the four-player version, Split Sixes, follows the same idea with different point splits.</li>
</ul>
""",
    faq=[
        ('How many players do you need for 9-Point?', '9-Point is built for three players. With four, most groups play a different game such as Wolf or Vegas.'),
        ('How are ties scored in 9-Point golf?', 'Two players tied for low get 4 each and the third gets 1. Two tied for high get 2 each and the low score gets 5. A three-way tie is 3 points each.'),
        ('How do you settle a 9-Point game?', 'There are 162 points in 18 holes, so the average is 54. Each player wins or pays the difference between their total and 54, at an agreed value per point.'),
    ],
)

ARTICLES['dots'] = dict(
    title='Dots Golf Game (Junk): Greenies, Sandies & More',
    h1='How to play Dots in golf',
    desc='Dots golf game rules explained: earning points for birdies, greenies, sandies, chip-ins and other good shots, how to settle up, and a worked example.',
    lede='Dots (also called Junk, Garbage or Trash) rewards good golf shots instead of good totals. Every birdie, greenie, sandy or chip-in earns a dot &mdash; so even a high handicapper can win the day with one great up-and-down.',
    facts=[('Players', '2 to 4+'), ('Format', 'Points for good shots'), ('Scoring', 'Dots'), ('Difficulty', 'Easy')],
    body="""
<h2>How Dots works</h2>
<p>Before the round, agree on which achievements earn a dot and what each dot is worth. During the round, you collect a dot every time you pull one off. At the end, players settle up on the difference in dots.</p>

<h2>Common dots</h2>
<div class="sg-table-wrap"><table>
  <thead><tr><th>Dot</th><th>How you earn it</th></tr></thead>
  <tbody>
    <tr><td><strong>Birdie</strong></td><td>One under par on a hole (an eagle is usually worth 2 or more)</td></tr>
    <tr><td><strong>Greenie</strong></td><td>Closest to the pin in regulation on a par 3, then make par or better</td></tr>
    <tr><td><strong>Sandy</strong></td><td>Make par or better after being in a bunker on the hole</td></tr>
    <tr><td><strong>Chippie</strong></td><td>Hole out from off the green</td></tr>
    <tr><td><strong>Polie</strong></td><td>Make a putt longer than the flagstick</td></tr>
    <tr><td><strong>Barkie</strong></td><td>Make par or better after hitting a tree</td></tr>
    <tr><td><strong>Arnie</strong></td><td>Make par or better without ever hitting the fairway (named for Arnold Palmer)</td></tr>
  </tbody>
</table></div>
<p>Some groups add negative dots, like losing one for a three-putt or a ball in the water.</p>

<h2>Settling up</h2>
<p>The fairest way is to pay the difference between every pair of players. At $1 a dot, if Anne finishes with 6 dots and Ben with 2, Ben pays Anne $4.</p>

<h2>A worked example: $1 a dot</h2>
<div class="sg-table-wrap"><table>
  <thead><tr><th>Player</th><th>Dots earned</th><th>Total</th></tr></thead>
  <tbody>
    <tr><td>Anne</td><td>2 birdies, 1 greenie, 1 polie</td><td class="win">4</td></tr>
    <tr><td>Ben</td><td>1 sandy, 1 chippie</td><td>2</td></tr>
    <tr><td>Cal</td><td>1 barkie</td><td>1</td></tr>
  </tbody>
</table></div>
<p>Pairwise: Ben pays Anne $2, Cal pays Anne $3 and Cal pays Ben $1. Anne finishes +$5, Ben &minus;$1 and Cal &minus;$4 &mdash; which adds up to zero.</p>

<h2>Why groups love Dots</h2>
<ul>
  <li><strong>Everyone has a chance.</strong> You don&rsquo;t need the lowest score to collect &mdash; one lucky chip-in counts.</li>
  <li><strong>It stacks with anything.</strong> Dots pairs well with a Nassau or Skins for extra action.</li>
  <li><strong>It&rsquo;s easy to customize.</strong> Add or drop dots to fit your group.</li>
</ul>
""",
    faq=[
        ('What is a greenie in golf?', 'A greenie is earned by the player whose tee shot finishes closest to the pin on a par 3, as long as it is on the green and they go on to make par or better.'),
        ('What is a sandy in golf?', 'A sandy is making par or better on a hole after being in a bunker on that hole, most often by getting up and down from a greenside bunker.'),
        ('Is Dots the same as Junk or Garbage?', 'Yes. Dots, Junk, Garbage and Trash are names for the same type of game, where you earn points for good shots and achievements.'),
        ('How do you pay out dots?', 'Most groups pay the difference between every pair of players at the agreed value per dot.'),
    ],
)

HUB_PAGE = dict(
    title='Golf Side Games Explained: Nassau, Skins, Wolf & More',
    h1='Golf side games, explained',
    desc='Rules and examples for the most popular golf side games and bets: Nassau, Skins, Wolf, Vegas, Snake, 9-Point and Dots. Pick a game for your next round.',
    lede='A side game turns a regular round into a competition &mdash; even if nobody in your group shoots the same score. Here&rsquo;s how the most popular golf games and bets work, with simple rules and worked examples.',
)

# ─────────────────────────── rendering ───────────────────────────

def head(title, desc, path, ld, og_image='/onlyBirdies/images/og.jpg'):
    url = BASE + path
    tags = [
        f'<title>{escape(title)}</title>',
        f'<meta name="description" content="{escape(desc)}">',
        f'<link rel="canonical" href="{url}">',
        '<link rel="icon" type="image/png" href="/onlyBirdies/images/onlybirdies-icon.png">',
        '<meta name="apple-itunes-app" content="app-id=6749419654">',
        '<meta property="og:type" content="article">',
        '<meta property="og:site_name" content="Happy Path Apps">',
        f'<meta property="og:title" content="{escape(title)}">',
        f'<meta property="og:description" content="{escape(desc)}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:image" content="{BASE}{og_image}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{escape(title)}">',
        f'<meta name="twitter:description" content="{escape(desc)}">',
        f'<meta name="twitter:image" content="{BASE}{og_image}">',
    ]
    tags += ['<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + '</script>' for d in ld]
    return ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            + '\n'.join(tags) + '\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@400;600;700;800&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">\n'
            '<style>' + base_css + footer_css + PAGE_CSS + '</style>\n</head>\n<body>\n\n' + nav_html + '\n')


def breadcrumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + p}
                                for i, (n, p) in enumerate(items)]}


def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s)


def cta(heading, text):
    return f"""
  <div class="sg-cta fade-up">
    <img class="icon" src="/onlyBirdies/images/onlybirdies-icon.png" alt="">
    <h2>{heading}</h2>
    <p>{text}</p>
    <div class="badges">
        {BADGES}
    </div>
  </div>"""


def game_cards(exclude=None):
    cards = []
    for g in GAMES:
        if g['slug'] == exclude:
            continue
        img = f'<img src="/onlyBirdies/images/{g["icon"]}" alt="">'
        if g['slug'] in WRITTEN:
            cards.append(f'<a class="sg-card" href="{HUB}{g["slug"]}/">{img}<h3>{g["name"]}</h3><p>{g["short"]}</p><span class="go">Read the rules &rarr;</span></a>')
        else:
            cards.append(f'<div class="sg-card soon">{img}<h3>{g["name"]}</h3><p>{g["short"]}</p><span class="go">Full guide coming soon</span></div>')
    return '\n      '.join(cards)


def tail():
    return '\n\n' + footer_html + '\n\n' + script_html + '\n</body>\n</html>\n'


def write(path, html):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf-8').write(html)
    print('wrote', path)


def render_game(g):
    a = ARTICLES[g['slug']]
    path = f'{HUB}{g["slug"]}/'
    ld = [
        {"@context": "https://schema.org", "@type": "Article", "headline": a['h1'], "description": a['desc'],
         "image": BASE + '/onlyBirdies/images/og.jpg', "dateModified": UPDATED, "datePublished": UPDATED,
         "author": {"@type": "Organization", "name": "Happy Path Apps", "url": BASE + '/'},
         "publisher": {"@type": "Organization", "name": "Happy Path Apps", "logo": {"@type": "ImageObject", "url": BASE + '/images/logo.png'}},
         "mainEntityOfPage": BASE + path},
        breadcrumbs_ld([('OnlyBirdies', '/onlyBirdies/'), ('Golf Side Games', HUB), (g['name'], path)]),
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in a['faq']]},
    ]
    facts = ''.join(f'<div class="sg-fact"><small>{k}</small><strong>{v}</strong></div>' for k, v in a['facts'])
    faq = '\n'.join(f'<details><summary>{escape(q)}</summary><p>{escape(ans)}</p></details>' for q, ans in a['faq'])
    html = head(a['title'], a['desc'], path, ld) + f"""
<section class="sg-hero">
  <div class="sg-hero-inner fade-up">
    <div class="sg-crumbs" role="navigation" aria-label="Breadcrumb"><a href="/onlyBirdies/">OnlyBirdies</a> <span>/</span> <a href="{HUB}">Golf side games</a> <span>/</span> <span>{g['name']}</span></div>
    <div class="sg-hero-title"><img src="/onlyBirdies/images/{g['icon']}" alt=""><h1>{a['h1']}</h1></div>
    <p class="sg-lede">{a['lede']}</p>
    <div class="sg-facts">{facts}</div>
  </div>
</section>

<section class="sg-body">
  <article class="sg-article">
{a['body']}
    <h2>{g['name']} FAQ</h2>
    <div class="sg-faq">
{faq}
    </div>
  </article>
{cta(f"Play {g['name']} without the math", f"OnlyBirdies keeps score for your whole group, tracks {g['name']} and your other side games as scores go in, and tells everyone who owes whom at the end of the round.")}
</section>

<section class="sg-more">
  <div class="sg-more-inner">
    <span class="ob-eyebrow">More side games</span>
    <h2 class="ob-section-title">Try another game</h2>
    <div class="sg-grid">
      {game_cards(exclude=g['slug'])}
    </div>
  </div>
</section>""" + tail()
    write(path.strip('/') + '/index.html', html)


def render_hub():
    h = HUB_PAGE
    ld = [
        {"@context": "https://schema.org", "@type": "CollectionPage", "name": h['h1'], "description": h['desc'], "url": BASE + HUB,
         "hasPart": [{"@type": "Article", "headline": ARTICLES[s]['h1'], "url": f'{BASE}{HUB}{s}/'} for s in sorted(WRITTEN)]},
        breadcrumbs_ld([('OnlyBirdies', '/onlyBirdies/'), ('Golf Side Games', HUB)]),
    ]
    html = head(h['title'], h['desc'], HUB, ld) + f"""
<section class="sg-hero">
  <div class="sg-hero-inner fade-up">
    <div class="sg-crumbs" role="navigation" aria-label="Breadcrumb"><a href="/onlyBirdies/">OnlyBirdies</a> <span>/</span> <span>Golf side games</span></div>
    <h1>{h['h1']}</h1>
    <p class="sg-lede">{h['lede']}</p>
  </div>
</section>

<section class="sg-body" style="padding-bottom: 40px;">
  <div class="sg-article">
    <h2 style="margin-top: 0;">Choosing a game</h2>
    <ul>
      <li><strong>Two players or two teams:</strong> a <a href="{HUB}nassau/">Nassau</a> is the classic.</li>
      <li><strong>Three or more, everyone for themselves:</strong> <a href="{HUB}skins/">Skins</a> keeps every hole interesting.</li>
      <li><strong>A foursome that wants strategy:</strong> <a href="{HUB}wolf/">Wolf</a> rotates teams every hole.</li>
      <li><strong>A foursome that likes big swings:</strong> <a href="{HUB}vegas/">Vegas</a> turns team scores into two-digit numbers.</li>
      <li><strong>A threesome:</strong> <a href="{HUB}nine-point/">9-Point</a> splits nine points on every hole.</li>
      <li><strong>Any group, any skill level:</strong> <a href="{HUB}dots/">Dots</a> pays for good shots, and <a href="{HUB}snake/">Snake</a> punishes three-putts.</li>
      <li><strong>Want more action?</strong> Stack them &mdash; plenty of groups play a Nassau and Skins at the same time.</li>
    </ul>
  </div>
</section>

<section class="sg-more" style="padding-top: 60px;">
  <div class="sg-more-inner">
    <span class="ob-eyebrow">The games</span>
    <h2 class="ob-section-title">Popular golf side games</h2>
    <div class="sg-grid">
      {game_cards()}
    </div>
  </div>
</section>

<section class="sg-body" style="padding-top: 20px;">
{cta('Every side game, tracked for you', 'OnlyBirdies keeps score for your group, tracks Nassau, Skins, Wolf, Vegas, Snake, 9-Point and Dots as you play, and settles the bets at the 19th hole.')}
</section>""" + tail()
    write(HUB.strip('/') + '/index.html', html)


if __name__ == '__main__':
    for g in GAMES:
        if g['slug'] in WRITTEN:
            render_game(g)
    render_hub()
