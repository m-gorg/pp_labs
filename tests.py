import sys

from werkzeug.datastructures import Headers
sys.path.append('E:\Projects\PPLab9\src')
import pytest
from flask_bcrypt import Bcrypt
import json
from config import app, session
from Database_model import engine, metadata, Category, User, tag_blog, Tag, Blog, EditedBlog

user_moderator = {
        "id": -1,
        "username": "moderator",
        "firstName": "mr",
        "lastName": "mr",
        "email": "mr@gmail.com",
        "password": Bcrypt().generate_password_hash("secret").decode('utf - 8'),
        "phone": "0304321256",
        "userRole": "moderator"
}

user_good_create_1 = {
        "id": 0,
        "username": "Denys23",
        "firstName": "Denys",
        "lastName": "Zakharkevych",
        "email": "denys@gmail.com",
        "password": "12345",
        "phone": "0503456578"
        }

user_good_create_2 = {
        "id": 1,
        "username": "Vladik05",
        "firstName": "Vlad",
        "lastName": "Trompak",
        "email": "vlad.trompak@gmail.com",
        "password": "54321",
        "phone": "0663468312"
        }

user_bad_1 = {
        "id": 0,
        "username": "Lavandos",
        "firstName": "Vladik",
        "lastName": "Trompak",
        "email": "lavandos@gmail.com",
        "password": ";jgs62",
        "phone": "+3806635583450"
        }

user_bad_2 = {
        "id": 1,
        "username": "Denys23",
        "firstName": "Denchuk",
        "lastName": "Zakhar",
        "email": "denisius@gmail.com",
        "password": "54321",
        "phone": "0503456578"
        }

user_bad_3 = {
        "id": 1,
        "username": "Lavandos",
        "firstName": "Vladik",
        "lastName": "Trompak",
        "email": "denys@gmail.com",
        "password": "12345",
        "phone": "0503456578"
        }

auth_moderator = {"Authorization": "Basic bW9kZXJhdG9yOnNlY3JldA=="}

auth_good_1 = {"Authorization": "Basic RGVueXMyMzoxMjM0NQ=="}

auth_good_2 = {"Authorization": "Basic VmxhZGlrMDU6NTQzMjE="}

auth_bad_1 = {"Authorization": "Basic RGVueXMyMz"}

user_good_get_1 = {
        "id": 0,
        "username": "Denys23",
        "firstName": "Denys",
        "lastName": "Zakharkevych",
        "email": "denys@gmail.com",
        "phone": "0503456578"
        }

user_good_update_1 = {
    "firstName": "Vlad",
    "lastName": "Trompak"
}

user_bad_update_1 = {
    "First Name": "Vlad"
}

user_bad_update_2 = {
    "username": "Lavandos",
    "firstName": "Vladik",
    "lastName": "Trompak",
    "email": "lavandos@gmail.com",
    "password": ";jgs62",
    "phone": "+3806635583450",
    "userStatus": "moderator"
}

blog_good_creating_1 = {
    "id": 0,
    "category_id": 1,
    "title": "THE BEST WALKING TOURS IN NEW ORLEANS",
    "contents": "New Orleans is dedicated to fun. Or, as they like to say here: laissez les bons temps rouler (let the good times roll)!",
    "tags": "1, 2"
}

blog_good_creating_2 = {
    "id": 1,
    "category_id": 2,
    "title": "THE BEST WALKING TOURS IN NEW ORLEANS",
    "contents": "New Orleans is dedicated to fun. Or, as they like to say here: laissez les bons temps rouler (let the good times roll)!",
    "tags": "2, 3"
}

blog_good_creating_3 = {
    "id": 2,
    "category_id": 3,
    "title": "THE BEST WALKING TOURS IN NEW ORLEANS",
    "contents": "New Orleans is dedicated to fun. Or, as they like to say here: laissez les bons temps rouler (let the good times roll)!",
    "tags": "4, 5"
}

