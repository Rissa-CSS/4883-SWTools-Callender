import youtube_dl

def downloadVid(url,name,extension):
    '''
    ext = extension
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(title)s.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',}],})

    
    with ydl:
        result = ydl.download([url])

    if 'entries' in result:
        # Can be a playlist or a list of videos
        video = result['entries'][0]
    else:
        # Just a video
        video = result
    
  
    ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',}],
        }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    '''


    ydl_opts = {
        'format': 'bestaudio/best',       
        'outtmpl': '%s.mp3'%(name),        
        'noplaylist' : True, 
        }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
downloadVid('https://www.youtube.com/watch?v=P88dK4BRYN4','Got Your Back','mp3')
'''
def downloadURL(url, preferredCodec=None, preferredQuality=None):
    """ Downloads song using youtube_dl and the song's youtube
    url.
    """
    #codec, quality = getCodecAndQuality()

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': preferredCodec,
            'preferredquality':preferredQuality,
        },
            {'key': 'FFmpegMetadata'},
        ],
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=True)
    except:
        print("Problem downloading " + url)
    return None 

downloadURL("https://www.youtube.com/watch?v=eCxaXqwRhvw")
'''