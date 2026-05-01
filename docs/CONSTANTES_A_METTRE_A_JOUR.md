# Constantes critiques à mettre à jour quand elles changent

Ce document liste **tous les endroits** où certaines valeurs business sont
codées en dur dans la plateforme Luxyra. Quand l'une d'elles change, faire
le tour de tous les fichiers ci-dessous.

---

## 1. Frais Stripe (CB EU)

**Valeur actuelle** : `1,5% + 0,25 €` (tarif standard Stripe France 2024-2026)

**Sources de vérité** :
- [Stripe France pricing](https://stripe.com/fr/pricing) (à vérifier régulièrement)
- Mai 2024 : Stripe a augmenté de 1,4% → 1,5% pour la France

**À modifier dans** :

| Fichier | Ligne (approx) | Quoi |
|---|---|---|
| `app.html` | ~14834 | `Math.round((brut*0.015 + 0.25)*100)/100` (calcul) |
| `app.html` | ~14830 | Header "Frais Stripe estimés (1,5% + 0,25€)" |
| `app.html` | ~14850 | Footer "Frais Stripe estimés (1,5% + 0,25€ — CB EU)" |
| `app.html` | ~14986 | Calcul dans pack ZIP : `0.015+0.25` |
| `app.html` | ~14988 | Header pack ZIP "Frais Stripe estimés (1,5%..." |
| `app.html` | ~14990 | Footer note pack ZIP "Frais estimés selon tarif standard..." |
| `aide.html` | ~217 | FAQ Stripe Connect : "frais Stripe : 1,5%..." |
| `tarifs.html` | ~223 | Bullet point Pro : "Stripe Connect : 1,5%..." |
| `tarifs.html` | ~314 | FAQ commission : "frais standards (1,5%..." |
| **edge function** `salon-onboarding-email` | dans `STRIPE_FEE_PCT` constant | "1,5%" |
| **edge function** `salon-onboarding-email` | dans `STRIPE_FEE_FIXED` constant | "0,25 €" |

**Conseil** : si les frais changent souvent, envisager de centraliser dans
une seule constante DB (`config_global.stripe_fee_pct`) lue côté UI.

**Tarifs spécifiques** (pour info, à mettre à jour aussi si change) :
- CB EU/EEE : 1,5% + 0,25 €
- CB UK : 2,5% + 0,25 €
- CB hors EU : 3,25% + 0,25 €
- SEPA Debit : 0,8% (max 5 €) + 0,25 €

---

## 2. Bonus SMS au 1er paiement Pro

**Valeur actuelle** : `150 SMS` one-shot (fini les 30/mois)

**À modifier dans** :

| Fichier | Quoi |
|---|---|
| `docs/luxyra-router-worker.js` | `case "invoice.paid"` → `+ 150` (Cloudflare Worker) |
| `app.html` | Plusieurs endroits "150 SMS offerts" (UI marketing) |
| `aide.html` | FAQ SMS |
| `tarifs.html` | Bullet point Pro |
| `inscription.html` | Article 3 du contrat |
| `cgv.html` | Article forfaits |
| `admin.html` | KPI page SMS |
| **edge function** `salon-onboarding-email` | constante `SMS_BONUS_FIRST_PAY` (centralisé v5) |

---

## 3. Prix unitaire SMS facturé

**Valeur actuelle** : `0,065 € TTC` par SMS

**À modifier dans** :

| Fichier | Quoi |
|---|---|
| `app.html` | Plusieurs mentions dans la section SMS Marketing |
| **edge function** `salon-onboarding-email` | constante `SMS_PRICE` (centralisé v5) |

---

## 4. Cotisations URSSAF micro-entrepreneur

**Valeurs actuelles 2024-2026** :
- Services BIC (prestations) : `22,2%`
- Ventes BIC (marchandises) : `12,3%`

**Source** : [autoentrepreneur.urssaf.fr](https://www.autoentrepreneur.urssaf.fr)

**À modifier dans** :
- `app.html` : `expDeclarationURSSAF()` et dans pack ZIP

**Note** : ces taux peuvent inclure ou exclure CFP / CFE selon les années,
vérifier le détail officiel.

---

## 5. Seuils micro-entrepreneur

**Valeurs actuelles 2024-2026** :

| Type | Seuil régime micro | Seuil franchise TVA |
|---|---|---|
| Services (BIC + BNC) | 77 700 € | 36 800 € |
| Ventes / restauration | 188 700 € | 91 900 € |

**Source** : [art. 50-0 et 293B du CGI](https://www.economie.gouv.fr/cedef/seuils-micro-entreprise)

**À modifier dans** :
- `app.html` : objet `MICRO_SEUILS = { ca_services, ca_ventes, tva_services, tva_ventes }`

---

## 6. Plan comptable général FR (codes comptes)

**Valeurs actuelles** (pour journal des ventes) :

| Compte | Usage |
|---|---|
| 706000 | Prestations de services |
| 707000 | Ventes de marchandises |
| 445710 | TVA collectée à 20% |
| 445720 | TVA collectée à 10% |
| 445730 | TVA collectée à 5,5% |
| 511000 | Banque (générique) |
| 511200 | Chèques à encaisser |
| 512000 | Banque - virements |
| 512100 | Banque - encaissements CB |
| 530000 | Caisse (espèces) |

**À modifier dans** :
- `app.html` : `expJournalComptable()` et dans pack ZIP

**Note** : ces codes sont stables (PCG ne change pratiquement jamais), pas
besoin de mettre à jour souvent.

---

## 7. Tarifs abonnements Luxyra

**Valeurs actuelles** :
- Essentiel : `14,99 € / mois`
- Pro : `24,99 € / mois`

**À modifier dans** :
- Tous les fichiers HTML qui affichent les prix
- `inscription.html`, `tarifs.html`, `pro.html`, `cgv.html`, `app.html` (modal upgrade)
- Cloudflare Worker (CONFIG.PRICE_ESSENTIAL et PRICE_PRO → IDs Stripe)
- Stripe Dashboard (créer nouveaux prix si changement)

---

## Méthode recommandée pour un futur changement

1. Mettre à jour la valeur dans la **source de vérité** (CGI, Stripe, URSSAF)
2. Faire un grep dans le repo : `grep -rn "1,5%\|0.015" .` (ou la valeur précédente)
3. Remplacer dans tous les fichiers listés ci-dessus
4. Re-déployer l'edge function si modifiée
5. Re-pousser via Cloudflare Worker si modifié
6. Mettre à jour ce document avec la nouvelle valeur + date du changement

## Historique

- 2026-05-01 : création du doc + Stripe 1,4% → 1,5% + NF525 "certifié" → "conforme"
- 2026-04-XX : Bonus 150 SMS one-shot (avant : 30 SMS/mois)
- 2026-04-XX : Métier + Nom + SIRET locked (modif super-admin uniquement)
