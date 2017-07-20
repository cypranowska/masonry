import http.client, urllib.request, urllib.parse, urllib.error, base64, json, time
from urllib.request import Request, ssl
from urllib.error import URLError, HTTPError

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

# Parses out the image url from the bing url (contentUrl value from the json)
def parse_bing_url(contentUrl):
    query_dict = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(contentUrl).query))
    return query_dict['r']

##Call this at your own risk
def download_im(data):
    url_list = [val['contentUrl'] for val in data['value']]
    im_format = [val['encodingFormat'] for val in data['value']]
    
    for i in range(len(url_list)): 
        if (im_format[i] == 'jpeg' or im_format[i] == 'jpg' or im_format == 'png'):
            url = parse_bing_url(url_list[i])
            filename = 'img_00' + str(i) + '.' + im_format[i]
            print(url, filename) # for debugging
            
            try:
                req = urllib.request.Request(url, headers={'User-Agent':'Magic Browser'})
                img = urllib.request.urlopen(req)
                #img = urllib.request.urlopen(url_list[i])
                output = open(filename, "wb")
                output.write(img.read())
                output.close()
                time.sleep(2)
            except HTTPError as e:
                print(e.code)
            except URLError as e:
                print(e.reason)
            except ssl.CertificateError as e:
                print(e)

        else:
            pass
