def lookup_closest_locale(locale, available):
  if isinstance(locale, str) and locale in available:
    return locale
  
  locales = []
  if isinstance(locale, list):
    locales = [] + locale
  else:
    locales.append(locale)

  for i in range(len(locales)):
    current = locales[i].split('-')
    while len(current) != 0:
      candidate = '-'.join(current)
      if candidate in available:
        return candidate

      current.pop()

def get_cardinal_category(num_string, locale):
    n, i, v, w, f, t = get_parts_of_num(num_string)

    closest_locale = lookup_closest_locale(locale, cardinals)

    if not closest_locale:
      # Fallback to default locale
      locale = "en" 

    cardinal_func = cardinals[closest_locale]

    if not cardinal_func:
      # Should be here different error message?
      raise Exception(f'Locale "{locale}" not supported')

    return cardinal_func(n, i, v, w, f, t);

def get_parts_of_num(num_string):
    '''
    Gets the different parts of a number in order to calculate which plurality
    rule to apply.
    Parts are specified at this URL:
    http://unicode.org/reports/tr35/tr35-numbers.html#Operands
    :returns:
        n: absolute value of the source number (integer and decimals).
        i: integer digits of n.
        v: number of visible fraction digits in n, with trailing zeros.
        w: number of visible fraction digits in n, without trailing zeros.
        f: visible fractional digits in n, with trailing zeros.
        t: visible fractional digits in n, without trailing zeros.
    '''

    decimal_split = str(num_string).split('.')
    i = abs(int(decimal_split[0]))

    if len(decimal_split) != 2:
        n = int(num_string)
        return n, i, 0, 0, 0, 0

    n = float(num_string)

    decimal_part = decimal_split[1]
    v = len(decimal_part)
    f = int(decimal_part)

    dec_part_no_trailing_zeros = decimal_part.rstrip('0')
    if not dec_part_no_trailing_zeros:
        return n, i, v, 0, f, 0

    w = len(dec_part_no_trailing_zeros)
    t = int(dec_part_no_trailing_zeros)

    return n, i, v, w, f, t

cardinals = { }