blog_bad_creating_1 = {
    "id": 0,
    "category_id": 1,
    "title": "THE MOST BEAUTIFUL BOOTS",
    "contents": "I have been on the hunt for the perfect tall lug boots this season and let me tell you guys, it was worth",
    "tags": "3, 4"
}

blog_bad_creating_2 = {
    "id": 5,
    "category_id": 2,
    "title": "THE MOST BEAUTIFUL BOOTS",
    "contents": "x" * 2001,
    "tags": "3, 4"
}

blog_bad_creating_3 = {
    "id": 6,
    "category_id": 10,
    "title": "THE MOST BEAUTIFUL BOOTS",
    "contents": "Do you like butternut squash but sometimes think it’s a bit too big? If so, super sweet and personal-sized honeynut squash is here to save the day!",
    "tags": "3, 4"
}

blog_good_get_1 = {
    "id": 0,
    "category_id": 1,
    "title": "THE BEST WALKING TOURS IN NEW ORLEANS",
    "contents": "New Orleans is dedicated to fun. Or, as they like to say here: laissez les bons temps rouler (let the good times roll)!",
    "tags": "1, 2",
    "author": "Denys23"
}

blog_bad_absent_id_get = 100

blog_good_find_by_tags = {
    "Tag1": 1,
    "Tag2": 2
}

blog_good_find_by_tags_info = {
    "1": {
        "id": 0,
        "category_id": 1,
        "title": "THE BEST WALKING TOURS IN NEW ORLEANS",
        "contents": "New Orleans is dedicated to fun. Or, as they like to say here: laissez les bons temps rouler (let the good times roll)!",
        "tags": "1, 2",
        "author": "Denys23"
    },
    "2": {
        "id": 1,
        "category_id": 2,
        "title": "THE BEST WALKING TOURS IN NEW ORLEANS",
        "contents": "New Orleans is dedicated to fun. Or, as they like to say here: laissez les bons temps rouler (let the good times roll)!",
        "tags": "2, 3",
        "author": "Denys23"
    }
}

blog_bad_find_by_tags = {
    "Tag1": 10,
    "Tag2": 13
}

blog_good_update = {
    "title": "Hello",
    "contents": "whatever"
}

limbo_good_create_1 = {
    "id": 0,
    "title": "THE BEST WALKING TOURS IN NEW ORLEANS",
    "contents": "Whaeeeeereeeeer",
    "originalBlog_id": 0
}

limbo_good_create_2 = {
    "id": 1,
    "title": "THE BEST",
    "contents": "Aliluuuuuuya",
    "originalBlog_id": 1
}

limbo_bad_id_taken_1 = {
    "id": 0,
    "title": "THE BEST",
    "contents": "Aliluuuuuuya",
    "originalBlog_id": 2
}

limbo_bad_long_content_1 = {
    "id": 2,
    "title": "THE BEST",
    "contents": "x" * 2001,
    "originalBlog_id": 2
}

limbo_bad_no_blog_found_1 = {
    "id": 2,
    "title": "THE BEST",
    "contents": "Aliluuuuuuya",
    "originalBlog_id": 100
}

limbo_good_get_1 = {
    "1": {
        "id": 0,
        "title": limbo_good_create_1['title'],
        "contents": limbo_good_create_1['contents'],
        "originalBlog_id": limbo_good_create_1['originalBlog_id']
    },
    "2": {
        "id": 1,
        "title": limbo_good_create_2['title'],
        "contents": limbo_good_create_2['contents'],
        "originalBlog_id": limbo_good_create_2['originalBlog_id']
    }
}

limbo_update_absent_id = 100

@pytest.fixture
def client():
    metadata.drop_all(engine)
    metadata.create_all(engine)
    yield app.test_client()
    session.close()

@pytest.fixture
def client_with_user_1(client):
    client.post('/user', json=user_good_create_1)
    return client

@pytest.fixture
def client_with_users_and_blogs(client, tags_and_categories_created):
    session.add(User(**user_moderator))
    client.post('/user', json=user_good_create_1)
    client.post('/user', json=user_good_create_2)
    client.post('/blog', headers=auth_good_1, json=blog_good_creating_1)
    client.post('/blog', headers=auth_good_1, json=blog_good_creating_2)
    client.post('/blog', headers=auth_good_1, json=blog_good_creating_3)
    return client

