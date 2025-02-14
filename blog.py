from flask import Flask, render_template, redirect, abort, request, jsonify
import json

app = Flask(__name__)

@app.route("/")
def index():
    return redirect("home")

@app.route("/home")
def home():
    titles = post_get_title()
    dates = post_get_date()
    post_id = post_get_id()
    posts = list(zip(titles,dates,post_id))
    return render_template("home.html",posts=posts)

@app.route("/admin/home")
def admin_home():
    titles = post_get_title()
    dates = post_get_date()
    post_id = post_get_id()
    posts = list(zip(titles,dates,post_id))
    return render_template("admin_home.html",posts=posts)

@app.route("/post/<string:post_id>")
def show_post(post_id):
    with open("saved_posts_json/posts.json", "r", encoding="utf-8") as saved_posts:
        posts_data = json.load(saved_posts) 
        for post in posts_data["posts"]:
            if post["post_id"] == post_id:
                return render_template("post.html",title=post["title"],date=post_get_date(post_id),content=post["content"])
        abort(404)

@app.route("/admin/new_post")
def new_post():
    return render_template("new_post.html")

@app.route("/404")
def redirect404():
    return render_template("new_post.html")

@app.route("/admin/edit/<string:post_id>")
def edit_post(post_id):
    with open("saved_posts_json/posts.json", "r", encoding="utf-8") as saved_posts:
        posts_data = json.load(saved_posts) 
        for post in posts_data["posts"]:
            day = post["date"]["day"]
            month = post["date"]["month"]
            year = post["date"]["year"]
            formated_date = (f"{year}-{month}-{day}")
            if post["post_id"] == post_id:
                return render_template("edit_post.html",post_id = post_id,title=post["title"],date=formated_date,content=post["content"])
        abort(404)

@app.route("/admin/new_post", methods=["POST"])
def save_post(post_id = None):
    try:
        title = request.form.get("title")
        date = request.form.get("date")
        content = request.form.get("post_area")

        if not title or not date or not content:
            return jsonify({"error":"Faltando parametros obrigatorios"}), 400

        with open("saved_posts_json/posts.json", "r", encoding="utf-8") as saved_posts:
            posts_data = json.load(saved_posts) 
            year = date[:4]
            month = date[5:7]
            day = date[8:10]
            new_post = {
                "post_id": str(len(posts_data["posts"]) + 1) ,
                "title": title,
                "date": {
                    "day": day,
                    "month": month,
                    "year": year
                },
                "content": content
            } 
            posts_data["posts"].append(new_post)
            with open("saved_posts_json/posts.json", "w", encoding="utf-8") as saved_json:
                json.dump(posts_data, saved_json, ensure_ascii=False, indent=4)
        return jsonify({"message": "Post salvo com sucesso"}), 200
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({"error": "Erro ao salvar post..."}), 500

@app.route("/admin/edit/<string:post_id>", methods=["POST"])
def edit_post_save(post_id):
    post_id = post_id.strip()

    try:
        title = request.form.get("title")
        date = request.form.get("date")
        content = request.form.get("post_area")

        if not title or not date or not content:
            return jsonify({"error":"Faltando parametros obrigatorios"}), 400

        delete_json_data(post_id)

        with open("saved_posts_json/posts.json", "r", encoding="utf-8") as saved_posts:
            posts_data = json.load(saved_posts) 
            year = date[:4]
            month = date[5:7]
            day = date[8:10]
            new_post = {
                "post_id": post_id ,
                "title": title,
                "date": {
                    "day": day,
                    "month": month,
                    "year": year
                },
                "content": content
            } 
            posts_data["posts"].append(new_post)
            with open("saved_posts_json/posts.json", "w", encoding="utf-8") as saved_json:
                json.dump(posts_data, saved_json, ensure_ascii=False, indent=4)
        sort_jsons()
        return jsonify({"message": "Post salvo com sucesso"}), 200
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({"error": "Erro ao salvar post..."}), 500

@app.route("/admin/delete/<string:post_id>")
def delete_json_data_redirect(post_id):
    post_id = post_id.strip()
    delete_json_data(post_id)

    return redirect("/admin/home"), 200
    
def post_get_title():
    posts_titles = []
    with open("saved_posts_json/posts.json", "r", encoding="utf-8") as saved_posts:
        posts_data = json.load(saved_posts) 
        
        for post in posts_data["posts"]: 
            posts_titles.append(post["title"])

    return posts_titles

def post_get_date(post_id=None):
    meses_do_ano = {
    "01": "Janeiro",
    "02": "Fevereiro",
    "03": "Março",
    "04": "Abril",
    "05": "Maio",
    "06": "Junho",
    "07": "Julho",
    "08": "Agosto",
    "09": "Setembro",
    "10": "Outubro",
    "11": "Novembro",
    "12": "Dezembro"
    }
    formated_dates = [] 

    with open("saved_posts_json/posts.json", "r", encoding="utf-8") as saved_posts:
        posts_data = json.load(saved_posts)

        if post_id is None:
            for post in posts_data["posts"]:
                day = post["date"]["day"]
                month = post["date"]["month"]
                year = post["date"]["year"]
                formated_dates.append(f"{day} de {meses_do_ano[month]} de {year}")

            return formated_dates
        else:
            for post in posts_data["posts"]:
                if post["post_id"] == post_id:
                    day = post["date"]["day"]
                    month = post["date"]["month"]
                    year = post["date"]["year"]
                    formated_date = (f"{day} de {meses_do_ano[month]} de {year}")
                    return formated_date
            return f"Error ao encontrar data..."

def post_get_id():
    post_id_list = []
    with open("saved_posts_json/posts.json", "r", encoding="utf-8") as saved_posts:
        posts_data = json.load(saved_posts)

        for post in posts_data["posts"]:
            post_id_list.append(post["post_id"])
    return post_id_list
            

def delete_json_data(post_id):
    new_data = []
    with open("saved_posts_json/posts.json", "r", encoding="utf-8") as saved_posts:
        posts_data = json.load(saved_posts) 

        for entry in posts_data["posts"]:
            if str(entry["post_id"]) != str(post_id):
                new_data.append(entry)
        
        posts_data["posts"] = new_data

        with open("saved_posts_json/posts.json", "w", encoding="utf-8") as saved_json:
            json.dump(posts_data, saved_json, ensure_ascii=False, indent=4)
        sort_jsons()

def sort_jsons():
    with open("saved_posts_json/posts.json", "r", encoding="utf-8") as saved_posts:
        posts_data = json.load(saved_posts) 
        posts_data["posts"] = sorted(posts_data["posts"], key=lambda x: int(x["post_id"]), reverse=False)

        with open("saved_posts_json/posts.json", "w", encoding="utf-8") as saved_json:
            json.dump(posts_data, saved_json, ensure_ascii=False, indent=4)
            
if __name__ == ("__main__"):
    app.run()
#editar "home.html" e "admin/home.html" para invez de loop.index utilizar o id do prorpio post