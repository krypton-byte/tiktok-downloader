### START OF FILE ###
### ================================================================================= ###
# Tikmate DOES NOT WORK, got error below: #
# TypeError: Tikmate.__init__() takes 1 positional argument but 2 were given #

# Proof: (uncomment 3 lines code below)
# from tiktok_downloader import Tikmate
# d=Tikmate("https://www.tiktok.com/@khaby.lame/video/7223746480698330394?lang=en")
# d[0].download('video.mp4')

### ================================================================================= ###

# TTDownloader DOES NOT WORK, got error below: #
# requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0) #

# Proof: (uncomment 3 lines code below)
# from tiktok_downloader import VideoInfo
# d=VideoInfo.service('https://www.tiktok.com/@khaby.lame/video/7223746480698330394?lang=en')
# d[0].download('video-TIKTOK.mp4')

### ================================================================================ ###

# Get Info DOES NOT WORK, got error below: #
# requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0) #

# Proof: (uncomment 3 lines code below)
# from tiktok_downloader import VideoInfo
# d = VideoInfo.get_info('https://www.tiktok.com/@khaby.lame/video/7223746480698330394?lang=en')
# print(d)

### ================================================================================ ###
### END OF FILE ###