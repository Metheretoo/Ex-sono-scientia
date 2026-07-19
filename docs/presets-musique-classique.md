# Presets pour Musique Classique — Guide de Configuration

## 🎹 Tableau Comparatif des Transcripteurs pour Chopin

| Paramètre | Piano Transcription (ByteDance) | Transkun (Sony) | hFT-Transformer (Sony) |
|---|---|---|---|
| **Meilleur pour** | Pop, rock, piano solo propre | Expressivité, nuance, piano complexe | Musique classique (Chopin, Debussy) |
| **Sensibilité notes graves** | Bonne | Moyenne | **Excellente** (protection explicite < Do1) |
| **Notes pianissimo** | Correctes | Bonnes | **Excellentes** (seuil 0.15-0.25) |
| **Détection pédale** | Moyenne | Bonne | **Excellente** (pédales longues) |
| **Arpèges rapides** | Standard | Très bons | **Excellents** (micro-rythmes) |
| **Rubato** | Bon | Excellent | **Excellent** |
| **Triolets** | Bon | Excellent | **Excellent** |
| **Filtrage harmonique** | Classique | Transkun | Anti-pédale spécialisé |

---

## 🎼 Presets Recommandés par Compositeur

### Chopin (Nocturnes, Mazurkas, Ballades)

| Preset | Transcripteur | Quantification | Seuil | Filtrage | Snap | Notes |
|---|---|---|---|---|---|---|
| **hFT-Classique** | hFT-Transformer | Légère (1/32) | 0.25 | Anti-pédale | 0.3 | **Recommandé** — équilibre parfait |
| **hFT-Expressif** | hFT-Transformer | Légère (1/32) | 0.15 | Anti-pédale | 0.2 | Nocturnes très doux, passages pianissimo |
| **hFT-Précision** | hFT-Transformer | Standard (1/16) | 0.35 | Classique renforcé | 0.45 | Mazurkas, passages virtuoses |
| **Precision** | Transkun | Précision (1/32) | 0.90 | Transkun | 0.90 | Alternative si hFT non disponible |
| **Ultra-classique** | Piano Transcription | Ultra-classique (1/16) | 0.30 | Ultra | 0.5 | Si Transkun/hFT indisponible |

### Debussy (L'Isle Joyeuse, Reflets)

| Preset | Transcripteur | Quantification | Seuil | Filtrage | Snap | Notes |
|---|---|---|---|---|---|---|
| **hFT-Classique** | hFT-Transformer | Légère (1/32) | 0.25 | Anti-pédale | 0.3 | **Recommandé** — arpèges préservés |
| **hFT-Expressif** | hFT-Transformer | Légère (1/32) | 0.15 | Anti-pédale | 0.2 | Arpèges très rapides, fluidité |
| **Classique-soft** | Piano Transcription | Classique-soft | 0.35 | Ultra | 0.5 | Alternative douce |

### Lisht (Études, Rhapsodies)

| Preset | Transcripteur | Quantification | Seuil | Filtrage | Snap | Notes |
|---|---|---|---|---|---|---|
| **hFT-Précision** | hFT-Transformer | Standard (1/16) | 0.35 | Classique renforcé | 0.45 | **Recommandé** — filtrage agressif |
| **Precision** | Transkun | Précision (1/32) | 0.90 | Transkun | 0.90 | Alternative très précise |
| **Ultra-classique** | Piano Transcription | Ultra-classique (1/16) | 0.30 | Ultra | 0.5 | Alternative si Transkun/hFT indisponible |

### Rachmaninoff (Études-Tableaux)

| Preset | Transcripteur | Quantification | Seuil | Filtrage | Snap | Notes |
|---|---|---|---|---|---|---|
| **hFT-Précision** | hFT-Transformer | Standard (1/16) | 0.35 | Classique renforcé | 0.45 | **Recommandé** — accords complexes |
| **Precision** | Transkun | Précision (1/32) | 0.90 | Transkun | 0.90 | Alternative |

### Bach/Clavecin (Transcriptions)

| Preset | Transcripteur | Quantification | Seuil | Filtrage | Snap | Notes |
|---|---|---|---|---|---|---|
| **Precision** | Transkun | Précision (1/32) | 0.90 | Transkun | 0.90 | **Recommandé** — précision maximale |
| **hFT-Précision** | hFT-Transformer | Standard (1/16) | 0.35 | Classique renforcé | 0.45 | Alternative avec meilleure pédale |

