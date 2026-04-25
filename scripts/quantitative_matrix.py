"""
Pokémon Card Quantitative Investment Matrix
Layer 1: BUY Decision Matrix (10 Criteria)
Layer 2: ACTION Engine (BUY/HOLD/SELL + Confidence)
"""

import csv
import json
from pathlib import Path
from datetime import datetime

def parse_csv(csv_path):
    """Parse Pokémon card CSV data."""
    cards = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Item Status'] != 'Active':
                continue
            try:
                cost = float(row['My Cost']) if row['My Cost'] else None
                market_value = float(row['PSA Estimate']) if row['PSA Estimate'] else None
                if not cost or not market_value:
                    continue
                card = {
                    'name': row['Item'].replace('2023 POKEMON ', '').replace('2021 POKEMON ', '').replace('2022 POKEMON ', '').replace('2024 POKEMON ', '').replace('2025 POKEMON ', '').replace('2019 POKEMON ', '').replace('2015 POKEMON ', '').replace('2013 POKEMON ', ''),
                    'subject': row['Subject'],
                    'variety': row['Variety'],
                    'grade': int(row['Grade']) if row['Grade'] else 10,
                    'cost': cost,
                    'market_value': market_value,
                    'year': row['Year'],
                    'set': row['Set'],
                }
                cards.append(card)
            except (ValueError, KeyError):
                continue
    return cards

def calculate_undervaluation(mv, cost):
    """Calculate undervaluation percentage."""
    if not cost:
        return 0
    return ((mv - cost) / cost) * 100

def get_demand_tier(subject):
    """Classify demand tier."""
    subject_upper = subject.upper()
    s_tier = ['PIKACHU']
    a_tier = ['MEW', 'EEVEE', 'EEVEELUTIONS', 'UMBREON', 'SYLVEON']
    if any(x in subject_upper for x in s_tier):
        return 'S'
    if any(x in subject_upper for x in a_tier):
        return 'A'
    return 'B'

def get_icon_tier(subject):
    """Classify icon tier."""
    return get_demand_tier(subject)

def get_visual_premium(variety):
    """Assess visual premium."""
    variety_upper = variety.upper() if variety else ''
    if 'FULL ART' in variety_upper or 'SPECIAL ART' in variety_upper or 'EX' in variety_upper:
        return 'High'
    if 'ART RARE' in variety_upper or 'HOLO' in variety_upper:
        return 'Medium'
    return 'Low'

def calculate_buy_score(underval_pct, demand, liquidity, icon_tier, pop_risk, momentum, entry, visual, catalyst, exit_ease, subject):
    """Calculate BUY score (0-10)."""
    score = 0
    # Undervaluation: +2 for >30%, +1 for 10-30%
    if underval_pct > 30:
        score += 2
    elif underval_pct >= 10:
        score += 1
    # Demand: +2 for S-tier
    if demand == 'S':
        score += 2
    elif demand == 'A':
        score += 1.5
    # Liquidity: +1.5 for High
    if liquidity == 'High':
        score += 1.5
    elif liquidity == 'Medium':
        score += 1
    # Visual: +1 for High
    if visual == 'High':
        score += 1
    elif visual == 'Medium':
        score += 0.5
    # Catalyst: +1 for Strong
    if catalyst == 'Strong':
        score += 1
    elif catalyst == 'Medium':
        score += 0.5
    # Exit: +1 for Easy
    if exit_ease == 'Easy':
        score += 1
    elif exit_ease == 'Moderate':
        score += 0.5
    # Penalties
    if pop_risk == 'High':
        score -= 1
    if momentum == 'Volatile':
        score -= 0.5
    # Thai market adjustment
    if any(x in subject.upper() for x in ['PIKACHU', 'EEVEE']):
        score += 0.5
    return min(10, max(0, score))

def calculate_confidence(buy_score, demand, catalyst, pop_risk, momentum):
    """Calculate confidence score (0-100%)."""
    base = buy_score * 10
    if demand == 'S':
        base += 10
    if catalyst == 'Strong':
        base += 5
    if pop_risk == 'High':
        base -= 10
    if momentum == 'Volatile':
        base -= 5
    return min(95, max(50, base))

