city = "Zürich"
currency = "CHF"
ticket_price = 4.20


def total_cost(number_of_tickets):
    """Return the total ticket cost in CHF."""
    return round(number_of_tickets * ticket_price, 2)
