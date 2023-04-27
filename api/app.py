from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import docx2txt
import PyPDF2
import os
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "allow_headers": "Content-Type"}})

@app.route('/', methods=['GET'])
@cross_origin()
def home():
    return '<h3 style="text-align: center; margin-top: 40px;">Salaam, (peace) welcome to matchapp api</h3>'

@app.route('/match', methods=['POST', 'OPTIONS'])
@cross_origin()
def match():
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Aceess-Control-Allow-Methods': 'POST'
        }
        return ('', 204, headers)
    else:
        if 'resumes' not in request.files:
            return 'No resume files found in request'
        
        # extract job description from the request
        job_description = request.form['description']

        # extract resume files from the request
        resume_files = request.files.getlist('resumes')

        # store resume contents in a dictionary
        resume_contents = {}
        for resume_file in resume_files:
            filename = resume_file.filename
            file_extension = os.path.splitext(filename)[1]
            if file_extension == '.pdf':
                pdf_reader = PyPDF2.PdfReader(resume_file)
                resume_text = ''
                for page in pdf_reader.pages:
                    resume_text += page.extract_text()
            elif file_extension == '.docx':
                resume_text = docx2txt.process(resume_file)
            else:
                continue
            resume_contents[filename] = resume_text

        # perform matching algorithm
        job_description_words = word_tokenize(job_description)
        results = []
        for filename, resume_text in resume_contents.items():
            resume_words = word_tokenize(resume_text)
            common_words = set(job_description_words) & set(resume_words)
            match_percentage = len(common_words) / len(job_description_words) * 100
            results.append({'filename': filename, 'match_percentage': match_percentage})

        # sort results by match percentage in descending order
        results = sorted(results, key=lambda x: x['match_percentage'], reverse=True)

        return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

