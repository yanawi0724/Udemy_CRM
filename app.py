from flask import render_template,request
from models import app,db,Customer,Item,Purchase,Purchase_detail
import sqlalchemy
from sqlalchemy import func
from datetime import datetime

#ページ遷移
# １．トップページ兼顧客登録ページ
@app.route("/")
def index():
    customers = Customer.query.all()
    return render_template("1_index.html",customers=customers)

# ２．商品管理ページ
@app.route("/item")
def item():
    items = Item.query.all()
    return render_template("2_item.html",items=items)

# ３．購入情報登録ページ
@app.route("/purchase")
def purchase():
    customers = Customer.query.all()
    items = Item.query.all()
    return render_template("3_purchase.html",customers=customers, items=items)

# ４．購入情報検索/分析ページ
@app.route("/purchase_data_statistics")
def purchase_data_statistics():
    joined_purchase_details = db.session.query(Purchase,Purchase_detail).join(Purchase_detail,Purchase.purchase_id==Purchase_detail.purchase_id).all()
    joined_purchase_details = db.session.query(Purchase,Purchase_detail,Customer).join(Purchase_detail,Purchase.purchase_id==Purchase_detail.purchase_id).join(Customer,Purchase.customer_id==Customer.customer_id).all()
    joined_purchase_details = db.session.query(Purchase,Purchase_detail,Customer,Item).join(Purchase_detail,Purchase.purchase_id==Purchase_detail.purchase_id).join(Customer,Purchase.customer_id==Customer.customer_id).join(Item,Purchase_detail.item_id==Item.item_id).all()
    customers = Customer.query.all()
    return render_template("4_purchase_data_statistics.html",joined_purchase_details=joined_purchase_details,customers=customers)

#機能系
#1-1.顧客登録
@app.route("/add_customer",methods=["GET","POST"])
def add_customer():
    customer_id = request.form["input-customer-id"]
    customer_name = request.form["input-customer-name"]
    age = int(request.form["input-age"])
    gender = request.form["input-gender"]
    customer = Customer(customer_id,customer_name,age,gender)
    

    try:
        db.session.add(customer)
        db.session.commit()
        return render_template("1-1_confirm_added_customer.html",customer=customer)
    # except Exception as e:
    except sqlalchemy.exc.IntegrityError:
        # db.session.rollback()  # ロールバックしてエラーを処理
        return render_template("error.html",customer=customer)
        # print(f"Error: {e}")
    print(customer_id)
    return customer_id

#1-2.性別で抽出
@app.route("/select_gender", methods=["POST"])
def select_gender():
    gender = request.form["input-gender2"]
    customers = Customer.query.filter(Customer.gender==gender).all()
    return render_template("1-2_result_select_gender.html",customers=customers)

#2-1.商品登録
@app.route("/add_item",methods=["GET","POST"])
def add_item():
    item_id = request.form["input-item-id"]
    item_name = request.form["input-item-name"]
    price = int(request.form["input-price"])
    item = Item(item_id,item_name,price)
    

    try:
        db.session.add(item)
        db.session.commit()
        return render_template("2-1_confirm_added_item.html",item=item)
    # except Exception as e:
    except sqlalchemy.exc.IntegrityError:
        # db.session.rollback()  # ロールバックしてエラーを処理
        return render_template("error.html",item=item)
        # print(f"Error: {e}")
    print(item_id)
    return item_id


#2-2.商品削除
@app.route("/delete_item",methods=["GET","POST"])
def delete_item():
    item_id = request.form["input-item-id"]
    item = Item.query.filter_by(item_id=item_id).first()   
    
    try:
        db.session.delete(item)
        db.session.commit()
        return render_template("2-2_confirm_deleted_item.html",item=item)
    # except Exception as e:
    except sqlalchemy.exc.IntegrityError:
        # db.session.rollback()  # ロールバックしてエラーを処理
        return render_template("error.html",item=item)
        # print(f"Error: {e}")
    print(item_id)
    return item_id

#2-3.商品更新
@app.route("/update_item",methods=["GET","POST"])
def update_item():
    item_id = request.form["input-item-id"]
    updated_item_name = request.form["input-item-name"]
    updated_price = request.form["input-item-price"]
    item = Item.query.filter_by(item_id=item_id).first()   
    
    try:
        item.item_name = updated_item_name
        item.price = updated_price
        db.session.add(item)
        db.session.commit()
        return render_template("2-3_confirm_updated_item.html",item=item)
    # except Exception as e:
    except sqlalchemy.exc.IntegrityError:
        # db.session.rollback()  # ロールバックしてエラーを処理
        return render_template("error.html",item=item)
        # print(f"Error: {e}")
    print(item_id)
    return item_id

