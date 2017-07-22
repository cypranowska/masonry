import http.client, urllib.request, urllib.parse, urllib.error, base64, json, time, sys, os.path

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'

def im_search(keyword,count,offset,api_key):
    headers = {
        'Content-Type': 'multipart/form-data',
        'Ocp-Apim-Subscription-Key': api_key,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }

    params = urllib.parse.urlencode({
        'q': keyword,
        'count': count,
        'offset': offset,
    })

    try:
        conn = http.client.HTTPSConnection('api.cognitive.microsoft.com')
        conn.request("GET", "/bing/v5.0/images/search?%s" % params, "{body}", headers)
        response = conn.getresponse()
        rawdata = response.read().decode('utf-8')
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    
    data = json.loads(rawdata)
    
    with open(str(keyword)+'.json', 'w') as outfile:
        json.dump(data, outfile)
    
    return data

#Call this at your own risk
def download_im(data, offset=0):
    url_list = [val['contentUrl'] for val in data['value']]
    im_format = [val['encodingFormat'] for val in data['value']]
    
    im_url = []
    
    for j in range(len(url_list)):
        parsed = urllib.parse.parse_qs(urllib.parse.urlparse(url_list[j]).query)
        im_url.append(parsed['r'][0]) 

    for i in range(len(url_list)): 
        if (im_format[i] == 'jpeg' or im_format[i] == 'jpg' or im_format == 'png'):
            filename = outputdir + 'img_00' + str(i+offset) + '.' + im_format[i]
            print("Saving %s..." % filename)
            try:
                req = urllib.request.Request(im_url[i], headers={'User-Agent': user_agent})
                img = urllib.request.urlopen(req)
                output = open(filename, "wb")
                output.write(img.read())
                output.close()
                time.sleep(2)
            except urllib.error.HTTPError as e:
                print(e.code)
                pass
            except urllib.error.URLError as e:
                print(e.reason)
                pass
            except urllib.request.ssl.CertificateError as e:
                print (e)
                pass

    print('Offset to add to count:', data["nextOffsetAddCount"])

if len(sys.argv) < 5:
    print("Usage: python create_im_lib.py <api-key> <query> <count> <offset> [<output-dir>] (optional)")
    sys.exit(2)

apikey = sys.argv[1]
query = sys.argv[2]
count = int(sys.argv[3])
offset = int(sys.argv[4])

if len(sys.argv) > 5:
    outputdir = sys.argv[5] + "/"
else:
    outputdir = "" # current directory

if not os.path.exists(outputdir):
    os.makedirs(outputdir)

print("Querying for image URLs...")
data = im_search(query, count, offset, apikey)
print("Downloading images...")
download_im(data, offset)
