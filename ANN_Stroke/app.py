import numpy as np
from flask import Flask, request, jsonify, render_template
from joblib import load

from tensorflow.keras.models import load_model
app = Flask(__name__)

model = load_model("stroke.h5")
sc=load("transform1.save")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/y_predict',methods=['POST'])
def y_predict():
    z = request.form['work_type']
    if (z == "Private"):
        o1,o2,o3,o4,o5 = 1,0,0,0,0
    if (z == "Self-employed"):
        o1,o2,o3,o4,o5 = 0,1,0,0,0
    if (z == "Govt_job"):
        o1,o2,o3,o4,o5 = 0,0,1,0,0
    if (z == "children"):
        o1,o2,o3,o4,o5 = 0,0,0,1,0
    if (z == "Never_work"):
        o1,o2,o3,o4,o5 = 0,0,0,0,1
        
    a = request.form['Residence_type']
    if (a == "Rural"):
        a1,a2 = 1,0
    if (a == "Urban"):
        a1,a2 = 0,1

    b = request.form['gender']
    if(b=='Female'):
        l1 = 0
    if(b=='Male'):
    	l1 = 1
        
    c = request.form['age']
    d = request.form['hypertension']
    e = request.form['heart_disease']
    f = request.form['ever_married']
    if(f=='Yes'):
        f1 = 1
    if(f=='No'):
    	f1 = 0
    g = request.form['avg_glucose_level']
    h = request.form['smoking_status']
    if (h == "formerly smoked"):
        h1,h2,h3,h4 = 1,0,0,0
    if (h == "never smoked"):
        h1,h2,h3,h4 = 0,1,0,0
    if (h == "smokes"):
        h1,h2,h3,h4 = 0,0,1,0
    if (h == "Unknown"):
        h1,h2,h3,h4 = 0,0,0,1

    total = [[o1,o2,o3,o4,o5,a1,a2,l1,c,d,e,f1,g,h1,h2,h3,h4]]
    prediction = model.predict(sc.transform(total))
    
    if(prediction==0):
        output = "He|She will not get stroke"
    else:
        output="He|She will get stroke"

    return render_template('index.html', prediction_text='Result: {}'.format(output))

if __name__ == "__main__":
    app.run(port=8086,debug=True)
