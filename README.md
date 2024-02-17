## Deploy Your Application with Heroku and GitHub

### Check Out the Deployed App
Explore the deployed app: [HybMotivationSurvey](https://hybmotivationsurvey-7b5b3d0eb29e.herokuapp.com/)

### Getting Started

#### Pre-requisites:
- **GitHub Account:** Ensure you have a GitHub account.
- **Heroku Account:** Make sure you're registered on Heroku.
- **Git:** Install Git on your computer ([Download Git](https://git-scm.com/downloads)).
- **Heroku CLI:** Install the Heroku Command Line Interface ([Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)).

### Push Code to GitHub

#### 1. Initialize a Git Repository
- Navigate to your project's directory in the terminal.
- Run `git init` to create a new Git repository.

#### 2. Add Your Project to the Repository
- Stage your project files with `git add .`.
- Commit the changes using `git commit -m "Initial commit"`.

#### 3. Create a GitHub Repository
- Visit [GitHub](https://github.com/) and create a new repository.

#### 4. Link Your Local Repository to GitHub
- Follow GitHub's instructions to link your local repository. Typically, it involves:
  ```
  git remote add origin https://github.com/yourusername/yourrepositoryname.git
  ```

#### 5. Push Your Code
- Push your code to GitHub:
  ```
  git push -u origin master
  ```
  Use `main` instead of `master` if your branch is named `main`.

### Deploy to Heroku

#### 1. Log in to Heroku CLI
- Open your terminal and log in to Heroku CLI with `heroku login`.

#### 2. Create a Heroku App
- Create a new app on Heroku with `heroku create`. This adds a Heroku remote to your repository.

#### 3. Deploy Your Application
- Deploy your application to Heroku:
  ```
  git push heroku master
  ```
  Replace `master` with `main` if necessary.

#### 4. Open Your Deployed Application
- Open your app in a browser with `heroku open`.

### Additional Resources

For a step-by-step video guide, search for the title or link directly on YouTube: ["Deploy to Heroku and Push Code to GitHub"](https://www.youtube.com/watch?v=nJHrSvYxzjE&t=306s). This video provides a detailed walkthrough to complement these instructions.


Note : Do extract the pages.zip inside the folder the all files will be saved in
