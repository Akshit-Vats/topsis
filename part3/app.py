from flask import Flask, render_template, request
import os
from topsis_program import run_topsis
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def send_email(receiver_email, file_path):
    msg = EmailMessage()
    msg["Subject"] = "Your TOPSIS Result"
    msg["From"] = "EMAIL_NAME"
    msg["To"] = receiver_email
    msg.set_content("Attached is your TOPSIS result file.")

    with open(file_path, "rb") as f:
        file_data = f.read()
        msg.add_attachment(file_data,
                           maintype="application",
                           subtype="octet-stream",
                           filename="result.csv")

    # Gmail SMTP
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("EMAIL_NAME", "EMAIL_PASS")
        smtp.send_message(msg)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        weights = request.form["weights"]
        impacts = request.form["impacts"]
        email = request.form["email"]

        input_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        output_path = os.path.join(app.config["UPLOAD_FOLDER"], "result.csv")

        file.save(input_path)

        run_topsis(input_path, weights, impacts, output_path)

        send_email(email, output_path)

        return "Result sent to your email!"

    return render_template("index.html")


if __name__ == "__main__":
    app.run()