/*
  Omilía ad tracking, loaded on /omilia/ and the aphasia guides.

  1. Loads the Google tag for Google Ads (once GOOGLE_ADS_ID is filled in).
  2. Counts a tap on an Omilía (patient app) App Store button as the "App Store click" conversion.
     Taps on the Omilía Therapist store link are not counted.
  3. Adds App Store Connect campaign tokens to Omilía store links (once APP_STORE_PT is filled in),
     so App Store Connect → Analytics → Acquisition shows downloads from ads separately:
       ct=gads_<campaign id>  visitor arrived from a Google ad (gclid or utm_source=google, utm_medium=cpc)
       ct=website             everyone else

  Leave a value empty to switch that part off. Nothing loads from Google while GOOGLE_ADS_ID is empty.
*/
(function () {
  var GOOGLE_ADS_ID = 'AW-18570280193';    // Google Ads → Goals → Conversions → your action → Tag setup, e.g. 'AW-123456789'
  var CONVERSION_LABEL = '1_FhCIfx3LYdEIH6_5ZF';    // same screen, the part after the slash in send_to, e.g. 'AbCdEfGhIjKlMn'
  var APP_STORE_PT = '118829916';       // App Store Connect → Analytics → Acquisition → Campaigns → Generate link, the pt= value

  var PATIENT_APP_ID = 'id1602156122';
  var KEY = 'omilia_ad_click';

  // Remember an ad visit for this browser session, so a visitor who lands on a guide
  // and then taps the store button on /omilia/ still counts as coming from the ad.
  var adVisit = null;
  try {
    var q = new URLSearchParams(location.search);
    if (q.get('gclid') || q.get('gbraid') || q.get('wbraid') ||
        (q.get('utm_source') === 'google' && q.get('utm_medium') === 'cpc')) {
      adVisit = { campaign: (q.get('utm_campaign') || '').replace(/[^\w-]/g, '').slice(0, 30) };
      sessionStorage.setItem(KEY, JSON.stringify(adVisit));
    } else {
      adVisit = JSON.parse(sessionStorage.getItem(KEY) || 'null');
    }
  } catch (e) { /* storage blocked: treat as a normal visit */ }

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  if (GOOGLE_ADS_ID) {
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(GOOGLE_ADS_ID);
    document.head.appendChild(s);
    gtag('js', new Date());
    gtag('config', GOOGLE_ADS_ID);
  }

  function isPatientStoreLink(a) {
    return a && a.hostname === 'apps.apple.com' && a.pathname.indexOf(PATIENT_APP_ID) !== -1;
  }

  function tagStoreLinks() {
    if (!APP_STORE_PT) return;
    var ct = adVisit ? 'gads' + (adVisit.campaign ? '_' + adVisit.campaign : '') : 'website';
    var links = document.querySelectorAll('a[href*="apps.apple.com"]');
    for (var i = 0; i < links.length; i++) {
      if (!isPatientStoreLink(links[i])) continue;
      var url = new URL(links[i].href);
      url.searchParams.set('pt', APP_STORE_PT);
      url.searchParams.set('ct', ct);
      url.searchParams.set('mt', '8');
      links[i].href = url.toString();
    }
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href]');
    if (!isPatientStoreLink(a)) return;
    if (GOOGLE_ADS_ID && CONVERSION_LABEL) {
      gtag('event', 'conversion', { send_to: GOOGLE_ADS_ID + '/' + CONVERSION_LABEL, transport_type: 'beacon' });
    }
  }, true);

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', tagStoreLinks);
  else tagStoreLinks();
})();
