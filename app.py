from flask import Flask, Response, request, abort
import os

app = Flask(__name__)

# IP المسموح به
ALLOWED_IP = "0"

def get_client_ip():
    """
    جلب IP الحقيقي حتى لو السيرفر خلف Proxy أو Vercel
    """
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.remote_addr


@app.route("/", methods=["GET"])
def show_file_content():
    client_ip = get_client_ip()

    # التحقق من IP
    if client_ip != ALLOWED_IP:
        abort(403)

    # التأكد من وجود الملف
    if not os.path.exists("text.txt"):
        return Response("ملف text.txt غير موجود", status=404, mimetype="text/plain")

    # قراءة محتوى الملف
    try:
        with open("text.txt", "r", encoding="utf-8") as file:
            content = file.read()
    except Exception as e:
        return Response(
            f"خطأ في قراءة الملف: {str(e)}",
            status=500,
            mimetype="text/plain"
        )

    # إرسال المحتوى كنص عادي
    return Response(content, mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
