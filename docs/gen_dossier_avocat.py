#!/usr/bin/env python3
"""Dossier technique Luxyra pour avocat fiscaliste - NF525.
v4 : logo Luxyra + commit Git précis + engagement maintien + couverture épurée."""
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                 Table, TableStyle, Image, Flowable)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from datetime import datetime

OUTPUT = "/sessions/quirky-affectionate-hypatia/mnt/outputs/luxyra_dossier_technique_NF525_v4.pdf"
LOGO_PATH = "/sessions/quirky-affectionate-hypatia/luxyra.fr/luxyra-logo.png"

# Métadonnées version du logiciel
COMMIT_HASH = "ffe1d8a39"  # ffe1d8a399525899018d338aff40bcdf71f7d975
COMMIT_DATE = "19 mai 2026 à 20:00 (UTC+2)"
VERSION_LOGICIEL = "v6.3"

# ===== COULEURS =====
GOLD = colors.HexColor("#8b5a2b")
GOLD_LIGHT = colors.HexColor("#c89456")
DARK = colors.HexColor("#1a1a1a")
TEXT = colors.HexColor("#222")
TEXT_LIGHT = colors.HexColor("#555")
BORDER = colors.HexColor("#ddd")
BG_LIGHT = colors.HexColor("#fafafa")

# ===== STYLES =====
ss = getSampleStyleSheet()

def make_style(name, **kw):
    base = kw.pop('parent', ss['Normal'])
    return ParagraphStyle(name, parent=base, **kw)

s_cover_doc = make_style('CoverDoc', fontSize=22, alignment=TA_CENTER, textColor=DARK, fontName='Helvetica-Bold', spaceAfter=8, leading=26)
s_cover_sub = make_style('CoverSub', fontSize=12, alignment=TA_CENTER, textColor=GOLD, fontName='Helvetica', spaceAfter=8)
s_cover_meta = make_style('CoverMeta', fontSize=10, alignment=TA_CENTER, textColor=TEXT_LIGHT, fontName='Helvetica', spaceAfter=4)
s_cover_ref = make_style('CoverRef', fontSize=9, alignment=TA_CENTER, textColor=TEXT_LIGHT, fontName='Helvetica-Oblique')

s_h1 = make_style('H1', fontSize=17, textColor=GOLD, fontName='Helvetica-Bold', spaceAfter=14, spaceBefore=10)
s_h2 = make_style('H2', fontSize=12, textColor=DARK, fontName='Helvetica-Bold', spaceAfter=8, spaceBefore=14)
s_body = make_style('Body', fontSize=10, textColor=TEXT, alignment=TA_JUSTIFY, leading=14, spaceAfter=8)
s_body_bullet = make_style('BodyBul', parent=s_body, leftIndent=14, bulletIndent=4, spaceAfter=4)
s_small = make_style('Small', fontSize=9, textColor=TEXT_LIGHT, spaceAfter=4, leading=12)
s_mono = make_style('Mono', fontName='Courier', fontSize=8.5, leading=11, backColor=colors.HexColor("#f5f5f5"), borderColor=BORDER, borderWidth=0.5, borderPadding=8, spaceBefore=6, spaceAfter=12, leftIndent=4, rightIndent=4)

s_cell_h = make_style('CellH', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white, leading=11)
s_cell = make_style('Cell', fontName='Helvetica', fontSize=8.5, textColor=TEXT, leading=11)
s_cell_b = make_style('CellB', fontName='Helvetica-Bold', fontSize=8.5, textColor=DARK, leading=11)
s_cell_s = make_style('CellS', fontName='Helvetica', fontSize=7.5, textColor=TEXT, leading=10)
s_cell_ref = make_style('CellRef', fontName='Helvetica-Bold', fontSize=8, textColor=GOLD, leading=10)
s_cell_check = make_style('CellChk', fontName='Helvetica-Bold', fontSize=12, alignment=TA_CENTER, textColor=colors.HexColor("#2d7a2d"))

def P(t, st=s_cell): return Paragraph(str(t), st)
def Ph(t): return Paragraph(str(t), s_cell_h)
def Pb(t): return Paragraph(str(t), s_cell_b)
def Ps(t): return Paragraph(str(t), s_cell_s)
def Pr(t): return Paragraph(str(t), s_cell_ref)
def Pc(t): return Paragraph(str(t), s_cell_check)

class HRule(Flowable):
    def __init__(self, width, thickness=0.5, color=BORDER, before=4, after=4):
        super().__init__()
        self.width = width; self.thickness = thickness; self.color = color
        self.before = before; self.after = after
    def wrap(self, *args): return (self.width, self.thickness + self.before + self.after)
    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, self.after, self.width, self.after)

