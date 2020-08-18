from wtforms import Form
from wtforms import StringField, FloatField, FileField, SelectField, IntegerField

from wtforms import validators

class SignalForm(Form):
    bandwidth = SelectField('Bandwidth', choices=[('octave', 'octave'), ('third', 'third')])          
    time = FloatField("Tiempo", [validators.DataRequired(message = "The time is required.")
	])
    frequency = IntegerField("Frecuencia", [validators.DataRequired(message = "The frequency is required.")
	])
    method = SelectField('Método', choices=[("Error [%]", 'Error [%]'), ("Armónicos [n]", 'Armónicos [n]')])          
    continuous =  SelectField('continua', choices=[("c", 'c'), ("d", 'd')])          
    value= FloatField("Valor", [validators.DataRequired(message = "The freq2 is required.")
	])
    audio = FileField('Audio File')
     
class ProcessingForm(Form):
    bandwidth = SelectField('Bandwidth', choices=[('octave', 'octave'), ('third', 'third')])          
    t60Method = SelectField('T60 Method', choices=[('t10', 't10'), ('t20', 't20'), ('t30', 't30')])

class SynthesizeForm(Form):
    time = IntegerField("Time", [validators.DataRequired(message = "The time is required.")
	])
    bandwidth = SelectField('Bandwidth', choices=[('octave', 'octave'), ('third', 'third')])          