ALLOWED_EXTENSIONS = set(['pdf', 'mp3', 'txt'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS