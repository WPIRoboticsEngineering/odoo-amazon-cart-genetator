import pickle
import odoorpc
import re
from datetime import datetime

logins = pickle.load(open('../logins.pickle','rb'))

odoo = odoorpc.ODOO('odoo.cs.wpi.edu', port=8069)
odoo.login('wpishop',logins['odoo']['username'],logins['odoo']['password']) 

ai = odoo.env['account.invoice']
po = odoo.env['purchase.order']  

def getRFQs(po):
    rfqs = []
    pors = po.browse(po.search([]))
    for p in pors:
        if p.state == 'draft':
            rfqs.append(p)
            
    return rfqs
    
def buildAmazonLink(rfq):
    for r in rfq:
        if r.partner_id.name == 'Amazon':
            ol = r.order_line
            print("Amazon %s"%(r))
            link = "https://www.amazon.com/gp/aws/cart/add.html?"
            item = 1;
            for l in ol:
                x = re.compile("(?:[/dp/]|$)([A-Z0-9]{10})") 
                if x.search(l.display_name):
                    m = x.search(l.display_name)
                    asin = l.display_name[m.start()+1:m.end()]
                    qty = int(l.product_qty)
                    if item!=1:
                        link = link + "&"
                    link = link + "ASIN.%d=%s&Quantity.%d=%d"%(item,asin,item,qty)
                    item+=1
            print(link) 


rfqs = getRFQs(po)
buildAmazonLink(rfqs)