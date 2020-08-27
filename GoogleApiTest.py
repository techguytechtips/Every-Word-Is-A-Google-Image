from google_images_search import GoogleImagesSearch
googletoken = open("GoogleToken.txt", "r").read().split()
geniustoken = open("GeniusToken.txt", "r")
gAPI = GoogleImagesSearch(googletoken[0], googletoken[1])
arr = ["test", "Hey", "Heavy", "Godzilla", "Example"]
i = 0
_search_params = {
        'q': arr[i],
        'fileType': 'jpg',
        'imgType': 'photo',
        'num': 1,
    }
for word in arr:
    _search_params['q'] = arr[i]
    try:
        gAPI.search(search_params=_search_params, path_to_dir="ImageCache", custom_image_name=str(i))
    except Exception as e:
        print(e)
    i += 1