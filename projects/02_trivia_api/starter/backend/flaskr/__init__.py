import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
questionsPerPlay = 5

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  questions = [question.format() for question in selection]
  paginate_questions_response = {
    'questions': questions[start:end],
    'total_questions': len(questions)
    }
  return paginate_questions_response
def format_to_dict(categories):
    dict={}
    for category in categories:
      dict[category.id]=category.type
    return dict
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/*":{"origins": "*"}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  # CORS Headers 
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def categories():
    try:
      #checking if the method is valid
      if request.method == 'GET':
        categories = Category.query.order_by(Category.id).all()
        return jsonify({
          'success': True,
          'categories': format_to_dict(categories)
        })
      #if not 
      # then inform that method is not allowed 
      else:
        abort(405)
    #if some thing went wrong
    except:
      abort(500)
  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=["GET", "POST"])
  def questions():
    #checking the method
    #if GET
    if request.method == 'GET':
      #validating the arguments
      category_id = request.args.get('currentCategory')
      try:
        if category_id == 'null' or category_id is None:
          questions = Question.query.all()
        elif (category_id is not None) and (category_id != "null"):
          category_id = int(request.args.get('currentCategory'))
        elif Category.query.filter(Category.id == category_id).one_or_none() is None:
          abort(404)
      #currentCategory argument is not vaild
      except:
        abort(400)
      questions = Question.query.all()
      data = paginate_questions(request, questions)
      current_questions = data.get("questions")
      #checking if there was a questions returned from paginate_questions function
      if len(current_questions) != 0:
        total_questions = data.get("total_questions")
        categories = Category.query.order_by(Category.id).all()
        categories = format_to_dict(categories)
        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': total_questions ,
          'current_category':category_id,
          'categories': categories
        })
      #informing about wrong page number
      else:
        abort(404)
    #if POST
    elif request.method == 'POST':
      # deciding whether to create a post or give questions
      search_term = request.args.get('searchTerm')
      #if it is a search request
      if search_term is not None:
        questions = Question.query.filter(
                                          Question.question.ilike('%{}%'.format(search_term))
                                          )
        questions = [question.format() for question in questions]
        if len(questions) != 0:
          return jsonify({
            'succes': True,
            'questions': questions,
            'total_questions_found': len(questions)
          })
        abort(404)
      #if it is a creation request
      elif search_term is None:
        try:
          question = request.json
          question = Question(
            answer = question['answer'],
            category = question['category'],
            difficulty = question['difficulty'],
            question = question['question'])
          question.insert()
          return jsonify({
            "success": True,
            "created": question.id
          })
        #if missing the required data for creating the question
        except:
          abort(400)
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route("/questions/<int:question_id>", methods=["DELETE"])
  def delete_question(question_id):
    #validation the method
    #if it is allowed
    if request.method == "DELETE":
      question = Question.query.filter(Question.id == question_id).one_or_none()
      #checking if the question exists
      if question is not None:       
        question.delete()
        return jsonify({
          "success": True,
          "deleted": question.id
        })
      #if not
      else:
        abort(404)
    #if not
    else:
      abort(405)
  '''
  @TODO: #Done in a previous section
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: #Done in a previous section
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  @app.route('/categories/<int:category_id>/questions')
  def question_by_category(category_id):
    questions = Question.query.filter(Question.category == category_id)
    questions = [question.format() for question in questions]
    return jsonify({
        'success': True,
        'questions': questions,
        'total_questions': len(questions),
        "current_category": category_id
      }) if len(questions) != 0 else abort(404)
  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods = ['POST'])
  def quizzes():
    res = request.json
    previous_questions = res['previous_questions']
    quiz_category = res['quiz_category']
    #quering at the begining of the game or at restarting
    if quiz_category['id'] == 0 or len(previous_questions) >= questionsPerPlay:
      questions = Question.query.all()
    #quering during the game
    else:
      questions = Question.query.filter(~(Question.id.in_(previous_questions)), Question.category == quiz_category['id'])
    questions = [question.format() for question in questions]
    #checking if there are questions after quering
    if len(questions) != 0:
      question = random.choice(questions)
      return jsonify({
        'question': question,
        'success': True,
        })
    #if not
    else:
      return jsonify({
        'message': "no more questions", 
        'success': False,
        })
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  #handling errors 
  #handling bad requests errors
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'Bad request',
    }), 400
  #handling resources not found errors
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'Resource not found',
    }), 404
  #handling not allowed methods errors
  @app.errorhandler(405)
  def not_allawed(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': 'Method not allowed',
    }), 405
  #handling unprocessable requests 
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'Unprocessable',
    }), 422
  #handling internal server errors
  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      'success': False,
      'error': 500,
      'message': 'Internal server error',
    }), 500
  return app