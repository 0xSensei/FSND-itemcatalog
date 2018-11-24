from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Catalog, CatalogItem, User
from flask import session as login_session
import random
import string
import os
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

APPLICATION_NAME = "Items Catalog"

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/catalog/')
def showcatalogs():
    catalogs = session.query(Catalog).order_by(asc(Catalog.name))
    items = session.query(CatalogItem).order_by(CatalogItem.id.desc()) \
        .limit(12).all()
    return render_template('catalogs.html', catalogs=catalogs, items=items,
                           login_session=login_session)


@app.route('/catalog/JSON')
def showcatalogs_js():
    catalogs = session.query(Catalog).order_by(asc(Catalog.name))
    return jsonify(catalogs=[catalog.serialize for catalog in catalogs])


@app.route('/catalog/<string:catalog_name>/')
@app.route('/catalog/<string:catalog_name>/items/')
def showitems(catalog_name):
    """
    docstring here
        :param catalog_name: 
    returns:
        a list of items based on the catalog name given and a list of catalogs to enhance user experince
    """
    print catalog_name
    catalog = session.query(Catalog).filter_by(name=catalog_name).one()
    catalogs = session.query(Catalog).order_by(asc(Catalog.name))
    items = session.query(CatalogItem).filter_by(
        catalog_id=catalog.id).all()
    return render_template('catalog.html', items=items, catalogs=catalogs)


@app.route('/catalog/<string:catalog_name>/JSON')
def showitems_js(catalog_name):
    """
    docstring here
        :param catalog_name: 
    returns:
        a list of items in json format
    """
    catalog = session.query(Catalog).filter_by(name=catalog_name).one()
    items = session.query(CatalogItem).filter_by(
        catalog_id=catalog.id).all()
    return jsonify(items=[i.serialize for i in items])


@app.route('/catalog/<string:catalog_name>/<string:item_name>')
def showitem(catalog_name, item_name):
    """
    docstring here
        :param catalog_name: 
        :param item_name: 
    returns:
        return the item object, based on the input for the item name
    """
    catalog = session.query(Catalog).filter_by(name=catalog_name).one()
    item = session.query(CatalogItem).filter_by(name=item_name).one()
    return render_template('item.html', item=item)


@app.route('/catalog/<string:catalog_name>/<string:item_name>/JSON')
def showitem_js(catalog_name, item_name):
    catalog = session.query(Catalog).filter_by(name=catalog_name).one()
    item = session.query(CatalogItem).filter_by(name=item_name,
                                                catalog=catalog).one()

    return jsonify(item.serialize)


@app.route('/catalog/item/new', methods=['GET', 'POST'])
def addItem():
    """
    docstring here
        input POST:
            csrf: will be used to prevent csrf attack
            form[name]: the item name to be added, must be unique
            form[description]: the item description to be added, could be None
            form[catalog]: the catalog name to be added, cannot be null
            files[file]: the image associate with the item, could be None
        Notes:
            the user must be authenticated to perform such actions
        
    """
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == "POST":
        print request.form['csrf'] == login_session['csrf']
        if request.form['csrf'] != login_session['csrf']:
                return "CSRF attack attempted"
        item = CatalogItem()
        if request.form['name']:
            item.name = request.form['name']
        else:
            flash('No item name provided')
            return redirect(request.url)
        if request.form['description']:
            item.description = request.form['description']
        if request.form['catalog']:
            catalog = request.form['catalog']
            item.catalog = session.query(Catalog).filter_by(name=catalog).one()
        if 'file' not in request.files:
            item.picture_name = None
        else:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = csrf() + filename
                file.save(os.path.join(app.static_folder, filename))
                item.picture_name = filename
        item.user_id = login_session['user_id']
        session.add(item)
        session.commit()
        return redirect('/')
    csrfd = csrf()
    login_session['csrf'] = csrfd
    catalogs = session.query(Catalog).order_by(asc(Catalog.name))
    return render_template('newitem.html', catalogs=catalogs, csrf=csrfd)


