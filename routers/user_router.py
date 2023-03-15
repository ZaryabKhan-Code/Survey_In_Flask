from flask import *
from config.config import *
from models.admin_models import *
from utils.user_utils import *
user_router  = Blueprint('user_model',__name__,static_folder='static', template_folder='views')
login_manager2.login_view = 'user_model.id_card_login'

@login_manager2.user_loader
def load_user(user_id):
    return LoadUserById(user_id)


@user_router.route('/')
def user_main_router():
    form = Form.query.first()
    return render_template('prompt.html',form = form),404

@user_router.route('/validate_id_card', methods=['POST'])
def validate_id_card_route():
    id_card = request.json['id_card']
    response = validate_id_card(id_card)
    return jsonify(response)


@user_router.route('/user/dashboard', methods=['POST', 'GET'])
@login_required
def user_dashboard():
    input_record = None 
    error = None
    try:
        user = get_user_other_user_information (current_user.id)
        if user:
            return redirect(url_for('user_model.user_disability'))  
        if current_user.is_filled:
             return redirect(url_for('user_model.user_survey'))
        if request.method == 'POST':
            input_record = {
                'user_id': current_user.id,
                'gender': request.form['radio'],
                'edad': request.form['edad'],
                'date_of_birth': request.form['birthday'],
                'blood_type': request.form['blood'],
                'blood_donor': request.form['Donate'],
                'language': request.form['languages'],
                'home_number': request.form['mobile'],
                'province': request.form['provinces']
            }
            db.session.add(OtherInformation(**input_record))
            db.session.commit()
            return redirect(url_for('user_model.user_disability'))   
    except Exception as e:
        error= f"An error occurred"
        logout_user()
        return redirect(url_for('user_model.id_card_login'))
    
    return render_template('form.html', input_record=input_record,error=error)



@user_router.route('/user', methods=['POST', 'GET'])
def id_card_login():
    try:
        form = Form.query.first()
        if request.method == 'POST':
            id_card = request.form['id_card']
            user = get_user_id_card(id_card)
            if not user:
                error_message = 'Not a Member of the Panamenista Party.'
                return render_template('prompt.html', error_message=error_message,form=form)
            if user.is_filled:
                error_message = 'Seems You already participated in the survey.'
                return render_template('prompt.html', error_message=error_message,form=form)
            login_user(user)
            return redirect(url_for('user_model.user_dashboard'))
        return render_template('prompt.html',form=form)
    except Exception as e:
        error_message = 'Access denied'
        return render_template('prompt.html', error_message=error_message,form=form)



    
@user_router.route('/user/disability')
@login_required
def user_disability():
    user = get_user_disability(current_user.id)
    if user:
        return redirect(url_for('user_model.user_education'))
    if current_user.is_filled:
        return redirect(url_for('user_model.user_survey'))
    return render_template('prompt2.html')

@user_router.route('/user/disability/Yes',methods=['GET','POST'])
def user_disabiltiy_yes():
    error = None
    try:
        user = get_user_disability(current_user.id)
        if user:
            return redirect(url_for('user_model.user_education'))  
        if current_user.is_filled:
             return redirect(url_for('user_model.user_survey'))
        if request.method == 'POST':
            input_record = {
                'user_id': current_user.id,
                'type': request.form['disabilities'],
                'specific_disability': request.form['disability']
            }
            db.session.add(Disability(**input_record))
            db.session.commit()
            return redirect(url_for('user_model.user_education'))   
    except Exception as e:
        error= f"An error occurred"
        logout_user()
        return redirect(url_for('user_model.id_card_login'))
    return render_template('disability.html',error=error)

@user_router.route('/user/disability/No',methods=['GET','POST'])
def user_disabiltiy_no():
    user = get_user_disability (current_user.id)
    try:
        if user:
            return redirect(url_for('user_model.user_education'))  
        if current_user.is_filled:
                return redirect(url_for('user_model.user_survey'))
        input_record = {
                    'user_id': current_user.id,
                    'type': None,
                    'specific_disability': None
                }
        db.session.add(Disability(**input_record))
        db.session.commit()
    except Exception as e:
        error= f"An error occurred"
        logout_user()
        return redirect(url_for('user_model.id_card_login'))
    return redirect(url_for('user_model.user_education'))   