def add_page_footer(canv, doc):
    canv.saveState()
    canv.setFont('Helvetica', 8)
    canv.setFillColor(TEXT_LIGHT)
    page_num = canv.getPageNumber()
    if page_num > 1:
        canv.drawRightString(A4[0] - 2*cm, 1.2*cm, f"Luxyra — Dossier technique NF525 — page {page_num}")
        canv.setStrokeColor(BORDER)
        canv.setLineWidth(0.3)
        canv.line(2*cm, 1.6*cm, A4[0] - 2*cm, 1.6*cm)
    canv.restoreState()

doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=2.2*cm, rightMargin=2.2*cm,
    topMargin=2*cm, bottomMargin=2.2*cm,
    title="Luxyra - Dossier technique NF525",
    author="Alexandre Jensen - Luxyra",
    subject="Conformité NF525 - BOI-CF-COM-10-80-30-10 et 20"
)

story = []

# ===========================================================================
# COUVERTURE — épurée, logo centré
# ===========================================================================
story.append(Spacer(1, 4*cm))

# Logo Luxyra centré (4cm de large)
try:
    logo = Image(LOGO_PATH, width=4*cm, height=4*cm, hAlign='CENTER')
    story.append(logo)
except Exception:
    pass

story.append(Spacer(1, 2*cm))
story.append(Paragraph("DOSSIER TECHNIQUE DE CONFORMITÉ", s_cover_doc))
story.append(Paragraph("Norme NF525", s_cover_sub))
story.append(HRule(15*cm, thickness=1, color=GOLD, before=8, after=16))
story.append(Paragraph("Présentation des mesures techniques mises en œuvre", s_cover_meta))
story.append(Paragraph(
    "BOI-CF-COM-10-80-30-10 · BOI-CF-COM-10-80-30-20", s_cover_ref))

story.append(Spacer(1, 8*cm))
story.append(HRule(15*cm, thickness=0.3, color=BORDER, before=4, after=8))
story.append(Paragraph(
    f"Document émis le {datetime.now().strftime('%d %B %Y').lstrip('0')} · "
    f"Version logiciel {VERSION_LOGICIEL} · Commit Git <font name=\"Courier\">{COMMIT_HASH}</font>",
    s_cover_ref))
story.append(PageBreak())

# ===========================================================================
# PAGE 2 — Identité éditeur + objet du dossier
# ===========================================================================
story.append(Paragraph("Identification de l'éditeur", s_h1))

ident_data = [
    [Pb("Forme juridique"), P("Entrepreneur individuel — micro-entrepreneur")],
    [Pb("Représentant légal"), P("M. Alexandre Jensen")],
    [Pb("Nom commercial"), P("Luxyra")],
    [Pb("SIRET"), P("910 928 464 00023")],
    [Pb("Code APE"), P("5829C — Édition de logiciels applicatifs")],
    [Pb("Adresse siège"), P("29 rue de l'Abbé Alexandre Pax, 57200 Sarreguemines, France")],
    [Pb("Site web"), P("https://luxyra.fr")],
    [Pb("Email"), P("contact@luxyra.fr")],
    [Pb("Régime TVA"), P("Franchise en base — article 293 B du CGI")],
    [Pb("Début d'activité"), P("24 mars 2026")],
]
t_ident = Table(ident_data, colWidths=[4.5*cm, 12*cm])
t_ident.setStyle(TableStyle([
    ('FONT', (0,0), (-1,-1), 'Helvetica', 9),
    ('BOX', (0,0), (-1,-1), 0.5, BORDER),
    ('LINEABOVE', (0,0), (-1,0), 2, GOLD),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.HexColor("#eee")),
    ('BACKGROUND', (0,0), (0,-1), BG_LIGHT),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LEFTPADDING', (0,0), (-1,-1), 10),
    ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ('TOPPADDING', (0,0), (-1,-1), 7),
    ('BOTTOMPADDING', (0,0), (-1,-1), 7),
]))
story.append(t_ident)

story.append(Spacer(1, 0.6*cm))
story.append(Paragraph("Référence du logiciel audité", s_h2))