@pytest.fixture
def client_with_full_database(client_with_users_and_blogs):
    client_with_users_and_blogs.post('/limbo', headers=auth_good_1, json=limbo_good_create_1)
    client_with_users_and_blogs.post('/limbo', headers=auth_good_1, json=limbo_good_create_2)
    return client_with_users_and_blogs

@pytest.fixture
def tags_and_categories_created():
    category1 = Category(name='Travel')
    category2 = Category(name='Fashion')
    category3 = Category(name='Food')
    category4 = Category(name='Lifestyle')
    category5 = Category(name='Music')
    session.add_all([category1, category2, category3, category4, category5])

    tag1 = Tag(name='eating')
    tag2 = Tag(name='beautiful place')
    tag3 = Tag(name='boots')
    tag4 = Tag(name='blogs for lifestyle')
    tag5 = Tag(name='FOOD')
    tag6 = Tag(name='Scenery')
    tag7 = Tag(name='How I like to eatttttt!')
    session.add_all([tag1, tag2, tag3, tag4, tag5, tag6, tag7])

    session.commit()

def test_root(client):
    resp = client.get('/')
    assert resp.status_code == 404

def test_user_creation_valid(client):
    resp = client.post('/user', json=user_good_create_1)
    assert resp.status_code == 200

def test_user_creating_invalid(client_with_user_1):
    resp = client_with_user_1.post('/user', json={})
    assert resp.json['message'] == 'No input data'
    assert resp.status_code == 400

    resp = client_with_user_1.post('/user', json=user_bad_1)
    assert resp.json['message'] == 'User with such id already exists'
    assert resp.status_code == 400

    resp = client_with_user_1.post('/user', json=user_bad_2)
    assert resp.json['message'] == 'Username already taken'
    assert resp.status_code == 400

    resp = client_with_user_1.post('/user', json=user_bad_3)
    assert resp.json['message'] == 'Email already taken'
    assert resp.status_code == 400

def test_user_login_valid(client_with_user_1):
    resp = client_with_user_1.get('/user/login', headers=auth_good_1)
    assert resp.status_code == 200

def test_user_login_invalid(client_with_user_1):
    resp = client_with_user_1.get('/user/login', headers=auth_bad_1)
    assert resp.status_code == 401

def test_user_logout_valid(client_with_user_1):
    resp = client_with_user_1.get('/user/logout', json=user_good_get_1)
    assert resp.status_code == 200

def test_user_logout_invalid(client_with_user_1):
    resp = client_with_user_1.get('/user/logout', json={})
    assert resp.status_code == 400
    assert resp.json['message'] == 'No input data'

    resp = client_with_user_1.get('/user/logout', json=user_bad_1)
    assert resp.status_code == 404
    assert resp.json['message'] == 'User does not exists'

def test_user_info_valid(client_with_user_1):
    uname = user_good_get_1['username']
    resp = client_with_user_1.get(f'/user/{uname}', headers=auth_good_1)
    assert resp.status_code == 200
    assert resp.json == user_good_get_1

def test_user_info_invalid(client_with_user_1):
    uname = user_good_get_1['username']
    resp = client_with_user_1.get(f'/user/{uname}', headers=auth_bad_1)
    assert resp.status_code == 401

    uname = user_bad_1['username']
    resp = client_with_user_1.get(f'/user/{uname}', headers=auth_good_1)
    assert resp.status_code == 403
    assert resp.json['message'] == 'Access denied'

def test_user_update_info_valid(client_with_user_1):
    uname = user_good_get_1['username']
    resp = client_with_user_1.put(f'/user/{uname}', headers=auth_good_1, json=user_good_update_1)
    assert resp.status_code == 200

