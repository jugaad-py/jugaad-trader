
## Install virtualenv

`# pip install virtualenv`

## Fork the repository

Fork the `jugaad-trader` repo. Here's a simple guide on [forking](https://docs.github.com/en/get-started/quickstart/fork-a-repo)


## Clone the repo and set up the environment

```
# git clone https://github.com/[your-github-user-id]/jugaad-trader.git
# cd jugaad-trader
# virtualenv env -p python3
# source env/bin/activate
# pip install -r requirements.txt
# pip install -r dev.requirements.txt
```

You are all set at this point. Now you can save your credentials and run the tests (This will log into your account and do basic check, refer code in tests folder before you run the tests).

```
# python -m jugaad_trader.cli zerodha savecreds
# pytest
```

You can run specific tests as well-

```
# pytest tests/test_console.py
# pytest tests/test_console.py::test_dashboard
```

Hopefully, all tests should pass.

## Make the changes

* Make your changes to fix the bug or add a new functionality 
* Write a test for the new change in `tests` folder at an appropriate place
* Run all the tests to make sure issue is fixed and it has not broken any other feature
* Please do not include any personally identifiable information in your code (eg. your username, password, DP/ID etc), either in test or code

## Push your code to cloned repo

```
# git add .
# git commit -m "Explain the change with comment"
# git push origin master
```

## Submit a pull request

Submit your pull request with an explaination of how you have solved the problem. Here's a simple guide on how to create a [pull request](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork).
