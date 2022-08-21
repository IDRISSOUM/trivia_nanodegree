import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app)
    CORS(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/api/categories")
    def retrieve_categories():
        selection = Category.query.order_by(Category.id).all()
        current_category = paginate_questions(request, selection)

        if len(current_category) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "categories": current_category,
                "total_categories": len(Category.query.all()),
            }
        )

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/api/questions', methods=['GET'])
    def get_questions():
        try:
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            if len(current_questions) == 0:
                abort(404)
            
            categories = Category.query.all()
            cat_list = {}

            for req in categories:
                cat_list[req.id] = req.type

            return jsonify({
                'success': True,
                'total_questions': len(Question.query.all()),
                'categories': cat_list,
                'questions': current_questions
            })
        except:
            abort(404)


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            deleted = Question.query.filter_by(id=question_id).one_or_none()
            if deleted is None:
                abort(404)
            len_quiz = len(Question.query.all())

            deleted.delete()
            selection = Category.query.order_by(Category.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'deleted': question_id,
                'success': True,
                'total_questions': len_quiz
            })
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/api/questions', methods=['POST'])
    def create_a_question():

        body = request.get_json()
        question = body.get('question', None)
        answer = body.get('answer', None)
        difficulty = body.get('difficulty', None)
        category = body.get('category',  None)
        
        try:
            insert_quiz = Question(question=question, answer=answer, difficulty=difficulty, category=category)
            insert_quiz.insert()

            return jsonify({
                    'success': True,
                    'created': insert_quiz.id,
                })
        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/api/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', None)

        if search_term:
            search_answer = Question.query.filter(
                Question.question.ilike('%' +search_term+ '%')).all()

            quiz = [question.format() for question in search_answer]
            len_answer = len(search_answer),

            return jsonify({
                'success': True,
                'questions': quiz,
                'total_questions': len_answer,
                'current_category': None
            })
        abort(404)


    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/api/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        category = Category.query.filter_by(id=category_id).one_or_none()
        if category is None:
            abort(404)
        try:
            questions = Question.query.filter_by(category=category.id).all()
            pagination_quiz = paginate_questions(request, questions)
            len_quiz = len(Question.query.all())

            return jsonify({
                'success': True,
                'total_questions': len_quiz,
                'current_category': category.type,
                'questions': pagination_quiz
            })

        except:
            abort(400)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/api/quizzes', methods=['POST'])
    def quizzes_game():
        try:
            body = request.get_json()
            prev_questions = body.get('previous_questions', None)
            category = body.get('quiz_category', None)

            category_id = category['id']
            pass_next_question = None
            
            if category_id is not None:
                get_questions = Question.query.filter_by(category=category_id).filter(Question.id.notin_((prev_questions))).all()    
            else:
                get_questions = Question.query.filter(Question.id.notin_((prev_questions))).all()
            
            if len(get_questions) > 0:
                pass_next_question = random.choice(get_questions).format()
            
            return jsonify({
                'question': pass_next_question,
                'success': True,
            })
        except Exception as e:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def unprocessable(error):
        return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
        }), 400
        
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found"
        }), 404

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def unprocessable(error):
        return jsonify({
        "success": False,
        "error": 500,
        "message": "internal error server"
        }), 500


    return app