ver_data = [
    [Pb("Version logiciel"), P(VERSION_LOGICIEL)],
    [Pb("Commit Git de référence"), P(f"<font name=\"Courier\">{COMMIT_HASH}</font>")],
    [Pb("Date du commit"), P(COMMIT_DATE)],
    [Pb("Dépôt"), P("https://github.com/Luxyra-fr/luxyra.fr")],
]
t_ver = Table(ver_data, colWidths=[4.5*cm, 12*cm])
t_ver.setStyle(TableStyle([
    ('FONT', (0,0), (-1,-1), 'Helvetica', 9),
    ('BOX', (0,0), (-1,-1), 0.5, BORDER),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.HexColor("#eee")),
    ('BACKGROUND', (0,0), (0,-1), BG_LIGHT),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LEFTPADDING', (0,0), (-1,-1), 10),
    ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(t_ver)

story.append(Spacer(1, 0.8*cm))
story.append(Paragraph("Objet du dossier", s_h2))
story.append(Paragraph(
    "Le présent dossier est destiné à être présenté à un cabinet d'avocat fiscaliste dans le cadre d'une demande "
    "de <b>consultation juridique d'opinion</b> sur la conformité du logiciel Luxyra aux exigences techniques de la "
    "norme NF525, telles que définies aux articles BOI-CF-COM-10-80-30-10 et BOI-CF-COM-10-80-30-20 du Bulletin "
    "Officiel des Finances Publiques, ainsi qu'aux dispositions du Décret n° 2016-1850 du 23 décembre 2016, de "
    "l'Arrêté du 22 mars 2017, de l'article L102 B du Livre des Procédures Fiscales et de l'article 242 nonies A "
    "du Code Général des Impôts.",
    s_body))
story.append(Paragraph(
    "<b>Engagement de l'éditeur</b> : Alexandre Jensen, en qualité d'éditeur du logiciel Luxyra, s'engage à maintenir "
    "la conformité du logiciel dans le temps et à mettre à jour les mesures techniques en cas d'évolution réglementaire. "
    "Toute modification substantielle du logiciel ou de la réglementation donnera lieu à une mise à jour du présent dossier.",
    s_body))

story.append(PageBreak())

# ===========================================================================
# SOMMAIRE
# ===========================================================================
story.append(Paragraph("Sommaire", s_h1))
toc = [
    ("1.", "Architecture technique générale", "4"),
    ("2.", "Mesures techniques de conformité NF525", "5"),
    ("3.", "Tableau de couverture des exigences BOI-CF-COM-10-80-30", "7"),
    ("4.", "Points dépendant de l'exploitation", "8"),
    ("5.", "Sollicitation d'opinion juridique et annexes disponibles", "9"),
]
toc_data = [[P(f"<b>{n}</b>"), P(t), P(p, make_style('right', alignment=TA_RIGHT, fontSize=9, textColor=TEXT_LIGHT))] for n, t, p in toc]
t_toc = Table(toc_data, colWidths=[1.5*cm, 13*cm, 2*cm])
t_toc.setStyle(TableStyle([
    ('FONT', (0,0), (-1,-1), 'Helvetica', 10),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ('TOPPADDING', (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ('LINEBELOW', (0,0), (-1,-1), 0.25, colors.HexColor("#f0f0f0")),
]))
story.append(t_toc)
story.append(PageBreak())

# ===========================================================================
# 1. ARCHITECTURE
# ===========================================================================
story.append(Paragraph("1. Architecture technique générale", s_h1))
story.append(Paragraph(
    "Luxyra est un logiciel SaaS multi-tenant (un compte par établissement utilisateur — salons de coiffure, "
    "instituts de beauté, barbiers, esthéticiennes, etc.) hébergé sur l'infrastructure Supabase (PostgreSQL "
    "managé, datacenter de Paris, France — région AWS eu-west-3) avec un frontend HTML/JavaScript distribué via "
    "Cloudflare Workers depuis le domaine luxyra.fr.",
    s_body))

story.append(Paragraph("1.1 Composants logiciels", s_h2))
arch_data = [
    [Ph("Couche"), Ph("Technologie"), Ph("Rôle")],
    [Pb("Base de données"), P("PostgreSQL 17.6 (Supabase, datacenter Paris — AWS eu-west-3)"), P("Stockage des tickets, clôtures, audit log, archives signées")],
    [Pb("API"), P("Supabase PostgREST + plus de 40 Edge Functions (Deno)"), P("Accès aux données via Row Level Security + logique métier sécurisée")],
    [Pb("Authentification"), P("Supabase Auth (JWT, bcrypt)"), P("Comptes établissements (gérants) + comptes clients finaux")],
    [Pb("Frontend"), P("HTML/JavaScript natif (app.html, admin.html, site.html)"), P("Interface tablette pour les professionnels + panneau d'administration éditeur")],
    [Pb("Hébergement"), P("Cloudflare Workers (frontend) + Supabase EU (données)"), P("Serveurs en France et Union européenne, conforme RGPD")],
    [Pb("Paiements"), P("Stripe Connect"), P("Encaissement des bons cadeaux et acomptes (compte connecté de l'établissement)")],
    [Pb("Emails transactionnels"), P("Brevo (ex-Sendinblue)"), P("Confirmations RDV, alertes monitoring, factures")],
]
t_arch = Table(arch_data, colWidths=[3.6*cm, 6.4*cm, 6.4*cm])
t_arch.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), GOLD),
    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#999")),
    ('INNERGRID', (0,0), (-1,-1), 0.25, BORDER),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 7),
    ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
]))
story.append(t_arch)

