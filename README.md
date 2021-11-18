click==8.0.3
ics==0.7
prettytable==2.4.0

pip3 install -r requirements.txt

pyhton3 main.py --help

python3 main.py --ics ./life.ics events add --name="csci 354" --begin="2021-11-08 09:00:00" --end="2021-11-08 10:00:00"
python3 main.py --ics ./life.ics events show
python3 main.py --ics ./life.ics events remove --uid="703c34cf-d681-4271-bd6b-24ab541e3a8a@703c.org"

python3 main.py --ics ./life.ics reminders show
python3 main.py --ics ./life.ics reminders add --name="Clean UP my room" --time="2021-11-08 08:00:00"
python3 main.py --ics ./life.ics reminders complete --uid 48aefcff-30b4-4f31-85a1-93692e8fbd5c
