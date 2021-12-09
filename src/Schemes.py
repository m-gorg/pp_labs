from marshmallow import Schema, fields, ValidationError, pre_load


class User_Schema(Schema):
    id = fields.Int()
    username = fields.Str()
    password = fields.Str()
    firstName = fields.Str()
    lastName = fields.Str()
    email = fields.Str()
    phone = fields.Str()
    userRole = fields.Str()


class User_Schema_Get(Schema):
    id = fields.Int()
    username = fields.Str()
    firstName = fields.Str()
    lastName = fields.Str()
    email = fields.Str()
    phone = fields.Str()

class Blog_Schema(Schema):
    id = fields.Int()
    author = fields.Str()
    category_id = fields.Int()
    title = fields.Str()
    contents = fields.Str()
    tags = fields.Str()


class EditedBlog_Schema(Schema):
    id = fields.Int()
    title = fields.Str()
    contents = fields.Str()
    originalBlog_id = fields.Int()


'''

create user
curl -X POST -H "Content-Type:application/json" --data-binary "{\"id\": 2, \"username\": \"user2\", \"password\": \"12345\", \"firstName\": \"heorii\", \"lastName\": \"mikhed\", \"email\": \"gmm@com\", \"phone\": \"36745\", \"userRole\": \"admin\"}" http://localhost:5000/user

login
curl -X GET -H "Content-Type:application/json" --data-binary "{\"username\": \"gorg\", \"password\": \"12345\"}" http://localhost:5000/user/login

logout
curl -X GET -H "Content-Type:application/json" --data-binary "{\"username\": \"gorg\"}" http://localhost:5000/user/logout

get user by username
curl -X GET -H "Content-Type:application/json" http://localhost:5000/user/gorg

update user
curl -X PUT -H "Content-Type:application/json" --data-binary "{\"firstName\": \"user\"}" http://localhost:5000/user/user2

delete user
curl -X DELETE -H "Content-Type:application/json" http://localhost:5000/user/gorg

''''''

post blog
curl -X POST -H "Content-Type:application/json" --data-binary "{\"id\": 3, \"category_id\": 10, \"title\": \"blog1\", \"contents\": \"abc defg\", \"tags\": \"1, 2\"}" http://localhost:5000/blog

post blog (error)
curl -X POST -H "Content-Type:application/json" --data-binary "{\"id\": 2, \"category_id\": 1, \"title\": \"few words\", \"contents\": \"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\", \"tags\": \"1\"}" http://localhost:5000/blog

get blog by id
curl -X GET -H "Content-Type:application/json" http://localhost:5000/blog/1

find blogs by tags
curl -X GET -H "Content-Type:application/json" --data-binary "{\"0\": 2}" http://localhost:5000/blog/findByTags

delete blog
curl -X DELETE -H "Content-Type:application/json" http://localhost:5000/blog/1

''''''

post blog edit
curl -X POST -H "Content-Type:application/json" --data-binary "{\"id\": 2, \"title\": \"few words\", \"contents\": \"redact2\", \"originalBlog_id\": 1}" http://localhost:5000/limbo

get blog edits
curl -X GET -H "Content-Type:application/json" http://localhost:5000/limbo

approve edit
curl -X PUT -H "Content-Type:application/json" http://localhost:5000/limbo/2

delete blog
curl -X DELETE -H "Content-Type:application/json" http://localhost:5000/limbo/1

'''