def determine_action(buy_score, underval_pct, liquidity):
    """Determine BUY/HOLD/SELL action."""
    if buy_score >= 8 and underval_pct >= 20 and liquidity in ['High', 'Medium']:
        return 'BUY'
    elif buy_score >= 6:
        return 'HOLD'
    else:
        return 'SELL'

def analyze_cards(cards):
    """Analyze all cards and return matrix results."""
    matrix_data = []
    for card in cards:
        underval = calculate_undervaluation(card['market_value'], card['cost'])
        demand = get_demand_tier(card['subject'])
        icon = get_icon_tier(card['subject'])
        visual = get_visual_premium(card['variety'])

        # Heuristics
        liquidity = 'High' if demand in ['S', 'A'] else 'Medium' if underval > 0 else 'Low'
        pop_risk = 'Low' if underval < 20 else 'Medium' if underval < 50 else 'High'
        momentum = 'Uptrend' if underval > 10 else 'Stable' if underval > -10 else 'Volatile'
        entry_barrier = 'Low' if card['cost'] < 100 else 'Medium' if card['cost'] < 500 else 'High'
        catalyst = 'Strong' if demand == 'S' else 'Medium' if demand == 'A' else 'Weak'
        exit_ease = 'Easy' if demand in ['S', 'A'] else 'Moderate' if demand == 'B' else 'Hard'

        buy_score = calculate_buy_score(underval, demand, liquidity, icon, pop_risk, momentum,
                                       entry_barrier, visual, catalyst, exit_ease, card['subject'])
        confidence = calculate_confidence(buy_score, demand, catalyst, pop_risk, momentum)
        action = determine_action(buy_score, underval, liquidity)

        reason = f"{action}: Underval {underval:.1f}%, {demand}-tier demand, {liquidity} liquidity"

        matrix_data.append({
            'card': card['subject'],
            'undervaluation_pct': round(underval, 1),
            'demand': demand,
            'liquidity': liquidity,
            'icon_tier': icon,
            'pop_risk': pop_risk,
            'momentum': momentum,
            'entry_barrier': entry_barrier,
            'visual': visual,
            'catalyst': catalyst,
            'exit_ease': exit_ease,
            'buy_score': round(buy_score, 2),
            'action': action,
            'confidence': round(confidence, 0),
            'reason': reason,
            'cost': card['cost'],
            'market_value': card['market_value'],
        })

    # Sort by buy_score descending
    matrix_data.sort(key=lambda x: x['buy_score'], reverse=True)

    # Identify key drivers and risks
    buy_cards = [m for m in matrix_data if m['action'] == 'BUY']
    high_underval = sorted(matrix_data, key=lambda x: x['undervaluation_pct'], reverse=True)[:3]
    high_risk = [m for m in matrix_data if m['pop_risk'] == 'High']

    return {
        'timestamp': datetime.now().isoformat(),
        'matrix': matrix_data,
        'summary': {
            'total_cards': len(matrix_data),
            'buy_count': len(buy_cards),
            'hold_count': len([m for m in matrix_data if m['action'] == 'HOLD']),
            'sell_count': len([m for m in matrix_data if m['action'] == 'SELL']),
        },
        'key_buy_drivers': [
            f"Pikachu/Eeveelution demand (S-tier)",
            f"Undervaluation > 30% threshold",
            f"High liquidity in primary market",
            f"Full Art / Special Art visual premium",
            f"Strong catalyst from new releases",
        ],
        'risk_flags': [
            f"High population risk on graded cards",
            f"Volatile momentum in secondary market",
            f"Niche collector demand concentration",
        ],
    }

if __name__ == '__main__':
    csv_path = Path(__file__).parent / 'My Collection CSV - 19.csv'
    cards = parse_csv(csv_path)
    result = analyze_cards(cards)
    print(json.dumps(result, indent=2))
