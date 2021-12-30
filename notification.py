import requests
from bs4 import BeautifulSoup
from difflib import get_close_matches
import schedule
import time

import os
from dotenv import load_dotenv

load_dotenv()

movie = input("What movie are you waiting for?\n").casefold()

# creating a list of movies found on coming soon page

page = requests.get("https://in.bookmyshow.com/chennai/movies/comingsoon", timeout=60)

soup1 = BeautifulSoup(page.content, "html.parser")

card = soup1.find("div", attrs={"class": "release-calandar mv-row"})

films = card.findAll("aside")

movies = {}

for film in films:

    url1 = film.a["href"]

    title = film.a["title"]

    movies.setdefault(title.casefold(), url1)


# getting correct movie input

while movie not in movies:

    matches = get_close_matches(movie, movies.keys())

    print("Sorry", movie, "is not found.Did you mean any of these movies?")

    for match in matches:

        print(match.capitalize())

    movie = input(
        "Which movie are you waiting for? (Enter quit to exit program.)\n"
    ).lower()

    if movie == "quit":

        exit()

        break


# checking whether movie is in the coming soon or now showing part of the website


def check():

    import smtplib

    if movie in movies:

        url2 = "https://in.bookmyshow.com" + movies[movie]

        page2 = requests.get(url2, timeout=5)

        soup2 = BeautifulSoup(page2.content, "html.parser")

        actionbook = soup2.find("div", attrs={"class": "action-book"})

        if actionbook:

            # creating email content

            if actionbook.find("div", attrs={"class": "more-showtimes"}):

                message = (
                    "Bookings are now open for "
                    + movie.capitalize()
                    + "\n"
                    + "Book your tickets now at "
                    + url2
                )

                print(
                    "Bookings open for "
                    + movie.capitalize()
                    + "Email sent successfully!"
                )

                exit()

            else:

                message = "Bookings are not open yet for" + movie.capitalize()

                print("Booking not open!")

                # sending email via python

                s = smtplib.SMTP(host="smtp.gmail.com", port=587)

                s.starttls()
                Sender_mail = os.getenv("SENDER_MAIL")
                Sender_mail_password = os.getenv("SENDER_PASSWORD")
                try:
                    s.login(Sender_mail, Sender_mail_password)

                except:
                    print("Wrong Mail_id or Password!")
                    exit()

                To_mail = "samyuktha9111@gmail.com"

                subject = movie.capitalize() + "-python results"

                Message = "Subject:" + subject + "\n\n" + message

                s.sendmail(Sender_mail, To_mail, Message)
                s.quit()


# running the check for every  hour

schedule.every(1).hours.do(check)

while True:

    schedule.run_pending()
    time.sleep(1)
