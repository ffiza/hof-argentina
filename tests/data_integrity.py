import unittest
import json
from datetime import datetime


class TestDataIntegrity(unittest.TestCase):
    def test_birth_and_death_dates(self):
        with open('data/raw/hof-argentina.json', 'r', encoding="UTF-8") as f:
            data = json.load(f)
        for d in data:
            is_correct = True
            birth_date = datetime.strptime(d["BirthDate"], "%d %B %Y")
            death_date = datetime.strptime(d["DeathDate"], "%d %B %Y") \
                if d["DeathDate"] != "" else None
            if death_date:
                is_correct = birth_date < death_date
            self.assertTrue(is_correct)

    def test_birth_dates(self):
        with open('data/raw/hof-argentina.json', 'r', encoding="UTF-8") as f:
            data = json.load(f)
        for d in data:
            birth_date = datetime.strptime(d["BirthDate"], "%d %B %Y")
            self.assertTrue(birth_date <= datetime.now())

    def test_death_dates(self):
        with open('data/raw/hof-argentina.json', 'r', encoding="UTF-8") as f:
            data = json.load(f)
        for d in data:
            death_date = datetime.strptime(d["DeathDate"], "%d %B %Y") \
                if d["DeathDate"] != "" else None
            if death_date:
                self.assertTrue(death_date <= datetime.now())

    def test_term_dates(self):
        with open('data/raw/hof-argentina.json', 'r', encoding="UTF-8") as f:
            data = json.load(f)
        for d in data:
            birth_date = datetime.strptime(d["BirthDate"], "%d %B %Y")
            death_date = datetime.strptime(d["DeathDate"], "%d %B %Y") \
                if d["DeathDate"] != "" else None
            for t in d["Terms"]:
                term_start_date = datetime.strptime(t["Start"], "%d %B %Y")
                term_end_date = datetime.strptime(t["End"], "%d %B %Y") \
                    if t["End"] != "" else None
                self.assertTrue(birth_date <= term_start_date)
                if death_date and not term_end_date:
                    self.assertTrue(term_start_date <= death_date)
                if term_end_date and not death_date:
                    self.assertTrue(birth_date <= term_end_date)
                    self.assertTrue(term_start_date <= term_end_date)
                    self.assertTrue(term_end_date <= datetime.now())
                if death_date and term_end_date:
                    self.assertTrue(term_end_date <= death_date)


if __name__ == '__main__':
    unittest.main()