@app.route('/catalog/<string:item_name>/edit', methods=['GET', 'POST'])
def editItem(item_name):
    """
    docstring here
        input POST:
            csrf: will be used to prevent csrf attack
            form[name]: the item name to be added, must be unique
            form[description]: the item description to be added, could be None
            form[catalog]: the catalog name to be added, cannot be null
            files[file]: the image associate with the item, could be None
        Notes:
            the user must be authenticated to perform such actions, and must be authorized which means he is the one created the item.
        
    """
    if 'username' not in login_session:
        return redirect('/login')
    item = session.query(CatalogItem).filter_by(name=item_name).one()
    if item.user_id != login_session['user_id']:
        flash("you can't edit others items ")
        return redirect('/')

    if request.method == "POST":
        print request.form['csrf'] == login_session['csrf']
        if request.form['csrf'] != login_session['csrf']:
                return "CSRF attack attempted"
        if request.form['name']:
            item.name = request.form['name']
        else:
            flash('No item name provided')
            return redirect(request.url)
        if request.form['description']:
            item.description = request.form['description']
        if request.form['catalog']:
            catalog = request.form['catalog']
            item.catalog = session.query(Catalog).filter_by(name=Catalog).one()
        if 'file' not in request.files:
            item.picture_name = None
        else:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = csrf() + filename
                file.save(os.path.join(app.static_folder, filename))
                item.picture_name = filename
        session.add(item)
        session.commit()
        return redirect('/')
    csrfd = csrf()
    login_session['csrf'] = csrfd
    catalogs = session.query(Catalog).order_by(asc(Catalog.name))

    return render_template('edititem.html', catalogs=catalogs, csrf=csrfd,
                           item=item)


@app.route('/catalog/<string:item_name>/delete', methods=['GET', 'POST'])
def deleteItem(item_name):
    """
    docstring here
        args:
            item_name: item name to be deleted
        input POST:
            csrf: will be used to prevent csrf attack
        Notes:
            the user must be authenticated to perform such actions, and must be authorized which means he is the one created the item.
        
    """
    if 'username' not in login_session:
        return redirect('/login')
    item = session.query(CatalogItem).filter_by(name=item_name).one()
    if item.user_id != login_session['user_id']:
        flash("you can't delete others items ")
        return redirect('/')

    if request.method == "POST":
        print request.form['csrf'] == login_session['csrf']
        if request.form['csrf'] != login_session['csrf']:
                return "CSRF attack attempted"
        session.delete(item)
        session.commit()
        return redirect('/')
    csrfd = csrf()
    login_session['csrf'] = csrfd
    catalogs = session.query(Catalog).order_by(asc(Catalog.name))
    return render_template('deleteitem.html', csrf=csrfd, item=item)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg', 'gif']


@app.route('/login')
def showLogin():
    """
    docstring here
    return:
        a login page for google oauth filled with csrf token for anti forgery
    """
    state = csrf()
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """
    docstring here
    return:
       will handle the user authntication into google using the code recived during login, will populate a user session if logged on and add him to database for new user
    """
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/disconnect')
def disconnect():
    """
    docstring here
    return:
        clear a user session and log him out.
    """
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showcatalogs'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showcatalogs'))


@app.route('/catalog.json')
def catalogJson():
    """
    docstring here
    return:
       a list of all categories and associated item in json format
    """
    catalogs = session.query(Catalog).order_by(asc(Catalog.name))

    category = []
    for i, catalog in enumerate(catalogs):
        category.append(catalog.serialize)
        items = session.query(CatalogItem).filter_by(
            catalog_id=catalog.id).all()
        for aa in items:
            category[i]['items'].append(aa.serialize)
        print category

    return jsonify(category=category)


def createUser(login_session):
    """
    docstring here
    return:
      create a new user based on the session data that was saved during google connect
    """
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception as e:
        return None


def csrf():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    return state


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


if __name__ == '__main__':
    app.secret_key = 'laksdlkajsdlkjasdlkjalksdnlkansdlnasdkanlsdknaslkdn'
    app.debug = True
    app.run(host='localhost', port=int(os.environ.get('PORT', 5000)))
