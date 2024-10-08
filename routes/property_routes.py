import io
import matplotlib
matplotlib.use('Agg')
from flask import Response, render_template, request, redirect, send_file, url_for, flash
from flask_login import login_required, current_user
from matplotlib import pyplot as plt
from app import app, db
from models.property import Property
from models.user import User

@app.route('/properties', methods=['GET'])
@login_required
def user_properties():
    properties = Property.query.filter_by(owner_id=current_user.id).all()
    total_property_value = sum(property.value for property in properties)
    return render_template('user_properties.html', properties=properties, total_property_value=total_property_value)

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

    return render_template('add_property.html', allowed_property_types=Property.allowed_property_types())

@app.route('/delete_property/<int:id>', methods=['POST'])
@login_required
def delete_property(id):
    property_to_delete = Property.query.get_or_404(id)
    db.session.delete(property_to_delete)
    db.session.commit()
    return redirect(url_for('user_properties'))

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
        return redirect(url_for('user_properties'))

    return render_template('transfer_ownership.html', property=property_to_transfer)

@app.route('/property_value_plot', methods=['GET'])
@login_required
def property_value_plot():
    properties = Property.query.filter_by(owner_id=current_user.id).all()

    years = []
    values = []
    for prop in properties:
        years.append(prop.date_added.year)
        values.append(prop.value)

    plt.figure(figsize=(7.5, 4.5))
    plt.plot(years, values, marker='o')
    plt.title('Your Total Value Over Time')
    plt.xlabel('Year')
    plt.ylabel('Value (£)')
    plt.grid(False)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return Response(img.getvalue(), mimetype='image/png')

