import os
from os.path import exists
import click
from ics import Calendar, Event, Todo
from datetime import datetime, date
from prettytable import PrettyTable
import uuid

# this is the overarching command that houses the clases and reminder manager and soon to be more managers
# this first cli() will be constructing the calendar variable to be used by the other commands. this is very important as the ics file will be our database.
@click.group()
@click.option('--ics', type=click.Path(writable=True), required=True)
@click.pass_context
def cli(ctx, ics):
    """ Life Manager App """
    if not exists(ics):
        with open(ics, 'x') as ics_file:
            pass
    if os.stat(ics).st_size != 0:
        with open(ics, 'r') as ics_file:
            calendar = Calendar(ics_file.read())
    else:
        calendar = Calendar()
        today = datetime.today()
        meal_1 = Event("Breakfast", datetime(today.year, today.month, today.day, 7), datetime(today.year, today.month, today.day, 7, 30))
        meal_2 = Event("Lunch", datetime(today.year, today.month, today.day, 12), datetime(today.year, today.month, today.day, 12, 30))
        meal_3 = Event("Dinner", datetime(today.year, today.month, today.day, 18), datetime(today.year, today.month, today.day, 18, 30))
        break_1 = Event("Mental Break 1", datetime(today.year, today.month, today.day, 12, 30), datetime(today.year, today.month, today.day, 13))
        break_2 = Event("Mental Break 2", datetime(today.year, today.month, today.day, 18, 30), datetime(today.year, today.month, today.day, 19))
        water_1 = Todo(name="Water Reminder 1", due=datetime(today.year, today.month, today.day, 10))
        water_2 = Todo(name="Water Reminder 2", due=datetime(today.year, today.month, today.day, 15))
        water_3 = Todo(name="Water Reminder 3", due=datetime(today.year, today.month, today.day, 20))
        calendar.events.add(meal_3)
        calendar.events.add(meal_2)
        calendar.events.add(meal_1)
        calendar.events.add(break_2)
        calendar.events.add(break_1)
        calendar.todos.add(water_1)
        calendar.todos.add(water_2)
        calendar.todos.add(water_3)

    ctx.obj = {
        "calendar": calendar,
        "ics_path": ics
    }


# this is the classes manager that will show, add, remove an later on do more
# it will be passing the context wiht the clandear object inside of it to the lower commands such as the show, add and remove and later on more.
@cli.group()
@click.pass_context
def events(ctx):
    """ Events Manager (Classes, Chores, Break, Meals) """
    pass


# this command print the current classes in the calnedar object in a pretty table format
@events.command()
@click.pass_obj
def show(obj):
    x = PrettyTable()
    x.field_names = ["UID", "Name", "Begin Time", "End Time", "Description"]
    for event in obj['calendar'].events:
        x.add_row([event.uid, event.name, event.begin, event.end, event.description])
    click.echo(x)
        
# this command add a class to the calendar and save it to the database and take the option flags name begin and end to consturct the class event
@events.command()
@click.option('--name', required=True)
@click.option('--begin', type=click.DateTime(), required=True)
@click.option('--end', type=click.DateTime(), required=True)
@click.pass_obj
def add(obj, name, begin, end):
    e = Event(name, begin, end, uid=str(uuid.uuid4()))
    obj['calendar'].events.add(e)
    save_ics(obj['calendar'], obj['ics_path'])


# this command removes a class with the uid specifcally to it to accurately find the class and remove. Uid used because names are not unique .
@events.command()
@click.option('--uid', required=True)
@click.pass_obj
def remove(obj, uid):
    event_to_be_removed = None
    for event in obj['calendar'].events:
        if event.uid == uid:
            event_to_be_removed = event
    
    obj['calendar'].events.remove(event_to_be_removed)
    save_ics(obj['calendar'], obj['ics_path'])


# rmeinder command group that will house the show, add and remove commands
@cli.group()
@click.pass_context
def reminders(ctx):
    """ Reminders """
    click.echo("reminders")


# this command print the current classes in the calnedar object in a pretty format
@reminders.command()
@click.pass_obj
def show(obj):
    x = PrettyTable()
    x.field_names = ["UID", "Name", "Time", "Completed"]
    for todo in obj['calendar'].todos:
        x.add_row([todo.uid, todo.name, todo.dtstamp, todo.completed])
    click.echo(x)

# this command complete a task that was added to the reminders database 
@reminders.command()
@click.option('--uid', required=True)
@click.pass_obj
def complete(obj, uid):
    todo_to_be_completed = None
    for todo in obj['calendar'].todos:
        if todo.uid == uid:
            todo_to_be_completed = todo
    if todo_to_be_completed == None:
        click.echo("Could not find the todo")
    else:
        todo_to_be_completed.completed = datetime.now()
        save_ics(obj['calendar'], obj['ics_path'])


# this command add a reminder to the calendar and save it to the database and take the option flags name begin and end to consturct the reminder event
@reminders.command()
@click.option('--name', required=True)
@click.option('--time', type=click.DateTime(), required=True)
@click.pass_obj
def add(obj, name, time):
    t = Todo(name=name, uid=str(uuid.uuid4()), due=time)
    obj['calendar'].todos.add(t)
    save_ics(obj['calendar'], obj['ics_path'])


# this command rmeoves!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! based on the uid provided to provide accuracy
@reminders.command()
@click.option('--uid', required=True)
@click.pass_obj
def remove(obj, uid):
    todo_to_be_removed = None
    for todo in obj['calendar'].todos:
        if todo.uid == uid:
            todo_to_be_removed = todo
    
    obj['calendar'].todos.remove(todo_to_be_removed)
    save_ics(obj['calendar'], obj['ics_path'])


@cli.group()
@click.pass_context
def chores(ctx):
    """ Chores """
    click.echo("chores")


@chores.command()
@click.pass_obj
def show(obj):
    x = PrettyTable()
    x.field_names = ["UID", "Name", "Time", "Completed"]
    for todo in obj['calendar'].todos:
        x.add_row([todo.uid, todo.name, todo.dtstamp, todo.completed])
    click.echo(x)

@chores.command()
@click.option('--uid', required=True)
@click.pass_obj
def complete(obj, uid):
    todo_to_be_completed = None
    for todo in obj['calendar'].todos:
        if todo.uid == uid:
            todo_to_be_completed = todo
    if todo_to_be_completed == None:
        click.echo("Could not find the todo")
    else:
        todo_to_be_completed.completed = datetime.now()
        save_ics(obj['calendar'], obj['ics_path'])


@chores.command()
@click.option('--name', required=True)
@click.option('--time', type=click.DateTime(), required=True)
@click.pass_obj
def add(obj, name, time):
    t = Todo(name=name, uid=str(uuid.uuid4()), due=time)
    obj['calendar'].todos.add(t)
    save_ics(obj['calendar'], obj['ics_path'])


@chores.command()
@click.option('--uid', required=True)
@click.pass_obj
def remove(obj, uid):
    todo_to_be_removed = None
    for todo in obj['calendar'].todos:
        if todo.uid == uid:
            todo_to_be_removed = todo
    
    obj['calendar'].todos.remove(todo_to_be_removed)
    save_ics(obj['calendar'], obj['ics_path'])

# this is the save util ics that will save the infromation from the add command for the clases manager and reminder manager
# ics is standard that have been improving with time thanks to the giants such as apple and google. To have used another database will be extra uncessary work
def save_ics(calendar, path):
    with open(path, 'w') as file:
        file.write(str(calendar))

if __name__ == '__main__':
    cli()