from flask import Flask, Response, request, abort
import os

app = Flask(__name__)
allowed_ip = '87.120.126.217'  # IP المسموح به

@app.route('/')
def show_file_content():
    # التحقق من عنوان IP
    if request.remote_addr != allowed_ip:
        return abort(403)  # ممنوع الوصول
    
    # التأكد من وجود الملف
    if not os.path.exists('text.txt'):
        return "ملف text.txt غير موجود", 404
    
    # قراءة محتوى الملف
    try:
        with open('text.txt', 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        return f"خطأ في قراءة الملف: {str(e)}", 500
    
    # إرسال المحتوى كنص عادي
    return Response(content, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