---

## 🛡️ Protection des Notes Graves

### Problème
Les transcripteurs IA ont tendance à supprimer les notes graves (en-dessous de Do1, MIDI < 36) car :
- Elles ont une faible vélocité perçue (fréquence basse = moins d'énergie)
- Les harmoniques de pédale masquent les attaques
- Le seuil de détection est trop strict pour les basses

### Solutions par transcripteur

#### hFT-Transformer (Recommandé)
- **Protection automatique** : notes < 36 sont systématiquement protégées
- **Seuil adapté** : onset_threshold 0.15-0.25 pour les passages doux
- **Filtrage anti-pédale** : spécialisé pour les harmoniques de pédale du piano

#### Transkun
- **Filtrage Transkun** : seuil de vélocité bas (0.25)
- **Protection grave** : notes < 36 avec vélocité > 0.3 conservées
- **Recommandé** : preset "Precision" + filtrage Transkun

#### Piano Transcription
- **Filtrage Ultra** : protection des basses avec vélocité > 0.25
- **Recommandé** : preset "Ultra-classique" + filtrage Ultra

---

## ⚙️ Guide de Réglage Fin

### Seuil de détection (Sensibilité)

| Vale slider | Seuil réel | Effet | Usage |
|---|---|---|---|
| 0.00 (gauche) | 0.20 | **Très haute sensibilité** | Notes pianissimo, Chopin nocturnes |
| 0.20 | 0.25 | **Haute sensibilité** | **Recommandé pour Chopin** |
| 0.40 | 0.35 | **Sensibilité modérée** | **Recommandé pour Liszt/Rachmaninoff** |
| 0.50 (centre) | 0.50 | Sensibilité normale | Usage général |
| 0.85 (droite) | 0.85 | **Basse sensibilité** | Éliminer le bruit, partitions propres |

### Snap de quantification

| Valeur | Effet | Usage |
|---|---|---|
| 0.0-0.2 | **Ultra-doux** | Nocturnes, musiques très expressives |
| 0.2-0.3 | **Très doux** | **Recommandé Chopin/Debussy** |
| 0.3-0.5 | **Moyen** | Liszt, Rachmaninoff, classique complexe |
| 0.5-0.7 | **Ferme** | Jazz, musique baroque |
| 0.8-1.0 | **Très ferme** | Débutants, simplification maximale |

### Filtrage harmonique

| Mode | Agressivité | Usage |
|---|---|---|
| **Anti-pédale** | Ciblée | **Recommandé Chopin/Debussy** |
| **Classique renforcé** | Modérée | Classique général |
| **Transkun-chord** | Contextuelle | Transkun |
| **Agressif** | Forte | Romantique complexe |
| **Ultra** | Maximum | Partitions très denses |

---

## 📋 Checklist pour une Bonne Transcription Classique

1. **Sélectionner le preset adapté** au compositeur
2. **Activer l'isolation Demucs** (sauf si enregistrement studio propre)
3. **Vérifier la détection du tempo** (doit être cochée)
4. **Vérifier la détection de la mesure** (doit être cochée)
5. **Vérifier la détection de la tonalité** (doit être cochée)
6. **Activer Rubato et Triolets**
7. **Vérifier que les notes graves sont présentes** (Do1, Ré1, Mi1)
8. **Ajuster le seuil de détection** si nécessaire
9. **Vérifier le snap** : plus doux = plus précis mais plus dense
10. **Exporter en PDF** pour consultation
11. **Exporter en MIDI** pour écoute/édition
12. **Exporter en MusicXML** pour MuseScore/Finale

---

## 🎯 Recommandations par Type de Fichier Source

| Type de fichier | Preset recommandé | Notes |
|---|---|---|
| **Enregistrement studio propre** | hFT-Classique | Meilleur résultat |
| **YouTube/MP3 compressé** | hFT-Classique + Demucs | Isolation nécessaire |
| **Enregistrement maison** | hFT-Expressif | Plus de sensibilité pour compenser la qualité |
| **Partition officielle + playback** | hFT-Précision | Moins de bruit = filtrage moins agressif |
| **Concert live** | hFT-Expressif + Demucs | Maximiser la détection |