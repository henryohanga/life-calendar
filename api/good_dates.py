import calendar


def sum_digits(number: int, match_on_single_digit: bool = True) -> int:
    if number < 10:
        return number

    sum_of_digits = sum(int(digit) for digit in str(number))

    if match_on_single_digit:
        return sum_digits(
            number=sum_of_digits,
            match_on_single_digit=match_on_single_digit,
        )
    return sum_of_digits


def good_date(
    date: str,
    sum_of_birth_date: int,
    match_on_single_digit: bool = True,
):
    date = date.replace("-", "")
    sum_of_date = sum_digits(
        number=int(date),
        match_on_single_digit=match_on_single_digit,
    )

    return sum_of_date == sum_of_birth_date


def good_dates(
    year: int,
    birth_date: str,
    match_on_single_digit: bool = True,
):
    """
    if not match_on_single_digit, then the sum of the digits in the date must
    be equal to the sum of the digits in the birth date
    otherwise, sum the digits until we get a single digit

    >>> good_dates(2024, "1990-05-01")
    """
    sum_of_birth_date = sum_digits(
        number=int(birth_date.replace("-", "")),
        match_on_single_digit=match_on_single_digit,
    )

    print(f"path number: {sum_of_birth_date}")

    dates = []
    for month in range(1, 13):
        for day in range(1, calendar.monthrange(int(year), month)[1] + 1):
            date = f"{year}-{month:02}-{day:02}"
            if good_date(
                date=date,
                sum_of_birth_date=sum_of_birth_date,
                match_on_single_digit=match_on_single_digit,
            ):
                dates.append(date)
    return dates


if __name__ == "__main__":
    dates = good_dates(
        year=2023,
        birth_date="1990-05-01",
        match_on_single_digit=True,
    )

    print(dates)
