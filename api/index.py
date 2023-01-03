from sanic import Sanic, response
from sanic.response import json, html, text
from models import myconn
#from jinja2 import Environment, PackageLoader, select_autoescape
import asyncio
#from tmbdapi import get_movie
import re
from datetime import datetime, timedelta
import pdb
from urllib.parse import urlparse, urlunsplit, unquote
from sanic_auth import Auth,User
from mywalet import gen_address,get_balans
#from psycopg2.errors import UniqueViolation,UndefinedFunction
from sanic_session import Session, InMemorySessionInterface
import qrcode
from aiohttp.client_exceptions import ClientConnectorError
from sanic_ext import render
#env = Environment(loader=PackageLoader('app', 'renders'),
                  #autoescape=select_autoescape(['html', 'xml', 'tpl']), enable_async=True)
import jinja2
app = Sanic(__name__)
app.config.AUTH_LOGIN_ENDPOINT = 'login'
session = InMemorySessionInterface(expiry=600)

@app.middleware('request')
async def add_session_to_request(request):
    await session.open(request)

auth = Auth(app)


app.static('/static', './static')

Session(app)

#async def render(tpl, **kwargs):

    #render = env.get_render(tpl)
    #content = await render.render_async(kwargs)
    #return html(content)


#async def temptext(tpl, **kwargs):

    #temptext = env.get_render(tpl)
    #content = await temptext.render_async(kwargs)
    #return text(content, content_type="application/xml")


@app.route('/search/', methods=['GET', 'POST'])
async def search(request):

    q = request.form.get('q')
    if q != None:

        conn = await myconn()

        value = await conn.fetch(f"SELECT COUNT(*) FROM rutor WHERE title LIKE '%{q}%'")
        rowsmy = await conn.fetch(f"SELECT * FROM rutor WHERE title  ILIKE '%{q}%' ORDER BY id LIMIT 200")
        total = value[0][0]
        await conn.close()
       
        content = await render('search.html', title='Sanic', total=total, rows=rowsmy)
        return content

@app.route('/login', methods=['GET', 'POST'])
async def login(request):
    try:
        if request.method == 'POST':
            conn = await  myconn()
            #cur = conn.cursor()
            username = request.form.get('username')
            password = request.form.get('password')
            print(username,"uuuuuuuuuuuuuuuuuuuuuuuuu")
           
            # fetch user from database
            #sql = '''SELECT * from usermy WHERE "username" = $1 and "password" = $2'''
            #await conn.execute('''SELECT * from usermy WHERE "username" = $1 and "password" = $2''',username,password)
            user = await conn.fetchrow('''SELECT * from usermy WHERE "username" = $1 and "password" = $2''',username,password)
            print("myuser",user)
            if user[4] == username and user[5] == password:
                print("+++++++++++++++++++++++++++")
                id = user[0]
                usern = user[4]
                user = User(id=id,name=username)
                auth.login_user(request,user)
                
                return response.redirect('/profile')

        return await render('login.html')

    except Exception as e:
        return await render('login.html',context={"error":"Неверный логин или пароль!"})
                   
    


@app.route('/register', methods=['GET','POST'])
async def register(request):
    try:
        if request.method == 'POST':
            conn = await  myconn()
            #cur = conn.cursor()
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            
              
            # execute the query
            #await conn.execute('SELECT count(*) from usermy;')
            results = await conn.fetchrow('SELECT count(*) from usermy;')
              
            print(results[0])
            await conn.execute('''INSERT INTO usermy(wallet,ordermy,email,username,password) VALUES($1,$2,$3,$4,$5)''',gen_address(results[0]+1),False,email,username,password)
            #conn.commit()
            await conn.close()
            return response.redirect("/profile")
        content = await render('register.html')
        return content
    except (AttributeError) as e:
        
        content = await render('register.html',error="Такой логин или емаил уже занят.")
        return content
            



@app.route('/logout')
@auth.login_required
async def logout(request):
    auth.logout_user(request)
    return response.redirect('/login')






@app.route('/profile')
@auth.login_required(user_keyword='user')
async def profile(request,user):
    conn= await myconn()
    #cur=conn.cursor()
    #await conn.execute('''SELECT * from usermy WHERE username=$1''',user.name)
    myorder = await conn.fetchrow('''SELECT * from usermy WHERE username=$1''',user.name)
    img = qrcode.make(myorder[1])
    
    img.save("static/qr/"+myorder[1] + ".png")

    request.ctx.session['user'] = myorder[4]
    request.ctx.session['ordermy'] = myorder[2]
    print(request.ctx.session['user'],
        request.ctx.session['ordermy'],"===================")
    balans = get_balans(myorder[1])
    if int(balans['balanse']) >= 5000:
        await conn.execute('''UPDATE usermy SET ordermy=$1,symma=$2 WHERE id =$3''',(True,balans['balanse'],myorder[0]))
        #conn.commit()
        await conn.close()

    content = await render("profile.html",context={"myorder":myorder,"balans":balans})
    return content




@app.route('/', methods=['GET', 'POST'])
async def index(request):

    offset = request.args.get('page')
    if offset:

        myint = int(offset + '0' + '0')
    else:
        offset = '0'
        myint = int(offset)
    try:
        conn = await myconn()

        value = await conn.fetch('SELECT COUNT(*) FROM rutor')

        rows = await conn.fetch('SELECT * FROM rutor ORDER BY id LIMIT 100 OFFSET $1', myint)
        total = value[0][0]
        await conn.close()

        return await render('index.html', context={"total":total, "rows":rows})
    except (OSError) as e:

        return await render('index.html')



@app.route('/<slug>')
async def detail(request, slug):
    
    try:
        print(request.ctx.session['ordermy'],"|||||||||||||||||||||||||||||")
        if request.ctx.session['ordermy']:
            ret = {}
            pattern = r'([А-Яа-я0-9].+?)([\/?\.?\(\)?\[\]?])'
            conn = await myconn()

            row = await conn.fetchrow('SELECT * FROM rutor WHERE info_hash = $1', slug)
            print("row",row)
            query = re.search(pattern, row['title']).group(1)
            print("query==", query)
            # try:

            #     vote_average, original_title, overview, poster_path = await get_movie(query)
                
            #     ret['nazvanie'] = original_title
            #     ret['vote'] = vote_average
            #     ret['opisanie'] = overview
            #     ret['image'] = poster_path
            #     print("ret",ret)
            #     content = await render('detail.html', row=row, ret=ret)
            #     #await conn.close()
            #     return content
            # except ClientConnectorError as e:
            #     content = await render('detail.html', row=row, ret=None)
            #     return content
            content = await render("detail.html",context={"row":row,"ret":None})
            return content

        else:
            return response.redirect("/login") 
    except KeyError as e:
        return response.redirect("/login")           


# sitemap dinamic

@app.route('/sitemap.xml', methods=['GET'])
async def sitemap(request):
    conn = await myconn()
    pages = []

    posts = await conn.fetch('SELECT * FROM rutor ORDER BY id LIMIT 10000')
    for post in posts:
        url = 'www.videofilms.cf' + \
            app.url_for('detail', slug=post['info_hash'])
        last_updated = post['updated']
        pages.append([url, last_updated])

    content = await render('sitemap.xml', pages=pages)

    return content


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, workers=4, debug=False, access_log=False)
