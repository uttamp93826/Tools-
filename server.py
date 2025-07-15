from flask import Flask, request, send_file, render_template_string
import PyPDF2
import io

app = Flask(__name__)

@app.route("/")
def index():
    return open("index.html", encoding="utf-8").read()

@app.route("/unlock", methods=["POST"])
def unlock_pdf():
    uploaded_file = request.files["pdf_file"]
    password = request.form["password"]
    reader = PyPDF2.PdfReader(uploaded_file)
    
    if reader.is_encrypted:
        try:
            reader.decrypt(password)
        except:
            return "Invalid password or unable to decrypt."

    writer = PyPDF2.PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    output_pdf = io.BytesIO()
    writer.write(output_pdf)
    output_pdf.seek(0)
    
    return send_file(output_pdf, as_attachment=True, download_name="unlocked.pdf", mimetype="application/pdf")

if __name__ == "__main__":
    app.run(debug=True)
