from ecommerce import *
from ecommerce.models import *
from sqlalchemy import func, or_


def search( pid = [x for x in range( Product.query.count()+1 )] ,min_price=0 , max_price=100000 , min_avg=0 , word=False ):
    
    if type(pid) == int :
        pid = [pid]


    search_query = db.session.query(Product.id).outerjoin(Order).outerjoin(Reviews).group_by(Product).having(or_(db.func.count(Reviews.id)==0 , db.func.avg(Reviews.stars) > min_avg )).subquery()


    #query = products.filter(Product.category.in_(pid))

    #if word :
     #   word = "%{}%".format(word)
      #  search_query = Product.query.join(search_query , search_query.c.id == Product.id).filter(Product.name.like(word)).subquery()

    
    search_query = Product.query.join(search_query , search_query.c.id == Product.id).filter(Product.id.in_(pid) , Product.price > min_price , Product.price < max_price )

    #if min_price:
    #    products = products.filter(Product.price > min_price )

    #if max_price:
    #    products = products.filter(Product.price < max_price )

    #search_query = search_query.all()
    #temp = search_query.all()
    
    products = []
    for product in search_query :
        row = product.__dict__
        row['supplier'] = product.supplier.get_info()
        row['avg_stars'] = product.get_review(avg=True)['avg']
        row['price'] =  float( row['price'] )
        if row['_sa_instance_state']:
            del row['_sa_instance_state']
        products.append(row)
    
    return products
