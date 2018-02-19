## Better words

[![Deploy on your own Heroku server!](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy) <-- click here to deploy this app on your own free Heroku server!

Learn more about your words and their social impact and build new habits around your language.


### Using the app

The bot will not message you about a word if you escape it with backticks.

TODO: add details about all the commands and how they work, once we build them


### Pushing changes to Heroku

1. `brew install heroku-toolbelt` (if you have heroku, you need to get it to recognize heroku-toolbelt instead, I just ininstalled heroku)

2. `heroku git:remote -a [name of your app] -r production`

3. `git push production [your_branch_name]:master` when you make changes


### DB stuff (to write better info about before we ship it)

* To seed your DB (load it up with the words/categories specified in yml), run `python -m better_words.db.seed`. If you add new words or change the yml file, you will need to reseed.

* Your DB, by default, will be sqlite based and stored in the file `db.sqlite`. If you want to use a different DB, such as postgres on heroku, specify the ENV var `DATABASE_URL`

* There are python models in `/models` representing each DB table for easy access