story.append(Paragraph("1.2 Tables fiscales (schéma <font name=\"Courier\">public</font>)", s_h2))
tables_data = [
    [Ph("Table"), Ph("Rôle dans la conformité NF525")],
    [Pb("tickets"), P("Tickets de caisse fiscaux (encaissements). Inaltérables après validation par triggers Postgres.")],
    [Pb("clotures"), P("Clôtures journalières Z. Chaînées par hash SHA-256. Inaltérables.")],
    [Pb("clotures_mensuelles"), P("Clôtures mensuelles signées. Chaînées par hash. Inaltérables.")],
    [Pb("clotures_annuelles"), P("Clôtures annuelles signées (grand total annuel). Chaînées. Inaltérables.")],
    [Pb("archives"), P("Archives annuelles complètes sérialisées en JSON canonique signé SHA-256. Inaltérables.")],
    [Pb("factures_clients"), P("Factures délivrées au client (art. 242 nonies A CGI). Numérotation continue, hash chaîné. Inaltérables.")],
    [Pb("audit_log"), P("Piste d'audit fiable (traçabilité de toutes les opérations). Inaltérable hors erreurs JavaScript techniques.")],
    [Pb("nf525_hash_seal"), P("Scellement automatique différé : chaque ligne fiscale est dupliquée sous forme de snapshot canonique chaîné.")],
    [Pb("nf525_inventory_snapshots"), P("Snapshot quotidien de volumétrie pour détecter toute disparition anormale de données fiscales.")],
]
t_tables = Table(tables_data, colWidths=[4.5*cm, 12*cm])
t_tables.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), GOLD),
    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#999")),
    ('INNERGRID', (0,0), (-1,-1), 0.25, BORDER),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
]))
story.append(t_tables)
story.append(PageBreak())

# ===========================================================================
# 2. MESURES TECHNIQUES
# ===========================================================================
story.append(Paragraph("2. Mesures techniques de conformité NF525", s_h1))

story.append(Paragraph("2.1 Inaltérabilité (BOI §60)", s_h2))
story.append(Paragraph(
    "Tout ticket validé (<font name=\"Courier\">status='paid'</font> ou <font name=\"Courier\">locked=true</font>) est protégé "
    "par trois triggers PostgreSQL qui interceptent toute tentative de modification ou de suppression :", s_body))
story.append(Paragraph(
    "<b>tickets_nf525_protect</b> (BEFORE UPDATE/DELETE) : déclenche une exception en cas de modification de l'un "
    "des 17 champs sensibles (items, totaux HT/TVA/TTC, taux de TVA, mode de paiement, date, heure, "
    "numéro, hash, identifiants client / collaborateur / établissement, etc.).", s_body))
story.append(Paragraph(
    "<b>ticket_nf525_delete</b> (BEFORE DELETE) : déclenche une exception pour tout appel issu des rôles "
    "applicatifs (anonyme, authentifié).", s_body))
story.append(Paragraph(
    "<b>trg_tickets_nf525_protect</b> : défense en profondeur supplémentaire (double protection sur "
    "DELETE et UPDATE).", s_body))
story.append(Paragraph(
    "Les clôtures (journalières, mensuelles, annuelles), les archives, les factures clients et le journal d'audit "
    "bénéficient de triggers d'inaltérabilité similaires. La seule manière de contourner ces protections est de positionner "
    "explicitement la variable de session <font name=\"Courier\">luxyra.allow_nf525_unlock = 'true'</font>, ce qui produit "
    "automatiquement une trace dans le journal d'audit (action <i>NF525_INALTERABILITE_BYPASSEE</i>) — utilisé "
    "uniquement pour les opérations de maintenance documentées.", s_body))

story.append(Paragraph("2.2 Sécurisation cryptographique (BOI §70)", s_h2))
story.append(Paragraph(
    "Chaque ticket est signé par un hash <b>SHA-256</b> (algorithme FIPS 180-4) calculé sur les données canoniques et "
    "chaîné avec le hash du ticket précédent du même établissement (champ <font name=\"Courier\">hash_prev</font>). "
    "Toute manipulation rompt la chaîne et est immédiatement détectable.", s_body))
story.append(Paragraph("Formule du hash d'un ticket :", s_small))
story.append(Paragraph(
    "SHA-256( \"TK\" | num | date | heure | total_ttc | total_ht | items | hash_prev | salon_id | siret )",
    s_mono))
story.append(Paragraph(
    "Les clôtures journalières, mensuelles, annuelles et les factures clients suivent le même mécanisme avec des "
    "préfixes distincts (<font name=\"Courier\">Z|</font>, <font name=\"Courier\">ZM|</font>, "
    "<font name=\"Courier\">ZA|</font>, <font name=\"Courier\">FC|</font>). La table <font name=\"Courier\">nf525_hash_seal</font> "
    "stocke un scellement automatique différé de chaque ligne fiscale avec champs <font name=\"Courier\">canonical_data</font>, "
    "<font name=\"Courier\">canonical_sha256</font>, <font name=\"Courier\">row_snapshot_sha256</font>, "
    "<font name=\"Courier\">chain_index</font>, <font name=\"Courier\">chain_prev_hash</font>, "
    "<font name=\"Courier\">chain_hash</font>. Ce double scellement permet une vérification de l'intégrité complète à tout moment.", s_body))

