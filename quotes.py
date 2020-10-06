## this games scrapes all quotes from a website, randomly chose one,
## and lets the user guess who is the author of the quote.

import requests
from bs4 import BeautifulSoup
from random import choice
from termcolor import colored, cprint

# get all quotes and their metadata from the current page.
# used by get_all_data()
def get_page_data(page):
    quotes = page.findAll(class_ = "quote")
    data = []
    for q in quotes:
        text = q.findChildren(class_="text")[0].get_text()
        auth = q.findChildren(class_="author")[0].get_text()
        link = q.find("a")["href"]
        data.append([text, auth, link])
    return (data)

# get the entirety of the quotes and their metadata in a 2-dimensional list.
def get_all_data():
    data = []
    pg = "/page/1"
    while True:
        response = requests.get(f"{url}{pg}")
        soup = BeautifulSoup(response.text, "html.parser")
        for q in get_page_data(soup):
            data.append(q)
        next_class = soup.find(class_="next")
        if next_class == None:
            break
        pg = soup.find(class_="next").find("a")["href"]
    return data

# get author birth's date and location, by scraping its 'about' about page.
# called from get_answer(), for the hints
def get_author_birth(link):
    response = requests.get(f"{url}{link}") 
    soup = BeautifulSoup(response.text, "html.parser")
    date = soup.find(class_="author-born-date").get_text()
    location = soup.find(class_="author-born-location").get_text()
    return date, location

# gets the user answer, and depending on witch attempt it is, gives hints.
# called from main_game()
def get_answer(curr_quote, attempt):
    c_hint = colored('Hint:', 'yellow')
    if attempt == 0:
        print("")
    elif attempt == 1:
        print(f"{c_hint} Author's first name inital is",
        curr_quote[1][0])
    elif attempt == 2:
        print(f"{c_hint} Author's last name initial is", 
        curr_quote[1].split(' ')[1][0])
    elif attempt == 3:
        date, location = get_author_birth(curr_quote[2])
        print(f"{c_hint} Author was born on {date} {location}")
    answer = ""
    while not answer:
        c_attempt = colored(str(4 - attempt), 'cyan')
        answer = input(f"remaining tries: {c_attempt} > ").strip()
    return (answer)

# this is the main game function. Get a quote, print it, ask for an answer, check it.
# if the user win, or lose at its last attempt, end the game.
def main_game():
    curr_quote = choice(all_quotes)
    print("*****************************************")
    cprint("From who is this quote?", color="magenta")
    print(curr_quote[0])

    attempt = 0
    while attempt < 4:
        answer = get_answer(curr_quote, attempt)
        if answer == curr_quote[1]:
            cprint("you win!", color="green")
            break
        elif attempt == 3:
            cprint("sorry, you lose!", color="red")
            c_auth = colored(curr_quote[1], color='cyan')
            print(f"the author of this quote was {c_auth}")
        attempt += 1


# let the user play new games until he doesn't wanna anymore.
if __name__ == "__main__":
    url = "http://quotes.toscrape.com"
    all_quotes = get_all_data()
    
    while True:
        again = ""
        main_game()
        while not again:
            again = input("play again? (y/*) ")
        print("")
        if again and again[0] != "y":
            print("goodbye!")
            break
