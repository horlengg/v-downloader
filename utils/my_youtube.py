from pytubefix import YouTube
import io

# po_token = "MnRp5wZIkhLGJGnfJ9yjIuIbWlhzb5I_l48uhmuPXUD1LmZ7U3Z_IZxd1H_SgjOvecMlAT3SebFFdFwPoXpHDasHCXeMxXGan51xVa06tVoeBFmcZtlxmXoawvM2JcGNs_gkLtUhBZ5HSkDMBCluBqw1qQYs7Q"
# visitor_data = "CgtYNldyZW9LWWdQayiEpZu5BjIKCgJLSBIEGgAgWw"

# po_token_verifier = {
#     "po_token": po_token,
#     "visitor_data": visitor_data
# }

class MyYoutube :
    def __init__(self , url):
        self.yt = YouTube(url, use_po_token=True)
        self.url = url
        self.resolutions = []
        self.audio_list = []
        self.thumbnail = ""
        self.title = ""
        self.description = ""
        self.duration = "00:00s"
    def process_streams(self):
        self.thumbnail = self.yt.thumbnail_url
        self.title = self.yt.title
        self.description = self.yt.description
        self.duration = self.get_video_duration()
        for stream in self.yt.streams.filter(only_video=True):
            if stream.mime_type == "video/mp4" and stream.resolution:
                if stream.resolution in [res["resolution"] for res in self.resolutions]:
                    continue
                resolution = stream.resolution 
                file_size = stream.filesize / (1024 * 1024)  # Convert bytes to MB
                self.resolutions.append({
                    "resolution": resolution,
                    "size": f"{file_size:.2f}MB",
                    "itag" : stream.itag,
                    "url" : f"/download?url={self.url}&itag={stream.itag}"
                })
        self.generate_audio()
    def generate_audio(self):
        audio = self.yt.streams.get_audio_only()
        if audio is None: 
            return
        for stream in self.yt.streams.filter(only_audio=True):
            if stream.itag in [res["itag"] for res in self.audio_list]:
                    continue
            file_size = stream.filesize / (1024 * 1024)
            self.audio_list.append({
                "abr" : stream.abr,
                "size" : f"{file_size:.2f}MB",
                "itag" : stream.itag,
                "url" : f"/download?url={self.url}&itag={stream.itag}"
            })
    def get_stream(self,itag:str) :
        return self.yt.streams.get_by_itag(itag)
    
    def get_file_blob(self,stream) :
        try :
            video_blob = io.BytesIO()
            stream.stream_to_buffer(video_blob)
            video_blob.seek(0)
            return video_blob
        except Exception as e :
            print(e)
    
    def get_video_duration(self):
        if self.yt is not None:
            duration_seconds = self.yt.length
            # Format the duration into HH:MM:SS
            hours = duration_seconds // 3600
            minutes = (duration_seconds % 3600) // 60
            seconds = duration_seconds % 60
            
            # Construct the duration string
            if hours > 0:
                duration = f"{hours:02}:{minutes:02}:{seconds:02}s"
            else:
                duration = f"{minutes:02}:{seconds:02}s"
                
            return duration
        else:
            return None