from flask import Flask, render_template,request,redirect,jsonify,send_file
from utils import MyYoutube

app = Flask(__name__)


@app.route('/')
def home():
    return redirect(location="/explore")

@app.route('/explore',methods=['GET','POST'])
def explore():
    if request.method == 'GET':
        return render_template('Explore.html',data=None)
    elif request.method == 'POST':
        link_url = request.form.get('link_url')
        try:
            if not link_url :
                msg = {
                    "msg" : "Link url is required!.",
                    "to" : "/",
                    "buttonTitle" : "Back to Home"
                }
                return render_template("Message.html",data=msg)
            elif not "https://youtu.be" in link_url :
                msg = {
                    "msg" : "Appologize, Currently we support YouTube videos only!.",
                    "to" : "/",
                    "buttonTitle" : "Back to Home"
                }
                return render_template("Message.html",data=msg)
            video = MyYoutube(url=link_url)
            video.process_streams()
            data = {
                "title" : video.title,
                "thumbnail" : video.thumbnail,
                "duration" : video.duration,
                "resolution_list" : video.resolutions,
                "audio_list" : video.audio_list,
                "url" : link_url,
            }
            
            return render_template("Explore.html",data=data)
        except Exception as e:
            data = {
                "msg" : str(e),
                "to" : "/",
                "buttonTitle" : "Back to Home"
            }
            return render_template("Message.html",data=data)

    

@app.route('/download', methods=['POST'])
def download():
    video_url = request.args.get('url')
    video_itag = request.args.get('itag')
    if video_itag is None or video_url is None:
        data = {
            "msg" : "Missing video itag or url",
            "to" : "/",
            "buttonTitle" : "Back to Home"
        }
        return render_template("Message.html",data=data)
    try:
        video = MyYoutube(url=video_url)
        video.process_streams()
        stream = video.get_stream(itag=video_itag)
        blob_file = video.get_file_blob(stream)
        file_name = video.title.strip()
        mimetype = "video/mp4"
        if stream.type == "audio" :
            file_name += ".mp3"
            mimetype = "audio/mp3"
        else :
            file_name += ".mp4"
        return send_file(blob_file, as_attachment=False, download_name=file_name, mimetype=mimetype)
    except Exception as e:
        return jsonify({"error": str(e)}), 400



if __name__ == '__main__':
    app.run(debug=True)