from flask import (
    Blueprint,
    render_template,
    request,
    send_from_directory,
    abort,
    current_app
)
from main.views import DATABASE
import os
import logging

loader_blueprint = Blueprint("loader_blueprint", __name__, template_folder="templates")

logger_mine = logging.getLogger("logger")


@loader_blueprint.route("/post/")
def loader_page():
    return render_template("post_form.html")


@loader_blueprint.route("/uploads/<path:path>")
@loader_blueprint.route("/uploads", methods=["POST"])
def uploaded_page(path=None):
    """
    Вьюшка загрузки нового сообщения - методом POST загрузка, без методо рендер
    :param path: Путь загрузки
    """
    if request.method == "POST":
        picture = request.files.get("picture")
        if not picture:  # Обработка исключения/ошибок
            logger_mine.error("Попытка загрузку неразрешенного типа файла")
            abort(400)
        elif picture.filename == "":
            logger_mine.info("Попытка загрузку сообщения без файла")
            abort(400)

        picture.save(f"./uploads/{picture.filename}")
        text = request.values.get("content")
        DATABASE.json_write(
                {"pic": "../../uploads/" + picture.filename, "content": text}
        )
        return render_template(
                "post_uploaded.html", added_text=text, added_picture=picture.filename
        )
    else:
        return send_from_directory("uploads", path)


# Обработка ошибок Блюпринта


@loader_blueprint.errorhandler(413)
@loader_blueprint.errorhandler(400)
def file_type_not_allowed(error):
    return (
            f"<h1><center><font color='red'>Error with picture file</font>"
            f"<br>File size are too large."
            f"<br>Sending message without picture not allowed."
            f"<br>Only PNG, JPG and GIF are allowed.</center></h1><hr>"
    )


@loader_blueprint.errorhandler(404)
def page_not_found(error):
    return (
            f"<h1><center><font color='red'>Error 404</font>"
            f"<br>Something goes wrong! Page not found.</center></h1><hr>"
    )