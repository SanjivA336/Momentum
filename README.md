# Momentum (WIP)
A website designed to track and recommend exercise and nutrition plans

## Features
### Current Features:
- User authentication
- Track individual exercises
- Create custom exercise schedules based on user preferences

### Todo:
- Display page: shows user progress over time in terms of exercise length/intensity
- Nutrition: Track user-inputted food and meals to determine calories, and macronutrients for the day
- Goals: Allow users to specify what goals they have (gain/lose weight, strength training, endurance training, etc.)
- Suggestions: Based on goals, form suggestions for what exercises and foods users should do/eat

## Commands to run:
### Windows
- Activate Virtual Environment:

      $ venv/Scripts/activate

- Set Flask Environment Variables:

      $ env:FLASK_APP="src/__init__.py"
      $ env:FLASK_ENV=development
    
- Run Development Server:
    
      $ flask run --debug

### MacOS
- Activate Virtual Environment:

      $ . venv/bin/activate

- Set Flask Environment Variables:

      $ export FLASK_APP=src/__init__.py
      $ export FLASK_ENV=development

- Run Development Server:
    
      $ flask run --debug

  
