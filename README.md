# EventBot

Bot Discord qui déverrouille automatiquement un salon texte quand une conférence vocale commence.

## Setup

### 1. Configurer les IDs dans `bot.py`

Dans la section `PAIRS`, remplace les IDs par ceux de tes salons :

```python
PAIRS = [
    {
        "voice_id": TON_ID_VOCAL,   # Clic droit sur le salon → Copier l'ID
        "text_id":  TON_ID_TEXTE,
    },
]
```

> Active le **Mode développeur** dans Discord : Paramètres → Avancé → Mode développeur

### 2. Permissions du bot

Dans le portail développeur Discord, donne au bot :
- `View Channels`
- `Manage Channels` (pour modifier les permissions)
- `Send Messages`

Et l'intent : **Server Members Intent** + **Voice States**

### 3. Déployer sur Railway

Variables d'environnement à ajouter :
```
DISCORD_TOKEN = ton_token_ici
PORT = 8080
```

Push sur GitHub → Railway détecte et déploie automatiquement.

## Comportement

| Situation | Action |
|---|---|
| 1ère personne rejoint le vocal | ✅ Salon texte déverrouillé |
| Dernière personne quitte le vocal | 🔒 Salon texte verrouillé |
| Bot dans le vocal | Ignoré (ne compte pas) |

## Ajouter plusieurs paires vocal/texte

```python
PAIRS = [
    {"voice_id": 111, "text_id": 222},
    {"voice_id": 333, "text_id": 444},
]
```
