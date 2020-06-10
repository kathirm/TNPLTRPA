import odoorpc
def load_languages(langs, db, ip='localhost', port=8069, username='admin', password='abcd123'):

    odoo=odoorpc.ODOO(ip,'jsonrpc',port)
    odoo.login(db, username, password)
    base_lng_model = odoo.env['base.language.install']

    for lang in langs:
        id = base_lng_model.create(
                {
                    'lang':lang,
                    'state': 'done', 
                    'overwrite':True,
                    'company_ids':[1],
                    'company_id':1
                    })
        result = base_lng_model.lang_install(id)
        print(result)


if __name__ == '__main__':
    langs = ['es_ES']

    load_languages(langs, 'MK2', ip='206.189.156.106')

