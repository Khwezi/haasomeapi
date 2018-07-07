from enum import Enum

class EnumInsurance(Enum):
	ABSOLUTE_PRICE_CHANGE = 0

	BE_PROFITABLE_IN_X_TRADES = 1

	DISABLE_ON_LOSSES = 2

	NEVER_SELL_CHEAPER = 3
	NEVER_BUY_HIGHER = 11

	OVERCOME_FEE = 4
	OVERCOME_DOUBLE_FEE = 5

	PERCENTAGE_PRICE_CHANGE = 6

	SCRIPT_INSURANCE = 7
	STABLE_TREND_ONLY = 8
	STAY_PROFITABLE = 9

	TRENDING_TREND_ONLY = 10

	HAAS_SCRIPT_INSURANCE = 12
	WAIT_AFTER_ORDER = 13