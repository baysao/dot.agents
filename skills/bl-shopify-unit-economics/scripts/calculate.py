"""Calculate one-order contribution. Usage: python3 calculate.py input.json."""
import json
import sys
from decimal import Decimal, InvalidOperation

def calculate(data):
    required = ('revenue', 'landed', 'variable_fees', 'refund_loss', 'target_margin')
    values = {}
    for key in required + (('actual_cpa',) if 'actual_cpa' in data else ()):
        if key not in data or isinstance(data[key], bool):
            raise ValueError('Missing or invalid field: ' + key)
        try:
            value = Decimal(str(data[key]))
        except InvalidOperation:
            raise ValueError('Invalid number: ' + key)
        if not value.is_finite() or value < 0:
            raise ValueError('Must be finite and nonnegative: ' + key)
        values[key] = value
    r = values['revenue']
    if r <= 0 or values['target_margin'] >= 1:
        raise ValueError('revenue must be positive; target_margin must be in [0,1)')
    c = sum(values[k] for k in ('landed', 'variable_fees', 'refund_loss'))
    cm = r-c
    target = cm-values['target_margin']*r
    out = dict(variable_cost=c, contribution_before_ads=cm,
               breakeven_cpa=cm if cm > 0 else None,
               breakeven_roas=r/cm if cm > 0 else None,
               target_cpa=target if target > 0 else None,
               target_roas=r/target if target > 0 else None,
               feasible_paid_acquisition=target > 0)
    if 'actual_cpa' in values:
        out['contribution_after_ads'] = cm-values['actual_cpa']
    return {k: str(v.quantize(Decimal('0.0001'))) if isinstance(v, Decimal) else v for k,v in out.items()}

if __name__ == '__main__':
    try:
        with open(sys.argv[1], encoding='utf-8') as f:
            result = calculate(json.load(f))
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, OSError, IndexError, TypeError, InvalidOperation) as error:
        print(json.dumps({'error': str(error)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(2)
