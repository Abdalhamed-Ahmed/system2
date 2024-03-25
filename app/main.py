import datetime
import os

# from pathlib import Path
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

import json

# BASE_DIR = Path(__file__).resolve().parent
# basedir = os.path.abspath(os.path.dirname(__file__))
basedir = os.getcwd()
# os.chdir(basedir)
print(basedir,"=====>")
# print(BASE_DIR)
print("cwd====> " + basedir)

app = Flask(__name__, template_folder=os.path.join(basedir, "app/templates"))
DB_path = "sqlite:///" + os.path.join(basedir, "app/database.db")
print("DataBasePath" + DB_path)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class paper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fileName = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    outgoingNum = db.Column(db.String(80))
    date = db.Column(db.String(80))
    incomingNum = db.Column(db.String(80))
    senderName = db.Column(db.String(80))
    subject = db.Column(db.Text, nullable=False)
    receiver = db.Column(db.String(80))
    archiveNumber = db.Column(db.String(80), nullable=True)
    imgs = db.Column(db.String(80))

    def __repr__(self):
        return f"<مكاتبة {self.fileName}>"
    
categories = [
    "مباحث",
    "قطاع الشمال",
    "قطاع الجنوب",
    "قطاع الشرق",
    "قطاع الغرب",
    "قطاع القاهرة الجديدة",
    "قطاع العاصمة الادارية",
    "جهات",
    "قطاع المجلس القومي",
]
fileNames = [
     ["",["مدة ميعاد","اعمال لجان","حقوق انسان","اعلام وعلاقات","التفتيش والرقابة","الشئون القانونية","المتابعة الخارجية","ملفات خاصة","توجيهات السيد الوزير","قطاع الامن","مفتش الداخلية","نائب المدير",]],
     ["جهات المديرية",[ "الحماية المدنية","الرخص","الرقابة","العلاقات داخلى","العمليات","المالية داخلى","المباحث داخلى","المرافق داخلى","المرور داخلى","التحقيقات","المركبات","النجدة","تقدير جهود","جهات داخلى","حراسة المنشات","شئون الافراد","شئون الظباط","الغرب داخلى","الجنوب داخلى","الشرق داخلى","الشمال داخلى","العاصمة الادارية الجديدة","القاهرة الجديدة","قوات الامن","مساعد المدير للامن",]],
     ["وزير",["مجلس النواب","مجلس الوزراء","المكتب الفنى"]]
]

input("Press Enter to continue...4")

@app.route("/test", methods=("GET",))
def testThat():
    if request.method == "Post":
        redirect("/")     

    return render_template("test.html")

@app.route("/", methods=("GET",))
def testpage():

    return render_template(
        "index.html"
    )

@app.route("/searchByName",methods=["POST"])
def search_by_Name () :
     data = request.get_json()
     name = data.get("name")
     papers = paper.query.filter(
                paper.subject.contains(name),
                )
     templatePapers = []
     for loopPaper in papers:
        insidePaper = {
            "fileName": eval(loopPaper.fileName),
            "outgoingNum": eval(loopPaper.outgoingNum),
        }
        templatePapers.append(insidePaper)
     return json.dumps({"papers":templatePapers})

@app.route("/updatePaperContent",methods=["POST"])
def updatePaperContent () :
     data = request.get_json()
     paper_id = data.get("id")
     paper_to_update = paper.query.get(paper_id)
     paper_to_update.fileName = str(data.get("fileName"))
    #  paper_to_update.category = str(data.get("category"))
     paper_to_update.outgoingNum = str(data.get("outgoingNum"))
     paper_to_update.senderName = str(data.get("senderName"))
     paper_to_update.incomingNum = str(data.get("incomingNum"))
     paper_to_update.subject = str(data.get("subject"))
     paper_to_update.receiver = str(data.get("receiver"))
     paper_to_update.date = str(data.get("date"))
     paper_to_update.archiveNumber = data.get("archiveNumber")
     db.session.commit()
     return json.dumps({"message":"sucess"})


@app.route("/add-answer/<int:paper_id>", methods=["GET","POST"])
def addAnswer(paper_id):
        paper_to_update = paper.query.get(paper_id)
        if request.method == "POST" :
            fileName = eval(paper_to_update.fileName)
            fileName.append(request.form["fileName"])
            category = eval(paper_to_update.category)
            category.append(request.form["category"])
            outgoingNum = eval(paper_to_update.outgoingNum)
            outgoingNum.append(request.form["outgoingNum"])
            senderName = eval(paper_to_update.senderName)
            senderName.append(request.form["senderName"])
            incomingNum = eval(paper_to_update.incomingNum)
            incomingNum.append(request.form["incomingNum"])
            subject = eval(paper_to_update.subject)
            subject.append(request.form["subject"])
            receiver = eval(paper_to_update.receiver)
            receiver.append(request.form["receiver"])
            date = eval(paper_to_update.date)
            date.append(datetime.datetime.now())
            archiveNumber = paper_to_update.archiveNumber
            # archiveNumber.append(request.form["archiveNumber"])

            paper_to_update.fileName = str(fileName)
            paper_to_update.category = str(category)
            paper_to_update.outgoingNum = str(outgoingNum)
            paper_to_update.senderName = str(senderName)
            paper_to_update.incomingNum = str(incomingNum)
            paper_to_update.subject = str(subject)
            paper_to_update.receiver = str(receiver)
            paper_to_update.date = str(date)
            paper_to_update.archiveNumber = archiveNumber            
            db.session.commit()
            return redirect("/information")
        print(paper_to_update)
        
        return render_template("addAnswer.html",paper=paper_to_update, categories= categories,fileNames=fileNames)

