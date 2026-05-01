# Email auto au client quand le salon modifie un RDV en ligne

**Date** : 2026-05-01
**Status** : ✅ Déployé et testé en réel (200 OK, mail reçu mobz57@hotmail.fr)

## Vue d'ensemble

Quand le salon modifie un RDV en ligne (date, heure, collaborateur, prestation, durée),
le client est automatiquement informé :

1. **Visuellement** dans son espace `compte.html` : bandeau orange "⚠️ Modification par
   le salon" avec diff Avant→Après et bouton "J'ai pris connaissance"
2. **Par email** Brevo : envoi automatique <2 sec après la modif via trigger Postgres

## Architecture

```
[Salon modifie RDV dans app.html]
         ↓
[saveAppointment() détecte id préfixé "online_"]
         ↓
[UPDATE rdv_online SET salon_modified_at, salon_modified_fields, ...]
         ↓
[Trigger Postgres trg_email_on_salon_rdv_modification]
         ↓
[fn_email_on_salon_rdv_modification() appelle pg_net.http_post]
         ↓
[Edge function rdv-online-modified-email]
         ↓
[Build email HTML stylé + diff visuel]
         ↓
[POST worker /api/email/custom → Brevo API]
         ↓
[Email reçu par client_email]
```

## Composants

### Edge function `rdv-online-modified-email` (v1)

- **Auth** : header `x-cron-secret` requis (utilise `avis_cron_secret` Vault)
- **Input** : `{ rdv_online_id: uuid }`
- **Logique** :
  1. Charge le RDV (date, heure, collab, service, salon_modified_fields)
  2. Charge le salon (nom + slug)
  3. Build email HTML avec :
     - Header doré Luxyra
     - Tableau "Avant → Après" pour chaque champ modifié
     - Carte "Votre nouveau RDV" en gros (date + heure)
     - CTA "Voir mon compte" → /compte.html
     - Footer avec liens
  4. POST `/api/email/custom` du worker Cloudflare → Brevo

### Trigger Postgres `trg_email_on_salon_rdv_modification`

- **Type** : AFTER INSERT OR UPDATE OF salon_modified_at
- **Sécurité** : SECURITY DEFINER (exécuté avec privilèges propriétaire)
- **Logique** :
  - Skip si `salon_modified_at` est NULL
  - Skip si UPDATE et la valeur n'a pas changé (anti-doublon)
  - Skip si `client_email` vide
  - Lit le secret depuis Vault
  - Appelle l'edge function via `pg_net.http_post` (async, non bloquant)

### DB : colonnes ajoutées sur `rdv_online`

| Colonne | Type | Description |
|---|---|---|
| `salon_modified_at` | timestamptz | Horodatage dernière modif salon (NULL = pas de modif) |
| `salon_modified_fields` | jsonb | Diff `{field: {old, new}, ...}` |
| `salon_modified_acknowledged_by_client` | bool | TRUE si client a cliqué "J'ai pris connaissance" |
| `salon_modified_acknowledged_at` | timestamptz | Quand le client a acquitté |

## Test réel effectué

```sql
-- 1. RDV créé pour mobz57@hotmail.fr (Excellence Coiffure, 15/05 14:00, Amandine)
-- 2. UPDATE simulant modif salon : heure 14:00→15:30, collab Amandine→Manue
-- 3. Trigger se déclenche → pg_net appelle edge function
-- 4. Réponse 200 OK : {"ok":true, "sent_to":"mobz57@hotmail.fr", "fields":["heure_rdv","collaborateur_id","collaborateur_nom"]}
-- 5. Email reçu en 1-2 sec dans la boîte
-- 6. Cleanup OK
```

## Anti-spam / robustesse

- **Pas d'email** si `client_email` est vide ou null
- **Pas de doublon** : trigger ne fire que si `salon_modified_at` change réellement
- **Idempotent** : si plusieurs UPDATE consécutifs avec même salon_modified_at → 1 seul email
- **Async** : pg_net non bloquant — la modif salon est immédiate, l'email part en background

## Limites connues

- Pas de mécanisme de retry si Brevo down (perte de l'email silencieuse)
- Pas de notification SMS (jugé pas prioritaire vs cost SMS)
- Pas de notification push web (cf. discussion : ~3-4h de dev, marche pas sur iOS sans PWA installée)

## Roadmap potentielle (non implémenté)

Si besoin futur :
- [ ] Notification push web (PWA installée)
- [ ] SMS optionnel pour clients sans email
- [ ] Email récap quotidien si plusieurs modifs sur mêmes RDV
- [ ] Trigger côté salon pour notifier que le client a acquitté
