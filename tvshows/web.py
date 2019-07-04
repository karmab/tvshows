from flask import Flask, render_template, request, jsonify
from kubernetes import client, config
import os
from random import choice
from tvshows.tvdbhelper import get_image
app = Flask(__name__)
port = os.environ.get('PORT', 9000)
debug = bool(os.environ.get('DEBUG', True))
db = os.environ.get('DB_NAME', 'tvshows')
host = os.environ.get('DB_HOST', '127.0.0.1')
user = os.environ.get('DB_USER', 'dbadmin')
password = os.environ.get('DB_PASSWORD', 'dbadmin')

DOMAIN = 'kool.karmalabs.com'
VERSION = 'v1'
NAMESPACE = os.environ['TVSHOWS_NAMESPACE'] if 'TVSHOWS_NAMESPACE' in os.environ else 'metal3'


def browse_tvshows():
    results = []
    crds = client.CustomObjectsApi()
    tvshows = crds.list_cluster_custom_object(DOMAIN, VERSION, 'tvshows')["items"]
    for tvshow in tvshows:
        name = tvshow.get("metadata")["name"]
        print("Parsing %s" % name)
        finale = choice(tvshow.get("spec")["finales"])
        if "image" not in tvshow.get("spec") or tvshow.get("spec")["image"] == '':
            image = get_image(name.replace('_', ' '))
            print("Found image %s for %s" % (image, name))
            tvshow["spec"]["image"] = image
            crds.replace_namespaced_custom_object(DOMAIN, "v1", NAMESPACE, "tvshows", name, tvshow)
            print("Handled image for %s" % name)
        else:
            image = tvshow.get("spec")["image"]
        results.append({'name': name, 'finale': finale, 'image': image})
    return results


@app.route('/')
def index():
    return render_template('index.html', content_type='application/json')


@app.route('/tvshows')
def list_tvshows():
    """

    :return:
    """
    tvshows = browse_tvshows()
    return render_template('tvshows.html', tvshows=tvshows, content_type='application/json')


@app.route('/new', methods=['POST'])
def add_tvshow():
    name = request.form['name'].lower()
    finale = request.form['finale']
    crds = client.CustomObjectsApi()
    tvshows = crds.list_cluster_custom_object(DOMAIN, VERSION, 'tvshows')["items"]
    exist = False
    for tvshow in tvshows:
        tvshowname = tvshow.get("metadata")["name"]
        if tvshowname == name:
            tvshow.get("spec")["finales"].append(finale)
            crds.replace_namespaced_custom_object(DOMAIN, "v1", NAMESPACE, "tvshows", name, tvshow)
            result = {'result': 'success'}
            exist = True
            break
    if not exist:
        body = {'kind': 'Tvshow', 'spec': {'finales': [finale]}, 'apiVersion': '%s/%s' % (DOMAIN, VERSION),
                'metadata': {'name': name, 'namespace': NAMESPACE}}
        try:
            crds.create_namespaced_custom_object(DOMAIN, VERSION, NAMESPACE, 'tvshows', body)
            result = {'result': 'success'}
        except Exception as e:
            message = [x.split(':')[1] for x in e.body.split(',') if 'message' in x][0].replace('"', '')
            result = {'result': 'failure', 'reason': message}
    response = jsonify(result)
    return response


@app.route('/delete', methods=['POST'])
def delete_tvshow():
    name = request.form['name']
    crds = client.CustomObjectsApi()
    try:
        crds.delete_namespaced_custom_object(DOMAIN, VERSION, NAMESPACE, 'tvshows', name, client.V1DeleteOptions())
        result = {'result': 'success'}
    except Exception as e:
        message = [x.split(':')[1] for x in e.body.split(',') if 'message' in x][0].replace('"', '')
        result = {'result': 'failure', 'reason': message}
    response = jsonify(result)
    return response


def run():
    """

    """
    app.run(host='0.0.0.0', port=port, debug=debug)


if __name__ == '__main__':
    if 'KUBERNETES_PORT' in os.environ:
        config.load_incluster_config()
    elif 'KUBECONFIG' in os.environ and os.path.exists(os.environ['KUBECONFIG']):
        kubeconfigfile = os.environ['KUBECONFIG']
        config.new_client_from_config(config_file=kubeconfigfile)
    else:
        config.load_kube_config()
    run()