story.append(Paragraph("2.3 Conservation 6 ans (BOI §80 — article L102 B LPF)", s_h2))
story.append(Paragraph(
    "Les données sont conservées dans la base PostgreSQL hébergée par Supabase. Aucun mécanisme automatique "
    "de purge n'est appliqué aux tables fiscales. Le seul travail de cleanup automatisé "
    "(<font name=\"Courier\">_monitoring_auto_cleanup</font>) supprime uniquement les erreurs JavaScript techniques "
    "(JS_ERROR, JS_CONSOLE_ERROR, JS_ERROR_PUBLIC) après 90 jours, qui ne font pas partie de la piste d'audit fiscale. "
    "Un snapshot d'inventaire quotidien (exécuté à 04:00 UTC) surveille toute baisse anormale de volumétrie et alerte "
    "automatiquement par email l'éditeur.", s_body))

story.append(Paragraph("2.4 Clôtures périodiques (BOI §90)", s_h2))
story.append(Paragraph("Trois niveaux de clôture, tous signés et chaînés :", s_body))
story.append(Paragraph(
    "<b>Clôture journalière (Z)</b> : émise par l'opérateur en fin de journée. Numérotation continue par établissement "
    "(contrainte unique <font name=\"Courier\">(salon_id, num)</font>). Hash SHA-256 chaîné. Stockée dans la table "
    "<font name=\"Courier\">clotures</font>. Un cron quotidien à 01:00 UTC détecte les journées avec activité sans Z "
    "et alerte l'éditeur.", s_body))
story.append(Paragraph(
    "<b>Clôture mensuelle</b> : générée automatiquement le 1er de chaque mois à 03:15 UTC. Agrège les Z du mois "
    "précédent avec hash chaîné. La cohérence des cumuls est vérifiée quotidiennement par "
    "<font name=\"Courier\">check_data_integrity()</font> (règles CUMUL_MOIS_INCOHERENT et CUMUL_ANNEE_INCOHERENT).", s_body))
story.append(Paragraph(
    "<b>Clôture annuelle</b> : générée automatiquement le 1er janvier à 03:30 UTC. Hash chaîné des clôtures mensuelles "
    "de l'année écoulée.", s_body))
story.append(Paragraph(
    "<b>Archive annuelle complète signée</b> : générée automatiquement le 1er février à 04:00 UTC. Sérialise l'intégralité "
    "de l'année (tickets + Z + ZM + ZA) en JSON canonique, calcule un hash SHA-256 et insère le tout dans la table "
    "<font name=\"Courier\">archives</font> (inaltérable).", s_body))

story.append(Paragraph("2.5 Traçabilité — piste d'audit fiable (BOI §110)", s_h2))
story.append(Paragraph(
    "La table <font name=\"Courier\">audit_log</font> centralise toutes les actions sensibles : création de ticket, "
    "clôture Z, clôture mensuelle, clôture annuelle, duplicata de ticket, duplicata de Z, effacement RGPD, "
    "ticket d'avoir, génération d'archive annuelle, encaissement par un opérateur tiers, etc. Chaque ligne contient "
    "l'identifiant de l'établissement, l'action, son détail, l'identifiant et le nom de l'opérateur, et un horodatage "
    "TIMESTAMPTZ (timezone-aware). Le trigger <font name=\"Courier\">audit_log_nf525_inalterable</font> empêche toute "
    "modification ou suppression des entrées du journal sauf les erreurs JavaScript techniques purgeables.", s_body))

story.append(Paragraph("2.6 Annulation conforme — ticket d'avoir (BOI §100)", s_h2))
story.append(Paragraph(
    "Un ticket validé ne peut jamais être modifié ni supprimé. Pour annuler une opération, la procédure "
    "<font name=\"Courier\">creer_ticket_avoir(ticket_origine_id, motif)</font> émet un nouveau ticket signé respectant les "
    "obligations suivantes :", s_body))
story.append(Paragraph("• Numérotation continue (prochain numéro de l'établissement)", s_body_bullet))
story.append(Paragraph("• Montants opposés au ticket d'origine (négatifs)", s_body_bullet))
story.append(Paragraph("• Lien explicite vers le ticket d'origine via <font name=\"Courier\">parent_ticket_id</font> et flag <font name=\"Courier\">is_avoir = true</font>", s_body_bullet))
story.append(Paragraph("• Motif obligatoire (minimum 3 caractères)", s_body_bullet))
story.append(Paragraph(
    "Le ticket d'origine est marqué <font name=\"Courier\">status='cancelled'</font> mais reste intact dans la base. Une "
    "contrainte <font name=\"Courier\">CHECK</font> en base garantit qu'un ticket d'avoir a obligatoirement un "
    "<font name=\"Courier\">parent_ticket_id</font> et un <font name=\"Courier\">total_ttc</font> négatif.", s_body))

