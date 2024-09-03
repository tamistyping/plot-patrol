from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import app, db
from models.property import Property
from models.user import User

@app.route('/properties', methods=['GET'])
@login_required
def index():
    properties = Property.query.filter_by(owner_id=current_user.id).all()
    return render_template('properties.html', properties=properties)

@app.route('/add_property', methods=['GET', 'POST'])
@login_required
def add_property():
    if request.method == 'POST':
        title = request.form['title']
        property_type = request.form['property_type']
        address = request.form['address']
        city = request.form['city']
        postcode = request.form['postcode']
        value = float(request.form['value'])

        new_property = Property(title=title, property_type=property_type, address=address,
                                city=city, postcode=postcode, value=value, owner_id=current_user.id)
        db.session.add(new_property)
        db.session.commit()
        return redirect(url_for('user_properties'))

    return render_template('add_property.html')

@app.route('/delete_property/<int:id>', methods=['POST'])
@login_required
def delete_property(id):
    property_to_delete = Property.query.get_or_404(id)
    
    db.session.delete(property_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/transfer_property/<int:id>', methods=['GET', 'POST'])
@login_required
def transfer_property(id):
    property_to_transfer = Property.query.get_or_404(id)

    if request.method == 'POST':
        new_owner_username = request.form['new_owner']
        new_owner = User.query.filter_by(username=new_owner_username).first()

        if not new_owner:
            flash('User does not exist!')
            return redirect(url_for('transfer_property', id=id))

        property_to_transfer.owner_id = new_owner.id
        db.session.commit()
        flash('Property ownership transferred successfully!')
        return redirect(url_for('index'))

    return render_template('transfer_property.html', property=property_to_transfer)
