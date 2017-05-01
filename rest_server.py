from flask import Flask, request, jsonify, Response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Posting
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)
# Create the appropriate app.route functions,
#test and see if they work
engine = create_engine('sqlite:///posting.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

validJsonKeys = ["name", "contents"]

def isValidJson(jsonbody):
    keys = jsonbody.keys()
    for key in keys:
        try :
            print(validJsonKeys.index(key))
        except ValueError as e:
            print(e)
            return False;
    return True
def getAllPosting():
    postings = session.query(Posting).all()
    return jsonify(postings=[i.serialize for i in postings])

def getPostingById(id):
    try :
        posting = session.query(Posting).filter_by(id = id).one()
    except Exception as e :
        print(e)
        return jsonify({'result' : 'fail'}), 500
    except NoResultFound as e:
        return jsonify({'result' : 'fail'}), 404
    else:
        return jsonify(posting=posting.serialize), 200

def postPosting(jsonbody):
    try:
        if (isValidJson(jsonbody) == False):
            return jsonify({"result": "invalid argument"}), 400
        posting = Posting(name = jsonbody['name'], contents = jsonbody['contents'])
        session.add(posting)
        session.commit()
    except Exception as e:
        print(e)
        return jsonify({'result' : 'fail'}), 500
    return jsonify(posting=posting.serialize), 201

def deletePostingById(id):
    try:
        posting = session.query(Posting).filter_by(id = id).one()
        session.delete(posting)
        session.commit()
    except NoResultFound as e:
        return jsonify({'result' : 'invalid id'}), 404
    except Exception as e:
        return jsonify({'result' : 'fail'}), 500
    else:
        return jsonify({'result' : 'success'}), 200

def updatePostingById(id, jsonbody):
    try:
        posting = session.query(Posting).filter_by(id = id).one()
        if (isValidJson(jsonbody) == False):
            return jsonify({'result' : "fail"}), 400
        name = jsonbody['name']
        contents = jsonbody['contents']
        if name:
            posting.name = name
        if contents:
            posting.contents = contents
            session.add(posting)
            session.commit()
    except NoResultFound as e:
        return jsonify({'result' : 'fail'}), 404
    except Exception as e:
        return jsonify({'result' : 'fail'}), 500

    return  jsonify(posting=posting.serialize), 200

#Make an app.route() decorator here for when the client sends the URI "/puppies"
@app.route("/posts", methods=['GET', 'POST'])
def requestHandleBase():
    #post get!!\
    if (request.method == "GET"):
        return getAllPosting()
    elif (request.method == "POST"):
        jsonbody = request.get_json()

        js, code = postPosting(jsonbody)
        return js, code
    return ""

@app.route('/posts/<int:id>', methods = ['GET', 'PUT', 'DELETE'])
def requestHandleById(id):
    #update db and update
    if (request.method == "GET"):
        js, code = getPostingById(id);
        return js, code
    elif (request.method == "PUT"):
        jsonbody = request.get_json()
        js, code = updatePostingById(id, jsonbody)
        return js, code
    elif (request.method == "DELETE"):
        js, code = deletePostingById(id)
        return js, code
    return ""


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
