# Full Stack Trivia API Backend

## Getting Started

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the backend directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the FLASK_ENV variable to development will detect file changes and restart the server automatically.

Setting the FLASK_APP variable to flaskr directs flask to use the flaskr directory and the __init__.py file to find the application.

## Tasks

These are the files you'd want to edit in the backend:

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

### Example API

`GET /api/categories Fetches a dictionary of all available categories`

- Request parameters: none
- Returns: An object with a single key, `categories`, that contains an object of `id: category_name` key: value pairs.

```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}

```

`GET /api/questions?page=<int:page_number> Fetches a paginated dictionary of questions of all available categories`

 - Request parameters (optional): page:int
 - Response:

```json
{
 "categories": {
   "1": "Science", 
   "2": "Art", 
   "3": "Geography", 
   "4": "History", 
   "5": "Entertainment", 
   "6": "Sports"
 }, 
  
 "questions": [
   {
     "answer": "Maya Angelou", 
     "category": 4, 
     "difficulty": 2, 
     "id": 5, 
     "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
   },  
   {
     "answer": "Escher", 
     "category": 2, 
     "difficulty": 1, 
     "id": 16, 
     "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
   }
 ], 
 "success": true, 
 "total_questions": 2
}

```

`DELETE /api/questions/<int:question_id> Delete an existing questions from the repository of available questions`

 - Request arguments: question_id:int
 - Response:

```json
{
  "deleted": "28", 
  "success": true
}
```

`POST /api/questions Add a new question to the repository of available questions`

 - Request body: {question:string, answer:string, difficulty:int, category:string}
 - Response:
 ```json
 {
  "created": 29, 
  "success": true
}
```
`POST /api/search Fetches all questions where a substring matches the search term (not case-sensitive)`

```json
{ 
  "questions": [
    {
      "answer": "Lisbon", 
      "category": 2, 
      "difficulty": 1, 
      "id": 29, 
      "question": "What is the capital of Portugal?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```

`GET /api/categories/<int:category_id>/questions Fetches a dictionary of questions for the specified category`

 - Request argument: category_id:int
 - Response:
 
```json
{ 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
  ], 
  "success": true, 
  "total_questions": 2
}
```

`POST /api/quizzes Fetches one random question within a specified category. Previously asked questions are not asked again.`

 - Request body: {previous_questions: arr, quiz_category: {id:int, type:string}}
 - Response:

 ```json
 {
  "question": {
    "answer": "The Liver", 
    "category": 1, 
    "difficulty": 4, 
    "id": 20, 
    "question": "What is the heaviest organ in the human body?"
  }, 
  "success": true
}
```

## Testing

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
