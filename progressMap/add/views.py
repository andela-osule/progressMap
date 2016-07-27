from flask import render_template, abort, flash, redirect, url_for
from flask_login import login_required, current_user
from . import add, forms
from .. import models, db

@add.route('/')
def main():
	return render_template('add.html')

@add.route('/article', methods=['GET', 'POST'])
@login_required
def article():
	form = forms.articleForm()
	if form.validate_on_submit():
		title = form.title.data
		course = form.course.data
		curriculum = form.curriculum.data
		description = form.description.data
		row = models.Articles(title=title, course=course, curriculum=curriculum, description=description, user=current_user)
		db.session.add(row)
		db.session.commit()
		
		flash("Added article '{}'.".format(form.title.data))
		return redirect(url_for('articles.show'))
	return render_template('addArticle.html', form=form)

@add.route('/course', methods=['GET', 'POST'])
def course():
	form = forms.courseForm()
	if form.validate_on_submit():
		title = form.title.data
		curriculum = form.curriculum.data
		if models.get_by_title(models.Curriculums, curriculum):
			curriculum = models.get_by_title(models.Curriculums, curriculum)
		else:
			flash('Sorry the curriculum you are trying to add to doesn\'t exist!')
			return render_template('addCourse.html', form=form)	
		description = form.description.data
		row = models.Courses(title=title, curriculum=curriculum, description=description, user=current_user)
		db.session.add(row)
		db.session.commit()
		
		flash("Added course '{}'.".format(form.title.data))
		return redirect(url_for('courses.show'))
	return render_template('addCourse.html', form=form)

@add.route('/curriculum', methods=['GET', 'POST'])
def curriculum():
	form = forms.curriculumForm()
	if form.validate_on_submit():
		title = form.title.data
		description = form.description.data
		row = models.Curriculums(title=title, description=description, user=current_user)
		db.session.add(row)
		db.session.commit()
		
		flash("Added curriculum '{}'.".format(form.title.data))
		return redirect(url_for('curriculums.show'))
	return render_template('addCurriculum.html', form=form)