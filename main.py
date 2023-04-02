from flask import Flask, request, make_response
import urllib.parse
import urllib.request
import re

app = Flask(__name__)

@app.route('/filter_m3u')
def filter_m3u():
    url = request.args.get('url')
    text = request.args.get('text')

    if url is None:
        return 'Debe proporcionar una URL m3u'
    elif text is None:
        return 'Debe proporcionar un texto de búsqueda'


    # Leer el archivo m3u y filtrar los elementos según los parámetros en EXTINF
    filtered_m3u = '#EXTM3U\n'
    with urllib.request.urlopen(urllib.parse.unquote(url)) as response:
        data = response.read().decode('utf-8')
        lines = data.split('\n')
        for i, line in enumerate(lines):
            if '#EXTINF' in line and urllib.parse.unquote(text) in line:
                # Si la línea contiene parámetros en EXTINF y el texto buscado, agregarla al archivo filtrado
                tvg_id = line.split('tvg-id="')[1].split('"')[0]
                tvg_name = line.split('tvg-name="')[1].split('"')[0]
                
                line = line.replace("tvg-id=\"{}\"".format(tvg_id), "tvg-id=\"{}\"".format(tvg_name))
                filtered_m3u += line + '\n'

                if i + 1 < len(lines):
                    # Si hay una siguiente línea, que se asume que es la URL, agregarla también al archivo filtrado
                    filtered_m3u += lines[i+1] + '\n'

    # Crear la respuesta y agregar el encabezado
    response = filtered_m3u
    #response = make_response(filtered_m3u)
    #response.headers['Content-Type'] = 'application/vnd.apple.mpegurl'

    # Devolver la respuesta
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5001)
