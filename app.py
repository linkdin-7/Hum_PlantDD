from flask import Flask, render_template, jsonify, request, Markup
from model import predict_image
import utils
# hu lib
import symptom_disease
import disease_treatment
import protein_disease
import disease_protein
import csv

app = Flask(__name__)

@app.route('/',methods=['GET'])
def main():
    return render_template('home.html')

@app.route('/PlanDT', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            file = request.files['file']
            img = file.read()
            prediction = predict_image(img)
            print(prediction)
            res = Markup(utils.disease_dic[prediction])
            return render_template('display.html', status=200, result=res)
        except:
            pass
    return render_template('index.html', status=500, res="Internal Server Error")











#dataset for symptoms and disease
with open('symptom_disease.csv', newline='') as f:
        reader = csv.reader(f)
        symptoms = next(reader)
        symptoms = symptoms[:len(symptoms)-1]
        
#dataset for disease and protein ID
with open('disease_protein.csv', newline='') as f3:
        reader = csv.reader(f3)
        pred = next(reader)
        pred = pred[:len(pred)-1]
        
#dataset for Protein Id and disease
with open('protein_disease.csv', newline='') as f2:
    reader = csv.reader(f2)
    proteins = next(reader)
    proteins = proteins[:len(proteins)-1]

        
#dataset for disease and treatment
with open('disease_treatment.csv', newline='') as f1:
        reader = csv.reader(f1)
        diseases = next(reader)
        diseases = diseases[:len(diseases)-1]
 

#UI of Symptom - Disease
@app.route('/HumanDT', methods=['GET','POST'])
def symptom():
        return render_template('includes/symptom_ui.html', symptoms=symptoms)

#UI of Disease - Protein ID    
@app.route('/protein_predict', methods=['GET'])
def disease():
        return render_template('includes/disease_protein_ui.html', pred=pred)

#UI of Protein ID - Disease    
@app.route('/protein_disease_predict', methods=['GET'])
def protein():
        return render_template('includes/protein_ui.html', proteins=proteins)

#UI of Disease - Treatment
@app.route('/treatment_predict', methods=['GET'])
def treatment():
        return render_template('includes/treatment_ui.html', diseases=diseases)

#code for taking inputs as symptoms from users to predict disease
@app.route('/disease_predict', methods=['POST'])
def disease_predict():
    selected_symptoms = []
    if(request.form['Symptom1']!="") and (request.form['Symptom1'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom1'])
    if(request.form['Symptom2']!="") and (request.form['Symptom2'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom2'])
    if(request.form['Symptom3']!="") and (request.form['Symptom3'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom3'])
    if(request.form['Symptom4']!="") and (request.form['Symptom4'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom4'])
    if(request.form['Symptom5']!="") and (request.form['Symptom5'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom5'])
    disease = symptom_disease.dosomething(selected_symptoms)
    return render_template('disease_predict.html',disease=disease,symptoms=symptoms)

#code for taking disease as input from users to predict protein id
@app.route('/protein_predict', methods=['POST'])
def protein_predict():
    selected_disease = []
    if(request.form['Disease1']!="") and (request.form['Disease1'] not in selected_disease):
        selected_disease.append(request.form['Disease1'])
    protein = disease_protein.dosomething(selected_disease)
    return render_template('disease_protein_predict.html',protein=protein,diseases=diseases)

#code for taking protein id as input from users to predict disease
@app.route('/protein_disease_predict', methods=['POST'])
def protein_disease_predict():
    selected_proteins = []
    if(request.form['Protein1']!="") and (request.form['Protein1'] not in selected_proteins):
        selected_proteins.append(request.form['Protein1'])
    disease = protein_disease.dosomething(selected_proteins)
    return render_template('protein_predict.html',disease=disease,proteins=proteins)

#code for taking disease as input from users to predict treatment
@app.route('/treatment_predict', methods=['POST'])
def treatment_predict():
    selected_disease = []
    if(request.form['Disease1']!="") and (request.form['Disease1'] not in selected_disease):
        selected_disease.append(request.form['Disease1'])
    treatment = disease_treatment.dosomething(selected_disease)
    return render_template('treatment_predict.html',treatment=treatment,diseases=diseases)


if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0',port=environ.get("PORT", 5000))
