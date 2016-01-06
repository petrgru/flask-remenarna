#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from flask import request, redirect, url_for, render_template, flash,jsonify,json,g,Response
from flask.ext.babel import gettext
from flask.ext.login import login_required
from app import db
from app.aplikace.models import Product,Promena
from forms import FileUploadForm,EditPromForm
from ..user import user
from ..aplikace import aplikace
from ..tasks import parsexlsdata,data_web_update,data_ean13_update,updatefile,toxml




@aplikace.route('/upload-xls', methods=['GET', 'POST'])
@login_required
def upload():
    import os
    from werkzeug.utils import secure_filename
    form = FileUploadForm()
    if form.validate_on_submit():
            data = request.files[form.filename.name].read()
            filename = secure_filename(form.filename.data.filename)
            file_path = os.path.join('./app/uploads/', filename)
            open(file_path, 'w').write(data)
            parsexlsdata.delay(file_path)
            flash('Data nahrana a budou se zpracovavat',category='info')
    task= json.loads(inspect().data)
    if task['task'][0]['id'] == '':
        busy=True
    else:
        busy=False
        flash('Data jsou zpracovavana pockejte nekolik minut a akci zopakujte pokud potrebujete...',category='info')


    return render_template("fileupload.html", form = form , user = user ,busy=busy)

@aplikace.route('/inspect', methods=['GET'])
@login_required
def inspect():
    method='active'
    from celery import Celery
    from ..config import base_config
    app = Celery('app', broker=base_config.BROKER_URL)
    #app = Celery('app', broker='redis://localhost:6379')
    inspect_result = getattr(app.control.inspect(), method)()
    app.close()
    ''' Nutno dodelat '''
    task=[]
    for key,value in inspect_result.iteritems():
        if inspect_result[key].__len__() > 0:
            task.append({"id":inspect_result[key][0]['id']})
        else:
            task.append({"id":''})
    return jsonify(task=task)



@aplikace.route('/list', methods=['GET', 'POST'])
@login_required
def list_products():

    from app.database import DataTable
    datatable = DataTable(
        model=Product,
        columns=[Product.Obj,Product.Popis,Product.CenaProdej,Product.sklad,Product.KL,Product.TL,Product.Foto],
        sortable=[Product.UID],
        searchable=[Product.Popis,Product.Obj],
        filterable=[Product.Popis],
        limits=[25, 50, 100],
        request=request
    )

    if g.pjax:
        return render_template(
            'products.html',
            datatable=datatable,
            stats=Product.stats()
        )

    return render_template(
        'product_list.html',
        datatable=datatable,
        stats=Product.stats()
    )

@aplikace.route('/webparse', methods=['GET'])
@login_required
def webparser():
    task= json.loads(inspect().data)
    if task['task'][0]['id'] == '':
        data_web_update.delay()
        flash('Data jsou zpracovavana pockejte nejakou hodinu a akci zopakujte pokud potrebujete...',category='info')
    else:
        flash('Process bezi pockejte nejakou hodinu a akci zopakujte pokud potrebujete...',category='info')

    return redirect(request.args.get('next') or url_for('index'))

@aplikace.route('/ean13', methods=['GET'])
@login_required
def ean13_regenerate():
    task= json.loads(inspect().data)
    if task['task'][0]['id'] == '':
        data_ean13_update.delay()
        flash('Data jsou zpracovavana pockejte nejakou hodinu a akci zopakujte pokud potrebujete...',category='info')
    else:
        flash('Process bezi pockejte nejakou hodinu a akci zopakujte pokud potrebujete...',category='info')

    return redirect(request.args.get('next') or url_for('index'))



@aplikace.route('/files-download', methods=['GET'])
@login_required
def downloadsoubory():
#    from ..tasks import updatefile
#    task= json.loads(inspect().data)
#    if task['task'][0]['id'] == '':
    updatefile()
    flash('Data jsou zpracovavana pockejte nejakou hodinu a akci zopakujte pokud potrebujete...',category='info')
#    else:
#        flash('Process bezi pockejte nejakou hodinu a akci zopakujte pokud potrebujete...',category='info')

    return redirect(request.args.get('next') or url_for('index'))

@aplikace.route('/xml', methods=['GET'])
@login_required
def generate_xml_file():
    toxml.delay()
    flash('Data jsou zpracovavana pockejte nejakou minutu a akci zopakujte pokud potrebujete...',category='info')
    return redirect(request.args.get('next') or url_for('index'))

@aplikace.route('/list_prom', methods=['GET', 'POST'])
@login_required
def list_prom():

    from app.database import DataTable
    datatable = DataTable(
        model=Promena,
        columns=[Promena.hodnota],
        sortable=[Promena.promena],
        searchable=[Promena.promena],
        filterable=[Promena.promena],
        limits=[25, 50, 100],
        request=request
    )

    if g.pjax:
        return render_template(
            'promenne.html',
            datatable=datatable,
            stats=Promena.stats()
        )

    return render_template(
        'list-prom.html',
        datatable=datatable,
        stats=Promena.stats()
    )


@aplikace.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_prom(id):
    user = Promena.query.filter_by(id=id).first_or_404()
    form = EditPromForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        user.update()
        flash(
            gettext('Prom edited'),
            'success'
        )
    return render_template('edit-prom.html', form=form, user=user)


@aplikace.route('/delete/<string:id>', methods=['GET'])
@login_required
def delete_prom(id):
    prom = Promena.query.filter_by(prom=id).first_or_404()
    prom.delete()
    flash(gettext('Promena smazana','success'))
    return redirect(url_for('.list_prom'))