def test_user_update_info_invalid(client_with_user_1):
    uname = user_good_get_1['username']
    resp = client_with_user_1.put(f'/user/{uname}', headers=auth_bad_1, json=user_good_update_1)
    assert resp.status_code == 401

    uname = user_bad_1['username']
    resp = client_with_user_1.put(f'/user/{uname}', headers=auth_good_1, json=user_good_update_1)
    assert resp.status_code == 401
    assert resp.json['message'] == 'Access denied'

    uname = user_good_get_1['username']
    resp = client_with_user_1.put(f'/user/{uname}', headers=auth_good_1, json={})
    assert resp.status_code == 400
    assert resp.json['message'] == 'No input data'

    resp = client_with_user_1.put(f'/user/{uname}', headers=auth_good_1, json=user_bad_update_1)
    assert resp.status_code == 400
    assert resp.json['message'] == 'Invalid input data provided'

    resp = client_with_user_1.put(f'/user/{uname}', headers=auth_good_1, json=user_bad_update_2)
    assert resp.status_code == 400
    assert resp.json['message'] == 'Invalid input data provided'

def test_user_delete_valid(client_with_user_1):
    uname = user_good_get_1['username']
    resp = client_with_user_1.delete(f'/user/{uname}', headers=auth_good_1)
    assert resp.status_code == 200
    assert resp.json == user_good_get_1

def test_user_delete_invalid(client_with_user_1):
    uname = user_good_get_1['username']
    resp = client_with_user_1.delete(f'/user/{uname}', headers=auth_bad_1)
    assert resp.status_code == 401

    uname = user_bad_1['username']
    resp = client_with_user_1.delete(f'/user/{uname}', headers=auth_good_1)
    assert resp.status_code == 401
    assert resp.json['message'] == 'Access denied'

def test_blog_creating_valid(client_with_user_1, tags_and_categories_created):
    resp = client_with_user_1.post('/blog', headers=auth_good_1, json=blog_good_creating_1)
    assert resp.status_code == 200

def test_blog_creating_invalid(client_with_users_and_blogs):
    resp = client_with_users_and_blogs.post('/blog', headers=auth_good_1, json={})
    assert resp.status_code == 400
    assert resp.json['message'] == 'No input data'

    resp = client_with_users_and_blogs.post('/blog', headers=auth_good_1, json=blog_bad_creating_1)
    assert resp.status_code == 400
    assert resp.json['message'] == 'Id taken'

    resp = client_with_users_and_blogs.post('/blog', headers=auth_good_1, json=blog_bad_creating_2)
    assert resp.status_code == 400
    assert resp.json['message'] == 'Too long!'

    resp = client_with_users_and_blogs.post('/blog', headers=auth_good_1, json=blog_bad_creating_3)
    assert resp.status_code == 404
    assert resp.json['message'] == 'Category does not exist'

def test_blog_info_valid(client_with_users_and_blogs):
    id = blog_good_creating_1['id']
    resp = client_with_users_and_blogs.get(f'/blog/{id}', headers=auth_good_1)
    assert resp.status_code == 200
    assert resp.json == blog_good_get_1

def test_blog_info_invalid(client_with_users_and_blogs):
    id = blog_bad_absent_id_get
    resp = client_with_users_and_blogs.get(f'/blog/{id}', headers=auth_good_1)
    assert resp.status_code == 404
    assert resp.json['message'] == 'Blog not found'

def test_blog_find_by_tags_valid(client_with_users_and_blogs):
    resp = client_with_users_and_blogs.get('/blog/findByTags', headers=auth_good_1, json=blog_good_find_by_tags)
    assert resp.status_code == 200
    assert resp.json == blog_good_find_by_tags_info

def test_blog_find_by_tags_invalid(client_with_users_and_blogs):
    resp = client_with_users_and_blogs.get('/blog/findByTags', headers=auth_good_1, json={})
    assert resp.status_code == 400
    assert resp.json['message'] == 'No input data'

    resp = client_with_users_and_blogs.get('/blog/findByTags', headers=auth_good_1, json=blog_bad_find_by_tags)
    assert resp.status_code == 404
    assert resp.json['message'] == 'No blogs found'

