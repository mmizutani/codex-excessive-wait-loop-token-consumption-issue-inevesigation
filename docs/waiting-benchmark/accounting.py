"""API-price valuation of reported token categories, not subscription billing."""
from decimal import Decimal

# Standard, non-regional API USD per million tokens, verified 2026-09-14.
# https://developers.openai.com/api/docs/pricing
RATES = {
    'gpt-6-astra': {'uncached': '10', 'cached': '1', 'write': '12.5', 'output': '50'},
    'gpt-5.6-sol': {'uncached': '4', 'cached': '.4', 'write': '5', 'output': '20'},
}

def price_response(model, usage):
    counts = {'input': usage['input_tokens'], 'cached': usage.get('cached_input_tokens', 0),
              'write': usage.get('cache_write_input_tokens', 0), 'output': usage['output_tokens']}
    counts['uncached'] = counts['input'] - counts['cached'] - counts['write']
    assert all(v >= 0 for v in counts.values()), 'Overlapping or negative token categories'
    assert 0 <= usage.get('reasoning_output_tokens', 0) <= counts['output']
    rates = {k: Decimal(v) for k,v in RATES[model].items()}
    if counts['input'] > 272000:
        for k in ('uncached', 'cached', 'write'):
            rates[k] *= 2
        rates['output'] *= Decimal('1.5')
    costs = {k: Decimal(counts[k])*rates[k]/1000000 for k in rates}
    return {'counts': counts, 'usd': {k: float(v) for k,v in costs.items()},
            'total_usd': float(sum(costs.values())), 'long_context': counts['input'] > 272000}

