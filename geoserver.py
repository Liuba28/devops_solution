from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import requests
import geojson

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>Welcome!</h1><p>You have reached the Fatmap API GBDX Server Component.</p></body></html>")

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # extract geojson from payload
        self._set_headers()
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))

        # extract geojson data from request payload
        try:
            data = geojson.loads(self.data_string)
            with open("geopayload.geojson", "w") as outfile:
                geojson.dump(data, outfile)
        except Exception as e:
            # if payload not of geojson format, return 400
            print(e)
            self.send_error(400, "Payload is not of geojson format.")
            return

        # create viable payload for gbdx
        features = data['features']
        feature = features[0]
        geometry = feature.geometry
        coordinates = geometry.coordinates

        # variable for holding payload necessary for gbdx POST
        thin = {"type": "Polygon", "coordinates": coordinates}
        thin_json = json.dumps(thin)

        # retrieve access token
        access_token = get_gbdx_access_token()

        # send post request to gbdx server
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer " + access_token}
        r = requests.post("https://geobigdata.io/catalog/v2/search", data=thin_json, headers=headers)
        print(r.text)
        print(r.json())

        json_response = r.json()
        json_response_string = json.dumps(json_response)

        # TODO: if payload OK, return 200 OK
        self.send_response(200)
        self.wfile.write(json_response_string)

        return

def get_gbdx_access_token():
    username = "xxx"
    password = "xxx"
    api_key = "xxx"

    url = 'https://geobigdata.io/auth/v1/oauth/token/'
    headers = {"Authorization": "Basic " + api_key, "Content-Type": "application/x-www-form-urlencoded"}
    params = {"grant_type": "password", "username": username, "password": password}
    results = requests.post(url, headers=headers, data=params)

    if results.status_code == 200:
        return results.json()['access_token']
    else:
        print('Authentication failed')
        return null


def run(server_class=HTTPServer, handler_class=S, port=3004):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print ('Starting httpd on port ' + str(port) + ' ...')

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
