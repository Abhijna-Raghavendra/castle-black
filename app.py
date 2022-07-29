from flask import Flask, render_template, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from openpyxl.workbook import Workbook
from openpyxl import load_workbook
from werkzeug.security import generate_password_hash, check_password_hash
#import RPi.GPIO as GPIO

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret key"

#GPIO.setwarnings(False)
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(18, GPIO.OUT)

wb = load_workbook('sheet.xlsx')
ws = wb.active


class LoginForm(FlaskForm):
	uname = StringField("Username:", validators=[DataRequired()])
	pswd = PasswordField("Password:", validators=[DataRequired()])
	submit = SubmitField("Submit")
	def validate_on_submit(self):
		if self.uname.data:
			for col in ws.iter_cols(min_row=2, min_col=1, max_col=1):
				for cell in col:
					if cell.value == self.uname.data:
						return check_password_hash(ws['B' + str(cell.row)].value, self.pswd.data)
			return False
		else:
			return True

class PswdForm(FlaskForm):
	pswd1 = PasswordField("New password:", validators=[DataRequired()])
	pswd2 = PasswordField("Confirm Password:", validators=[DataRequired()])
	submit = SubmitField("Submit")
	def change_pswd(self, usr):
		if (self.pswd1.data == self.pswd2.data) and (self.pswd1.data != None):
			for col in ws.iter_cols(min_row=2, min_col=1, max_col=1):
				for cell in col:
					if cell.value == usr:
						ws['B' + str(cell.row)] = generate_password_hash(self.pswd1.data)
						wb.save('sheet.xlsx')
						print('succesfully edited')
						return True
		else:
			return False

@app.route('/', methods=['GET','POST'])
def login():
	uname = None
	form = LoginForm()
	if form.validate_on_submit():
		uname = form.uname.data
		form.uname.data = ''
		form.pswd.data = ''
	else:
		uname = 'error'
	return render_template('index.html', uname = uname, form = form)

@app.route('/change_pswd/<usr>', methods=['GET','POST'])
def chng_pswd(usr):
	form = PswdForm()
	pswd1 = None
	pswd2 = None
	if form.change_pswd(usr):
		pswd1 = 'set successfully'
		form.pswd1.data = ''
		form.pswd2.data = ''
	return render_template('/pswd_chng.html', status = pswd1, form = form)


@app.route('/<command>', methods=['GET','POST'])
def process(command):
	#if command == 'open':
	#GPIO.output(18,0)
	#elif command == 'close':
	#GPIO.output(18,1)
	return render_template('thankyou.html', cmd = command)

	
if __name__ == '__main__':
	app.run(debug=True, host ='0.0.0.0')