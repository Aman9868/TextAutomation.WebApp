import torch
from transformers import pipeline
import nltk
from flair.data import Sentence
from flair.models import SequenceTagger
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from flask import render_template,request,redirect,url_for,logging,flash,session
from string import punctuation
from textblob import  Word
from user.forms import RegisterForm,LoginForm
from user.models import User
from user import app,db
from flask_login import login_user

##-------------------------Login--------------------------------------------#####
@app.route('/login',methods=['GET','POST'])
def login_page():
    form=LoginForm()
    if form.validate_on_submit():
        # if user information is not correct it means user passing wrong details to the server
        user_auth=User.query.filter_by(username=form.username.data).first()
        if user_auth and user_auth.check_password(attempted_password=form.password.data):
            login_user(user_auth)
            flash(f'Success! You are logged in as: {user_auth.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html',form=form)


#####---------------------------Register------------------------------------------#####
@app.route('/register',methods=['GET','POST'])
def register_page():
    form=RegisterForm()
    if form.validate_on_submit():
        user_create=User(username=form.username.data,email_address=form.email_address.data,
                         password=form.password1.data)
        db.session.add(user_create)
        db.session.commit()
        return redirect(url_for('login_page'))
    if form.errors !={}:
        for err in form.errors.values():
            flash(f'There was an error with creating a user: {err}', category='danger')
    return render_template('register.html',form=form)










##########----------------------------Home-------------------------------------------------------###
@app.route("/")
@app.route("/home")
def home_page():
    return render_template('index.html')

@app.route("/service")
def service():
    return render_template("service.html")
@app.route("/contact")
def contact():
    return render_template('contact.html')
def login():
    return render_template('login.html')
@app.route("/tryitout")
def tryit():
    return render_template('tryitout.html')
@app.route("/projects")
def project_page():
    return render_template('projects.html')
@app.route("/analyze")
def analyze():
    finaltext = request.args.get('text', 'default')
    removestop = request.args.get('removestop','off')
    removepunc = request.args.get('removepunc', 'off')
    mask = request.args.get('mask', 'off')
    sentiment = request.args.get('sentiment', 'off')
    spell = request.args.get('spell', 'off')
    summary=request.args.get('summary','off')
    token = request.args.get('token', 'off')
    generate=request.args.get('generate','off')
    zeroshot=request.args.get('zeroshot','off')
### ---------------------------Stopwords Removal-------------------------------#####
    if removestop == "on":
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(finaltext)
        filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
        result=' '.join([i for i in filtered_sentence])
        params1 = 'Removed Stopwords'
        params2=result
        return render_template('analyze.html',purpose=params1,analyzed_text=params2)

####--------------------------------Remove Punctuations------------------------------#####
    elif (removepunc == "on"):
        def strip_punctuation(s):
            return ''.join(c for c in s if c not in punctuation)
        params4 = strip_punctuation(finaltext)
        params3='Remove Punctuations'
        return render_template('analyze.html', purpose=params3, analyzed_text=params4)
####------------------------------Spell Checker--------------------------------------#####
    elif (spell == "on"):
        w = Word(finaltext)
        check = w.spellcheck()
        param5 = 'Spell Check'
        params6=check
        return render_template('analyze.html', purpose=param5, analyzed_text=params6)
######------------------------Text Summarization----------------------------------------####
    elif (summary=="on"):
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        sm=summarizer(finaltext,max_length=130, min_length=30, do_sample=False)[0]
        sm=sm['summary_text']
        param7='Summarizer'
        return render_template('analyze.html', purpose=param7, analyzed_text=sm)
#####---------------- Token Classifictaion----------------------------------------####
    elif (token=="on"):
        def tokenclass(text):
            tagger = SequenceTagger.load("flair/ner-english")  # Load the NER Tagger
            sentence = Sentence(text)  # Make a Sentence
            res = tagger.predict(sentence)  # Run NER over Sentence
            rs = sentence.get_spans('ner')  # Print NER tag
            return rs
        param8='Token Classification'
        param9=tokenclass(finaltext)
        return render_template('analyze.html', purpose=param8, analyzed_text=param9)
########-------------------------Sentiment Analysis-----------------------------######
    elif (sentiment=="on"):
        sent = pipeline('sentiment-analysis')
        res=sent(finaltext)[0]
        param10=res['label']
        param11='Sentiment Analysis'
        return render_template('analyze.html', purpose=param11, analyzed_text=param10)

#####------------------------Fill Mask-----------------------------------------#####
    elif (mask=="on"):
        classifier = pipeline("fill-mask")
        items=classifier(finaltext)
        param13='Fill Mask'
        return render_template('analyze2.html', purpose=param13, items=items)
#######----------------------Text Generation-----------------------------------####
    elif (generate=="on"):
        generator = pipeline('text-generation', model='gpt2')
        param14='Text Generation'
        param15=generator(finaltext,num_return_sequences=3)
        return render_template('analyze.html', purpose=param14, analyzed_text=param15)



#app.run(debug=True)
