PHOTOS_PREFIX = "/photos/mobilemegallery"

NAME = L('MobileMe Gallery')

BASE_URL = 'http://gallery.me.com/%s?webdav-method=truthget&feedfmt=json&depth=1'
ALBUM_URL = '%s?webdav-method=truthget&feedfmt=json&depth=1'

ART           = 'art-default.jpg'
ICON          = 'icon-default.png'

####################################################################################################

def Start():

    Plugin.AddPrefixHandler(PHOTOS_PREFIX, PhotosMainMenu, NAME, ICON, ART)

    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
    Plugin.AddViewGroup("Pictures", viewMode="Pictures", mediaType="items")

    MediaContainer.art = R(ART)
    MediaContainer.title1 = NAME
    DirectoryItem.thumb = R(ICON)

def PhotosMainMenu():

    dir = MediaContainer(viewGroup="List",noCache=True)
    dir.Append(Function(DirectoryItem(ParseGallery,"My Gallery",subtitle="Personal MobileMe gallery",thumb=R(ICON),art=R(ART)),query = Prefs['username']))
 
    dir.Append(Function(InputDirectoryItem(ParseGallery,"Search users","Search users",thumb=R(ICON),art=R(ART))))

    dir.Append(PrefsItem(title=L("Preferences"),subtile="",summary="",thumb=R(ICON)))

    return dir
    
def getThumb(url):
  try:
    data = HTTP.Request(url, cacheTime=CACHE_1WEEK).content
    return DataObject(data, 'image/jpeg')
  except:
    return Redirect(R(ICON))

def getBkgnd(url):
  try:
    data = HTTP.Request(url, cacheTime=CACHE_1WEEK).content
    return DataObject(data, 'image/jpeg')
  except:
    return Redirect(R(ART)) 
 
def ParseGallery(sender,query=None):
  if id == None:
    return MessageContainer("Error","Please enter a valid username in the Prefernce menu")
    
  dir = MediaContainer(viewGroup="List")
  try:
    JsonObject = JSON.ObjectFromURL(BASE_URL % query)
  except:
    return MessageContainer("Error","Please enter a valid username in the Prefernce menu")
  
  for album in JsonObject['records']:
    if album['type'] == 'Album' or album['type'] == 'ApertureAlbum':
      albumthumb = album['keyImagePath'].replace('#','/')+'/web.jpg'
      albumkey = album['keyImagePath'].replace('#','/')+'/large.jpg'
      dir.Append(Function(DirectoryItem(ParseAlbum,title = album['title']+' ('+str(album['numPhotos'])+')',subtitle=album['updated'],thumb=albumthumb, art=albumkey),id=album['url']))

  if Prefs['album_sort_order'] == "By Date Descending": 
    dir.Reverse()
  if Prefs['album_sort_order'] == "A to Z" or Prefs['album_sort_order'] == "Z to A": 
    dir.Sort('title')
  if Prefs['album_sort_order'] == "Z to A": 
    dir.Reverse()
  return dir
  
def ParseAlbum(sender,id):
  dir = MediaContainer(viewGroup="Pictures", art=sender.art)
  JsonObject = JSON.ObjectFromURL(ALBUM_URL % id)
  for pic in JsonObject['records']:
    if pic['type'] == 'Photo':
      try: 
        dir.Append(PhotoItem(pic['largeImageUrl'],title = pic['title'],subtitle=pic['photoDate'],thumb=pic['squareDerivativeUrl']))
      except:
        dir.Append(PhotoItem(pic['webImageUrl'],title = pic['title'],subtitle=pic['photoDate'],thumb=pic['squareDerivativeUrl']))
        
  if Prefs['photo_sort_order'] == "By Date Ascending": 
    dir.Sort('subtitle') 
  if Prefs['photo_sort_order'] == "By Date Descending": 
    dir.Sort('subtitle').Reverse()
  if Prefs['photo_sort_order'] == "A to Z": 
    dir.Sort('title')
  if Prefs['photo_sort_order'] == "Z to A": 
    dir.Sort('title').Reverse()      
  return dir

     
    
  
