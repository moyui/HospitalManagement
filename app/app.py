from flask import redirect, request, url_for

@app.before_request
def before_request():
    path = request.path
    doctorinfoid = request.cookies.get('doctorid')
    if doctorinfoid is None:
        if path != '/' or path != '/login':
            redirect('/login')
    return