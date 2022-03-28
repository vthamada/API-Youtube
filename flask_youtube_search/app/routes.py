from app import youtube_api
from flask import Blueprint, render_template, request, redirect, url_for

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    videos = []
    if request.method == 'POST':
        search = request.form.get('query')
        videos = youtube_api.search(search)

    return render_template('index.html', videos=videos)


@main.route('/salvar/', methods=['GET', ])
def salvar():
    video = []
    video_id = str(request.args.get('id'))
    video = youtube_api.pesquisa_video(video_id)
    youtube_api.salvar_video(video[0])

    return redirect(url_for('main.videos_salvos'))


@main.route('/apagar_video/', methods=['GET', ])
def apagar_video():
    video_id = str(request.args.get('id'))
    video = youtube_api.video_dados(video_id)
    youtube_api.apagar_video(video)

    return redirect(url_for('main.videos_salvos'))


@main.route('/videos_salvos/', methods=['GET', ])
def videos_salvos():
    videos = youtube_api.videos_salvos()
    return render_template('videos.html', videos=videos)


@main.route('/editar_video/', methods=['GET', ])
def editar_video():
    video_id = str(request.args.get('id'))
    video = youtube_api.video_dados(video_id)
    return render_template('editar.html', video=video)


@main.route('/save_edit/', methods=['POST', ])
def save_edit():
    video_id = request.form['video_id']
    title_edit = request.form['title_edit']
    description_edit = request.form['description_edit']
    video = youtube_api.video_dados(video_id)

    youtube_api.update_title(video, title_edit)

    youtube_api.update_resumo(video, description_edit)

    return redirect(url_for('main.videos_salvos'))


@main.route('/dados_video/', methods=['GET', ])
def dados_video():
    video_id = str(request.args.get('id'))
    video = youtube_api.video_dados(video_id)
    return render_template('view.html', video=video)

@main.route('/teste/', methods=['GET', ])
def teste(): 
    return render_template('teste.html')

