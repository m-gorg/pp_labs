from flask import jsonify, request, Blueprint
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from Database_model import *
from Schemes import *
from config import session

api_blueprint = Blueprint("api_blueprint", __name__)
auth = HTTPBasicAuth()

@auth.get_user_roles
def get_user_roles(user):
    return user.userRole

@auth.verify_password
def verify_password(username, password):
    found_user = session.query(User).filter_by(username=username).first()
    if not found_user:
        return False
    if Bcrypt().check_password_hash(found_user.password, password):
        return found_user


@api_blueprint.route("/user", methods=["POST"])
def create_user():

    data = request.get_json()
    if not data:
        return {"message": "No input data"}, 400

    found_user = session.query(User).filter_by(id=data['id']).first()
    if found_user:
        return {"message": "User with such id already exists"}, 400

    found_user = session.query(User).filter_by(
        username=data['username']).first()
    if found_user:
        return {"message": "Username already taken"}, 400

    found_user = session.query(User).filter_by(
        email=data['email']).first()
    if found_user:
        return {"message": "Email already taken"}, 400

    data['password'] = Bcrypt().generate_password_hash(
        data['password']).decode('utf - 8')

    user = User(**data)
    session.add(user)
    session.commit()

    return jsonify(User_Schema_Get().dump(user))


@api_blueprint.route('/user/login', methods=['GET'])
@auth.login_required
def login_user():
    found_user = auth.current_user()
    return jsonify(User_Schema_Get().dump(found_user))


@api_blueprint.route('/user/logout', methods=['GET'])
def logout_user():

    data = request.get_json()
    if not data:
        return {"message": "No input data"}, 400

    found_user = session.query(User).filter_by(
        username=data['username']).first()
    if not found_user:
        return {"message": "User does not exists"}, 404

    return jsonify(User_Schema_Get().dump(found_user))


@api_blueprint.route('/user/<string:uname>', methods=['GET'])
@auth.login_required
def get_user_by_username(uname):
    logged_user = auth.current_user()
    if logged_user.username != uname:
        return { "message": "Access denied" }, 403

    found_user = session.query(User).filter_by(username=uname).first()

    return jsonify(User_Schema_Get().dump(found_user))


@api_blueprint.route('/user/<string:uname>', methods=['PUT'])
@auth.login_required
def update_user(uname):
    logged_user_info = auth.current_user()
    if logged_user_info.username != uname:
        return {"message": "Access denied"}, 401

    data = request.get_json()
    if not data:
        return {"message": "No input data"}, 400

    found_user = session.query(User).filter_by(username=uname).first()

    attributes = User.__dict__.keys()
    for key, value in data.items():
        if key not in attributes:
            return {"message": "Invalid input data provided"}, 400
        setattr(found_user, key, value)

    session.commit()

    return jsonify(User_Schema_Get().dump(session.query(User).filter_by(username=found_user.username).first()))


@api_blueprint.route('/user/<string:uname>', methods=['DELETE'])
@auth.login_required
def delete_user(uname):
    logged_user_info = auth.current_user()
    if logged_user_info.username != uname:
        return { "message": "Access denied" }, 401

    found_user = session.query(User).filter_by(username=uname).first()

    output = User_Schema_Get().dump(found_user)

    session.delete(found_user)
    session.commit()

    return jsonify(output)


@api_blueprint.route('/blog/<int:id>', methods=['GET'])
def get_blog_by_id(id):

    found_blog = session.query(Blog).filter_by(id=id).first()
    if not found_blog:
        return {"message": "Blog not found"}, 404

    return jsonify(Blog_Schema().dump(found_blog))


@api_blueprint.route('/blog/findByTags', methods=['GET'])
def get_blogs_by_tags():

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
        res[i + 1] = Blog_Schema().dump(session.query(Blog).filter_by(id=result[i]).first())
    return jsonify(res)


