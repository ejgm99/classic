from __future__ import annotations

from collections import Counter

from jira import JIRA
from jira.client import ResultList
from jira.resources import Issue

import typer
import pdb
import json 

from rich.console import Console
from rich.layout import Layout
from rich import print as p
from rich.table import Table
from rich.panel import Panel
# Some Authentication Methods

import json
import os

creds = {}

with open(f"{os.path.expanduser("~")}/.classic/atlassian.json") as file:
    creds = json.load(file) 

jira = JIRA(
    server = "https://gwhoppo.atlassian.net/",
    basic_auth=("jonathan.e.marino99@gmail.com","ATATT3xFfGF0UL0zXtzRXvCmUpzYgVZ-ntuEC6h98WTPrKddgMyxE3cOlzfh1dh2RIJGZJ45izb7osqqoGg2yKjy6F_waNuuNUA8PgJFIysjU1nRyhlvuA9qO8wUH4MM7Vhv5eEnO1OWFi9QGNvFQw13ts84vJMBRC2V5Ac_MZpdG7zeKGfZZQg=0EB20720")  # a us712020:e9483ca0-abb1-4991-97fd-57085874897eer7712020password tuple [Not recommended]
)

app = typer.Typer()
todo_filter = 'assignee = currentUser() AND status = "To Do"'
prog_filter = 'assignee = currentUser() AND status = "In Progress"'


@app.command()
def init():
    todo = jira.search_issues(todo_filter)
    prog = jira.search_issues(prog_filter)
    display_fields(todo,prog)

def generate_table(title,array):
    table = Table(title = 'title')
    for i in array:
        table.add_row(Panel(i.fields.summary,title=i.key))
    return table

def display_fields(todo, progress):
    layout = Layout()
    a = [str(i)*5 for i in range(0,10)]
    todo_table = Table(title='todo')
    prog_table = Table(title='prog')
    todo_table.add_column("todo")
    prog_table.add_column("prog")
    for i in a:
        todo_table.add_row(Panel(i))
    layout.split_row(
        Layout(name="left"),
        Layout(name="right"),
    )
    todo_table = generate_table('todo',todo)
    prog_table = generate_table('prog',progress)
    layout["left"].update(todo_table)
    layout["right"].update(prog_table)
    p(layout)
