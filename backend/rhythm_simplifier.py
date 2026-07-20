"""
rhythm_simplifier.py — Simplification rythmique "Beginner" (mode débutant)

Objectif :
  Simplifier AGGRESSIVEMENT les durées de notes pour rendre la partition
  ultra-lisible pour les débutants.
  
  Règles du mode "Beginner" :
  - UNIQUEMENT noires (1 beat) et croches (0.5 beat)
  - ZÉRO double-croches, zéro pointé, zéro syncope
  - Fusionner les notes adjacentes de même pitch
  - Réduire le tempo pour compenser la simplification
  - Re-compter les temps par mesure après simplification

Usage :
  from rhythm_simplifier import simplify_rhythm
  score_data = simplify_rhythm(score_data)
"""

import math
from typing import Dict, Any, List


# ✅ Durées autorisées pour le mode "Beginner" : uniquement noires + croches
BEGINNER_DURATIONS = [1.0, 0.5]  # noire, croche

# Mapping duration (en beats) → (dur_str, dots) pour VexFlow
# Beginner : uniquement noire (q) et croche (8)
BEGINNER_DURATION_TO_STR = {
    1.0: ('q', 0),   # noire
    0.5: ('8', 0),   # croche
    2.0: ('h', 0),   # blanche (si fusion donne 2 beats)
    4.0: ('w', 0),   # ronde (si fusion donne 4 beats)
}

# Ratio de simplification du tempo
# Pour un morceau à 120 BPM en mode smooth, on veut que le rendu soit
# comme un morceau à ~90 BPM simplifié → tempo × 0.75 (légèrement plus lent)
BEGINNER_TEMPO_RATIO = 0.75


def _round_to_beginner(duration: float) -> float:
    """
    Arrondit une durée à une valeur "Beginner" (noire ou croche uniquement).
    
    Règles :
    - duration < 0.375 → 0.5 (croche)
    - 0.375 ≤ duration < 0.875 → 0.5 (croche)
    - 0.875 ≤ duration < 1.375 → 1.0 (noire)
    - 1.375 ≤ duration < 2.375 → 2.0 (blanche)
    - duration ≥ 2.375 → 4.0 (ronde)
    
    Args:
        duration : durée en beats
        
    Returns:
        durée arrondie à une valeur Beginner
    """
    if duration < 0.375:
        return 0.5  # croche minimum
    elif duration < 0.875:
        return 0.5  # croche
    elif duration < 1.375:
        return 1.0  # noire
    elif duration < 2.375:
        return 2.0  # blanche
    else:
        return 4.0  # ronde


def _duration_to_vexflow(duration: float) -> tuple:
    """
    Convertit une durée en beats → (dur_str, dots) pour VexFlow.
    Beginner : uniquement noire, croche, blanche, ronde.
    
    Args:
        duration : durée en beats
        
    Returns:
        tuple (dur_str, dots)
    """
    if duration in BEGINNER_DURATION_TO_STR:
        return BEGINNER_DURATION_TO_STR[duration]
    
    # Fallback : trouver la valeur Beginner la plus proche
    target = _round_to_beginner(duration)
    return BEGINNER_DURATION_TO_STR.get(target, ('q', 0))


def _normalize_time_signature(notes_by_voice: Dict[str, List[Dict[str, Any]]]) -> List[int]:
    """
    Calcule le nouveau chiffrage de mesure après simplification.
    
    Prend le temps total de chaque voix et trouve le PGCD pour normaliser.
    Retourne [numérateur, dénominateur] arrondi à un chiffrage standard.
    
    Args:
        notes_by_voice : dict avec clés 'treble', 'bass'
        
    Returns:
        [numerator, denominator] pour le nouveau time signature
    """
    # Prend le temps max entre les deux mains
    times = []
    for voice_notes in notes_by_voice.values():
        if not voice_notes:
            continue
        total = sum(n.get('duration', 0) for n in voice_notes)
        times.append(total)
    
    if not times:
        return [4, 4]
    
    max_beats = max(times)
    
    # Trouver le chiffrage standard le plus proche
    standard_sigs = [(2, 4), (3, 4), (4, 4), (3, 8), (6, 8), (9, 8), (12, 8)]
    best_sig = [4, 4]
    best_diff = float('inf')
    
    for num, den in standard_sigs:
        target_beats = num * (4.0 / den)
        diff = abs(max_beats - target_beats)
        if diff < best_diff:
            best_diff = diff
            best_sig = [num, den]
    
    # Si la différence est trop grande (> 0.5 beat), prendre le chiffrage suivant
    if best_diff > 0.5:
        # Trouver le chiffrage supérieur
        for num, den in standard_sigs:
            target_beats = num * (4.0 / den)
            if target_beats >= max_beats:
                best_sig = [num, den]
                break
    
    return best_sig


