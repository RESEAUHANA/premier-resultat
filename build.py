# -*- coding: utf-8 -*-
"""Génère le site de l'offre « site à 500 € + SEO à 100 €/mois » dans le dossier site/.

Tout le texte est dans ce fichier et dans metiers.py : on modifie ici, puis
    python build.py
reconstruit toutes les pages, le sitemap, robots.txt et llms.txt.
"""
import html, json, re
from datetime import date
from pathlib import Path
from metiers import METIERS

# ---------------------------------------------------------------- réglages
MARQUE = "Premier Résultat"
MARQUE_HTML = 'Premier<span>Résultat</span>'
SITE_URL = "https://premierresultat.fr"   # domaine à réserver
VILLE = "Marseille"
CONTACT = {
    "telephone": "06 99 30 58 73",
    "whatsapp": "33699305873",
    "email": "sihem.kazitani13@gmail.com",
    "rendezvous": "",    # lien d'agenda en ligne (vide = bouton masqué)
}
PRIX_SITE = 500
NB_FOIS = 5
PRIX_SEO = 100
ENGAGEMENT = 6
PAGES_MAX = 10
AUJOURDHUI = date.today().isoformat()

OUT = Path(__file__).parent / "site"

# ---------------------------------------------------------------- outils
def sans_balises(t):
    return re.sub(r"<[^>]+>", "", t).replace("&nbsp;", " ")

def url(chemin):
    return SITE_URL + "/" + ("" if chemin == "index.html" else chemin)

def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"

ORGA = {
    "@type": "ProfessionalService",
    "@id": SITE_URL + "/#entreprise",
    "name": MARQUE,
    "url": SITE_URL + "/",
    "description": f"Création de sites internet pour artisans, commerçants et PME à {PRIX_SITE} € (jusqu'à {PAGES_MAX} pages, fiche Google comprise), puis référencement Google à {PRIX_SEO} € par mois.",
    "areaServed": {"@type": "Country", "name": "France"},
    "address": {"@type": "PostalAddress", "addressLocality": VILLE, "addressCountry": "FR"},
    "priceRange": f"{PRIX_SITE} €",
    "knowsLanguage": "fr",
}
if CONTACT["telephone"]:
    ORGA["telephone"] = CONTACT["telephone"]
if CONTACT["email"]:
    ORGA["email"] = CONTACT["email"]

MENU = [
    ("index.html", "Accueil"),
    ("offre.html", "Ce qui est compris"),
    ("metiers.html", "Métiers"),
    ("visibilite-ia.html", "Visibilité IA"),
    ("tarifs.html", "Tarifs"),
]

def entete(actif):
    liens = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == actif else ""}>{t}</a>' for h, t in MENU
    )
    sous = "".join(f'<a class="sous" href="{m["slug"]}.html">{m["menu"]}</a>' for m in METIERS)
    mobile = "".join(f'<a href="{h}">{t}</a>' for h, t in MENU[:3]) + sous + '<a href="visibilite-ia.html">Visibilité IA</a><a href="tarifs.html">Tarifs</a><a href="contact.html">Contact</a>'
    return f'''<header class="nav">
  <div class="c">
    <a class="logo" href="index.html" aria-label="{MARQUE}, accueil">{MARQUE_HTML}</a>
    <nav class="liens" aria-label="Navigation principale">{liens}</nav>
    <div class="droite">
      <a class="btn p" href="contact.html">Demander mon site</a>
      <details class="burger"><summary aria-label="Ouvrir le menu">☰</summary><nav aria-label="Menu mobile">{mobile}</nav></details>
    </div>
  </div>
</header>'''

def pied():
    metiers = "".join(f'<a href="{m["slug"]}.html">{m["menu"]}</a>' for m in METIERS)
    return f'''<footer class="pied">
  <div class="c">
    <div class="g">
      <div><a class="logo" href="index.html">{MARQUE_HTML}</a>
        <p style="margin-top:12px;max-width:320px">Sites internet et référencement Google pour artisans, commerçants et PME. {PRIX_SITE}&nbsp;€ le site, payable en {NB_FOIS} fois.</p></div>
      <div><h3>L'offre</h3><nav aria-label="L'offre"><a href="offre.html">Ce qui est compris</a><a href="visibilite-ia.html">Visibilité dans les IA</a><a href="tarifs.html">Tarifs</a><a href="metiers.html">Tous les métiers</a><a href="contact.html">Contact</a></nav></div>
      <div><h3>Métiers</h3><nav aria-label="Métiers">{metiers}</nav></div>
      <div><h3>Informations</h3><nav aria-label="Informations légales"><a href="mentions-legales.html">Mentions légales</a><a href="confidentialite.html">Confidentialité</a></nav></div>
    </div>
    <div class="bas"><span>© {date.today().year} {MARQUE}</span><span>Site conçu et référencé par nos soins</span></div>
  </div>
</footer>'''

RDV_HTML = ('        <a class="moyen" href="' + CONTACT['rendezvous'] + '"><span class="ic" aria-hidden="true">▣</span><span><b>Réserver un appel de 15 minutes</b><small>Choisissez votre créneau</small></span></a>') if CONTACT['rendezvous'] else ''

def bloc_contact(titre="Parlons de votre site", texte="Réponse sous 24 h ouvrées. Le premier échange est gratuit et ne vous engage à rien.", activite=""):
    rdv = RDV_HTML
    return f'''<section class="sec nuit contact" id="contact" aria-labelledby="contact-h2">
  <div class="c">
    <p class="sur">Contact</p>
    <h2 id="contact-h2">{titre}</h2>
    <p class="chapo">{texte}</p>
    <div class="g">
      <div class="moyens">
        <a class="moyen" data-lien="telephone" href="tel:+33699305873"><span class="ic" aria-hidden="true">☎</span><span><b>Appeler</b><small>06 99 30 58 73</small></span></a>
        <a class="moyen" data-lien="whatsapp" href="https://wa.me/33699305873"><span class="ic" aria-hidden="true">✆</span><span><b>Écrire sur WhatsApp</b><small>Réponse dans la journée</small></span></a>
{rdv}      </div>
      <form class="f" data-formulaire>
        <label>Votre nom<input name="nom" autocomplete="name" required></label>
        <label>Votre activité et votre ville<input name="activite" value="{activite}" placeholder="Ex. : plombier à Marseille" required></label>
        <label>Téléphone ou e-mail<input name="coordonnees" required></label>
        <label>Votre besoin<textarea name="message" placeholder="Nouveau site, site à refaire, fiche Google, référencement…"></textarea></label>
        <button class="btn" type="submit">Envoyer ma demande</button>
        <p class="m" data-retour>Vos informations servent uniquement à vous recontacter. <a href="confidentialite.html">Confidentialité</a></p>
      </form>
    </div>
  </div>
</section>'''

