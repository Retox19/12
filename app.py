from flask import Flask
from main.views import main_blueprint


from loader.views import loader_blueprint
import logger_init

app = Flask(__name__)  #
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024
app.config["UPLOAD_EXTENSIONS"] = [".jpg,", ".png", ".gif"]

app.register_blueprint(main_blueprint, url_prefix="/")
app.register_blueprint(loader_blueprint, url_prefix="/")

if __name__ == "__main__":
    app.run(debug=True)

