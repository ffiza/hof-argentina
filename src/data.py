import json
from datetime import datetime


def calculate_decimal_age(date1: datetime,
                          date2: datetime) -> float:
    delta = date2 - date1
    seconds = delta.total_seconds()
    seconds_per_year = 365.25 * 24 * 60 * 60
    return round(seconds / seconds_per_year, 2)


def read_data() -> list:
    REFERENCE_START_DATE = datetime(1900, 1, 1)

    with open('data/raw/hof-argentina.json', 'r', encoding="UTF-8") as f:
        hofs = json.load(f)

    data = []
    for hof in hofs:
        first_term_start_date = datetime.strptime(
            hof["Terms"][0]["Start"], "%d %B %Y")

        if first_term_start_date >= REFERENCE_START_DATE:
            birth_date = datetime.strptime(hof["BirthDate"], "%d %B %Y")
            death_date = datetime.strptime(hof["DeathDate"], "%d %B %Y") \
                if hof["DeathDate"] != "" else None

            most_recent_age = calculate_decimal_age(birth_date, datetime.now())
            is_alive = True
            if death_date:
                most_recent_age = calculate_decimal_age(birth_date, death_date)
                is_alive = False

            d = {
                "Name": hof["Name"],
                "BirthDate": hof["BirthDate"],
                "MostRecentAge": most_recent_age,
                "IsAlive": is_alive,
            }

            terms_age = []
            for t in hof["Terms"]:
                term_start_date = datetime.strptime(t["Start"], "%d %B %Y")
                term_end_date = datetime.strptime(t["End"], "%d %B %Y") \
                    if t["End"] != "" else None
                age_at_start = calculate_decimal_age(
                    birth_date, term_start_date)
                age_at_end = most_recent_age
                if term_end_date:
                    age_at_end = calculate_decimal_age(
                        birth_date, term_end_date)
                terms_age.append((round(age_at_start / most_recent_age, 2),
                                  round(age_at_end / most_recent_age, 2)))

            d["TermsAges"] = terms_age

            data.append(d)

    return data


if __name__ == "__main__":
    data = read_data()
    for i in range(len(data)):
        print(data[i])
