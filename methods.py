from flask import jsonify, request, Blueprint
from flask_bcrypt import Bcrypt
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from models import *
from Schemes import *

Session = sessionmaker()
Session.configure(bind=engine)

api_blueprint = Blueprint("api_blueprint", __name__)

@api_blueprint.route("/user", methods=["POST"])
def create_user():
    session = Session()

    data = request.get_json()
    if not data:
        return {"message": "No input data"}, 400

    found_user = session.query(User).filter_by(id=data['id']).first()
    if found_user:
        return {"message": "User already exists"}, 400

    found_user = session.query(User).filter_by(username=data['username']).first()
    if found_user:
        return {"message": "Username already taken"}, 400

    data['password'] = Bcrypt().generate_password_hash(data['password']).decode('utf - 8')

    user = User(**data)
    session.add(user)
    session.commit()

    return jsonify(User_Schema().dump(user))


@api_blueprint.route('/user/login', methods=['GET'])
def login_user():
    session = Session()

    data = request.get_json()
    if not data:
        return {"message": "No input data"}, 400

    found_user = session.query(User).filter_by(username=data['username']).first()
    if not found_user:
        return {"message": "User does not exists"}, 404

    if not Bcrypt().check_password_hash(found_user.password, data['password']):
        return {"message": "Wrong password"}, 400

    return jsonify(User_Schema().dump(found_user))


@api_blueprint.route('/user/logout', methods=['GET'])
def logout_user():
    session = Session()

    data = request.get_json()
    if not data:
        return {"message": "No input data"}, 400

    found_user = session.query(User).filter_by(username=data['username']).first()
    if not found_user:
        return {"message": "User does not exists"}, 404


    return jsonify(User_Schema().dump(found_user))


@api_blueprint.route('/user/<string:uname>', methods=['GET'])
def get_user_by_username(uname):
    session = Session()

    found_user = session.query(User).filter_by(username=uname).first()
    if not found_user:
        return {"message": "User not found"}, 404


    return jsonify(User_Schema().dump(found_user))


@api_blueprint.route('/user/<string:uname>', methods=['PUT'])
def update_user(uname):
    session = Session()

    data = request.get_json()
    if not data:
        return {"message": "No input data"}, 400

    found_user = session.query(User).filter_by(username=uname).first()
    if not found_user:
        return {"message": "User does not exists"}, 404

    if 'id' in data.keys():
        check_user = session.query(User).filter_by(id=data['id']).first()
        if check_user:
            return {"message": "Id already taken"}, 400

    if 'username' in data.keys():
        check_user = session.query(User).filter_by(username=data['username']).first()
        if check_user:
            return {"message": "Username already taken"}, 400

    attributes = User.__dict__.keys()
    for key, value in data.items():
        if key not in attributes:
            return {"message": "Invalid input data provided"}, 400
        setattr(found_user, key, value)

    session.commit()

    return jsonify(User_Schema().dump(session.query(User).filter_by(username=found_user.username).first()))


@api_blueprint.route('/user/<string:uname>', methods=['DELETE'])
def delete_user(uname):
    session = Session()

    found_user = session.query(User).filter_by(username=uname).first()
    if not found_user:
        return {"message": "User does not exists"}, 404

    output = User_Schema().dump(found_user)

    session.delete(found_user)
    session.commit()

    return jsonify(output)


@api_blueprint.route('/blog/<int:id>', methods=['GET'])
def get_blog_by_id(id):
    session = Session()

    found_blog = session.query(Blog).filter_by(id=id).first()
    if not found_blog:
        return {"message": "Blog not found"}, 404

    return jsonify(Blog_Schema().dump(found_blog))