SCRIPT = """<script>
const CONTACT = %s;
(function(){
  const a = (k,u) => document.querySelectorAll('[data-lien="'+k+'"]').forEach(e => { if(u) e.href = u; });
  if (CONTACT.telephone) { a("telephone","tel:"+CONTACT.telephone.replace(/\\s/g,"")); document.querySelectorAll('[data-texte="telephone"]').forEach(e=>e.textContent=CONTACT.telephone); }
  if (CONTACT.whatsapp) a("whatsapp","https://wa.me/"+CONTACT.whatsapp);
  if (CONTACT.rendezvous) a("rendezvous",CONTACT.rendezvous);
  document.querySelectorAll("[data-formulaire]").forEach(f => f.addEventListener("submit", e => {
    e.preventDefault();
    const d = new FormData(f), r = f.querySelector("[data-retour]");
    if (!CONTACT.email) { r.textContent = "Le formulaire n'est pas encore relié à une adresse e-mail."; return; }
    const corps = "Nom : "+d.get("nom")+"\\nActivité : "+d.get("activite")+"\\nContact : "+d.get("coordonnees")+"\\n\\n"+(d.get("message")||"");
    location.href = "mailto:"+CONTACT.email+"?subject="+encodeURIComponent("Demande de site internet")+"&body="+encodeURIComponent(corps);
    r.textContent = "Votre messagerie s'ouvre avec la demande prête à envoyer.";
  }));
})();
</script>""" % json.dumps(CONTACT, ensure_ascii=False)

def page(chemin, titre, description, corps, schemas=(), og_type="website"):
    graph = {"@context": "https://schema.org", "@graph": [ORGA, *schemas]}
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(titre)}</title>
<meta name="description" content="{html.escape(description)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url(chemin)}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{MARQUE}">
<meta property="og:title" content="{html.escape(titre)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{url(chemin)}">
<meta property="og:locale" content="fr_FR">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#101623">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Antonio:wght@400..600&family=Archivo:wdth,wght@100..125,400..800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css?v=5">
{ld(graph)}
</head>
<body>
{entete(chemin)}
<main>
{corps}
</main>
{pied()}
{SCRIPT}
</body>
</html>
'''

def fil(*etapes):
    morceaux = ['<a href="index.html">Accueil</a>'] + [
        (f'<a href="{h}">{t}</a>' if h else t) for h, t in etapes
    ]
    return '<p class="fil">' + " › ".join(morceaux) + "</p>"

def schema_fil(*etapes):
    items = [{"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE_URL + "/"}]
    for i, (h, t) in enumerate(etapes, start=2):
        items.append({"@type": "ListItem", "position": i, "name": t, "item": url(h)})
    return {"@type": "BreadcrumbList", "itemListElement": items}

def schema_faq(faq):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": sans_balises(r)}} for q, r in faq
    ]}

def bloc_faq(faq, titre="Questions fréquentes", sous="Ce qu'on nous demande avant de commencer", alt=False):
    items = "".join(f"<details><summary>{q}</summary><p>{r}</p></details>" for q, r in faq)
    return f'''<section class="sec{" alt" if alt else ""}" id="questions" aria-labelledby="faq-h2">
  <div class="c"><p class="sur">{titre}</p><h2 id="faq-h2">{sous}</h2><div class="faq">{items}</div></div>