@app.route("/update/<int:paper_id>", methods=["GET","POST"])
def updatePaper(paper_id):
        paper_to_update = paper.query.get(paper_id)
        # return it from json to normal array
        selectedPaper = {
            "id": paper_to_update.id,
            "fileName": eval(paper_to_update.fileName),
            "category": eval(paper_to_update.category),   
            "outgoingNum": eval(paper_to_update.outgoingNum),
            "senderName": eval(paper_to_update.senderName),
            "incomingNum": eval(paper_to_update.incomingNum),
            "subject": eval(paper_to_update.subject),
            "receiver": eval(paper_to_update.receiver),
            "archiveNumber": paper_to_update.archiveNumber,
            "date":eval(paper_to_update.date),
            "paperLength":len(eval(paper_to_update.fileName)),
        }
        if request.method == "POST":
            paper_to_update.fileName = str(request.form["fileName"])
            paper_to_update.category = str(request.form["category"])
            paper_to_update.outgoingNum = str(request.form["outgoingNum"])
            paper_to_update.senderName = str(request.form["senderName"])
            paper_to_update.incomingNum = str(request.form["incomingNum"])
            paper_to_update.subject = str(request.form["subject"])
            paper_to_update.receiver = str(request.form["receiver"])
            paper_to_update.archiveNumber = request.form["archiveNumber"]
            db.session.commit()
            return redirect("/information")

        return render_template("update.html",paper = selectedPaper, categories= categories,fileNames=fileNames)

@app.route("/delete/<int:paper_id>", methods=["GET","POST"])
def deletePaper(paper_id):
        paper_to_update = paper.query.get(paper_id)
        db.session.delete(paper_to_update)
        db.session.commit()
        return redirect("/information")

@app.route("/information", methods=("GET",))
def home():
    params_fileName = request.args.get("fileName")
    params_archiveNumber = request.args.get("archiveNumber")
    params_subject = request.args.get("subjectFilter")
    params_receiverNum = request.args.get("receiverNumberFilter")
    params_receiverName = request.args.get("receiverNameFilter")
    params_senderNumber = request.args.get("senderNumberFilter")
    params_senderName = request.args.get("senderNameFilter")
    papers = []

    if params_fileName or params_archiveNumber or params_subject or params_receiverNum or params_receiverName or params_senderNumber or params_senderName :
        if params_archiveNumber == "continue" :
            papers = paper.query.filter(
                paper.fileName.contains(params_fileName),
                paper.outgoingNum.contains(params_receiverNum),
                paper.receiver.contains(params_receiverName),
                paper.incomingNum.contains(params_senderNumber),
                paper.senderName.contains(params_senderName),
                paper.subject.contains(params_subject),
                paper.archiveNumber == ""
                )
        else : 
            if params_archiveNumber == "finished" :
                papers = paper.query.filter(
                    paper.fileName.contains(params_fileName),
                    paper.outgoingNum.contains(params_receiverNum),
                    paper.receiver.contains(params_receiverName),
                    paper.incomingNum.contains(params_senderNumber),
                    paper.senderName.contains(params_senderName),
                    paper.subject.contains(params_subject),
                    paper.archiveNumber != ""
                    )
            else : 
                papers = paper.query.filter(
                    paper.fileName.contains(params_fileName),
                    paper.outgoingNum.contains(params_receiverNum),
                    paper.receiver.contains(params_receiverName),
                    paper.incomingNum.contains(params_senderNumber),
                    paper.senderName.contains(params_senderName),
                    paper.subject.contains(params_subject),

                    )
         
    else:
        papers = paper.query.all()

    templatePapers = []
    for loopPaper in papers:
        insidePaper = {
            "id": loopPaper.id,
            "fileName": eval(loopPaper.fileName),
            "category": eval(loopPaper.category),   
            "outgoingNum": eval(loopPaper.outgoingNum),
            "senderName": eval(loopPaper.senderName),
            "incomingNum": eval(loopPaper.incomingNum),
            "subject": eval(loopPaper.subject),
            "receiver": eval(loopPaper.receiver),
            "archiveNumber": loopPaper.archiveNumber,
            "date":eval(loopPaper.date),
            "paperLength":len(eval(loopPaper.fileName)),
        }
        templatePapers.append(insidePaper)
    return render_template(
        "informations.html",papers=templatePapers, categories=categories, fileNames=fileNames
    )


@app.route("/create/", methods=("GET", "POST"))
def create_paper():
    if request.method == "POST":
        fileName = []
        category = []
        outgoingNum = []
        senderName = []
        incomingNum = []
        subject = []
        receiver = []
        date = []
        fileName.append(request.form["fileName"])
        category.append(request.form["category"])
        outgoingNum.append(request.form["outgoingNum"])
        senderName.append(request.form["senderName"])
        incomingNum.append(request.form["incomingNum"])
        subject.append(request.form["subject"])
        receiver.append(request.form["receiver"])
        date.append(datetime.datetime.now())

        new_paper = paper(
            fileName=str(fileName),
            category=str(category),
            outgoingNum=str(outgoingNum),
            senderName=str(senderName),
            incomingNum=str(incomingNum),
            subject=str(subject),
            receiver=str(receiver),
            archiveNumber= request.form["archiveNumber"],
            date = str(date)    
        )

        # Add the paper object to the database
        db.session.add(new_paper)
        db.session.commit()

        
    return render_template("create.html", categories=categories, fileNames=fileNames)




if __name__ == "__main__":
    # user_in = input("create database? (y/n)")

    with app.app_context():
        input("Press Enter to continue...7")

        db.create_all()
        input("Press Enter to continue...8")

    app.run(debug=True)
    input("Press Enter to continue...9")


input("Press Enter to continue...")