@api_blueprint.route('/blog/findByTags', methods=['GET']) ###
def get_blogs_by_tags():
    session = Session()

    data = request.get_json()
    if not data:
        return {"message": "No input data"}, 400

    quer = []
    for key, value in data.items():
        found_blog = session.query(tag_blog).filter_by(tag_id=value)
        if not found_blog:
            continue
        for i in found_blog:
            quer.append(i[1])

    if not quer:
        return {"message": "No blogs found"}, 404

    result = list(set(quer))

    res = {}
    for i in range(len(result)):
        res[i + 1] = EditedBlog_Schema().dump(session.query(Blog).filter_by(id=result[i]).first())
    return jsonify(res)


@api_blueprint.route("/blog", methods=["POST"])
def create_blog():
    session = Session()

    data = request.get_json()
    if not data:
        return {"message": "No input data"}, 400

    blog = session.query(Blog).filter_by(id=data['id']).first()
    if blog:
        return {"message": "Id taken"}, 400

    if len(data['contents']) > 2000:
        return {"message": "Too long!"}, 400

    categ = session.query(Category).filter_by(id=data['category_id']).first() ###

    if not categ:
        return {"message": "Category does not exist"}, 404

    blog = Blog(**data)
    session.add(blog)
    session.commit()

    for i in [int(i) for i in data['tags'].split(', ')]:
        ins = tag_blog.insert().values(tag_id=i, blog_id=data['id'])
        engine.execute(ins)

    return jsonify(Blog_Schema().dump(blog))


@api_blueprint.route('/blog/<int:id>', methods=['DELETE'])
def delete_blog(id):
    session = Session()

    found_blog = session.query(Blog).filter_by(id=id).first()
    if not found_blog:
        return {"message": "Blog does not exists"}, 404

    output = Blog_Schema().dump(found_blog)

    session.delete(found_blog)
    session.commit()

    return jsonify(output)


@api_blueprint.route("/limbo", methods=["POST"])
def create_edited_blog():
    session = Session()

    data = request.get_json()
    if not data:
        return {"message": "No input data"}, 400

    limbo = session.query(EditedBlog).filter_by(id=data['id']).first()

    if limbo:
        return {"message": "Id taken"}, 400

    if len(data['contents']) > 2000:
        return {"message": "Too long!"}, 400

    original = session.query(Blog).filter_by(id=data['originalBlog_id']).first()

    if not original:
        return {"message": "Blog does not exist"}, 404


    blog = EditedBlog(**data)
    session.add(blog)
    session.commit()

    return jsonify(EditedBlog_Schema().dump(blog))


@api_blueprint.route("/limbo", methods=["GET"])
def get_edited_blogs():
    session = Session()

    limbo = session.query(EditedBlog)
    quer = [EditedBlog_Schema().dump(i) for i in limbo]
    if not quer:
        return {"message": "No blogs available"}, 404
    res = {}
    for i in range(len(quer)):
        res[i + 1] = quer[i]
    return res


@api_blueprint.route("/limbo/<int:id>", methods=["PUT"])
def approve_edited_blog(id):
    session = Session()

    limbo = session.query(EditedBlog).filter_by(id=id).first()

    if not limbo:
        return {"message": "Blog edit does not exists"}, 404

    blog = session.query(Blog).filter_by(id=limbo.originalBlog_id).first()

    if blog is None:
        return {"message": "Blog does not exists"}, 404

    setattr(blog, 'title', limbo.title)
    setattr(blog, 'contents', limbo.contents)
    session.commit()

    return jsonify(Blog_Schema().dump(session.query(Blog).filter_by(id=limbo.originalBlog_id).first())) ###


@api_blueprint.route('/limbo/<int:id>', methods=['DELETE'])
def delete_edited_blog(id):
    session = Session()

    found_blog = session.query(EditedBlog).filter_by(id=id).first()
    if not found_blog:
        return {"message": "Blog does not exists"}, 404

    d = tag_blog.delete().where(tag_blog.blog_id == id)
    d.execute()

    output = EditedBlog_Schema().dump(found_blog)

    session.delete(found_blog)
    session.commit()

    return jsonify(output)