story.append(Paragraph("2.7 Réimpression de duplicata (BOI §120)", s_h2))
story.append(Paragraph(
    "Toute réimpression d'un ticket ou d'une clôture Z affiche obligatoirement la mention <b>DUPLICATA</b> dans un encadré "
    "noir épais centré en haut du document. Chaque réimpression est tracée dans le journal d'audit (action DUPLICATA_TICKET "
    "ou DUPLICATA_CLOTURE_Z) avec horodatage et identifiant de l'opérateur émetteur.", s_body))

story.append(Paragraph("2.8 Sécurité multi-tenant — RLS", s_h2))
story.append(Paragraph(
    "PostgreSQL Row Level Security est activée sur toutes les tables sensibles. Les politiques d'accès filtrent strictement "
    "par établissement (jointure entre <font name=\"Courier\">salon_id</font> et "
    "<font name=\"Courier\">salons.user_id = auth.uid()</font>) afin d'empêcher toute fuite de données entre établissements. "
    "Les Edge Functions internes utilisent <font name=\"Courier\">service_role</font> uniquement lorsque l'opération "
    "requiert un bypass contrôlé (inscription d'un client, génération de facture, etc.) — ce qui est tracé dans le journal d'audit.", s_body))

story.append(PageBreak())

# ===========================================================================
# 3. TABLEAU AUDIT
# ===========================================================================
story.append(Paragraph("3. Tableau de couverture des exigences BOI-CF-COM-10-80-30", s_h1))
story.append(Paragraph(
    "Le tableau ci-dessous présente chaque exigence réglementaire identifiée et l'implémentation correspondante dans "
    "le logiciel Luxyra. L'évaluation finale de la conformité juridique relève du cabinet d'avocat consulté.",
    s_body))

audit_data = [
    [Ph("Référence"), Ph("Exigence réglementaire"), Ph("État"), Ph("Implémentation dans Luxyra")],
    [Pr("BOI §60"), Ps("Inaltérabilité (modification et suppression interdites)"), Pc("✓"), Ps("Triggers tickets_nf525_protect, ticket_nf525_delete, trg_tickets_nf525_protect, audit_log_nf525_inalterable, clotures_z_inalterable, clotures_mens_inalterable, clotures_annu_inalterable, archives_inalterable, factures_clients_inalterable. Bypass uniquement via flag de session tracé en audit.")],
    [Pr("BOI §70"), Ps("Sécurisation par chaînage cryptographique"), Pc("✓"), Ps("Hash SHA-256 (FIPS 180-4) sur tickets, clôtures Z/mensuelles/annuelles, archives, factures clients. Chaînage par hash_prev. Double scellement nf525_hash_seal avec chain_index croissant.")],
    [Pr("BOI §80"), Ps("Conservation 6 ans (article L102 B LPF)"), Pc("✓"), Ps("Aucun cron de purge sur les tables fiscales. Snapshot quotidien d'inventaire pour détection d'altération. Hébergement Supabase EU avec sauvegardes managées.")],
    [Pr("BOI §90"), Ps("Archivage périodique signé"), Pc("✓"), Ps("Génération automatique d'une archive annuelle JSON canonique signée SHA-256 dans la table archives (inaltérable). Cron au 1er février.")],
    [Pr("BOI §100"), Ps("Annulation par contre-ticket"), Pc("✓"), Ps("RPC creer_ticket_avoir : numérotation continue, montants négatifs, parent_ticket_id obligatoire, motif obligatoire (3 caractères minimum). Contrainte CHECK en base.")],
    [Pr("BOI §110"), Ps("Traçabilité — piste d'audit fiable"), Pc("✓"), Ps("Table audit_log avec operator_id, operator_name, timestamp_action timezone-aware. Trigger d'inaltérabilité. Plus de 20 catégories d'actions tracées.")],
    [Pr("BOI §120"), Ps("Duplicata identifié et tracé"), Pc("✓"), Ps("Mention DUPLICATA imprimée en encadré sur tickets et Z réémis. Trace audit DUPLICATA_TICKET / DUPLICATA_CLOTURE_Z.")],
    [Pr("BOI-20 §1"), Ps("Z journalier obligatoire en fin de journée"), Pc("✓"), Ps("Cron quotidien 01:00 UTC détecte les journées avec activité sans Z et alerte automatiquement.")],
    [Pr("BOI-20 §2"), Ps("Clôture mensuelle recommandée"), Pc("✓"), Ps("Cron automatique au 1er du mois à 03:15 UTC. Table clotures_mensuelles signée et chaînée.")],
    [Pr("BOI-20 §3"), Ps("Clôture annuelle obligatoire"), Pc("✓"), Ps("Cron automatique au 1er janvier à 03:30 UTC. Table clotures_annuelles signée et chaînée.")],
    [Pr("BOI-20 §4"), Ps("Numérotation continue sans rupture"), Pc("✓"), Ps("Contraintes UNIQUE(salon_id, num) sur tickets, clotures, clotures_mensuelles, clotures_annuelles, factures_clients.")],
    [Pr("BOI-20 §5"), Ps("Identification de l'opérateur"), Pc("✓"), Ps("Champs collaborateur_id et collaborateur_nom sur tickets. Contrainte CHECK tickets_operator_required.")],
    [Pr("BOI-20 §6"), Ps("Horodatage avec source fiable"), Pc("✓"), Ps("Tous champs TIMESTAMPTZ NOT NULL. Source = horloge serveur PostgreSQL UTC synchronisée NTP.")],
    [Pr("BOI-20 §7"), Ps("Données minimales obligatoires du ticket"), Pc("✓"), Ps("num, date, heure, total_ttc, total_ht, total_tva, taux_tva, mode_paiement, SIRET (rendu obligatoire pour les établissements actifs via trigger).")],
    [Pr("BOI-20 §8"), Ps("Cohérence des cumuls périodiques"), Pc("✓"), Ps("Règles CUMUL_MOIS_INCOHERENT et CUMUL_ANNEE_INCOHERENT dans check_data_integrity() exécuté quotidiennement.")],
    [Pr("Art. 242 nonies A CGI"), Ps("Facture client (sur demande, B2B ou > 25 €)"), Pc("✓"), Ps("Table factures_clients et RPC generer_facture_client. Numérotation continue, hash chaîné, inaltérable.")],
    [Pr("Décret 2016-1850"), Ps("Mention TICKET DE CAISSE"), Pc("✓"), Ps("Inscrit en tête de chaque ticket émis (fonction de génération PDF côté frontend).")],
    [Pr("RGPD art. 17"), Ps("Droit à l'effacement"), Pc("✓"), Ps("RPC rgpd_delete_client_atomic (transaction PostgreSQL). Les tickets fiscaux ne sont pas supprimés (art. 17.3.b — conservation pour obligation légale).")],
    [Pr("RGPD art. 7"), Ps("Consentement marketing opt-in actif"), Pc("✓"), Ps("Cases SMS et email non pré-cochées sur formulaires d'inscription. Conforme à la délibération CNIL 2020-091.")],
]

