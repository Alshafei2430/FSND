# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql

```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions'
- Fetches a dictionary contaioning a list of 10 questions in which every element is an object with keys answer, category, difficulty, id, question and values are the corresponding string of that key and number of total questions, current category and a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.
- Request Arguments: currentCategory which is an intger corresponding to the category's id, page which is also an integer.
- Returns: An object with keys, questions:list_of_questions,number_of_total_questions:number_of_total_questions, current_category:category_id, categories:list_of_categories key:value pairs.
{"categories": {
"1": "Science", 
"2": "Art", 
"3": "Geography", 
"4": "History", 
"5": "Entertainment", 
"6": "Sports"
}, 
"current_category": null, 
"questions": [
{"answer": "Maya Angelou", 
"category": 4, 
"difficulty": 2, 
"id": 5, 
"question": "Whose autobiography is entitled 'I Know Why theCagedBird Sings'?"}, 
{"answer": "Tom Cruise", 
"category": 5, 
"difficulty": 4, 
"id": 4, 
"question": "What actor did author Anne Rice first denounce,thenpraise in the role of her beloved Lestat?"}, 
{"answer": "Edward Scissorhands", 
"category": 5, 
"difficulty": 3, 
"id": 6, 
"question": "What was the title of the 1990 fantasy directed byTimBurton about a young man with multi-bladed appendages?"}, 
{"answer": "Brazil", 
"category": 6, 
"difficulty": 3, 
"id": 10, 
"question": "Which is the only team to play in every soccer WorldCuptournament?"}, 
{"answer": "Uruguay", 
"category": 6, 
"difficulty": 4, 
"id": 11, 
"question": "Which country won the first ever soccer World Cupin1930?"}, 
{"answer": "George Washington Carver", 
"category": 4, 
"difficulty": 2, 
"id": 12, 
"question": "Who invented Peanut Butter?"}, 
{"answer": "Lake Victoria", 
"category": 3, 
"difficulty": 2, 
"id": 13, 
"question": "What is the largest lake in Africa?"}, 
{"answer": "The Palace of Versailles", 
"category": 3, 
"difficulty": 3, 
"id": 14, 
"question": "In which royal palace would you find the Hall ofMirrors"}, 
{"answer": "Agra", 
"category": 3, 
"difficulty": 2, 
"id": 15, 
"question": "The Taj Mahal is located in which Indian city?"}, 
{"answer": "Mona Lisa", 
"category": 2, 
"difficulty": 3, 
"id": 17, 
"question": "La Giaconda is better known as what?"}
], 
"success": true, 
"total_questions": 18
}
GET '/categories/{id}/questions'
- Fetches a dictionary of questions based on a category in which every element is an object with keys answer, category, difficulty, id, question and values are the corresponding string of that key, the current category and total number of questions.
- Request Arguments: id of the requested category.
- Returns: An object with keys, questions: that contains a list of questions in which every element is an object of, answer:answer_string, category: category_id, difficulty: difficulty_string, id: id_string,question:question_string key:value pairs,current_category:category_idtotal_questions: total_questions'number key value pairs.
{"current_category": 5, 
"questions": [{"answer": "Tom Cruise", 
"category": 5, 
"difficulty": 4, 
"id": 4, 
"question": "What actor did author Anne Rice first denounce,thenpraisein the role of her beloved Lestat?"} 
{"answer": "Edward Scissorhands", 
"category": 5, 
"difficulty": 3, 
"id": 6, 
"question": "What was the title of the 1990 fantasy directed byTimBurton about a young man with multi-bladed appendages?"}], 
"success": true, 
"total_questions": 2}

POST '/questions'
- Creates a new question if you provided a json object with keys answer, category, difficulty, id, question and values are the corresponding string of that key or Fetches a dictionary of questions based on a search in case you provided a search term term as argument.
- Request Arguments: searchTerm if you want to search.
- Returns:
1. An object with keys, created: created_quiestion_id key:value pairs.
{"success": True,
"created": question.id}
2. An object with keys, questions: list_of_questions, total_questions_found:number_of_questions_found key:value pairs.
{'succes': True,
'questions': [
{"answer": "Maya Angelou", 
"category": 4, 
"difficulty": 2, 
"id": 5, 
"question": "Whose autobiography is entitled 'I Know Why theCagedBird Sings'?"},
{"answer": "Mona Lisa", 
"category": 2, 
"difficulty": 3, 
"id": 17, 
"question": "La Giaconda is better known as what?"}],
'total_questions_found': 2}

POST '/quizzes'
- Fetches a dictionary of a random question which is an object with keys answer, category, difficulty, id, question and values are the corresponding string of that key.
- Request Arguments: None
- Returns: An object with key question:object_of_random_question key: value pairs 
{'question': 
{"answer": "Tom Cruise", 
"category": 5, 
"difficulty": 4, 
"id": 4, 
"question": "What actor did author Anne Rice firstdenounce, then praise in the role of her beloved Lestat?"},
'success': True,}

DELETE '/questions/{id}'
- Deletes a question 
- Request Arguments: The id of the question to be deleted.
- Returns: An object with key deleted:id_of_deleted_question key:value pairs.
{'deleted': 5,
'success': True,}
```
## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```