def test_blog_update_info_valid(client_with_users_and_blogs):
    id = blog_good_creating_1['id']
    resp = client_with_users_and_blogs.put(f'/blog/{id}', headers=auth_good_1, json=blog_good_update)
    assert resp.status_code == 200

def test_blog_update_info_invalid(client_with_users_and_blogs):
    id = blog_bad_absent_id_get
    resp = client_with_users_and_blogs.put(f'/blog/{id}', headers=auth_good_1, json=blog_good_update)
    assert resp.status_code == 404
    assert resp.json['message'] == 'Blog does not exists'

    id = blog_good_creating_1['id']
    resp = client_with_users_and_blogs.put(f'/blog/{id}', headers=auth_good_2, json=blog_good_update)
    assert resp.status_code == 403
    assert resp.json['message'] == 'Access denied'

    id = blog_good_creating_1['id']
    resp = client_with_users_and_blogs.put(f'/blog/{id}', headers=auth_good_1, json={})
    assert resp.status_code == 400
    assert resp.json['message'] == 'No input data'

def test_blog_delete_invalid(client_with_users_and_blogs):
    id = blog_bad_absent_id_get
    resp = client_with_users_and_blogs.delete(f'/blog/{id}', headers=auth_good_1)
    assert resp.status_code == 404
    assert resp.json['message'] == 'Blog does not exists'

    id = blog_good_creating_1['id']
    resp = client_with_users_and_blogs.delete(f'/blog/{id}', headers=auth_good_2)
    assert resp.status_code == 403
    assert resp.json['message'] == 'Access denied'

def test_limbo_creating_valid(client_with_users_and_blogs):
    resp = client_with_users_and_blogs.post('/limbo', headers=auth_good_1, json=limbo_good_create_1)
    assert resp.status_code == 200

def test_limbo_creating_invalid(client_with_full_database):
    resp = client_with_full_database.post('/limbo', headers=auth_good_1, json={})
    assert resp.status_code == 400
    assert resp.json['message'] == 'No input data'

    resp = client_with_full_database.post('/limbo', headers=auth_good_1, json=limbo_bad_id_taken_1)
    assert resp.status_code == 400
    assert resp.json['message'] == 'Id taken'

    resp = client_with_full_database.post('/limbo', headers=auth_good_1, json=limbo_bad_long_content_1)
    assert resp.status_code == 400
    assert resp.json['message'] == 'Too long!'

    resp = client_with_full_database.post('/limbo', headers=auth_good_1, json=limbo_bad_no_blog_found_1)
    assert resp.status_code == 404
    assert resp.json['message'] == 'Blog does not exist'

def test_limbo_info_valid(client_with_full_database):
    resp = client_with_full_database.get('/limbo', headers=auth_moderator)
    assert resp.status_code == 200
    assert resp.json == limbo_good_get_1

def test_limbo_info_invalid(client_with_full_database):
    resp = client_with_full_database.get('/limbo', headers=auth_good_1)
    assert resp.status_code == 403

def test_limbo_update_valid(client_with_full_database):
    id = limbo_good_create_1['id']
    resp = client_with_full_database.put(f'/limbo/{id}', headers=auth_moderator)
    assert resp.status_code == 200

def test_limbo_update_invalid(client_with_full_database):
    id = limbo_update_absent_id
    resp = client_with_full_database.put(f'/limbo/{id}', headers=auth_moderator)
    assert resp.status_code == 404
    assert resp.json['message'] == 'Blog edit does not exists'

def test_limbo_delete_valid(client_with_full_database):
    id = limbo_good_create_1['id']
    resp = client_with_full_database.delete(f'/limbo/{id}', headers=auth_moderator)
    assert resp.status_code == 200

def test_limbo_delete_invalid(client_with_full_database):
    id = limbo_update_absent_id
    resp = client_with_full_database.delete(f'/limbo/{id}', headers=auth_moderator)
    assert resp.status_code == 404
    assert resp.json['message'] == 'Blog does not exists'


if __name__ == '__main__':
    pytest.main()