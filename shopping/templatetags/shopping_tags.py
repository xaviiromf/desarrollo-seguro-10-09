from django import template

register = template.Library()

@register.filter(name='clp')
def clp(value):
    """
    Formatea un número o valor a Pesos Chilenos (CLP).
    Ejemplo: 15490 -> "$15.490"
    """
    if value is None or value == '':
        return '$0'
    try:
        val = int(round(float(value)))
        return f"${val:,.0f}".replace(',', '.')
    except (ValueError, TypeError):
        return str(value)
