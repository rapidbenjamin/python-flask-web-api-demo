#!/usr/bin/python
# -*- coding: utf-8 -*-

# ------- IMPORT DEPENDENCIES ------- 
import datetime
import sendgrid
import os
import json
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
from flask import request, render_template, flash, current_app, redirect, abort, jsonify, url_for
from forms import *
from time import time
from flask_login import login_required, current_user
from PIL import Image

# ------- IMPORT LOCAL DEPENDENCIES  -------
from app import app, logger
from . import assets_page
from models import Assets
from app.helpers import *
from app.localization import get_locale, get_timezone
from app import config_name
from config import app_config
from constants import *



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app_config[config_name].ALLOWED_EXTENSIONS


def resize_image_to_max(image_path, max_size):
    max_size = max_size
    image = Image.open(image_path)
    original_size = max(image.size[0], image.size[1])

    if original_size >= max_size:
        # resized_file = open(image_path.split('.')[0] + '_resized.jpg', "w")
        if (image.size[0] > image.size[1]):
            resized_width = max_size
            resized_height = int(round((max_size/float(image.size[0]))*image.size[1])) 
        else:
            resized_height = max_size
            resized_width = int(round((max_size/float(image.size[1]))*image.size[0]))

        image = image.resize((resized_width, resized_height), Image.ANTIALIAS)
        image.save(image_path, 'JPEG')



# -------  ROUTINGS AND METHODS  ------- 


# All assets
@assets_page.route('/')
@assets_page.route('/<int:page>')
def assets(page=1):
    try:
        m_assets = Assets()
        list_assets = m_assets.all_data(page, app.config['LISTINGS_PER_PAGE'])
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = [{'id' : d.id, 'title_en_US' : d.title_en_US, 'description_en_US' : d.description_en_US, 'title_fr_FR' : d.title_fr_FR, 'description_fr_FR' : d.description_fr_FR} for d in list_assets.items])
        else:
            return render_template("assets/index.html", list_assets=list_assets, app = app)

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        #abort(404)






# Show asset
@assets_page.route('/show/<int:id>')
def show(id=1):
    try:
        m_assets = Assets()
        m_asset = m_assets.read_data(id)
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = m_asset)
        else:
            return render_template("assets/show.html", asset=m_asset, app = app)

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)


# New asset
@assets_page.route('/new', methods=['GET', 'POST'])
def new():
    try :
        # request.form only contains form input data. request.files contains file upload data. 
        # You need to pass the combination of both to the form. 
        form = Form_Record_Add(CombinedMultiDict((request.files, request.form)))

        if request.method == 'POST':

            if form.validate():

                # check if the post request has the file part
                if 'data_file_name' not in request.files :
                    # redirect to the form page or Json response
                    if request.is_xhr == True :
                        return jsonify(data = {message : "No file part", form : form}), 422, {'Content-Type': 'application/json'}
                    else:
                        flash("No file part", category="danger")
                        return redirect(request.url)
                
                # file = request.files['data_file_name']
                file = form.data_file_name.data

                # if user does not select file, browser also submit a empty part without filename
                if file.filename == '' :
                    # redirect to the form page or Json response
                    if request.is_xhr == True :
                        return jsonify(data = {message : "No selected file", form : form}), 422, {'Content-Type': 'application/json'}
                    else:
                        flash("No selected file", category="danger")
                        return redirect(request.url)

                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filename = filename.encode('utf-8')

                    target_dir = os.path.abspath(app_config[config_name].UPLOAD_FOLDER)
                    target = target_dir + '/' + filename
                    
                    print("------------ FILE  ------------\n" + str(target))
                    # if target not exist
                    if not os.path.isdir(target_dir):
                        os.mkdir(target_dir)

                    file.save(target)

                    # resize if too high
                    resize_image_to_max(target, app_config[config_name].MAX_SIZE)

                    filesize = os.stat(target).st_size
                    filetype = file.content_type


                    # image processing thumbnail 
                    infilename, ext = os.path.splitext(target)
                    im = Image.open(target)

                    filewidth, fileheight = im.size

                    im.thumbnail(app_config[config_name].THUMBNAIL_SIZE)
                    im.save(infilename + ".thumbnail" + ext)


                    assets = Assets()

                    sanitize_form = {
                        'assetable_id': form.assetable_id.data,
                        'assetable_type': form.assetable_type.data,

                        'data_file_name': filename,
                        'data_content_type': filetype,
                        'data_file_size': filesize,

                        'asset_type' : form.asset_type.data,
                        'width': filewidth,
                        'height': fileheight,

                        'description_en_US' : form.description_en_US.data,
                        'description_fr_FR' : form.description_fr_FR.data,

                        'is_active' : form.is_active.data,
                        'created_at' : form.created_at.data
                    }

                    assets.create_data(sanitize_form)
                    logger.info("Adding a new record.")
                    
                    if request.is_xhr == True:
                        return jsonify(data = { message :"Record added successfully.", form: form }), 200, {'Content-Type': 'application/json'}
                    else : 
                        flash("Record added successfully.", category="success")
                        return redirect("/assets")

        form.action = url_for('assets_page.new')
        form.created_at.data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

         # html or Json response
        if request.is_xhr == True:
            return jsonify(data = form), 200, {'Content-Type': 'application/json'}
        else:
            return render_template("assets/edit.html", form=form, title='New', app = app)
    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)


