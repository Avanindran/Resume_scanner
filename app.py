#Resume screener

from flask import Flask, render_template
import pdfplumber
import docx2txt
import os
import spacy
import re


#Extract from pdf

def extract_text_from_pdf(pdf_path):
  text = ""
  with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
      text += page.extract_text() + "\n"
  return text.strip()

#Extract from docx
def extract_text_from_docx(docx_path):
  return docx2txt.process(docx_path)

#extract key information(eg. education, skills, contact)
nlp = spacy.load("en_core_web_sm")

def extract_name(text):
  doc = nlp(text) 
  for ent in doc.ents:
    if ent.label_ == "PERSON":
      return ent.text
  return None

#extract contact information

def extract_email(text):
  email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
  email_matches = re.findall(email_pattern, text)
  return email_matches[0] if email_matches else None

def extract_phone(text):
  phone_pattern = r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
  phone_matches = re.findall(phone_pattern, text)
  return phone_matches[0] if phone_matches else None
  
  


#extract education
def extract_education(text):
  education_list = ["diploma", "bachelor", "bachelors", "masters", "doctor", "phd", "post graduate", "A levels", "GCSE", "GCSEs", "A' levels", "AS level", "degree",]
  Found_education = [education for education in education_list if education.lower() in text.lower()]
  
  return Found_education
  

#extract poly if local poly
def extract_poly(text):
  poly_list = ["Republic polytechnic", "Ngee Ann polytechnic", " singapore polytechnic", "nanyang polytechnic", "temasek polytechnic",]
  Found_poly = [poly for poly in poly_list if poly.lower() in text.lower()]

  return Found_poly

#extract skills
def extract_skills(text):
  skills_list = ["communication", "customer service", "finance", "data-    entry", "leadership", "teamwork"]
  found_skills = [skill for skill in skills_list if skill.lower() in text.lower()]
  return found_skills
  
    
#DATA using pandas
import pandas as pd

def process_resume(file_path):
  text = extract_text_from_pdf(file_path)
  name = extract_name(text)
  email = extract_email(text)
  phone = extract_phone(text)
  education = extract_education(text)
  poly = extract_poly(text)
  skills = extract_skills(text)
  return {
    "name": name,
    "email": email,
    "phone": phone,
    "education": education,
    "poly": poly,
    "skills": skills
  }



app = Flask(__name__)
@app.route("/")

def hello():
  
  return render_template("home.html")


if __name__ == "__main__":
  app.run(debug = True, host = "0.0.0.0")