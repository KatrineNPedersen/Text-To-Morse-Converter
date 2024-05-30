import os

from wtforms.fields.simple import SubmitField, TextAreaField
from wtforms.validators import DataRequired

from dictionary import text_morse_dictionary
from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = os.environ.get("FLASK_KEY")


# Create Form for text input:
class TextForm(FlaskForm):
    input = TextAreaField("Text To Convert:", render_kw={'class': 'input-field'}, validators=[DataRequired()])
    submit = SubmitField("Click To Translate")


def encode(text):
    morse_text = ""
    for character in text:
        if character not in text_morse_dictionary:
            pass
        morse_text += (text_morse_dictionary[character] + " ")
    return morse_text


def decode(text):
    standard_text = ""
    letters = text.split(" ")
    values = list(text_morse_dictionary.values())
    keys = list(text_morse_dictionary.keys())
    for letter in letters:
        standard_text += keys[values.index(letter)]
    return standard_text


@app.route("/", methods=["GET", "POST"])
def index():
    form = TextForm()
    if form.validate_on_submit():
        text = form.input.data
        return redirect(url_for("converted_text", text=text))
    return render_template("index.html", form=form)


@app.route("/morse", methods=["GET", "POST"])
def converted_text():
    if request.method == "POST":
        return redirect(url_for("index"))
    text = request.args.get('text')
    is_morse = True
    for character in text:
        if character.isalpha() or character in "[@_!#$%^&*()<>?}{~:]":
            is_morse = False
            break
    return render_template("code.html", text=text, translated_text=decode(text) if is_morse else encode(text),
                           is_morse=is_morse)


if __name__ == "__main__":
    app.run(debug=True)
