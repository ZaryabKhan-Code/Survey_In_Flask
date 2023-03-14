from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl import Workbook
from flask import *
from config.config import *
from utils.admin_utils import *
from models.user_models import *
import bcrypt
import pdfkit


admin_router = Blueprint('admin_model', __name__,
                         static_folder='static', template_folder='views')
login_manager.login_view = 'admin_model.admin_login'


@login_manager.user_loader
def load_user(user_id):
    return LoadUserById(user_id)


@admin_router.route('/register', methods=['GET', 'POST'])
@login_required
def admin_register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not username or not email or not password or not confirm_password:
            error_message = 'Please fill out all fields.'
            return render_template('register.html', error_message=error_message)

        if password != confirm_password:
            error_message = 'Passwords do not match.'
            return render_template('register.html', error_message=error_message)

        existing_user = get_admin_username(username)
        if existing_user:
            error_message = 'That username is already taken.'
            return render_template('register.html', error_message=error_message)

        existing_email = get_admin_email(email)
        if existing_email:
            error_message = 'That email is already taken.'
            return render_template('register.html', error_message=error_message)

        new_user = Admin(username=username, email=email,
                         password=password, is_confirmed=False)
        db.session.add(new_user)
        db.session.commit()
        send_verification_email(email, username)
        message = "Registration successful, activation link sent to email"
        return render_template('register.html', message=message)
    return render_template('register.html')


@admin_router.route('/admin', methods=['POST', 'GET'])
def admin_login():
    success_message = request.args.get('success_message')
    if current_user.is_authenticated:
        return redirect(url_for('admin_model.admin_dashboard'))
    try:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user = get_admin_email(email)
            if not user:
                error_message = 'Incorrect email or password.'
                return render_template('login.html', error_message=error_message, success_message=success_message)
            if not bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'):
                error_message = 'Incorrect email or password.'
                return render_template('login.html', error_message=error_message, success_message=success_message)
            login_user(user)
            return redirect(url_for('admin_model.admin_dashboard'))
        return render_template('login.html', success_message=success_message)
    except Exception as e:
        error_message = 'Login access denied'
        return render_template('login.html', error_message=error_message, success_message=success_message)


@admin_router.route('/check_email/<email>')
@login_required
def check_email(email):
    email_admin = get_admin_email(email)
    if email_admin:
        return jsonify({'error': 'Email already exists'})
    else:
        return jsonify({})


@admin_router.route('/check_username/<username>')
@login_required
def check_username(username):
    username_admin = get_admin_username(username)
    if username_admin:
        return jsonify({'error': 'Username already exists'})
    else:
        return jsonify({})


@admin_router.route('/activate')
def activate():
    if current_user.is_authenticated:
        return redirect(url_for('admin_model.admin_dashboard'))
    token = request.args.get('token')
    try:
        email = verify_activation_token(token)
        if email is not None:
            activate = get_admin_email(email)
            activate.is_confirmed = True
            db.session.commit()
            delete_token(token)
            flash('Your email has been verified. You can now log in.')
            return render_template('verification_result.html', success=True)
        else:
            return render_template('verification_result.html', success=False)
    except Exception as e:
        return f'Error Creating Token Contact Support'


@admin_router.route('/diplomas/<int:user_id>/<filename>', methods=['GET'])
def download_diploma(user_id, filename):
    diploma = Diploma.query.filter_by(user_id=user_id).first()
    if diploma is None:
        abort(404, description='Diploma not found!')

    if filename == diploma.filename_diploma_image:
        file_data = diploma.diploma_image
    elif filename == diploma.filename_identity_proof:
        file_data = diploma.identity_proof
    elif filename == diploma.filename_personal_photo:
        file_data = diploma.personal_photo
    else:
        abort(404, description='File not found!')

    response = make_response(file_data)
    response.headers.set('Content-Type', 'application/octet-stream')
    response.headers.set('Content-Disposition', 'attachment',
                         filename=f'User_Id:{user_id}_'+filename)
    return response


@admin_router.route('/user/show/information')
@login_required
def admin_dashboard():
    try:
        user = User.query.all()
        return render_template('dashboard.html', user=user)
    except Exception as e:
        message = f'Error'
        return render_template('dashboard.html', message=message)


@admin_router.route('/logout')
@login_required
def admin_logout():
    success_message = 'User Successfully Logout'
    logout_user()
    return redirect(url_for('admin_model.admin_login', success_message=success_message))


@admin_router.route('/user/details/<id>', methods=['POST', 'GET'])
@login_required
def user_information(id):
    user = User.query.filter_by(id=id).first()
    other_info = OtherInformation.query.filter_by(user_id=id).first()
    disability = Disability.query.filter_by(user_id=id).first()
    university = University.query.filter_by(user_id=id).first()
    degreeprogram = DegreeProgram.query.filter_by(user_id=id).first()
    vocationaltrainingcenters = Vocationaltrainingcenters.query.filter_by(
        user_id=id).first()
    institution = Institution.query.filter_by(user_id=id).first()
    technicalTraining = TechnicalTraining.query.filter_by(user_id=id).first()
    diploma = Diploma.query.filter_by(user_id=id).first()
    return render_template('user_deatils.html', user_id=id, user=user, other_info=other_info, disability=disability, university=university, institution=institution, degreeprogram=degreeprogram, vocationaltrainingcenters=vocationaltrainingcenters, technicalTraining=technicalTraining, diploma=diploma)


path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)


@admin_router.route('/pdf')
@login_required
def generate_pdf():
    html = render_template('index.html')
    pdf = pdfkit.from_string(html, False, configuration=config)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
    return response


