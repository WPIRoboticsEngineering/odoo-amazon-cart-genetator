import pickle
import odoorpc
import re
from datetime import datetime

logins = pickle.load(open('../logins.pickle','rb'))

odoo = odoorpc.ODOO('odoo.cs.wpi.edu', port=8069)
odoo.login('wpishop',logins['odoo']['username'],logins['odoo']['password']) 

ai = odoo.env['account.invoice']
po = odoo.env['purchase.order']  

# POs marked as 'draft' are RFQs. Get current RFQs and return a list.
def getRFQs(po):
    rfqs = []
    pors = po.browse(po.search([]))
    for p in pors:
        # If state is 'draft' then it is a RFQ
        if p.state == 'draft':
            rfqs.append(p)
            
    return rfqs

    
def buildAmazonLink(rfq):
    for r in rfq:
        # make sure our RFQ is an amazon one.
        if r.partner_id.name == 'Amazon':
            ol = r.order_line
            print("Amazon %s"%(r))
            link = "https://www.amazon.com/gp/aws/cart/add.html?"
            item = 1;
            # For each line item, extract ASIN and QTY
            for l in ol:
                # ASIN extraction REGEX. The asin can be in a URL, surrounded by brackets
                # or in a url surrounded by brackets, or whatever, it's really inconsistent.
                #x = re.compile("(?:[/dp/]|$)([A-Z0-9]{10})") 
                x = re.compile("(B[A-Z0-9]{9})") 
                #Only add it to the URL if we have a match
                
                if x.search(l.display_name):
                    print("Match")
                    m = x.search(l.display_name)
                    asin = l.display_name[m.start():m.end()]
                    qty = int(l.product_qty)
                    # Add ASIN and QTY to GET request.
                    if item!=1:
                        link = link + "&"
                    link = link + "ASIN.%d=%s&Quantity.%d=%d"%(item,asin,item,qty)
                    item+=1
                print(l.display_name)
                print("")
            print("")
            print(link) 


rfqs = getRFQs(po)
buildAmazonLink(rfqs)