from flask import Flask, render_template, request, redirect, url_for, flash, session
from sqlalchemy import create_engine, text
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

app.secret_key = os.getenv("SECRET_KEY")
engine = create_engine(os.getenv("MSSQL_CONNECTION"))
mongo_client = MongoClient(os.getenv("MONGO_URI"))
mongo_db = mongo_client["kullanicilar"]
mongo_collection = mongo_db["kullanicilar"]
 

@app.before_request
def ensure_veritabani_selected():
    allowed_endpoints = {"veritabani_sec", "static"}
    if request.endpoint not in allowed_endpoints and "veritabani" not in session:
        return redirect(url_for("veritabani_sec"))

@app.route("/veritabani", methods=["GET", "POST"])
def veritabani_sec():
    if request.method == "POST":
        session["veritabani"] = request.form.get("veritabani")
        return redirect(url_for("index"))
    return render_template("veritabanisec.html")

@app.route("/")
def index():
    db = session.get("veritabani")
    try:
        if db == "mongodb":
            data = list(mongo_collection.find())
        else:
            with engine.connect() as conn:
                result = conn.execute(text("SELECT * FROM kullanicilar"))
                data = result.fetchall()
    except Exception as e:
        flash(f"Veri cekme hatasi: {str(e)}", "error")
        data = []

    return render_template("index.html", data=data, veritabani=db)

@app.route("/ekle")
def ekle():
    db = session.get("veritabani")
    return render_template("ekle.html", veritabani=db)

@app.route("/kaydet", methods=["POST"])
def kaydet():
    db = session.get("veritabani")

    isim = request.form.get("isim")
    soyisim = request.form.get("soyisim")
    email = request.form.get("email")

    if not isim or not soyisim or not email:
        flash("Tüm alanlar doldurulmalıdır!", "error")
        return redirect(url_for("ekle"))

    try:
        if db == "mongodb":
            mongo_collection.insert_one({"isim": isim, "soyisim": soyisim, "email": email})
            flash("MongoDB: Kullanıcı eklendi!", "success")
        else:
            with engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO kullanicilar (isim, soyisim, email)
                    VALUES (:isim, :soyisim, :email)
                """), {"isim": isim, "soyisim": soyisim, "email": email})
                conn.commit()
            flash("MSSQL: Kullanıcı eklendi!", "success")
    except Exception as e:
        flash(f"Kaydetme hatası: {str(e)}", "error")

    return redirect(url_for("index"))

@app.route("/sil", methods=["GET", "POST"])
def sil():
    db = session.get("veritabani")

    if request.method == "POST":
        user_id = request.form.get("id")
        if not user_id:
            flash("Kullanıcı seçilmedi!", "error")
            return redirect(url_for("sil"))

        try:
            if db == "mongodb":
                mongo_collection.delete_one({"_id": ObjectId(user_id)})
                flash("MongoDB: Kullanıcı silindi.", "success")
            else:
                with engine.connect() as conn:
                    conn.execute(text("DELETE FROM kullanicilar WHERE id = :id"), {"id": user_id})
                    conn.commit()
                flash("MSSQL: Kullanıcı silindi.", "success")
        except Exception as e:
            flash(f"Silme hatası: {str(e)}", "error")
        return redirect(url_for("index"))

    try:
        if db == "mongodb":
            data = list(mongo_collection.find())
        else:
            with engine.connect() as conn:
                result = conn.execute(text("SELECT * FROM kullanicilar"))
                data = result.fetchall()
    except Exception as e:
        flash(f"Veri çekme hatası: {str(e)}", "error")
        data = []

    return render_template("sil.html", data=data, veritabani=db)

@app.route("/guncelle", methods=["GET", "POST"])
def guncelle():
    db = session.get("veritabani")

    if request.method == "POST":
        user_id = request.form.get("id")
        isim = request.form.get("isim")
        soyisim = request.form.get("soyisim")
        email = request.form.get("email")

        try:
            if db == "mongodb":
                mongo_collection.update_one(
                    {"_id": ObjectId(user_id)},
                    {"$set": {"isim": isim, "soyisim": soyisim, "email": email}}
                )
                flash("MongoDB: Kullanıcı güncellendi!", "success")
            else:
                with engine.connect() as conn:
                    conn.execute(text("""
                        UPDATE kullanicilar
                        SET isim = :isim, soyisim = :soyisim, email = :email
                        WHERE id = :id
                    """), {
                        "id": user_id,
                        "isim": isim,
                        "soyisim": soyisim,
                        "email": email
                    })
                    conn.commit()
                flash("MSSQL: Kullanıcı güncellendi!", "success")
        except Exception as e:
            flash(f"Güncelleme hatası: {str(e)}", "error")
        return redirect(url_for("index"))

    try:
        if db == "mongodb":
            data = list(mongo_collection.find())
        else:
            with engine.connect() as conn:
                result = conn.execute(text("SELECT * FROM kullanicilar"))
                data = result.fetchall()
    except Exception as e:
        flash(f"Veri çekme hatası: {str(e)}", "error")
        data = []

    return render_template("guncelle.html", data=data, veritabani=db)

@app.route("/veritabani_degistir")
def veritabani_degistir():
    session.pop("veritabani", None)
    return redirect(url_for("veritabani_sec"))

if __name__ == "__main__":
    app.run(debug=True)
