from flask import Flask ,render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from instabot import Bot

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.secret_key = "secret key"

bot = Bot()

bot.login(username=username,password=password)

db = SQLAlchemy(app)

class Followers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "Follower: " + str(self.username)

class Followings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "Following: " + str(self.username)

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(1000), nullable=False)

class Medias(db.Model):
    id = db.Column(db.String(100),primary_key=True)
    likers_ids  = db.Column(db.String(100), nullable=False)



db.create_all()
db.session.commit()

@app.route('/')
def hello():
    return"Hello World"



# @app.route('/login',methods = ['GET','POST'])
# def index():
#     error = None
#     if request.method == "POST":
#         username = request.form['username']
#         password = request.form['password']

#         bot = Bot()
#         try:
#             bot.login(username=username,password=password)
 
#             return redirect('/')
#         except:
#             error = "Invalid Credentials. Please Try Again"
#             print('a')
        
#         return render_template("login.html",error=error)
#     elif request.method == "GET":
#         return render_template("login.html",error=error)

@app.route('/followers', methods = ['GET','POST'])
def followers():
    if request.method == "POST":
        followers_ids = bot.get_user_followers(request.form['username'])
        
        for follower_id in followers_ids:
            user_id = follower_id
            username = bot.get_username_from_user_id(follower_id)

            new_follower = Followers(username=username, user_id = user_id)
            db.session.add(new_follower)
            db.session.commit()
        return redirect('/followers')
    else:
        current_followers = Followers.query.all()
        print(current_followers)
        return render_template("followers.html",followers = current_followers)


@app.route('/followers/clear')
def delete_followers():
    Followers.query.delete()
    db.session.commit()
    return redirect('/followers')

@app.route('/followings', methods = ['GET','POST'])
def followings():
    if request.method == "POST":
        followings_ids = bot.get_user_following(request.form['username'])
        
        for following_id in followings_ids:
            user_id = following_id
            username = bot.get_username_from_user_id(following_id)

            new_following = Followings(username=username, user_id = user_id)
            db.session.add(new_following)
            db.session.commit()
        return redirect('/followings')
    else:
        current_followings = Followings.query.all()
        print(current_followings)
        return render_template("followings.html",followings = current_followings)

@app.route('/followings/clear')
def delete_followings():
    Followings.query.delete()
    db.session.commit()
    return redirect('/followings')

@app.route('/messages', methods = ['GET','POST'])
def messages():
    if request.method == "POST":
        message = request.form['message']
        user_id = bot.get_user_id_from_username(request.form['username'])
        username = bot.get_username_from_user_id(user_id)
        bot.send_message(message,username)

        new_message = Messages(user_id=user_id,username=username,message=message)
        db.session.add(new_message)
        db.session.commit()
        return redirect('/messages')
    else:
        messages = Messages.query.all()
        return render_template("messages.html",messages = messages)

@app.route('/messages/clear')
def delete_messages():
    Messages.query.delete()
    db.session.commit()
    return redirect('/messages')
    
@app.route('/getlikers/', methods = ['GET','POST'])
def get_likers():
    if request.method == "POST":
        url = request.form["url"]
        media_id = bot.get_media_id_from_link(url)
        likers = bot.get_media_likers(media_id=media_id)
        for liker_id in likers:
            username = bot.get_username_from_user_id(liker_id)
            print(username)
        # return redirect('/getlikers')
    else:
        return render_template("getlikers.html")










if __name__ == "__main__":
    app.run(debug=True)