t_audit = Table(audit_data, colWidths=[2.6*cm, 4.6*cm, 1.2*cm, 8.4*cm], repeatRows=1)
t_audit.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), GOLD),
    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#999")),
    ('INNERGRID', (0,0), (-1,-1), 0.25, BORDER),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 5),
    ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('ALIGN', (2,0), (2,-1), 'CENTER'),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
]))
story.append(t_audit)
story.append(PageBreak())

# ===========================================================================
# 4. POINTS D'EXPLOITATION
# ===========================================================================
story.append(Paragraph("4. Points dépendant de l'exploitation", s_h1))
story.append(Paragraph(
    "Certains aspects de la conformité dépendent de la configuration d'exploitation et non du code applicatif. Ils sont "
    "présentés ici pour transparence et complétude du dossier.", s_body))

story.append(Paragraph("4.1 Sauvegardes Supabase (Point-in-Time Recovery)", s_h2))
story.append(Paragraph(
    "La conservation 6 ans des données fiscales est garantie au niveau applicatif par l'absence de mécanismes de purge "
    "(cf. §2.3) et par les triggers d'inaltérabilité. La redondance physique des données est assurée par les sauvegardes "
    "automatiques du prestataire d'hébergement Supabase. L'activation de la fonctionnalité PITR (Point-In-Time Recovery, "
    "sauvegarde point-in-time sur 7 jours minimum) requiert l'abonnement au plan Pro de Supabase. Cette activation est "
    "recommandée pour la conformité à l'article L102 B du LPF.", s_body))

story.append(Paragraph("4.2 Interface utilisateur de la facture client", s_h2))
story.append(Paragraph(
    "La logique métier de génération de facture client (table <font name=\"Courier\">factures_clients</font> et RPC "
    "<font name=\"Courier\">generer_facture_client</font>) est en place et conforme aux exigences de numérotation, de "
    "signature et d'inaltérabilité. L'intégration de l'interface utilisateur correspondante (bouton « Émettre facture » "
    "dans l'application destinée au professionnel) est planifiée pour une prochaine version du frontend, sans impact "
    "sur la conformité technique de la base.", s_body))

