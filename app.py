import os
import uuid
from pathlib import Path
from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
from convert import convert_file, CONVERTERS

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50 MB

UPLOAD_DIR = Path("/tmp/converter/uploads")
OUTPUT_DIR = Path("/tmp/converter/outputs")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = set(CONVERTERS.keys())


def allowed(filename):
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def upload_and_convert():
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Nome de arquivo vazio."}), 400

    if not allowed(file.filename):
        return jsonify({"error": "Formato não suportado."}), 400

    original_name = secure_filename(file.filename)
    unique_id = uuid.uuid4().hex
    input_path = UPLOAD_DIR / f"{unique_id}_{original_name}"
    file.save(input_path)

    try:
        md_content = convert_file(input_path)
    except Exception as e:
        input_path.unlink(missing_ok=True)
        return jsonify({"error": str(e)}), 500

    output_name = f"{unique_id}_{Path(original_name).stem}.md"
    output_path = OUTPUT_DIR / output_name
    output_path.write_text(md_content, encoding="utf-8")
    input_path.unlink(missing_ok=True)

    return jsonify({
        "preview": md_content[:3000],
        "download_id": output_name,
        "filename": Path(original_name).stem + ".md"
    })


@app.route("/download/<download_id>")
def download(download_id):
    # Segurança: impede path traversal
    safe_name = secure_filename(download_id)
    output_path = OUTPUT_DIR / safe_name
    if not output_path.exists():
        return jsonify({"error": "Arquivo não encontrado."}), 404
    return send_file(
        output_path,
        as_attachment=True,
        download_name=safe_name.split("_", 1)[-1]  # remove o UUID do nome
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)