# Edit asset
@assets_page.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id=1):
    try : 

        # check_admin()

        assets = Assets()
        asset = assets.query.get_or_404(id)

        # request.form only contains form input data. request.files contains file upload data. 
        # You need to pass the combination of both to the form. 
        form = Form_Record_Add(CombinedMultiDict((request.files, request.form)))

        if request.method == 'POST':
            if form.validate():
                

                # check if the post request has the file part
                if 'data_file_name' not in request.files :
                    # redirect to the form page or Json response
                    if request.is_xhr == True :
                        return jsonify(data = {message : "No file part", form : form}), 422, {'Content-Type': 'application/json'}
                    else:
                        flash("No file part", category="danger")
                        return redirect(request.url)
                
                # file = request.files['data_file_name']
                file = form.data_file_name.data

                # if user does not select file, browser also submit a empty part without filename
                if file.filename == '' :
                    # redirect to the form page or Json response
                    if request.is_xhr == True :
                        return jsonify(data = {message : "No selected file", form : form}), 422, {'Content-Type': 'application/json'}
                    else:
                        flash("No selected file", category="danger")
                        return redirect(request.url)

                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filename = filename.encode('utf-8')

                    target_dir = os.path.abspath(app_config[config_name].UPLOAD_FOLDER)
                    target = target_dir + '/' + filename
                    
                    # Remove previous image
                    prev_target = target_dir + '/' + asset.data_file_name
                    print("------------ PREV FILE  ------------\n" + str(prev_target))
                    # remove previous thumbnail first
                    prev_infilename, prev_ext = os.path.splitext(prev_target)
                    os.remove(prev_infilename + '.thumbnail' + prev_ext) if os.path.isfile(prev_infilename + '.thumbnail' + prev_ext) else None
                    # remove previous file last
                    os.remove(prev_target) if os.path.isfile(prev_target) else None

                    print("------------ FILE  ------------\n" + str(target))
                    # if target not exist
                    if not os.path.isdir(target_dir):
                        os.mkdir(target_dir)

                    

                    file.save(target)

                    # resize if too high
                    resize_image_to_max(target, app_config[config_name].MAX_SIZE)

                    filesize = os.stat(target).st_size
                    filetype = file.content_type

                    # image processing thumbnail 
                    infilename, ext = os.path.splitext(target)
                    im = Image.open(target)

                    filewidth, fileheight = im.size


                    im.thumbnail(app_config[config_name].THUMBNAIL_SIZE)
                    im.save(infilename + ".thumbnail" + ext)

                    sanitize_form = {
                        'assetable_id': form.assetable_id.data, 
                        'assetable_type': form.assetable_type.data, 

                        'data_file_name': filename, 
                        'data_content_type': filetype, 
                        'data_file_size': filesize, 

                        'asset_type' : form.asset_type.data,
                        'width': filewidth,
                        'height': fileheight,

                        'description_en_US' : form.description_en_US.data,
                        'description_fr_FR' : form.description_fr_FR.data,

                        'is_active' : form.is_active.data,
                        'created_at' : form.created_at.data
                    }

                    assets.update_data(asset.id, sanitize_form)
                    logger.info("Editing a new record.")
                    
                    if request.is_xhr == True:
                        return jsonify(data = { message :"Record updated successfully.", form: form }), 200, {'Content-Type': 'application/json'}
                    else : 
                        flash("Record updated successfully.", category="success")
                        return redirect("/assets")

        form.action = url_for('assets_page.edit', id = asset.id)

        form.assetable_id.data = asset.assetable_id
        form.assetable_type.data = asset.assetable_type

        form.data_file_name.data = asset.data_file_name
        form.data_content_type.data = asset.data_content_type
        form.data_file_size.data = asset.data_file_size

        form.asset_type.data = asset.asset_type
        form.width.data = asset.width
        form.height.data = asset.height

        form.description_en_US.data = asset.description_en_US
        form.description_fr_FR.data = asset.description_fr_FR

        form.is_active.data = asset.is_active
        form.created_at.data = string_timestamp_utc_to_string_datetime_utc(asset.created_at, '%Y-%m-%d')

        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = form), 200, {'Content-Type': 'application/json'}
        else:
            return render_template("assets/edit.html", form=form, title='Edit', app = app)
    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)



# Delete asset
@assets_page.route('/delete/<int:id>')
def delete(id=1):
    try:
        assets = Assets()
        asset = assets.query.get_or_404(id)

        target_dir = os.path.abspath(app_config[config_name].UPLOAD_FOLDER)
        target = target_dir + '/' + asset.data_file_name

        # remove thumbnail first
        infilename, ext = os.path.splitext(target)
        os.remove(infilename + '.thumbnail' + ext) if os.path.isfile(infilename + '.thumbnail' + ext) else None

        # remove file last
        os.remove(target) if os.path.isfile(target) else None

        

        assets.delete_data(asset.id)
        # html or Json response
        if request.is_xhr == True:
            return jsonify(data = {message:"Record deleted successfully.", asset : m_asset})
        else:
            flash("Record deleted successfully.", category="success")
            return redirect(url_for('assets_page.assets'))

    except Exception, ex:
        print("------------ ERROR  ------------\n" + str(ex.message))
        flash(str(ex.message), category="warning")
        abort(404)