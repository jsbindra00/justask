from flask import Flask, render_template, request, redirect, make_response, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# tell our app where the database is located.
    # 3 slashes is a relative path
    # 4 slashes is an absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# initialise the database with the app.
db = SQLAlchemy(app)

# Class to configure the format of data in the database.
class Todo(db.Model):
    # configuring the display of the database.
    id = db.Column(db.Integer, primary_key=True)
    # 200 chars big, an entry in this column cannot be empty.
    content = db.Column(db.String(200), nullable=False)

    completed = db.Column(db.Integer, default=0)

    # default value in this column is the date created.
    date_created = db.Column(db.String(200), default="currentdate")

    # string representation of the class
        # returns the id of the task.
    def __repr__(self):
        return '<Task %r' % self.id



# The route decorator tells flask what URL should trigger this function.
    # Routes refer to URL patterns of an app (such as myapp.com/home or myapp.com/about)
# adding two methods that this route can accept.
    # we can send data to the template, and also recieve
@app.route('/', methods=["POST", 'GET'])
def index():
    #request holds the http request object.

    # post data from the html to the database.
    if request.method == "POST":
        # pass in the ID of the input tag.
        task_content = request.form['content']

        # initialise a task object to push to the database
        task_object = Todo(content=task_content)

        try:
            # push the entry to the db.
            db.session.add(task_object)
            db.session.commit()

            # serve the main page back to the user.
            return redirect("/")

        except:
            print("failed")    
    # display the html..
    else:
        # pull all of the stored tasks in the database.
        storedTasks = Todo.query.order_by(Todo.date_created).all()

        # save the variable for use in jinja2 html.
        # serve the main page back to the user.

        # render_template tells flask to serve the html page to the user which we generate with a Jinja template.
        return render_template("index.html", tasks=storedTasks)


if __name__=="__main__":
    app.run(debug=True)