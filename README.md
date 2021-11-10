

python3 life_manager/main.py --ics ./life.ics classes add --name="csci 354" --begin="2021-11-08 09:00:00" --end="2021-11-08 10:00:00"
python3 life_manager/main.py --ics ./life.ics classes show
python3 life_manager/main.py --ics ./life.ics classes remove --uid="703c34cf-d681-14271-bd6b-24ab541e3a8a@703c.org"

python3 life_manager/main.py --ics ./life.ics reminders show
python3 life_manager/main.py --ics ./life.ics reminders add --name="Drink Water" --time="2021-11-08 08:00:00"
python3 life_manager/main.py --ics ./life.ics reminders complete --uid 48aefcff-30b4-4f31-85a1-93692e8fbd5c


libraries used:
click | https://click.palletsprojects.com/en/8.0.x/
ics | https://pypi.org/project/ics/
prettytable | https://pypi.org/project/prettytable/