import re
from flask_app import app
from flask import render_template,redirect,request,flash,session
from flask_app.models.painting import Painting

@app.route("/paintings")
def user():
    if(session):
        paintings = Painting.get_all_paintings()
        data={
            "user_id":session["user_id"]
        }
        purchpaintings = Painting.get_all_purchpaintings(data)
        print(purchpaintings)
        return render_template("paintings.html", paintings=paintings,purchpaintings=purchpaintings)
    else:
        return redirect("/")

@app.route("/painting/create")
def create_painting():
    if(session):        
        return render_template("addPainting.html")
    else:
        return redirect("/")

@app.route("/painting/createpainting", methods=["POST"])
def create_painting_db():
    if(session): 
        if not Painting.validate_painting(request.form):
            return redirect("/painting/create")    

        data = {
            "title": request.form["title"],
            "description": request.form["description"],
            "price": request.form["price"],
            "quantity": request.form["quantity"],
            "user_id":session["user_id"]
        }
        Painting.create_painting(data)
        return redirect("/paintings")
    else:
        return redirect("/")

@app.route("/painting/view/<int:id>")
def painting_view(id):
    if(session): 
        data = {
            "painting_id":id
        }
        painting = Painting.view_painting(data)
        num_purchased = list(Painting.count_purchased(data))
        print(f"I AM NUM PURCHASED {num_purchased}")
        return render_template("paintingInfo.html",painting=painting,num_purchased=num_purchased)
    else:
        return redirect("/")

@app.route("/painting/edit/<int:id>")
def painting_edit(id):
    if(session): 
        session["painting_id"] = id
        data = {
            "painting_id":id
        }
        painting = Painting.view_painting(data)
        return render_template("editPainting.html", painting=painting)
    else:
        return redirect("/")


@app.route("/painting/editpainting/<int:id>", methods=["POST"])
def painting_edit_db(id):
    
    if(session):

        if not Painting.validate_painting(request.form):
            return redirect(f"/painting/edit/{session['painting_id']}")   

        data = {
            "title": request.form["title"],
            "description": request.form["description"],
            "price": int(request.form["price"]),
            "user_id":session["user_id"],
            "quantity":request.form["quantity"],
            "painting_id":id
        }
        print(f"painting id is {data['painting_id']}")
        Painting.edit_painting(data)
        return redirect("/paintings")
    else:
        return redirect("/")

@app.route("/painting/delete/<int:id>")
def painting_delete(id):
    if(session): 
        data = {
            "painting_id":id
        }
        Painting.delete_painting(data)
        return redirect("/paintings")
    else:
        return redirect("/")

@app.route("/painting/buy/<int:id>")
def painting_buy(id):
    if(session): 
        data = {
            "painting_id":id,
            "user_id":session["user_id"]
        }
        Painting.buy_painting(data)
        return redirect("/paintings")
    else:
        return redirect("/")