@api_blueprint.route("/blog", methods=["POST"])
@auth.login_required
def create_blog():
    logged_user_info = auth.current_user()

    data = request.get_json()
    if not data:
        return {"message": "No input data"}, 400

    blog = session.query(Blog).filter_by(id=data['id']).first()
    if blog:
        return {"message": "Id taken"}, 400

    if len(data['contents']) > 2000:
        return {"message": "Too long!"}, 400

    categ = session.query(Category).filter_by(id=data['category_id']).first()

    if not categ:
        return {"message": "Category does not exist"}, 404

    data["author"] = logged_user_info.username
    blog = Blog(**data)
    session.add(blog)
    session.commit()

    for i in [int(i) for i in data['tags'].split(', ')]:
        ins = tag_blog.insert().values(tag_id=i, blog_id=data['id'])
        engine.execute(ins)

    return jsonify(Blog_Schema().dump(blog))


@api_blueprint.route('/blog/<int:id>', methods=['PUT'])
@auth.login_required
def change_blog(id):

    blog = session.query(Blog).filter_by(id=id).first()

    if not blog:
        return {"message": "Blog does not exists"}, 404

    logged_user = auth.current_user()
    if blog.author != logged_user.username:
        return { "message": "Access denied" }, 403

    data = request.get_json()
    if not data:
        return {"message": "No input data"}, 400

    print('=================>', blog.__dict__)
    if data.get('title'):
        setattr(blog, 'title', data['title'])
    if data.get('contents'):
        setattr(blog, 'contents', data['contents'])
    session.commit()

    return jsonify(Blog_Schema().dump(session.query(Blog).filter_by(id=id).first()))

@api_blueprint.route('/blog/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_blog(id):

    found_blog = session.query(Blog).filter_by(id=id).first()
    if not found_blog:
        return {"message": "Blog does not exists"}, 404

    logged_user = auth.current_user()
    if found_blog.author != logged_user.username:
        return { "message": "Access denied" }, 403

    output = Blog_Schema().dump(found_blog)


    session.delete(found_blog)
    session.commit()

    return jsonify(output)


@api_blueprint.route("/limbo", methods=["POST"])
@auth.login_required
def create_edited_blog():

    data = request.get_json()
    if not data:
        return {"message": "No input data"}, 400

    limbo = session.query(EditedBlog).filter_by(id=data['id']).first()

    if limbo:
        return {"message": "Id taken"}, 400

    if len(data['contents']) > 2000:
        return {"message": "Too long!"}, 400

    original = session.query(Blog).filter_by(
        id=data['originalBlog_id']).first()

    if not original:
        return {"message": "Blog does not exist"}, 404

    blog = EditedBlog(**data)
    session.add(blog)
    session.commit()

    return jsonify(EditedBlog_Schema().dump(blog))


@api_blueprint.route("/limbo", methods=["GET"])
@auth.login_required(role='moderator')
def get_edited_blogs():

    limbo = session.query(EditedBlog)
    quer = [EditedBlog_Schema().dump(i) for i in limbo]
    if not quer:
        return {"message": "No blogs available"}, 404
    res = {}
    for i in range(len(quer)):
        res[i + 1] = quer[i]
    return res


@api_blueprint.route("/limbo/<int:id>", methods=["PUT"])
@auth.login_required(role='moderator')
def approve_edited_blog(id):

    limbo = session.query(EditedBlog).filter_by(id=id).first()

    if not limbo:
        return {"message": "Blog edit does not exists"}, 404

    blog = session.query(Blog).filter_by(id=limbo.originalBlog_id).first()

    if blog is None:
        return {"message": "Blog does not exists"}, 404

    setattr(blog, 'title', limbo.title)
    setattr(blog, 'contents', limbo.contents)
    session.commit()

    return jsonify(Blog_Schema().dump(session.query(Blog).filter_by(id=limbo.originalBlog_id).first()))


@api_blueprint.route('/limbo/<int:id>', methods=['DELETE'])
@auth.login_required(role='moderator')
def delete_edited_blog(id):

    found_blog = session.query(EditedBlog).filter_by(id=id).first()
    if not found_blog:
        return {"message": "Blog does not exists"}, 404

    output = EditedBlog_Schema().dump(found_blog)

    session.delete(found_blog)
    session.commit()

    return jsonify(output)