#2-4.商品名で抽出
@app.route("/select_item_name",methods=["GET","POST"])
def select_item_name():
    item_name = request.form["input-item-name"]
    select_target = "%{}%".format(item_name)
    items = Item.query.filter(Item.item_name.like(select_target)).all()
    result_type = "抽出"

    return render_template("2-4_confirm_selected_item.html",items=items,result_type=result_type)

#2-5.単価で並べ替え
@app.route("/sorting_item",methods=["GET","POST"])
def sorting_item():
    order_type = request.form["order-type"]
    if order_type == "ascending":
        items = Item.query.order_by(Item.price).all()
    else:
        items = Item.query.order_by(Item.price.desc()).all()
    result_type = "並べ替え"
    return render_template("2-4_confirm_selected_item.html",items=items,result_type=result_type)

#3-1.購入情報登録
@app.route("/add_purchase",methods=["GET","POST"])
def add_purchase():
    customer_name = request.form["input-customer-name"]
    item_name1 = request.form["input-item-name1"]
    quantity1 = request.form["input-quantity1"]
    item_name2 = request.form["input-item-name2"]
    quantity2 = request.form["input-quantity2"]
    date = request.form["input-date"]
    date = datetime.strptime(date,"%Y-%m-%d")
    customer = Customer.query.filter_by(customer_name=customer_name).first()
    purchase = Purchase(customer.customer_id,date)
    
    try:
        db.session.add(purchase)
        db.session.commit()
    # except Exception as e:
    except sqlalchemy.exc.IntegrityError:
        # db.session.rollback()  # ロールバックしてエラーを処理
        return render_template("error.html")
    
    item1 = Item.query.filter_by(item_name=item_name1).first()
    purchase_detail = Purchase_detail(purchase.purchase_id,item1.item_id,quantity1)

    try:
        db.session.add(purchase_detail)
        db.session.commit()
    # except Exception as e:
    except sqlalchemy.exc.IntegrityError:
        # db.session.rollback()  # ロールバックしてエラーを処理
        return render_template("error.html")
    

    if item_name2:
        item2 = Item.query.filter_by(item_name=item_name2).first()
        purchase_detail = Purchase_detail(purchase.purchase_id,item2.item_id,quantity2)

        try:
            db.session.add(purchase_detail)
            db.session.commit()
        # except Exception as e:
        except sqlalchemy.exc.IntegrityError:
            # db.session.rollback()  # ロールバックしてエラーを処理
            return render_template("error.html")

    return render_template("3-1_confirm_purchase.html", purchase=purchase)

#3-2.購入情報削除
@app.route("/delete_purchase",methods=["GET","POST"])
def delete_purchase():
    purchase_id = request.form["input-purchase-id"]
    purchase = Purchase.query.filter_by(purchase_id=purchase_id).first()
    
    try:
        db.session.delete(purchase)
        db.session.commit()
        return render_template("3-2_confirm_deleted_purchase.html",purchase=purchase)
    # except Exception as e:
    except sqlalchemy.exc.IntegrityError:
        # db.session.rollback()  # ロールバックしてエラーを処理
        return render_template("error.html",purchase=purchase)
        # print(f"Error: {e}")

