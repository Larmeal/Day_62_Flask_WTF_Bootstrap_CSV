from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

data = pd.read_csv("cafe-data.csv")
dict = data.to_dict('split')
dict_len = len(dict["index"])

print(dict)
print(dict_len)

class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL()])
    opening_time = StringField('Opening Time e.g. 8AM', validators=[DataRequired()])
    closing_time = StringField('Closing Time e.g. 5:30PM', validators=[DataRequired()])
    coffee_rating = SelectField("Coffee Rating", choices=["☕️", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"], validators=[DataRequired()])
    wifi_rating = SelectField("Wifi Strength Rating", choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"], validators=[DataRequired()])
    power_rating = SelectField("Power Socket Availability", choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"], validators=[DataRequired()])
    submit = SubmitField('Submit')

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        dict_test = {
            "Cafe Name": [form.cafe.data],
            "Location": [form.location.data],
            "Open": [form.opening_time.data],
            "Close": [form.closing_time.data],
            "Coffee": [form.coffee_rating.data],
            "Wifi": [form.wifi_rating.data],
            "Power": [form.power_rating.data]
        }
        save = pd.DataFrame(dict_test)
        save.to_csv("cafe-data.csv", index=False, mode="a", header=False)

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    data = pd.read_csv("cafe-data.csv")
    dict = data.to_dict('split')
    dict_len = len(dict["index"])
    return render_template('cafes.html', cafes=dict, length=dict_len)


if __name__ == '__main__':
    app.run(debug=True)