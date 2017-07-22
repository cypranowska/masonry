# masonry
Inception model retrained to recognize construction site images

Retrieve bing image search results by running `create-im-lib.py`:

```
python create_im_lib.py <api-key> <query> <count> <offset> [<output-dir> (optional)]
```
* `<api-key>` is the API key to access bing image search. [Get a 30-day free
  trial key](https://azure.microsoft.com/en-us/try/cognitive-services/?api=bing-image-search-api).
* `<query>` is the search string to use to fetch images.
* `<count>` is the number of images to fetch.
* `<offset>` is the offset in the search results to start retrieving images.
(That is, skip the first `<offset>` images in the result.)
* `<output-dir>` is the location to save the image files. If omitted, save
  in the current directory. Images are saved with the filename
  `img_###.jpeg`.
