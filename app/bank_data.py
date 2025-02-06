import random

# Симуляция банковских предложений (позже можно заменить API запросами)
BANK_OFFERS = {
    "Sberbank": {"loan_rate": 0.12, "deposit_rate": 0.07},
    "Tinkoff": {"loan_rate": 0.10, "deposit_rate": 0.08},
    "Alfa-Bank": {"loan_rate": 0.11, "deposit_rate": 0.075},
    "Raiffeisen": {"loan_rate": 0.09, "deposit_rate": 0.085},
    "UniCredit": {"loan_rate": 0.13, "deposit_rate": 0.065},
}

def get_best_bank_offers():
    """ Возвращает лучшие условия по кредитам и депозитам из банков. """
    best_loan = min(BANK_OFFERS.items(), key=lambda x: x[1]["loan_rate"])
    best_deposit = max(BANK_OFFERS.items(), key=lambda x: x[1]["deposit_rate"])
    
    return {
        "best_loan": {"bank": best_loan[0], "rate": best_loan[1]["loan_rate"]},
        "best_deposit": {"bank": best_deposit[0], "rate": best_deposit[1]["deposit_rate"]},
    }