def simplify_measure_voice(
    notes: List[Dict[str, Any]], 
    beats_per_measure: float
) -> List[Dict[str, Any]]:
    """
    Simplifie les durées d'une voix (main gauche ou droite) dans une mesure.
    
    Règles Beginner :
    1. Arrondir TOUTES les durées à noire (1.0) ou croche (0.5)
    2. Fusionner les notes adjacentes de même pitch
    3. Zéro 16th, zéro pointé, zéro syncope
    
    Args:
        notes : liste de notes VexFlow (dict)
        beats_per_measure : nombre de beats dans la mesure
        
    Returns:
        liste de notes simplifiées
    """
    if not notes:
        return notes
    
    simplified = []
    
    for note in notes:
        if note.get('isRest', False):
            # Les silences : arrondir à la valeur Beginner la plus proche
            raw_dur = note.get('duration', 0.5)
            target_dur = _round_to_beginner(raw_dur)
            target_dur = max(0.5, target_dur)  # minimum = croche
            
            dur_str, dots = _duration_to_vexflow(target_dur)
            
            simplified_note = {
                'id': note.get('id', ''),
                'keys': note.get('keys', []),
                'durationStr': dur_str,
                'dots': dots,
                'isRest': True,
                'startBeat': note.get('startBeat', 0),
                'duration': target_dur,
                'midiPitch': None,
                'hand': note.get('hand', 'treble'),
                'amplitude': 0,
            }
            simplified.append(simplified_note)
            continue
        
        # Notes : arrondir à noire ou croche
        raw_dur = note.get('duration', 1.0)
        target_dur = _round_to_beginner(raw_dur)
        target_dur = max(0.5, target_dur)  # minimum = croche
        
        dur_str, dots = _duration_to_vexflow(target_dur)
        
        simplified_note = {
            'id': note.get('id', ''),
            'keys': note.get('keys', []),
            'durationStr': dur_str,
            'dots': dots,
            'isRest': False,
            'startBeat': note.get('startBeat', 0),
            'duration': target_dur,
            'midiPitch': note.get('midiPitch'),
            'hand': note.get('hand', 'treble'),
            'amplitude': note.get('amplitude', 0),
        }
        
        simplified.append(simplified_note)
    
    # Fusionner les notes adjacentes de même pitch
    simplified = _merge_adjacent_same_pitch(simplified)
    
    return simplified


def _merge_adjacent_same_pitch(notes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Fusionne les notes adjacentes de même pitch dont la somme
    correspond à une valeur Beginner (noire, croche, blanche, ronde).
    
    Args:
        notes : liste de notes simplifiées
        
    Returns:
        liste de notes avec fusion appliquée
    """
    if len(notes) < 2:
        return notes
    
    merged = [notes[0].copy()]
    
    for i in range(1, len(notes)):
        current = notes[i]
        last = merged[-1]
        
        # Ne pas fusionner silences et notes
        if current.get('isRest', False) != last.get('isRest', False):
            merged.append(current)
            continue
        
        if current.get('isRest', False):
            # Fusionner deux silences adjacents
            new_dur = _round_to_beginner(last['duration'] + current['duration'])
            new_dur = max(0.5, new_dur)
            dur_str, dots = _duration_to_vexflow(new_dur)
            new_silence = last.copy()
            new_silence['duration'] = new_dur
            new_silence['durationStr'] = dur_str
            new_silence['dots'] = dots
            merged[-1] = new_silence
            continue
        
        # Même pitch ?
        if current.get('midiPitch') != last.get('midiPitch'):
            merged.append(current)
            continue
        
        # Même main ?
        if current.get('hand') != last.get('hand'):
            merged.append(current)
            continue
        
        # Somme des durées
        sum_dur = last['duration'] + current['duration']
        target_sum = _round_to_beginner(sum_dur)
        
        # Fusionner si la somme est "propre"
        if abs(sum_dur - target_sum) / max(target_sum, 0.5) < 0.15:
            new_note = last.copy()
            new_note['duration'] = target_sum
            new_note['durationStr'], new_note['dots'] = _duration_to_vexflow(target_sum)
            merged[-1] = new_note
        else:
            merged.append(current)
    
    return merged


def simplify_rhythm(score_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simplifie le rythme complet d'une partition en mode "Beginner".
    
    Modifications :
    1. Remplacer TOUTES les durées par noires (1.0) ou croches (0.5)
    2. Réduire le tempo (× 0.75)
    3. Fusionner les notes adjacentes de même pitch
    
    Args:
        score_data : dict ScoreData (retourné par build_score)
        
    Returns:
        dict ScoreData avec rythmes simplifiés
    """
    if not score_data or 'measures' not in score_data:
        return score_data
    
    # Réduire le tempo
    original_tempo = score_data.get('tempo', 120)
    new_tempo = max(60, int(original_tempo * BEGINNER_TEMPO_RATIO))
    score_data['tempo'] = new_tempo
    print(f"[Smooth] Tempo: {original_tempo} → {new_tempo} BPM")
    
    measures = score_data.get('measures', [])
    
    for measure in measures:
        # Simplifier la main droite
        if 'treble' in measure:
            measure['treble'] = simplify_measure_voice(
                measure['treble'], 4.0
            )
        
        # Simplifier la main gauche
        if 'bass' in measure:
            measure['bass'] = simplify_measure_voice(
                measure['bass'], 4.0
            )
    
    return score_data