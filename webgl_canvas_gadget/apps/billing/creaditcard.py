#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Adapted from:
- http://www.djangosnippets.org/snippets/764/
- http://www.satchmoproject.com/trac/browser/satchmo/trunk/satchmo/apps/satchmo_utils/views.py
- http://tinyurl.com/shoppify-credit-cards
"""
import re


# Well known card regular expressions.
CARDS = {
    'Visa': re.compile(r"^4\d{12}(\d{3})?$"),
    'Mastercard': re.compile(r"^(5[1-5]\d{4}|677189)\d{10}$"),
    'Dinersclub': re.compile(r"^3(0[0-5]|[68]\d)\d{11}$"),
    'Amex': re.compile("^3[47]\d{13}$"),
    'Discover': re.compile("^(6011|65\d{2})\d{12}$"),
}

TEST_NUMBERS = []

# 4242424242424242    Visa
# 4012888888881881    Visa
# 4000056655665556    Visa (debit)
# 5555555555554444    MasterCard
# 5200828282828210    MasterCard (debit)
# 5105105105105100    MasterCard (prepaid)
# 378282246310005    American Express
# 371449635398431    American Express
# 6011111111111117    Discover
# 6011000990139424    Discover
# 30569309025904    Diners Club
# 38520000023237    Diners Club
# 3530111333300000    JCB
# 3566002020360505    JCB


def verify_credit_card(number):
    """Returns the card type for given card number or None if invalid."""
    return CreditCard(number).verify()


class CreditCard(object):
    def __init__(self, number):
        self.number = number

    def is_number(self):
        """True if there is at least one digit in number."""
        self.number = re.sub(r'[^\d]', '', self.number)
        return self.number.isdigit()

    def is_mod10(self):
        """Returns True if number is valid according to mod10."""
        double = 0
        total = 0
        for i in range(len(self.number) - 1, -1, -1):
            for c in str((double + 1) * int(self.number[i])):
                total = total + int(c)
            double = (double + 1) % 2
        return (total % 10) == 0

    def is_test(self):
        """Returns True if number is a test card number."""
        # Note: test numbers cannot be used in the PP Pro sandbox.
        # Instead, use the credit card number associated with a
        # sandbox account (Test Accounts -> View Details).
        return self.number in TEST_NUMBERS

    def get_type(self):
        """Return the type if it matches one of the cards."""
        for card, pattern in CARDS.items():
            if pattern.match(self.number):
                return card
        return None

    def verify(self):
        """Returns the card type if valid else None."""
        if self.is_number() and not self.is_test() and self.is_mod10():
            return self.get_type()
        return None