</section>'''

# ---------------------------------------------------------------- contenus communs
COMPRIS_SITE = [
    f"Jusqu'à {PAGES_MAX} pages : accueil, une page par service, à propos, zone d'intervention, avis, contact…",
    "Textes rédigés pour vos clients et pour Google, à partir d'un appel de 15 minutes",
    "Lisible sur téléphone, tablette et ordinateur, rapide à charger",
    "Création et remplissage complet de votre fiche Google (Google Maps)",
    "Formulaire de contact, bouton d'appel et bouton WhatsApp",
    "Bases du référencement : titres, descriptions, données structurées, plan du site",
    "Inscription dans Google Search Console pour que Google découvre le site",
    "Site préparé pour les IA (ChatGPT, Gemini, Perplexity) : robots autorisés, fichier llms.txt, données structurées",
    "Adresse sécurisée (https), mentions légales et page confidentialité",
    "Le site vous appartient une fois réglé",
]
COMPRIS_SEO = [
    "Une nouvelle page ou un article chaque mois sur ce que cherchent vos clients",
    "Fiche Google tenue à jour : publications, photos, horaires, réponses aux avis préparées",
    "Inscription et cohérence dans les annuaires utiles (Pages Jaunes, Apple Plans, Bing…)",
    "Corrections techniques pour garder un site rapide et sans erreur",
    "Suivi de vos positions sur les recherches de votre ville",
    "Visibilité dans les IA : vérification chaque mois de ce que répondent ChatGPT, Gemini et Perplexity à vos clients, et contenus ajustés en conséquence",
    "Un compte rendu mensuel court, en français clair",
]

BABA = [
    ("Un site qui s'affiche bien sur téléphone", "La majorité de vos clients vous cherchent depuis leur téléphone. Tout est pensé pour eux d'abord : texte lisible, boutons faciles à toucher, numéro cliquable."),
    ("Une fiche Google complète", "C'est souvent ce qu'un client voit avant votre site : horaires, photos, avis, itinéraire. Nous la créons, la remplissons et la relions au site."),
    ("Des pages qui répondent aux vraies recherches", "« Plombier fuite Marseille », « coiffeur sans rendez-vous Lyon » : une page par service et par besoin, pas une page fourre-tout."),
    ("Les réglages que Google attend", "Titres et descriptions uniques, données structurées, plan du site, adresse sécurisée, inscription dans Search Console."),
    ("Des clients qui vous contactent en un geste", "Appel, WhatsApp, formulaire : le contact est visible sur chaque page, sans chercher."),
    ("Les obligations légales", "Mentions légales, page confidentialité, consentement si des outils de mesure sont utilisés. Rien qui puisse vous être reproché."),
    ("Un site que les IA savent lire", "ChatGPT, Gemini, Perplexity et le mode IA de Google répondent de plus en plus à la place des moteurs. Le site leur est ouvert et décrit votre entreprise dans un format qu'ils comprennent."),
]

IA_POINTS = [
    ("Ouvert aux robots des IA", "Le site autorise explicitement les robots de ChatGPT, Claude, Perplexity, Gemini et Bing à le lire. Beaucoup de sites les bloquent sans le savoir."),
    ("Une fiche d'identité pour les IA", "Un fichier llms.txt et des données structurées résument qui vous êtes, ce que vous faites, où et à quel prix, sans ambiguïté."),
    ("Des réponses aux vraies questions", "Les IA citent les pages qui répondent clairement à une question. Vos pages et vos FAQ sont rédigées dans ce sens."),
    ("Les mêmes informations partout", "Nom, adresse, téléphone, horaires identiques sur le site, la fiche Google et les annuaires : les IA recoupent leurs sources avant de recommander."),
    ("Des avis qui parlent de vous", "Les IA s'appuient aussi sur vos avis Google. Les encourager et y répondre compte autant pour elles que pour vos clients."),
    ("Un suivi chaque mois", "Pendant le suivi mensuel, nous posons aux principales IA les questions que se posent vos clients, et nous notons si votre entreprise apparaît."),
]

IA_Q = {
    "site-internet-plombier": "Quel plombier appeler pour une fuite à Marseille ?",
    "site-internet-electricien": "Qui peut installer une borne de recharge chez moi à Marseille ?",
    "site-internet-restaurant": "Un bon restaurant italien avec terrasse à Marseille ?",
    "creation-site-e-commerce": "Où acheter des bougies artisanales en ligne ?",
    "site-internet-coiffeur": "Un coiffeur spécialiste des cheveux bouclés à Marseille ?",
    "site-internet-garage-mecanicien": "Un garage honnête pour changer mes plaquettes à Marseille ?",
    "site-internet-sophrologue": "Un sophrologue pour le stress au travail à Marseille ?",
    "site-internet-masseur": "Où offrir un massage en carte cadeau à Marseille ?",
}

ETAPES = [
    ("Un appel de 15 minutes", "Vous expliquez votre métier, votre zone et ce que vous voulez mettre en avant."),
    ("Vous envoyez l'essentiel", "Logo si vous en avez un, quelques photos, vos services et vos horaires."),
    ("Vous relisez", "Vous recevez un lien pour voir le site et votre fiche Google, vous demandez vos corrections."),
    ("Mise en ligne", "Le site est publié, Google en est informé. Le suivi mensuel démarre si vous l'avez choisi."),
]

FAQ_GENERALE = [
    ("Le site est-il vraiment à moi ?", f"Oui. Une fois les {PRIX_SITE} € réglés, le site et ses textes vous appartiennent. Vous pouvez le garder sans prendre le suivi mensuel."),
    ("Comment se passe le paiement en plusieurs fois ?", f"Le site est réglé en {NB_FOIS} mensualités de {PRIX_SITE // NB_FOIS} €, sans frais. Le travail commence dès la première."),
    ("Suis-je obligé de prendre le référencement ?", f"Non. Le site peut être commandé seul. Le suivi à {PRIX_SEO} € par mois est conseillé si vous voulez que de nouveaux clients vous trouvent sur Google."),
    (f"Pourquoi un engagement de {ENGAGEMENT} mois pour le référencement ?", f"Google met plusieurs mois à prendre en compte le travail fait sur un site. En dessous de {ENGAGEMENT} mois, on ne peut pas juger du résultat."),
    ("Garantissez-vous la première place sur Google ?", "Non, et personne ne peut le garantir honnêtement. Ce qui est garanti, c'est le travail fait chaque mois et un compte rendu clair de vos positions."),
    ("Y a-t-il des frais en plus ?", "Seulement le nom de domaine (l'adresse de votre site), réservé à votre nom, qui coûte en général une dizaine d'euros par an. Tout autre frais éventuel est annoncé avant de commencer."),
    ("Pouvez-vous me faire recommander par ChatGPT ?", "Personne ne peut garantir qu'une IA vous citera. Ce que nous faisons : rendre votre site lisible par les IA, donner des informations claires et cohérentes partout, répondre aux questions de vos clients, et vérifier chaque mois ce que les IA disent de vous. <a href=\"visibilite-ia.html\">En savoir plus</a>."),
    ("J'ai déjà un site, pouvez-vous le reprendre ?", "Oui. Selon son état, il est refait dans le cadre de l'offre ou simplement suivi en référencement."),
    ("En combien de temps le site est-il en ligne ?", "Comptez en général deux à trois semaines après l'appel, selon la rapidité avec laquelle vous envoyez photos et informations."),
]

def ticket():
    return f'''<aside class="ticket" aria-label="Résumé des prix">
  <p class="tt">L'offre en deux lignes</p>
  <div class="l"><div>Site + fiche Google<small>jusqu'à {PAGES_MAX} pages · {NB_FOIS} × {PRIX_SITE // NB_FOIS} €</small></div><b>{PRIX_SITE} €</b></div>
  <div class="l"><div>Référencement Google et IA<small>suivi mensuel · {ENGAGEMENT} mois minimum</small></div><b>{PRIX_SEO} €<i> /mois</i></b></div>
  <small style="margin-top:8px">Prix annoncé avant de commencer, sans devis à rallonge.</small>