story.append(Paragraph("4.3 Statut de certification NF525", s_h2))
story.append(Paragraph(
    "Le logiciel Luxyra n'a pas encore été soumis à la certification NF525 officielle délivrée par un organisme tiers "
    "agréé AFNOR (LNE ou Infocert). L'éditeur s'appuie à ce stade sur l'<b>attestation individuelle d'éditeur</b> autorisée "
    "par la loi de finances 2018 (article 88 de la loi 2017-1837 du 30 décembre 2017), laquelle est publiée sur le site "
    "à l'adresse <font name=\"Courier\">https://luxyra.fr/nf525-attestation-generale.html</font>.", s_body))
story.append(Paragraph(
    "La consultation juridique d'opinion sollicitée auprès du cabinet d'avocat fiscaliste vise à apporter une expertise "
    "tierce sur la solidité technique de cette attestation individuelle, dans l'attente d'une éventuelle certification "
    "officielle ultérieure.", s_body))

story.append(PageBreak())

# ===========================================================================
# 5. SOLLICITATION
# ===========================================================================
story.append(Paragraph("5. Sollicitation d'opinion juridique", s_h1))
story.append(Paragraph(
    "Sur la base du présent dossier, l'éditeur sollicite du cabinet d'avocat fiscaliste une <b>consultation juridique "
    "d'opinion écrite</b> portant sur le respect par le logiciel Luxyra des exigences techniques de la norme NF525 "
    "visées aux dispositions suivantes :", s_body))
story.append(Spacer(1, 0.2*cm))
story.append(Paragraph("• BOI-CF-COM-10-80-30-10 — Caractéristiques", s_body_bullet))
story.append(Paragraph("• BOI-CF-COM-10-80-30-20 — Modalités d'application", s_body_bullet))
story.append(Paragraph("• Décret n° 2016-1850 du 23 décembre 2016", s_body_bullet))
story.append(Paragraph("• Arrêté du 22 mars 2017", s_body_bullet))
story.append(Paragraph("• Article L102 B du Livre des Procédures Fiscales", s_body_bullet))
story.append(Paragraph("• Article 242 nonies A du Code Général des Impôts", s_body_bullet))
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph(
    "La note d'opinion devra être <b>utilisable commercialement</b> sur le site et la documentation Luxyra, ainsi que "
    "présentable lors d'éventuels contrôles fiscaux portant sur un établissement utilisateur du logiciel.", s_body))
story.append(Paragraph(
    "L'éditeur s'engage à fournir tout complément technique nécessaire à la mission : accès au code source, schéma "
    "complet de la base de données (DDL), exports d'archives signées, démonstration en environnement de test, etc.", s_body))

story.append(Spacer(1, 0.8*cm))
story.append(Paragraph("Contact pour échanges techniques", s_h2))
contact_data = [
    [Pb("Nom"), P("M. Alexandre Jensen")],
    [Pb("Qualité"), P("Éditeur — micro-entrepreneur")],
    [Pb("Email"), P("contact@luxyra.fr")],
    [Pb("Adresse"), P("29 rue de l'Abbé Alexandre Pax, 57200 Sarreguemines")],
    [Pb("SIRET"), P("910 928 464 00023")],
]
t_contact = Table(contact_data, colWidths=[3.5*cm, 13*cm])
t_contact.setStyle(TableStyle([
    ('BOX', (0,0), (-1,-1), 0.5, BORDER),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.HexColor("#eee")),
    ('BACKGROUND', (0,0), (0,-1), BG_LIGHT),
    ('LINEABOVE', (0,0), (-1,0), 1.5, GOLD),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('LEFTPADDING', (0,0), (-1,-1), 10),
    ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ('TOPPADDING', (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
]))
story.append(t_contact)

story.append(Spacer(1, 0.8*cm))
story.append(Paragraph("Annexes disponibles sur demande", s_h2))
annexes = [
    "Schéma SQL complet des tables fiscales (DDL)",
    "Code source des triggers d'inaltérabilité",
    "Code source des fonctions de scellement SHA-256",
    "Exemples d'archives annuelles signées (JSON canonique)",
    "Extraits du journal d'audit (audit_log) couvrant une période d'activité",
    "Accès à une démonstration en environnement de test",
]
for a in annexes:
    story.append(Paragraph(f"• {a}", s_body_bullet))

story.append(Spacer(1, 1*cm))
story.append(HRule(15*cm, thickness=0.5, color=BORDER, before=4, after=4))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    f"<i>Document établi par M. Alexandre Jensen, éditeur de Luxyra (SIRET 910 928 464 00023), "
    f"sur la version {VERSION_LOGICIEL} du logiciel (commit Git {COMMIT_HASH}).</i>",
    make_style('Foot', fontSize=8, textColor=TEXT_LIGHT, alignment=TA_CENTER, leading=11)))

doc.build(story, onFirstPage=add_page_footer, onLaterPages=add_page_footer)
print(f"PDF généré : {OUTPUT}")
