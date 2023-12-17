import calendar


def _good_date(
    date: str,
    sum_of_birth_date: int,
    match_on_single_digit: bool = True,
):
    date = date.replace("-", "")
    sum_of_date = _sum_digits(
        number=int(date),
        match_on_single_digit=match_on_single_digit,
    )

    return sum_of_date == sum_of_birth_date


def good_dates(
    year: int,
    birth_date: str,
    match_on_single_digit: bool = True,
):
    sum_of_birth_date = _sum_digits(
        number=int(birth_date.replace("-", "")),
        match_on_single_digit=match_on_single_digit,
    )

    dates = []
    for month in range(1, 13):
        for day in range(1, calendar.monthrange(int(year), month)[1] + 1):
            date = f"{year}-{month:02}-{day:02}"
            if _good_date(
                date=date,
                sum_of_birth_date=sum_of_birth_date,
                match_on_single_digit=match_on_single_digit,
            ):
                dates.append(date)
    return dates


def _sum_digits(number: int, match_on_single_digit: bool = True) -> int:
    if number < 10:
        return number

    sum_of_digits = sum(int(digit) for digit in str(number))

    if match_on_single_digit:
        return _sum_digits(
            number=sum_of_digits,
            match_on_single_digit=match_on_single_digit,
        )
    return sum_of_digits
