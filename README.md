# README: Distinctiveness and Complexity

This is a web application built using the Django framework with Python for the backend and JavaScript for the frontend. The application is based on a website designed for a computer school that sells courses for the Microsoft Office suite. The main purpose of the application is to inform about the available courses and, although it is not very visually appealing, it can simulate purchases, where a user can add and remove items from their cart. The theme of the project is similar to Commerce, but it differs by having products listed directly on the site, and purchases are made using a shopping cart. All purchase information is recorded for each user who made it.

The application has several pages, all rendered by the `views.py` file. Instead of being written entirely in HTML, each page is dynamically created with the help of data passed by Django's context. Unfortunately, I did not have ideas to implement APIs in this application, as all courses are registered by the admin, and there is no need to search for external information. The JavaScript implementation was done on the main page, where there is a countdown timer indicating the limited time of an offer.

In addition to the concepts learned during the course, an AI technique was also applied within the application. In the search field for the name of a course, NLP (Natural Language Processing) is used to identify what the user typed and show similar courses through semantic similarity.

## What’s contained in each file you created

- `urls.py`: Contains all the URLs of the application.
- `views.py`: Contains the routes of the application, which render the HTML files.
- `models.py`: Contains the database models.
- `util.py`: Contains a function that returns the semantic similarity of an input with the existing courses using NLP.
- `templates/`: A folder that contains all the HTML files that are dynamically generated with Django.
- `static/`: A folder that contains Bootstrap, CSS, fonts, images, and JavaScript files that help render the pages.

## How to run your application

To run the application, you need to install the `sklearn` package using the command:

```bash
pip install sklearn