# 4-1.購入情報検索
@app.route("/search_purchase",methods=["GET","POST"])
def search_purchase():
    item_name = request.form["input-item-name"]
    customer_name = request.form["input-customer-name"]
    date = request.form["input-date"]
    # gender = request.form.get("input-gender3")

    if item_name:
        search_target = "%{}%".format(item_name)
        items = Item.query.filter(Item.item_name.like(search_target)).all()
        # item_id_list = []
        # for item in items:
        #     item_id_list.append(item.item_id)
        item_id_list = [item.item_id for item in items]
    # if customer_name and gender:
    #     customer = Customer.query.filter(customer_name==customer_name,gender==gender).first()
    #     customer_id = customer.customer_id
    if customer_name:
    #     customer = Customer.query.filter(customer_name==customer_name,gender==gender).first()
    #     customer_id = customer.customer_id
    # elif customer_name:
        customer = Customer.query.filter(customer_name==customer_name).first()
        customer_id = customer.customer_id
    # elif gender:
    #     customers = Customer.query.filter(gender==gender).all()
    #     customer_id_list = [customer.customer_id for customer in customers]
    else:
        customer = None
    if date:
        date = datetime.strptime(date,"%Y-%m-%d")

    is_customer_or_date = True
    # if customer_id_list:
    #     purchases = Purchase.query.filter(Purchase.customer_id.in_(customer_id_list),Purchase.date==date).all()
    # elif customer and date:
    if customer and date:
        purchases = Purchase.query.filter(Purchase.customer_id==customer_id,Purchase.date==date).all()
    elif customer:
        purchases = Purchase.query.filter(Purchase.customer_id==customer_id).all()
    elif date:
        purchases = Purchase.query.filter(Purchase.date==date).all()
    else:
        is_customer_or_date = False
    
    if is_customer_or_date:
    #     purchase_id_list = []
    #     for purchase in purchases:
    #         purchase_id_list.append(purchase.purchase_id)
        purchase_id_list = [purchase.purchase_id for purchase in purchases]
    
    if is_customer_or_date and item_name:
        purchase_details = Purchase_detail.query.filter(Purchase_detail.item_id.in_(item_id_list),Purchase_detail.purchase_id.in_(purchase_id_list)).all()
        return render_template("4-1_result_search_purchase.html",purchase_details=purchase_details)
    elif is_customer_or_date:
        purchase_details = Purchase_detail.query.filter(Purchase_detail.purchase_id.in_(purchase_id_list)).all()
        return render_template("4-1_result_search_purchase.html",purchase_details=purchase_details)
    elif item_name:
        purchase_details = Purchase_detail.query.filter(Purchase_detail.item_id.in_(item_id_list)).all()
        return render_template("4-1_result_search_purchase.html",purchase_details=purchase_details)
    else:
        return render_template("error.html")

# 4-2.総顧客数算出
@app.route("/count_customers",methods=["GET","POST"])
def count_customers():
    statistics_type = "総顧客数"
    number_of_customers = db.session.query(Customer).count()
    result = str(number_of_customers)+" 人"
    return render_template("4-2_result_statistics.html",statistics_type=statistics_type,result=result)

# 4-3.総販売商品数量算出
@app.route("/count_quantity",methods=["GET","POST"])
def count_quantity():
    statistics_type = "総販売商品数量"
    total_quantity = db.session.query(func.sum(Purchase_detail.quantity)).first()
    for row in total_quantity:
        result = row
    result = str(int(result))+" 個"
    return render_template("4-2_result_statistics.html",statistics_type=statistics_type,result=result)

# 4-4.総売上算出
@app.route("/total_sales",methods=["GET","POST"])
def total_sales():
    statistics_type = "総売上"
    joined_table = db.session.query(Purchase_detail.purchase_id,Item.price,Item.item_id,Purchase_detail.quantity).join(Item,Purchase_detail.item_id==Item.item_id).all()
    total_sales = 0
    for row in joined_table:
        if row.quantity:
            sale = row.price * int(row.quantity)
            total_sales += sale
    result = str(total_sales)+" 円"

    return render_template("4-2_result_statistics.html",statistics_type=statistics_type,result=result)

# 4-5.販売数量商品別ランキング
@app.route("/ranking_items",methods=["GET","POST"])
def ranking_items():
    statistics_type = "販売数量商品別ランキング"
    purchase_details = Purchase_detail.query.all()
    item_count_dict ={} # {item_id_A:総数量, item_id_B:総数量}
    for purchase_detail in purchase_details:
        item_id = purchase_detail.item_id
        quantity = purchase_detail.quantity
        if quantity:
            if item_count_dict.get(item_id) is None:
                item_count_dict[item_id] = quantity
            else:
                item_count_dict[item_id] += quantity
    # print(item_count_dict.items())
    item_count_dict = sorted(item_count_dict.items(),key=lambda x:x[1],reverse=True)
    items = []
    for index,item_tuple in enumerate(item_count_dict):
        item = list(item_tuple)
        item_name = Item.query.filter_by(item_id=item[0]).first().item_name
        item.append(item_name)
        item.append(str(index+1)+" 位")
        items.append(item)
    return render_template("4-3_result_ranking_items.html",statistics_type=statistics_type,items=items)

if __name__=="__main__":
    app.run(debug=True)