from flask import current_app
import os
def save_file(file, folder_name):
    folder_path = os.path.join(current_app.root_path, 'static', folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
    file_path = os.path.join(folder_path, file.filename)
    file.save(file_path)
    
    return file_path
@user_router.route('/user/education')
@login_required
def user_education():
    try:            
        if current_user.is_filled:
            return redirect(url_for('user_model.user_survey')) 
    except Exception as e:
        error= f"An error occurred"
        logout_user()
        return redirect(url_for('user_model.id_card_login'))
    return render_template('prompt3.html'),404

@user_router.route('/user/university',methods=['POST','GET'])
@login_required
def user_university_yes():
    try:
        if current_user.is_filled:
            return redirect(url_for('user_model.user_survey'))
        if request.method=='POST':
            input_record = {
                    'user_id': current_user.id,
                    'student_center': request.form['uni'],
                    'bachelor_or_technician_1': request.form['bt'],
                    'bachelor_or_technician_2':request.form['bt2'],
                    'mastery_1':request.form['master'],
                    'mastery_2':request.form['master2'],
                    'doctrate':request.form['doc'],
                    'institute_or_technical_training_center':request.form['ex'],
                    'professional_education_and_training':request.form['ed'],
                    'vocational_training_or_additional_training':request.form['mes']
                } 
            db.session.add(University(**input_record))
            db.session.commit()
            field_names = request.form.get('field_name')
            record1 = DegreeProgram(user_id=current_user.id,degree=field_names)
            db.session.add(record1)
            db.session.commit()
            
            field_names2 = request.form.get('field_name2')
            record2 = TechnicalTraining(user_id=current_user.id,technicalTraining=field_names2)
            db.session.add(record2)
            db.session.commit()
            field_names3 = request.form.getlist('field_name3')
            record3= Vocationaltrainingcenters(user_id=current_user.id,Vocationaltrainingcenters=field_names3)
            db.session.add(record3)
            db.session.commit()
            job_experience = request.form.get('name')
            diploma_image = request.files['myfile']
            identity_proof = request.files['myfile2']
            personal_photo = request.files['myfile3']
            new_diploma = Diploma(user_id=current_user.id,
                                job_experience=job_experience,
                                diploma_image=diploma_image.read(),
                                identity_proof=identity_proof.read(),
                                personal_photo=personal_photo.read(),
                                filename_diploma_image=diploma_image.filename,
                                filename_identity_proof=identity_proof.filename,
                                filename_personal_photo=personal_photo.filename,
                                adddownload = '/diplomas/'f'{current_user.id}''/download/images')

            db.session.add(new_diploma)
            db.session.commit()
            current_user.is_filled = True
            db.session.commit()
            input_record2 = {
                    'user_id': current_user.id,
                    'trainingcenter': None,
                    'othervocationaltraining': None,
                    'training':None,
                    'addtraining':None
                } 
            db.session.add(Institution(**input_record2))
            db.session.commit()
            return redirect(url_for('user_model.user_survey'))
    except Exception as e:
        error= f"An error occurred"
        logout_user()
        return redirect(url_for('user_model.id_card_login'))
    return render_template('university.html'),404

@user_router.route('/user/institution',methods=['POST','GET'])
@login_required
def user_university_no():
    try:
        if current_user.is_filled:
            return redirect(url_for('user_model.user_survey'))
        if request.method=='POST':
            input_record = {
                    'user_id': current_user.id,
                    'trainingcenter': request.form['ex'],
                    'othervocationaltraining': request.form['field_name1'],
                    'training':request.form['ed'],
                    'addtraining':request.form['mes']
                } 
            db.session.add(Institution(**input_record))
            db.session.commit()
            job_experience = request.form.get('name')
            diploma_image = request.files['myfile']
            identity_proof = request.files['myfile2']
            personal_photo = request.files['myfile3']
            new_diploma = Diploma(user_id=current_user.id,
                                job_experience=job_experience,
                                diploma_image=diploma_image.read(),
                                identity_proof=identity_proof.read(),
                                personal_photo=personal_photo.read(),
                                filename_diploma_image=diploma_image.filename,
                                filename_identity_proof=identity_proof.filename,
                                filename_personal_photo=personal_photo.filename,
                                adddownload = '/diplomas/'f'{current_user.id}''/download/images')
            db.session.add(new_diploma)
            db.session.commit()
            current_user.is_filled = True
            db.session.commit()
            input_record2 = {
                    'user_id': current_user.id,
                    'student_center': None,
                    'bachelor_or_technician_1': None,
                    'bachelor_or_technician_2':None,
                    'mastery_1':None,
                    'mastery_2':None,
                    'doctrate':None,
                    'institute_or_technical_training_center':None,
                    'professional_education_and_training':None,
                    'vocational_training_or_additional_training':None
                } 
            db.session.add(University(**input_record2))
            db.session.commit()
            record = DegreeProgram(user_id=current_user.id,degree=None)
            db.session.add(record)
            record2 = TechnicalTraining(user_id=current_user.id,technicalTraining=None)
            db.session.add(record2)
            db.session.commit()
            record3= Vocationaltrainingcenters(user_id=current_user.id,Vocationaltrainingcenters=None)
            db.session.add(record3)
            db.session.commit()
            db.session.commit()
            return redirect(url_for('user_model.user_survey'))
    except Exception as e:
        return f"An error occurredf'{e}"
    return render_template('no.html'),404

@user_router.route('/user/survey')
@login_required
def user_survey():
    logout_user()
    return render_template('thank_you.html')




@user_router.route('/user/intrested',methods=['POST','GET'])
def user_intrested():
    try:
        if request.method=='POST':
            id_card = request.form['id_card']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            current_email_address = request.form['email']
            address = request.form['address']
            city =  request.form['city']
            province = request.form['province']
            country  = request.form['country']
            check_id_card = get_user_id_card(id_card)
            if check_id_card:
                error_message = 'Id_Card is already registered'
                return render_template('not_member.html',error_message=error_message)
            check_email = get_user_by_email(current_email_address)
            if check_email:
                error_message = 'Emails is already registered'
                return render_template('not_member.html',error_message=error_message)
            add_record  =  UnregisterUser(id_card=id_card,first_name=first_name,last_name=last_name,current_email_address=current_email_address,address=address,city=city,province=province,country=country)
            db.session.add(add_record) 
            db.session.commit()   
            return render_template('thank2.html')       
    except Exception:
        return redirect(url_for('user_model.id_card_login'))
    return render_template('not_member.html')