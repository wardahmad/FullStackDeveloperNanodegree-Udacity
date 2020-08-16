* $ export FLASK_APP=api.py
* $ export FLASK_ENV=development
* $ flask run

## 

* $ curl -X POST http://www.example.com/tasks/
* $ curl http://127.0.0.1:5000/books?page=1
* $ curl http://127.0.0.1:5000/books/1 -X PATCH -H "Content-Type: application/json" -d '{"rating":"10"}'
* $ curl -X DELETE http://127.0.0.1:5000/books/8
* $ curl -X POST -H "Content-Type: application/json" -d '{"title":"testBook","author":"ward","rating":"55"}' http://127.0.0.1:5000/books

* $ python test_flaskr.py