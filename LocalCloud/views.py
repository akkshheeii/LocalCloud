from flask import Blueprint, render_template, redirect, request, current_app, send_file, url_for, flash
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user, user_unauthorized
import os
from .models import User, File
from . import db

views = Blueprint("views", __name__)

@views.route('/home')
def home():
    if request.method =="GET":
        return render_template('index.html')

@views.route("/dashboard", methods = ["POST","GET"])
def dashboard():
        if not current_user.is_authenticated:
                print("Not authenticated")
                return redirect('/login')
        
        Files = File.query.filter_by(user_id = current_user.id).all()
        print(f"{current_user} - {Files}")
        


        def format_size(size):
            if size==0:
                return f"0"
            elif size < 1024:
                return f"1 KB"

            elif size < 1024 ** 2:
                return f"{size / 1024:.2f} KB"

            elif size < 1024 ** 3:
                return f"{size / (1024 ** 2):.2f} MB"

            else:
                return f"{size / (1024 ** 3):.2f} GB"
        len = File.query.filter_by(user_id = current_user.id).count()


        if len > 0:
            min_file = min(Files, key=lambda f: f.file_size)
            max_file = max(Files, key=lambda f: f.file_size)
            avg_size = current_user.storage_used / len

            min_size = format_size(min_file.file_size)
            max_size = format_size(max_file.file_size)
            avg_size = format_size(avg_size)

        else:
            min_size = "0 B"
            max_size = "0 B"
            avg_size = "0 B"
       
        used_storage = format_size(current_user.storage_used)
        total_storage = format_size(current_user.storage_limit)
        storage_percentage = round(((current_user.storage_used / current_user.storage_limit)*100),2)
        remaining_storage = format_size(current_user.storage_limit - current_user.storage_used)
        Imagec = File.query.filter_by(filetype = "Image").count()
        Docsc = File.query.filter_by(filetype = "Document").count()
        Videoc = File.query.filter_by(filetype = "Video").count()
        Audioc = File.query.filter_by(filetype = "Audio").count()
        Archivec = File.query.filter_by(filetype = "Archive").count()
        Applicationc = File.query.filter_by(filetype = "Application").count()
        Fontc = File.query.filter_by(filetype = "Font").count()
        dbc = File.query.filter_by(filetype = "Database").count()
        Otherc = File.query.filter_by(filetype = "Other").count()

        return render_template(
            "userhome.html",
            user=current_user,
            files=Files,
            filecount = len,
            used_storage=used_storage,
            total_storage=total_storage,
            remaining_storage=remaining_storage,
            storage_percentage = storage_percentage,
            minfile = min_size,
            maxfile = max_size,
            avgfile = avg_size,
            Images = Imagec,
            Docs = Docsc,
            Videos = Videoc,
            Audios = Audioc,
            Archives = Archivec,
            Apps = Applicationc,
            Fonts = Fontc,
            dbs = dbc,
            Others = Otherc
        )

