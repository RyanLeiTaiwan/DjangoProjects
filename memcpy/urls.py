"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
# from django.contrib.auth import views as auth_views
from memcpy import home_views, login_views, user_views, book_views, entry_views, flashcard_views, \
        quiz_views, leaderboard_views

# TODO: Avoid using "(.+)" to represent digit parameters because URL 'function/abcde' will raise exceptions
urlpatterns = [
    # Home page
    url(r'^$', home_views.home, name='home'),
    # Built-in authentication with our own template login page
    url(r'^login[/]?$', login_views.login, {'template_name': 'memcpy/login.html'}, name='login'),
    # Logout a user and send them back to the login page
    url(r'^logout[/]?$', user_views.logout, name='logout'),
    # User registration
    url(r'^register$', user_views.register, name='register'),

    # View profile
    url(r'^view-profile/(?P<user_id>[0-9]+)[/]?$', user_views.view_profile, name='view-profile'),
    # Edit profile
    url(r'^update-profile', user_views.update_profile, name='update-profile'),
    # Upload photo in profile edit page
    url(r'^upload-photo/(.+)$', user_views.upload_photo, name='upload_photo'),
    # Show profile photo
    url(r'^profile_photo/(.+)$', user_views.get_photo, name='profile_photo'),

    # Browse all books
    url(r'^books[/]?$', book_views.list_all_books, name='books'),
    # Create a book
    url(r'^create-book[/]?$', book_views.create_book, name='create-book'),
    # Show book photo
    url(r'^book_photo/(?P<book_id>[0-9]+)[/]?$', book_views.get_photo, name='book_photo'),

    # Browse all entries of a book
    url(r'^book/(?P<book_id>[0-9]+)[/]?$', entry_views.list_all_entries, name='book'),
    # Create an entry
    url(r'^create-entry/(?P<book_id>[0-9]+)[/]?$', entry_views.create_entry, name='create-entry'),
    # Show entry photo
    url(r'^entry_photo/(?P<entry_id>[0-9]+)[/]?$', entry_views.get_photo, name='entry_photo'),

    # Browse an entry and its flashcards (learning mode)
    url(r'^entry/(?P<entry_id>[0-9]+)[/]?$', entry_views.view_entry, name='entry'),
    # Create a flashcard
    url(r'^create-flashcard/(?P<entry_id>[0-9]+)[/]?$', flashcard_views.create_flashcard, name='create-flashcard'),
    # Show flashcard photo
    url(r'^flashcard_photo/(?P<flashcard_id>[0-9]+)[/]?$', flashcard_views.get_photo, name='flashcard_photo'),

    # Quiz from a random book
    url(r'^random-quiz[/]?$', quiz_views.random_quiz, name='random-quiz'),
    # Quiz from a specific book
    url(r'^quiz/(?P<book_id>[0-9]+)[/]?$', quiz_views.quiz, name='quiz'),
    # url(r'^quiz[/]?$', quiz_views.start_quiz, name='quiz'),
    url(r'^quiz-entries/(?P<book_id>[0-9]+)[/]?$', quiz_views.get_quiz_entries, name='quiz-entries'),
    # url(r'^quiz-entries/(\d+)/(\d+)$', quiz_views.quiz_entries, name='quiz-entries')

    # Leader board
    url(r'^leader-board[/]?$', leaderboard_views.leader_board, name='leader-board'),
]