@admin_router.route('/diplomas/<int:user_id>/download/PDF')
@login_required
def download_zip_pdf(user_id):
    diploma2 = Diploma.query.filter_by(user_id=user_id).first()

    if diploma2 is None:
        abort(404, description='Diploma not found!')
    user = User.query.filter_by(id=user_id).first()
    other_info = OtherInformation.query.filter_by(user_id=user_id).first()
    disability = Disability.query.filter_by(user_id=user_id).first()
    university = University.query.filter_by(user_id=user_id).first()
    degreeprogram = DegreeProgram.query.filter_by(user_id=user_id).first()
    vocationaltrainingcenters = Vocationaltrainingcenters.query.filter_by(
        user_id=user_id).first()
    institution = Institution.query.filter_by(user_id=user_id).first()
    technicalTraining = TechnicalTraining.query.filter_by(
        user_id=user_id).first()
    diploma = Diploma.query.filter_by(user_id=user_id).first()
    options = {
        'page-size': 'A4',
        'margin-top': '0',
        'margin-right': '0',
        'margin-bottom': '0',
        'margin-left': '0',
    }
    html = render_template('pdfgenerator.html', user_id=id, user=user, other_info=other_info, disability=disability, university=university, institution=institution,
                           degreeprogram=degreeprogram, vocationaltrainingcenters=vocationaltrainingcenters, technicalTraining=technicalTraining, diploma=diploma)
    pdf = pdfkit.from_string(
        html, False, options=options, configuration=config)

    files = [
        (f'{user.first_name}_diploma_File_' +
         diploma2.filename_diploma_image, diploma2.diploma_image),
        (f'{user.first_name}_identity_proof_' +
         diploma2.filename_identity_proof, diploma2.identity_proof),
        (f'{user.first_name}_personal_photo_' +
         diploma2.filename_personal_photo, diploma2.personal_photo),
        (f'{user.first_name}_' + 'Information.pdf', pdf)
    ]

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for filename, data in files:
            zip_file.writestr(filename, data)

    zip_buffer.seek(0)
    response = make_response(zip_buffer.getvalue())
    response.headers.set('Content-Type', 'application/zip')
    response.headers.set('Content-Disposition', 'attachment',
                         filename=f'UserRecord_{user.id_card}_PDF_Record.zip')
    return response


@admin_router.route('/diplomas/<int:user_id>/download/EXCEL', methods=['POST', 'GET'])
@login_required
def download_zip_excel(user_id):
    user = User.query.filter_by(id=user_id).first()
    other_info = OtherInformation.query.filter_by(user_id=user_id).first()
    disability = Disability.query.filter_by(user_id=user_id).first()
    university = University.query.filter_by(user_id=user_id).first()
    degreeprogram = DegreeProgram.query.filter_by(user_id=user_id).first()
    vocationaltrainingcenters = Vocationaltrainingcenters.query.filter_by(
        user_id=user_id).first()
    institution = Institution.query.filter_by(user_id=user_id).first()
    technicalTraining = TechnicalTraining.query.filter_by(
        user_id=user_id).first()
    diploma = Diploma.query.filter_by(user_id=user_id).first()

    wb = Workbook()
    ws = wb.active
    ws['A1'] = 'User Information'
    ws.merge_cells('A1:B1')
    ws['A1'].font = Font(size=16, bold=True)
    ws['A1'].alignment = Alignment(horizontal='center')

    # Set the font, alignment, and border for the label cells
    label_font = Font(bold=True)
    label_alignment = Alignment(horizontal='right', wrap_text=True)
    label_border = Border(bottom=Side(style='thin'))

    # Set the font and border for the value cells
    value_font = Font()
    value_border = Border(bottom=Side(style='thin'))

    # Populate the user information cells
    user_info = [('A2', 'First Name', user.first_name),             ('A3', 'Last Name', user.last_name),             ('A4', 'ID Card', user.id_card),             ('A5', 'Current Email Address', user.current_email_address),
                 ('A6', 'Address', user.address),             ('A7', 'City', user.city),             ('A8', 'Province', user.province),             ('A9', 'Country', user.country),             ('A10', 'Is Filled', user.is_filled)]
    for cell, label, value in user_info:
        ws[cell] = label
        ws[cell].font = label_font
        ws[cell].alignment = label_alignment
        ws[cell].border = label_border

        ws.cell(row=ws[cell].row, column=2, value=value)
        ws.cell(row=ws[cell].row, column=2).font = value_font
        ws.cell(row=ws[cell].row, column=2).border = value_border

    excel_buffer = io.BytesIO()
    wb.save(excel_buffer)
    excel_buffer.seek(0)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, mode='w') as zip_file:
        zip_file.writestr(
            f'{user.first_name}_Information.xlsx', excel_buffer.getvalue())
        for file_name, file_data in [
            (f'{user.first_name}_diploma_File_' +
             diploma.filename_diploma_image, diploma.diploma_image),
            (f'{user.first_name}_identity_proof_' +
             diploma.filename_identity_proof, diploma.identity_proof),
            (f'{user.first_name}_personal_photo_' +
             diploma.filename_personal_photo, diploma.personal_photo)
        ]:
            zip_file.writestr(file_name, file_data)

    zip_buffer.seek(0)

    response = make_response(zip_buffer.getvalue())
    response.headers.set('Content-Type', 'application/zip')
    response.headers.set('Content-Disposition', 'attachment',
                         filename=f'UserRecord_{user.id_card}_Excel_Record.zip')
    return response
