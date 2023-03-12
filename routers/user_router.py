from flask import *
from config.config import *
from utils.user_utils import *
user_router  = Blueprint('user_model',__name__,static_folder='static', template_folder='views')
login_manager2.login_view = 'user_model.id_card_login'

@login_manager2.user_loader
def load_user(user_id):
    return LoadUserById(user_id)


@user_router.route('/')
def user_main_router():
    return render_template('prompt.html'),404

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
    
    return render_template('form.html', input_record=input_record,error=error)



@user_router.route('/user', methods=['POST', 'GET'])
def id_card_login():
    try:
        if request.method == 'POST':
            id_card = request.form['id_card']
            user = get_user_id_card(id_card)
            if user.is_filled:
                error_message = 'Survey Form Already Filled.'
                return render_template('prompt.html', error_message=error_message)
            if not user:
                error_message = 'Not a Member of the Panamenista Party.'
                return render_template('prompt.html', error_message=error_message)
            login_user(user)
            return redirect(url_for('user_model.user_dashboard'))
        return render_template('prompt.html')
    except Exception as e:
        error_message = 'Access denied'
        return render_template('prompt.html', error_message=error_message)



    
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
    return render_template('disability.html',error=error)

@user_router.route('/user/disability/No',methods=['GET','POST'])
def user_disabiltiy_no():
    user = get_user_disability (current_user.id)
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
    return redirect(url_for('user_model.user_education'))   

from flask import current_app
import os
def save_file(file, folder_name):
    """
    Saves a file to the specified folder and returns the file path.
    :param file: file object to save
    :param folder_name: name of the folder to save the file in
    :return: file path of the saved file
    """
    # create the folder if it doesn't exist
    folder_path = os.path.join(current_app.root_path, 'static', folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
    # save the file
    file_path = os.path.join(folder_path, file.filename)
    file.save(file_path)
    
    # return the file path
    return file_path
@user_router.route('/user/education')
@login_required
def user_education():
    if current_user.is_filled:
        return redirect(url_for('user_model.user_survey')) 
    return render_template('prompt3.html'),404

@user_router.route('/user/university',methods=['POST','GET'])
@login_required
def user_university_yes():
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
        field_names = request.form.getlist('field_name1[]')
        for field_name in field_names:
            record = DegreeProgram(user_id=current_user.id,degree=field_name)
        db.session.add(record)
        
        field_names2 = request.form.getlist('field_name2[]')
        for field_name in field_names2:
            record = TechnicalTraining(user_id=current_user.id,technicalTraining=field_name)
        db.session.add(record)
        field_names3 = request.form.getlist('field_name3[]')
        for field_name in field_names3:
            record = Vocationaltrainingcenters(user_id=current_user.id,Vocationaltrainingcenters=field_name)
        db.session.add(record)
        job_experience = request.form.get('name')
        diploma_image = request.files.get('myfile')
        identity_proof = request.files.get('myfile2')
        personal_photo = request.files.get('myfile3')
        diploma = Diploma(user_id=current_user.id, job_experience=job_experience)
        diploma.diploma_image = bytes(save_file(diploma_image, 'diploma'), 'utf-8')
        diploma.identity_proof = bytes(save_file(identity_proof, 'identity'), 'utf-8')
        diploma.personal_photo = bytes(save_file(personal_photo, 'image'), 'utf-8')
        db.session.add(diploma)
        db.session.commit()
        current_user.is_filled = True
        db.session.commit()
        return "Surevy filled"
    return render_template('university.html'),404

@user_router.route('/user/institution')
@login_required
def user_university_no():
    if current_user.is_filled:
        return redirect(url_for('user_model.user_survey')) 
    return render_template('intitute.html'),404

@user_router.route('/user/survey')
@login_required
def user_survey():
    logout_user()
    return 'Survey Filled'