</aside>'''

def bloc_offres(alt=True):
    l1 = "".join(f"<li>{x}</li>" for x in COMPRIS_SITE)
    l2 = "".join(f"<li>{x}</li>" for x in COMPRIS_SEO)
    return f'''<section class="sec{" alt" if alt else ""}" id="offre" aria-labelledby="offre-h2">
  <div class="c">
    <p class="sur">L'offre</p>
    <h2 id="offre-h2">Deux prix, tout est écrit</h2>
    <p class="chapo">Vous savez ce que vous payez et ce que vous recevez avant de vous engager.</p>
    <div class="offres">
      <article class="offre"><span class="et">Étape 1</span><h3>Votre site et votre fiche Google</h3>
        <p class="px">{PRIX_SITE} €</p><p class="mod">Payable en {NB_FOIS} fois : {NB_FOIS} × {PRIX_SITE // NB_FOIS} €, sans frais</p>
        <ul class="liste">{l1}</ul><a class="btn b2" href="contact.html">Je veux mon site</a></article>
      <article class="offre v"><span class="et">Étape 2</span><h3>Votre référencement Google et IA</h3>
        <p class="px">{PRIX_SEO} € <small>/ mois</small></p><p class="mod">Engagement de {ENGAGEMENT} mois, le temps que Google réagisse</p>
        <ul class="liste">{l2}</ul><a class="btn" href="contact.html">Je veux être trouvé</a></article>
    </div>
  </div>
</section>'''

def bloc_etapes(alt=False):
    li = "".join(f"<li><h3>{t}</h3><p>{p}</p></li>" for t, p in ETAPES)
    return f'''<section class="sec{" alt" if alt else ""}" id="etapes" aria-labelledby="etapes-h2">
  <div class="c"><p class="sur">Comment ça marche</p><h2 id="etapes-h2">Quatre étapes, peu de travail pour vous</h2><ol class="etapes">{li}</ol></div>
</section>'''

def bloc_metiers(titre="Une page pensée pour chaque métier", exclure=None, alt=False):
    cartes = "".join(
        f'<a class="carte" href="{m["slug"]}.html"><h3>{m["carte_titre"]}</h3><p>{m["carte_texte"]}</p></a>'
        for m in METIERS if m["slug"] != exclure
    )
    return f'''<section class="sec{" alt" if alt else ""}" id="metiers" aria-labelledby="met-h2">
  <div class="c"><p class="sur">Métiers</p><h2 id="met-h2">{titre}</h2>
  <p class="chapo">Un plombier, un restaurant et un sophrologue ne sont pas cherchés de la même façon. Chaque site est construit autour des recherches de vos clients.</p>
  <div class="cartes t4">{cartes}</div></div>
</section>'''

def bloc_ia_accueil():
    cartes = "".join(f'<div class="carte"><h3>{t}</h3><p>{p}</p></div>' for t, p in IA_POINTS[:3])
    return f'''<section class="sec nuit" id="ia" aria-labelledby="ia-h2">
  <div class="c">
    <p class="sur">Google, et maintenant les IA</p>
    <h2 id="ia-h2">Vos clients posent aussi la question à ChatGPT</h2>
    <p class="chapo">« Quel plombier appeler à Marseille ? », « un bon coiffeur pour cheveux bouclés près de chez moi ? » : de plus en plus de gens demandent directement à une IA. Elle répond avec quelques noms. Votre site est préparé pour qu'elle puisse vous connaître.</p>
    <div class="cartes t3">{cartes}</div>
    <div class="act" style="margin-top:26px;display:flex;flex-wrap:wrap;gap:12px"><a class="btn b2" href="visibilite-ia.html">Comment ça marche</a></div>
  </div>
</section>'''

def bloc_ia_metier(m):
    q = IA_Q.get(m["slug"], "")
    return f'''<section class="sec nuit" aria-labelledby="iam-h2">
  <div class="c"><p class="sur">Visibilité dans les IA</p><h2 id="iam-h2">Quand un client demande à ChatGPT</h2>
  <div class="texte">
    <p>De plus en plus de clients ne tapent plus seulement des mots-clés : ils posent une question complète à une IA, comme <strong style="color:#fff">« {q} »</strong>. L'IA répond avec quelques noms, puisés dans les sites, les fiches Google et les avis qu'elle trouve.</p>
    <p>Votre site est ouvert aux robots des IA, décrit votre activité dans un format qu'elles comprennent, et répond aux questions de vos clients. Pendant le suivi mensuel, nous vérifions ce que les principales IA répondent sur votre métier dans votre ville. Personne ne peut garantir d'être cité, mais un site clair et cohérent met toutes les chances de votre côté. <a href="visibilite-ia.html" style="color:#f5a58d">En savoir plus</a>.</p>
  </div></div>
</section>'''

# ---------------------------------------------------------------- pages
def accueil():
    baba = "".join(f'<div class="carte"><span class="n">{i:02d}</span><h3>{t}</h3><p>{p}</p></div>' for i, (t, p) in enumerate(BABA, 1))
    corps = f'''<section class="hero">
  <div class="c g">
    <div>
      <p class="sur">Artisans, commerçants, indépendants, PME</p>
      <h1>Création de site internet pour PME à {PRIX_SITE}&nbsp;€, fiche Google comprise</h1>
      <p class="chapo">Un vrai site de {PAGES_MAX} pages maximum, rédigé et référencé, avec votre fiche Google créée et remplie. Payable en {NB_FOIS} fois. Ensuite, {PRIX_SEO}&nbsp;€ par mois pour monter dans les recherches de votre ville, sur Google et dans les IA comme ChatGPT.</p>
      <div class="act"><a class="btn" href="contact.html">Demander mon site</a><a class="btn b2" href="offre.html">Voir ce qui est compris</a></div>
      <ul class="coches"><li>Prix fixe annoncé avant de commencer</li><li>Le site vous appartient</li><li>Pas de jargon</li></ul>
    </div>
    {ticket()}
  </div>
</section>

<section class="sec" id="probleme" aria-labelledby="pb-h2">
  <div class="c">
    <p class="sur">Le constat</p>
    <h2 id="pb-h2">Vos clients vous cherchent sur Google avant de vous appeler</h2>
    <div class="texte">
      <p>Quand une fuite d'eau inonde une cuisine ou qu'on cherche un restaurant pour ce soir, on ne feuillette plus d'annuaire : on tape trois mots sur son téléphone et on appelle l'un des premiers résultats. Si votre entreprise n'apparaît pas, ou si elle apparaît avec une fiche vide et un site daté, le client appelle le concurrent.</p>
      <p>Beaucoup de petites entreprises se retrouvent coincées entre deux mauvaises options : un site à plusieurs milliers d'euros, ou un abonnement « clé en main » qui coûte cher sur trois ans et dont elles ne sont jamais propriétaires. Notre offre est faite pour sortir de ce choix : un site sérieux, à vous, à un prix que l'on peut assumer.</p>
    </div>
  </div>
</section>

<section class="sec alt" id="baba" aria-labelledby="baba-h2">
  <div class="c">
    <p class="sur">Le B.A.-BA, fait correctement</p>
    <h2 id="baba-h2">Ce que tout site d'entreprise devrait avoir</h2>
    <p class="chapo">Rien d'exotique : les bases que Google et vos clients attendent, posées proprement dès le premier jour.</p>
    <div class="cartes t3">{baba}</div>
  </div>
</section>

{bloc_offres(alt=False)}
{bloc_ia_accueil()}
{bloc_metiers(alt=False)}
{bloc_etapes(alt=True)}
{bloc_faq(FAQ_GENERALE[:7])}
{bloc_contact()}'''
    schemas = [
        {"@type": "WebSite", "@id": SITE_URL + "/#site", "url": SITE_URL + "/", "name": MARQUE, "inLanguage": "fr-FR", "publisher": {"@id": ORGA["@id"]}},
        schema_faq(FAQ_GENERALE[:7]),
    ]
    return page("index.html",
        f"Création de site internet PME à {PRIX_SITE} €, fiche Google comprise | {MARQUE}",
        f"Site professionnel jusqu'à {PAGES_MAX} pages + fiche Google pour {PRIX_SITE} €, payable en {NB_FOIS} fois. Référencement à {PRIX_SEO} €/mois. Pour artisans, commerçants et PME.",
        corps, schemas)

def offre():
    baba = "".join(f'<div class="carte"><h3>{t}</h3><p>{p}</p></div>' for t, p in BABA)
    pages_type = [
        ("Accueil", "Qui vous êtes, ce que vous faites, où, et comment vous joindre, visible en cinq secondes."),
        ("Une page par service", "Chaque prestation a sa page, pour répondre précisément à ce que les clients tapent sur Google."),
        ("Zone d'intervention", "Les villes et quartiers où vous travaillez, pour être trouvé au-delà de votre adresse."),
        ("À propos", "Votre parcours, vos qualifications, vos photos : ce qui donne confiance."),
        ("Avis et réalisations", "Vos avis Google et vos chantiers, plats ou coupes, selon votre métier."),
        ("Contact", "Téléphone, WhatsApp, formulaire, plan d'accès et horaires."),
    ]
    pt = "".join(f'<div class="carte"><h3>{t}</h3><p>{p}</p></div>' for t, p in pages_type)
    faq = FAQ_GENERALE[5:] + [
        ("Qui rédige les textes ?", "Nous. Vous n'avez rien à écrire : un appel de 15 minutes suffit, puis vous relisez et corrigez ce qui ne vous ressemble pas."),
        ("Pourrai-je modifier le site moi-même ?", "Les petites modifications (horaires, tarifs, photos) sont faites pour vous sur simple message pendant le suivi mensuel. Hors suivi, elles sont faites sur demande, avec un prix annoncé avant."),
    ]
    corps = f'''<section class="hero">
  <div class="c">
    {fil(("", "Ce qui est compris"))}
    <p class="sur">Ce qui est compris</p>
    <h1>Un site complet et une fiche Google, pas une page vide</h1>
    <p class="chapo">Pour {PRIX_SITE}&nbsp;€, vous avez tout ce dont une entreprise a besoin pour être trouvée et contactée. Voici le détail, sans astérisque.</p>
  </div>
</section>
{bloc_offres(alt=False)}
<section class="sec alt" aria-labelledby="pages-h2">
  <div class="c"><p class="sur">Jusqu'à {PAGES_MAX} pages</p><h2 id="pages-h2">Les pages que l'on retrouve sur la plupart des sites</h2>
  <p class="chapo">La liste exacte dépend de votre métier : un restaurant a besoin d'une carte, un plombier d'une page « urgence », un sophrologue d'une page « déroulé d'une séance ».</p>
  <div class="cartes t3">{pt}</div></div>
</section>
<section class="sec" aria-labelledby="fiche-h2">
  <div class="c"><p class="sur">Fiche Google</p><h2 id="fiche-h2">Votre fiche Google créée et remplie, pas seulement « réclamée »</h2>
  <div class="texte">
    <p>La fiche Google (celle qui s'affiche sur Google Maps et à droite des résultats) est souvent le premier contact entre vous et un client. Une fiche à moitié remplie fait perdre des appels.</p>
    <p>Nous la créons ou la reprenons, choisissons les bonnes catégories, ajoutons vos services, horaires, zone d'intervention, photos et description, puis la relions à votre site. Google envoie en général un code de validation par courrier ou par vidéo : nous vous guidons pour cette étape, qui doit être faite par vous.</p>
  </div></div>
</section>
<section class="sec alt" aria-labelledby="baba2-h2">
  <div class="c"><p class="sur">Le B.A.-BA</p><h2 id="baba2-h2">Les bases posées dès la mise en ligne</h2><div class="cartes t3">{baba}</div></div>
</section>
{bloc_etapes()}
{bloc_faq(faq, alt=True)}
{bloc_contact()}'''
    schemas = [schema_fil(("offre.html", "Ce qui est compris")), schema_faq(faq)]
    return page("offre.html", f"Ce que comprend un site à {PRIX_SITE} € : {PAGES_MAX} pages et fiche Google | {MARQUE}",
        f"Le détail de l'offre : site jusqu'à {PAGES_MAX} pages rédigé et référencé, fiche Google créée et remplie, Search Console, mentions légales. {PRIX_SITE} € en {NB_FOIS} fois.",
        corps, schemas)

def tarifs():
    faq = FAQ_GENERALE[:6]
    corps = f'''<section class="hero">
  <div class="c g">
    <div>{fil(("", "Tarifs"))}
      <p class="sur">Tarifs</p>
      <h1>Site internet à {PRIX_SITE}&nbsp;€ en {NB_FOIS} fois, référencement à {PRIX_SEO}&nbsp;€ par mois</h1>
      <p class="chapo">Deux prix fixes, pour toutes les entreprises. Pas de devis à rallonge, pas d'options cachées.</p>
    </div>
    {ticket()}
  </div>
</section>
{bloc_offres(alt=False)}
<section class="sec alt" aria-labelledby="cmp-h2">
  <div class="c"><p class="sur">Pour comparer</p><h2 id="cmp-h2">Ce que coûte un site sur trois ans</h2>
  <div class="texte">
    <p>Un site d'entreprise se juge sur la durée, pas sur le prix de départ. Les formules « site en abonnement » affichent souvent une mensualité basse, mais le site ne vous appartient pas et la facture s'accumule tant que vous restez.</p>
    <p>Chez nous, le site coûte {PRIX_SITE}&nbsp;€ une fois, et il est à vous. Le référencement à {PRIX_SEO}&nbsp;€ par mois est un travail réel (nouvelles pages, fiche Google, suivi), que vous pouvez arrêter après {ENGAGEMENT} mois si vous le souhaitez.</p>
  </div></div>
</section>
{bloc_faq(faq)}
{bloc_contact()}'''
    offres = {"@type": "OfferCatalog", "name": "Offre site et référencement", "itemListElement": [
        {"@type": "Offer", "name": f"Création de site internet (jusqu'à {PAGES_MAX} pages) et fiche Google", "price": PRIX_SITE, "priceCurrency": "EUR"},
        {"@type": "Offer", "name": "Référencement Google mensuel", "price": PRIX_SEO, "priceCurrency": "EUR",
         "priceSpecification": {"@type": "UnitPriceSpecification", "price": PRIX_SEO, "priceCurrency": "EUR", "unitCode": "MON"}},
    ]}
    schemas = [schema_fil(("tarifs.html", "Tarifs")), schema_faq(faq),
               {"@type": "Service", "name": "Création de site internet et référencement Google", "provider": {"@id": ORGA["@id"]}, "areaServed": "France", "hasOfferCatalog": offres}]
    return page("tarifs.html", f"Tarifs : site internet {PRIX_SITE} € en {NB_FOIS} fois, SEO {PRIX_SEO} €/mois | {MARQUE}",
        f"Site professionnel et fiche Google à {PRIX_SITE} €, payable en {NB_FOIS} × {PRIX_SITE // NB_FOIS} €. Référencement Google à {PRIX_SEO} € par mois, {ENGAGEMENT} mois minimum. Prix fixes.",
        corps, schemas)

def hub_metiers():
    corps = f'''<section class="hero">
  <div class="c">{fil(("", "Métiers"))}
    <p class="sur">Métiers</p>
    <h1>Création de site internet par métier</h1>
    <p class="chapo">Chaque métier a ses recherches, ses obligations et ses clients. Choisissez le vôtre pour voir comment son site est construit.</p>
  </div>
</section>
{bloc_metiers(titre="Choisissez votre métier")}
<section class="sec alt" aria-labelledby="autre-h2">
  <div class="c"><p class="sur">Votre métier n'est pas dans la liste ?</p><h2 id="autre-h2">L'offre s'adapte à toutes les petites entreprises</h2>
  <div class="texte"><p>Menuisier, peintre, paysagiste, fleuriste, photographe, auto-école, boulangerie, cabinet de conseil… La méthode est la même : comprendre ce que vos clients cherchent, leur donner une page claire pour chaque besoin, et une fiche Google complète. <a href="contact.html">Parlez-nous de votre activité</a>.</p></div></div>
</section>
{bloc_contact()}'''
    schemas = [schema_fil(("metiers.html", "Métiers")),
               {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i, "url": url(m["slug"] + ".html"), "name": m["carte_titre"]} for i, m in enumerate(METIERS, 1)]}]
    return page("metiers.html", f"Création de site internet par métier : artisans, commerces, bien-être | {MARQUE}",
        "Plombier, électricien, restaurant, coiffeur, garage, sophrologue, massage, e-commerce : un site construit autour des recherches de vos clients.",
        corps, schemas)

def page_metier(m):
    puces = "".join(f"<li>{r}</li>" for r in m["recherches"])
    intro = "".join(f"<p>{p}</p>" for p in m["intro"])
    pages_l = "".join(f"<li>{p}</li>" for p in m["pages"])
    fiche = "".join(f"<li>{p}</li>" for p in m["fiche"])
    points = "".join(f'<div class="carte"><h3>{t}</h3><p>{p}</p></div>' for t, p in m["points"])
    prix = m.get("prix_html") or f'''<section class="sec alt" aria-labelledby="px-h2">
  <div class="c"><p class="sur">Prix</p><h2 id="px-h2">{m["prix_titre"]}</h2>
  <div class="texte"><p>Site jusqu'à {PAGES_MAX} pages et fiche Google : <strong>{PRIX_SITE}&nbsp;€</strong>, payable en {NB_FOIS} fois ({NB_FOIS} × {PRIX_SITE // NB_FOIS}&nbsp;€). Référencement mensuel : <strong>{PRIX_SEO}&nbsp;€ par mois</strong>, {ENGAGEMENT} mois minimum, facultatif. <a href="offre.html">Voir le détail de ce qui est compris</a>.</p></div></div>
</section>'''
    corps = f'''<section class="hero">
  <div class="c g">
    <div>{fil(("metiers.html", "Métiers"), ("", m["menu"]))}
      <p class="sur">{m["surtitre"]}</p>
      <h1>{m["h1"]}</h1>
      <p class="chapo">{m["chapo"]}</p>
      <div class="act"><a class="btn" href="#contact">{m["cta"]}</a><a class="btn b2" href="#pages">Voir les pages prévues</a></div>
    </div>
    {ticket()}
  </div>
</section>

<section class="sec" aria-labelledby="rch-h2">
  <div class="c"><p class="sur">Ce que tapent vos clients</p><h2 id="rch-h2">{m["recherches_titre"]}</h2>
  <ul class="puces">{puces}</ul>
  <div class="texte">{intro}</div></div>
</section>

<section class="sec alt" id="pages" aria-labelledby="pg-h2">
  <div class="c"><p class="sur">Jusqu'à {PAGES_MAX} pages</p><h2 id="pg-h2">{m["pages_titre"]}</h2>
  <ul class="liste">{pages_l}</ul></div>
</section>

<section class="sec" aria-labelledby="fi-h2">
  <div class="c"><p class="sur">Fiche Google</p><h2 id="fi-h2">{m["fiche_titre"]}</h2>
  <ul class="liste">{fiche}</ul></div>
</section>

<section class="sec alt" aria-labelledby="pt-h2">
  <div class="c"><p class="sur">Ce qui fait la différence</p><h2 id="pt-h2">{m["points_titre"]}</h2>
  <div class="cartes t3">{points}</div></div>
</section>

{prix.replace("sec alt", "sec") if "prix_html" not in m else m["prix_html"]}
{bloc_ia_metier(m)}
{bloc_faq(m["faq"], sous=m["faq_titre"], alt=True)}
{bloc_metiers(titre="Les autres métiers", exclure=m["slug"])}
{bloc_contact(titre=m["contact_titre"], activite=m["activite"])}'''
    schemas = [
        schema_fil(("metiers.html", "Métiers"), (m["slug"] + ".html", m["menu"])),
        {"@type": "Service", "name": m["service"], "serviceType": "Création de site internet et référencement local",
         "audience": {"@type": "BusinessAudience", "name": m["audience"]}, "provider": {"@id": ORGA["@id"]}, "areaServed": "France",
         **({"offers": {"@type": "Offer", "price": PRIX_SITE, "priceCurrency": "EUR"}} if "prix_html" not in m else {})},
        schema_faq(m["faq"]),
    ]
    return page(m["slug"] + ".html", m["title"], m["description"], corps, schemas)

def visibilite_ia():
    cartes = "".join(f'<div class="carte"><span class="n">{i:02d}</span><h3>{t}</h3><p>{p}</p></div>' for i, (t, p) in enumerate(IA_POINTS, 1))
    faq = [
        ("Qu'est-ce que le référencement dans les IA ?", "C'est le travail qui aide les assistants comme ChatGPT, Gemini, Perplexity ou le mode IA de Google à comprendre votre entreprise et à la proposer quand on leur pose une question sur votre métier. On parle aussi de GEO."),
        ("Est-ce différent du référencement Google ?", "C'est complémentaire. Les IA s'appuient en grande partie sur les mêmes sources que Google : votre site, votre fiche Google, vos avis, les annuaires. Un bon référencement Google est la base, auquel on ajoute ce que les IA attendent en plus."),
        ("Pouvez-vous garantir que ChatGPT me recommandera ?", "Non. Personne ne contrôle les réponses d'une IA, et elles varient d'une question à l'autre. Ce que nous garantissons, c'est le travail fait et un suivi honnête de ce que les IA disent de vous."),
        ("Est-ce compris dans le prix ?", f"Oui. La préparation du site pour les IA est comprise dans le site à {PRIX_SITE} €. Le suivi mensuel des IA fait partie du référencement à {PRIX_SEO} € par mois."),
        ("Les IA lisent-elles vraiment les petits sites ?", "Oui, quand elles cherchent des informations locales, elles consultent les sites et les fiches des entreprises. Encore faut-il que le site ne bloque pas leurs robots et que les informations soient claires."),
    ]
    corps = f'''<section class="hero">
  <div class="c">{fil(("", "Visibilité IA"))}
    <p class="sur">Visibilité dans les IA</p>
    <h1>Référencement dans ChatGPT et les IA pour petites entreprises</h1>
    <p class="chapo">Vos clients ne cherchent plus seulement sur Google : ils demandent aussi à ChatGPT, Gemini ou Perplexity. Votre site et votre fiche Google sont préparés pour que ces IA puissent vous connaître et vous proposer.</p>
    <div class="act"><a class="btn" href="contact.html">Demander mon site</a><a class="btn b2" href="tarifs.html">Voir les tarifs</a></div>
  </div>
</section>
<section class="sec" aria-labelledby="pq-h2">
  <div class="c"><p class="sur">Pourquoi maintenant</p><h2 id="pq-h2">La question ne se tape plus, elle se pose</h2>
  <div class="texte">
    <p>Sur Google, on tape « plombier Marseille ». Dans une IA, on écrit une vraie phrase : « j'ai une fuite sous l'évier, qui appeler ce soir à Marseille ? ». L'IA ne montre pas dix liens : elle donne quelques noms, avec une explication. Être dans cette courte liste devient aussi important que d'être en première page.</p>
    <p>Pour choisir, les IA recoupent ce qu'elles trouvent : votre site, votre fiche Google, vos avis, les annuaires. Une entreprise dont les informations sont claires, complètes et identiques partout a beaucoup plus de chances d'être citée qu'une entreprise au site vide ou contradictoire.</p>
  </div></div>
</section>
<section class="sec alt" aria-labelledby="cf-h2">
  <div class="c"><p class="sur">Ce que nous faisons</p><h2 id="cf-h2">Six chantiers pour être connu des IA</h2><div class="cartes t3">{cartes}</div></div>
</section>
<section class="sec" aria-labelledby="hn-h2">
  <div class="c"><p class="sur">Honnêteté</p><h2 id="hn-h2">Ce que personne ne peut promettre</h2>
  <div class="texte"><p>Les réponses des IA changent selon la question, le moment et l'outil utilisé. Méfiez-vous de qui vous garantit d'être « recommandé par ChatGPT ». Nous vous promettons un travail sérieux et un compte rendu clair chaque mois, pas un résultat que personne ne contrôle.</p></div></div>
</section>
{bloc_offres(alt=True)}
{bloc_faq(faq, sous="Vos questions sur la visibilité dans les IA")}
{bloc_contact()}'''
    schemas = [schema_fil(("visibilite-ia.html", "Visibilité IA")), schema_faq(faq),
               {"@type": "Service", "name": "Visibilité dans les IA (ChatGPT, Gemini, Perplexity) pour petites entreprises", "serviceType": "Référencement dans les moteurs de réponse IA (GEO)", "provider": {"@id": ORGA["@id"]}, "areaServed": "France"}]
    return page("visibilite-ia.html", f"Référencement ChatGPT et IA pour petites entreprises | {MARQUE}",
        "Être proposé par ChatGPT, Gemini et Perplexity : site ouvert aux IA, informations cohérentes, suivi mensuel. Compris dans l'offre, sans promesse impossible.",
        corps, schemas)

def contact():
    corps = f'''<section class="hero">
  <div class="c">{fil(("", "Contact"))}
    <p class="sur">Contact</p>
    <h1>Demander votre site internet</h1>
    <p class="chapo">Dites-nous votre métier et votre ville. Nous vous rappelons pour un échange de 15 minutes, gratuit et sans engagement, puis vous recevez le prix et le délai par écrit.</p>
  </div>
</section>
{bloc_contact(titre="Comment préférez-vous nous joindre ?")}
{bloc_etapes(alt=True)}'''
    return page("contact.html", f"Contact : demander votre site internet à {PRIX_SITE} € | {MARQUE}",
        "Demandez votre site internet et votre fiche Google : appel, WhatsApp, formulaire ou rendez-vous. Échange de 15 minutes gratuit et sans engagement.",
        corps, [schema_fil(("contact.html", "Contact"))])

def legal(chemin, titre, h1, blocs):
    contenu = "".join(f"<h2>{t}</h2>" + "".join(f"<p>{p}</p>" for p in ps) for t, ps in blocs)
    corps = f'''<section class="sec legal"><div class="c">{fil(("", h1))}<h1>{h1}</h1>{contenu}<p style="margin-top:28px;color:var(--doux)">Mise à jour : {AUJOURDHUI}</p></div></section>'''
    return page(chemin, f"{titre} | {MARQUE}", f"{titre} du site {MARQUE}.", corps, [schema_fil((chemin, h1))])

MENTIONS = [
    ("Éditeur du site", ["Le site Premier Résultat est édité par Arslane Kaouadji, entrepreneur individuel (micro-entreprise) immatriculé au Registre national des entreprises — SIREN 106 977 879 — SIRET 106 977 879 00019 — code APE 7021Z — siège : 4 C boulevard Latil, 13008 Marseille, France — téléphone : 06 99 30 58 73 — e-mail : sihem.kazitani13@gmail.com — TVA non applicable, article 293 B du Code général des impôts (franchise en base)."]),
    ("Directrice de la publication", ["Sihem Kazi-Tani, joignable aux coordonnées ci-dessus."]),
    ("Hébergement", ["GitHub Pages, GitHub Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis, github.com."]),
    ("Activité", ["Premier Résultat accompagne les artisans, commerçants, indépendants et petites entreprises dans leur visibilité en ligne : conception et réalisation de sites internet, création et suivi de fiches d'établissement Google, référencement naturel et visibilité dans les moteurs de recherche à intelligence artificielle."]),
    ("Propriété intellectuelle", ["L'ensemble du site (textes, structure, design, code) est protégé par le droit d'auteur. Toute reproduction, représentation ou adaptation, totale ou partielle, sans autorisation écrite est interdite. Les marques et noms cités appartiennent à leurs titulaires respectifs."]),
    ("Responsabilité", ["Nous nous efforçons de maintenir des informations exactes et à jour, sans garantie d'exhaustivité. Les exemples de recherches et de questions présentés sont des illustrations de la méthode et ne constituent ni une promesse de résultat ni une garantie de positionnement dans un moteur de recherche ou une réponse d'intelligence artificielle. L'éditeur ne saurait être tenu responsable des dommages directs ou indirects résultant de l'accès au site ou de son utilisation."]),
    ("Liens", ["Le site peut contenir des liens vers des sites tiers dont l'éditeur ne contrôle pas le contenu."]),
    ("Données personnelles", ['Le traitement des données collectées via le site est décrit dans la <a href="confidentialite.html">politique de confidentialité</a>.']),
    ("Droit applicable", ["Le site est soumis au droit français. Tout litige relatif à son utilisation relève des tribunaux compétents de Marseille, sous réserve des règles d'ordre public applicables aux consommateurs."]),
]
CONFIDENTIALITE = [
    ("Responsable du traitement", ["Arslane Kaouadji, entrepreneur individuel — SIRET 106 977 879 00019 — 4 C boulevard Latil, 13008 Marseille — sihem.kazitani13@gmail.com."]),
    ("Données collectées", ["Uniquement les informations que vous envoyez via le formulaire, WhatsApp, e-mail ou téléphone : nom, activité, ville, coordonnées et message."]),
    ("Finalité et base légale", ["Vous recontacter et vous envoyer une proposition. Base légale : les mesures précontractuelles prises à votre demande."]),
    ("Destinataires", ["Les données ne sont ni vendues ni cédées. Elles transitent par les services utilisés pour vous répondre (messagerie électronique, WhatsApp)."]),
    ("Durée de conservation", ["3 ans après le dernier échange pour les prospects, puis suppression."]),
    ("Vos droits", ["Accès, rectification, effacement, opposition et limitation, en écrivant à sihem.kazitani13@gmail.com. Vous pouvez saisir la CNIL (cnil.fr)."]),
    ("Cookies", ["Ce site n'utilise aucun cookie de mesure d'audience ni de publicité. Les polices de caractères sont chargées depuis Google Fonts."]),
]

def page_404():
    corps = f'''<section class="sec final"><div class="c"><p class="sur">Erreur 404</p><h1>Cette page n'existe pas</h1>
<p class="chapo">Elle a peut-être été déplacée. Voici les pages les plus utiles.</p>
<div class="act"><a class="btn" href="index.html">Accueil</a><a class="btn b2" href="metiers.html">Métiers</a><a class="btn b2" href="tarifs.html">Tarifs</a></div></div></section>'''
    return page("404.html", f"Page introuvable | {MARQUE}", "Page introuvable.", corps).replace(
        '<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">')

FAVICON = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#101623"/><text x="32" y="44" text-anchor="middle" font-family="Arial,sans-serif" font-weight="700" font-size="38" fill="#e4572e">1</text></svg>'''

def llms(pages_seo):
    lignes = [f"# {MARQUE}", "",
        f"> Création de sites internet pour artisans, commerçants, indépendants et PME en France : site jusqu'à {PAGES_MAX} pages et fiche Google créée et remplie pour {PRIX_SITE} €, payable en {NB_FOIS} fois. Référencement Google et visibilité dans les IA (ChatGPT, Gemini, Perplexity) à {PRIX_SEO} € par mois, {ENGAGEMENT} mois minimum, facultatif.",
        "", "Le site appartient au client une fois réglé. Aucune promesse de première place sur Google. Seul frais en plus : le nom de domaine, à son nom.", "", "## Pages", ""]
    for chemin, titre, desc in pages_seo:
        lignes.append(f"- [{titre}]({url(chemin)}) : {desc}")
    return "\n".join(lignes) + "\n"

# ---------------------------------------------------------------- génération
def main():
    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    fichiers = {
        "index.html": accueil(),
        "offre.html": offre(),
        "tarifs.html": tarifs(),
        "metiers.html": hub_metiers(),
        "visibilite-ia.html": visibilite_ia(),
        "contact.html": contact(),
        "mentions-legales.html": legal("mentions-legales.html", "Mentions légales", "Mentions légales", MENTIONS),
        "confidentialite.html": legal("confidentialite.html", "Politique de confidentialité", "Confidentialité", CONFIDENTIALITE),
        "404.html": page_404(),
    }
    for m in METIERS:
        fichiers[m["slug"] + ".html"] = page_metier(m)
    for nom, contenu in fichiers.items():
        (OUT / nom).write_text(contenu, encoding="utf-8")
    (OUT / "assets" / "favicon.svg").write_text(FAVICON, encoding="utf-8")

    indexables = [n for n in fichiers if n != "404.html"]
    prio = {"index.html": "1.0", "offre.html": "0.9", "tarifs.html": "0.9", "metiers.html": "0.8"}
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for n in indexables:
        p = prio.get(n, "0.3" if n in ("mentions-legales.html", "confidentialite.html") else "0.8")
        sitemap.append(f"  <url><loc>{url(n)}</loc><lastmod>{AUJOURDHUI}</lastmod><priority>{p}</priority></url>")
    sitemap.append("</urlset>")
    (OUT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")

    robots = ["User-agent: *", "Allow: /", ""]
    for bot in ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "Applebot-Extended", "Bingbot"]:
        robots += [f"User-agent: {bot}", "Allow: /", ""]
    robots.append(f"Sitemap: {SITE_URL}/sitemap.xml")
    (OUT / "robots.txt").write_text("\n".join(robots) + "\n", encoding="utf-8")

    pages_seo = [
        ("index.html", "Accueil", f"l'offre site à {PRIX_SITE} € + référencement à {PRIX_SEO} €/mois, le B.A.-BA d'un site d'entreprise"),
        ("offre.html", "Ce qui est compris", f"détail du site jusqu'à {PAGES_MAX} pages, de la fiche Google et du suivi mensuel"),
        ("tarifs.html", "Tarifs", f"{PRIX_SITE} € en {NB_FOIS} fois, {PRIX_SEO} € par mois, {ENGAGEMENT} mois minimum"),
        ("metiers.html", "Métiers", "liste des métiers accompagnés"),
        ("visibilite-ia.html", "Visibilité dans les IA", "site préparé pour ChatGPT, Gemini et Perplexity, suivi mensuel de ce que disent les IA, sans promesse de citation"),
    ] + [(m["slug"] + ".html", m["carte_titre"], sans_balises(m["description"])) for m in METIERS] + [
        ("contact.html", "Contact", "appel, WhatsApp, formulaire, rendez-vous"),
    ]
    (OUT / "llms.txt").write_text(llms(pages_seo), encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    print(f"{len(fichiers)} pages générées dans {OUT}")

if __name__ == "__main__":
    main()