@views.route("/upload", methods=["GET","POST"])
@login_required
def upload():

    if request.method == "POST":
        print("Uploading.. ")
        file = request.files.get("file")

        if file:
            file.seek(0, os.SEEK_END)
            filesize = file.tell()
            file.seek(0)
            print(filesize)
            if current_user.storage_used + filesize > current_user.storage_limit:
                flash("Storage limit exceeded!", "error")
                return print("OVER SIZE")
            
            filename = secure_filename(
                file.filename
            )
            extension = filename.rsplit(".", 1)[1].lower() if "." in filename else ""

            if extension in [
                "jpg", "jpeg", "png", "gif", "bmp", "webp",
                "svg", "ico", "tiff", "heic"
            ]:
                filetype = "Image"

            elif extension in [
                "mp4", "avi", "mov", "mkv", "wmv",
                "flv", "webm", "mpeg", "3gp"
            ]:
                filetype = "Video"

            elif extension in [
                "mp3", "wav", "aac", "flac",
                "ogg", "m4a", "wma"
            ]:
                filetype = "Audio"

            elif extension in [
                "pdf", "doc", "docx", "txt", "rtf",
                "ppt", "pptx", "xls", "xlsx",
                "csv", "odt", "ods", "odp"
            ]:
                filetype = "Document"

            elif extension in [
                "zip", "rar", "7z", "tar",
                "gz", "bz2", "xz", "iso"
            ]:
                filetype = "Archive"

            elif extension in [
                "py", "java", "cpp", "c",
                "cs", "js", "ts", "html",
                "css", "php", "rb", "go",
                "swift", "kt", "sql", "json",
                "xml", "yml", "yaml", "sh"
            ]:
                filetype = "Code"

            elif extension in [
                "exe", "msi", "apk", "ipa",
                "deb", "rpm", "dmg", "app"
            ]:
                filetype = "Application"

            elif extension in [
                "ttf", "otf", "woff", "woff2"
            ]:
                filetype = "Font"

            elif extension in [
                "db", "sqlite", "sqlite3"
            ]:
                filetype = "Database"

            else:
                filetype = "Other"

            user_folder = f"{current_user.id}-{current_user.username}"

            user_path = os.path.abspath(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    user_folder
                )
            )

            os.makedirs(user_path, exist_ok=True)

            filepath = os.path.join(
                user_path,
                filename
            )

            file.save(filepath)

           
            new_file = File(
                filename=filename,
                filepath=filepath,
                file_size=os.path.getsize(filepath),
                filetype= filetype,
                user_id=current_user.id
            )
            

            db.session.commit()

            db.session.add(new_file)
            current_user.storage_used = sum(
                f.file_size for f in File.query.filter_by(user_id=current_user.id).all()
            )
            db.session.commit()
            print(f"UPLOADED {filename}")
            flash("File uploaded successfully!", "success")

    return redirect('/dashboard')

@views.route("/rename/<int:file_id>", methods=["POST"])
@login_required
def rename(file_id):

    file = File.query.filter_by(
        id=file_id,
        user_id=current_user.id
    ).first()

    if not file:
        return redirect(url_for("views.dashboard"))

    new_name = secure_filename(request.form.get("filename"))

    if not new_name:
        return redirect(url_for("views.dashboard"))

    folder = os.path.dirname(file.filepath)

    new_path = os.path.join(folder, new_name)

    os.rename(file.filepath, new_path)

    file.filename = new_name
    file.filepath = new_path

    db.session.commit()
    flash("File renamed successfully!", "success")
    return redirect(url_for("views.dashboard"))



@views.route("/download/<int:file_id>")
@login_required
def download(file_id):

    file = File.query.filter_by(
        id=file_id,
        user_id=current_user.id
    ).first()

    if not file:
        print("File not found.", "error")
        return redirect(url_for("views.dashboard"))
    print(file.filepath)
    print(os.path.exists(file.filepath))
    print("Path:", file.filepath)
    print("Exists:", os.path.exists(file.filepath))
    print("Absolute:", os.path.abspath(file.filepath))
    flash("File Sent!", "success")
    return send_file(
        file.filepath,
        as_attachment=True,
        download_name=file.filename
    )

@views.route("/delete/<int:file_id>", methods=["POST"])
@login_required
def delete(file_id):
    if request.method == "GET":
        print('NO')
    file = File.query.filter_by(
        id=file_id,
        user_id=current_user.id
    ).first()

    if not file:
        print("File not found.", "error")
        return redirect(url_for("views.dashboard"))

    if os.path.exists(file.filepath):
        os.remove(file.filepath)

    db.session.delete(file)
    db.session.commit()
    current_user.storage_used = sum(
    f.file_size for f in File.query.filter_by(user_id=current_user.id).all()
    )

    db.session.commit()

    flash("File uploaded successfully!", "success")

    return redirect(url_for("views.dashboard"))

