from flask import jsonify, request, render_template, url_for, flash, redirect
import numpy as np
import json
from keras.models import load_model
from tensorflow import get_default_graph
from sklearn.externals import joblib #for loading standard scaler
from project.convert import Converter
from project.forms import RegistrationForm, LoginForm
from project.db_models import User, Award, Activity
from project import application, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import desc

def loadModel(name):
    # load json and create model
    fileName = "project/nn_files/"+name+".h5"
    return load_model(fileName)


def loadScaler(name):
    #load scaler
    fileName = "project/nn_files/"+name+".save"
    return joblib.load(fileName) 

prediction_models = ((loadModel("model_1"), loadScaler("scaler_1")), (loadModel("model_2"), loadScaler("scaler_2")), (loadModel("model_3"), loadScaler("scaler_3")), (loadModel("model_4"), loadScaler("scaler_4")))
graph = get_default_graph() #doesn't work without this for some reason
converter = Converter()
model_sat2 = loadModel("model_sat2")
scaler_sat2 = loadScaler("scaler_sat2")
	
def calculateGrade(c_user):
	#input: current user
	#output: letter grade
    (gpa, act, sat2, essay, recommendation, award, activity) = (c_user.gpa, c_user.test, c_user.sat2_avg, c_user.essay, c_user.recommendation, c_user.award_score, c_user.activity_score)
    act = converter.convert_test([float(act)])[0]
    score = round(gpa/4*15 + act/36*15 + sat2/800*5 + essay/10*7.5 + recommendation/10*7.5 + (activity if activity <= 40 else 40)/40*40 + (award if award <= 40 else 40)/40*10)
    grade = ''
    if score >= 98:
        grade = 'A+'
    elif score >= 93:
        grade = 'A'
    elif score >= 90:
        grade = 'A-'
    elif score >= 88:
        grade = 'B+'
    elif score >= 83:
        grade = 'B'
    elif score >= 80:
        grade = 'B-'
    elif score >= 78:
        grade = 'C+'
    elif score >= 73:
        grade = 'C'
    elif score >= 70:
        grade = 'C-'
    elif score >= 68:
        grade = 'D+'
    elif score >= 63:
        grade = 'D'
    elif score >= 60:
        grade = 'D-'
    else:
        grade = 'F'
    
    return grade
    

@application.route("/")
def index():
    return render_template("home.html", board_img = url_for('static', filename='board.jpg'))


@application.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
		#saves user dashboard modal preference
        current_user.show_modal = request.form.get('check') == "true"
        db.session.commit()
        return ""
    else:
        return render_template("dashboard.html", academic_img = url_for('static', filename='academics.jpg'), activity_img = url_for('static', filename='activity.jpg'), award_img = url_for('static', filename='award.jpg'))
    
@application.route("/faq", methods = ['GET'])
@login_required
def faq():
    return render_template("faq.html")
    
@application.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        '''hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fname=form.fname.data, lname=form.lname.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()'''
        return redirect(url_for('dashboard'))
    return render_template("register.html", form=form)
    
    
@application.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
			#handles navigation to a different page that requires login
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("login.html", form=form)  


@application.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@application.route("/about")
def about():
    return render_template("about.html", library_img = url_for('static', filename='library.jpg'), classroom_img = url_for('static', filename='classroom.jpg'), book_img = url_for('static', filename='book.jpg'))  


@application.route("/stats")
@login_required
def stats():
	#sends values to stats.html page for dropdowns
    gender_objects = [{"value":0, "name":"Male"}, {"value":1, "name":"Female"}]
    race_objects = [{"value":3, "name":"American Indian or Alaska Native"}, {"value":2, "name":"Black / African American"}, {"value":1, "name":"Latino"}, {"value":0, "name":"White / Caucasian"}, {"value":-1, "name":"Asian American"}]
    school_objects = [{"value":0, "name":"Public"}, {"value":1, "name":"Private"}, {"value":0.5, "name":"Homeschooled"}]
    region_objects = [{"value":0, "name":"Northeast"}, {"value":1, "name":"Midwest"}, {"value":2, "name":"West"}, {"value":3, "name":"South"}]
    sat2_objects = [{"value":1, "name":"1"}, {"value":2, "name":"2"}, {"value":3, "name":"3"}, {"value":4, "name":"4"}, {"value":5, "name":"5"}]
    sat2_values = [i for i in [current_user.sat1, current_user.sat2, current_user.sat3, current_user.sat4, current_user.sat5] if i != None]
    return render_template("stats.html", gender_objects = gender_objects, race_objects = race_objects, school_objects = school_objects, region_objects = region_objects, sat2_objects = sat2_objects, sat2_values = sat2_values)


@application.route("/activities", methods=['GET', 'POST'])
@login_required
def activities():
    if request.method == 'POST':
        if request.form.get('message') == 'getSaved':
            package = []
            activities = Activity.query.filter(Activity.user==current_user).all()
            for activity in activities:
                package.append({"name":activity.name, "hours":activity.hours, "weeks":activity.weeks, "years":activity.years, "impact":(1.5 if activity.impact else 1.0), "leadership": (2.0 if activity.leadership else 1.0), "type":activity.activity_type})
        return jsonify({"activities": package})
    else:
        return render_template("activities.html", community_college_img = url_for('static', filename='community_college.jpg'), state_img = url_for('static', filename='asu.jpg'), good_img = url_for('static', filename='umich.jpg'), elite_img = url_for('static', filename='mit.jpg'))


@application.route("/awards")
@login_required
def awards():
    user_awards = Award.query.filter(Award.user==current_user).all()
    ap_awards = [{"value":1, "name":"Scholar"}, {"value":2, "name":"Scholar With Honor/Distinction"}, {"value":3, "name":"Capstone/WE Service/PLTW"}, {"value":4, "name":"State or National Scholar"}]
    nmsc_awards = [{"value":5, "name":"Commended"}, {"value":6, "name":"Semifinalist"}]
    generic_awards = [{"value":7, "name":"International"}, {"value":8, "name":"National"}, {"value":9, "name":"State"}, {"value":10, "name":"Local"}, {"value":11, "name":"National Honor Society"}, {"value":12, "name":"School"}]
    return render_template("awards.html", community_college_img = url_for('static', filename='community_college.jpg'), state_img = url_for('static', filename='asu.jpg'), good_img = url_for('static', filename='umich.jpg'), elite_img = url_for('static', filename='mit.jpg'), user_awards=user_awards, ap_awards=ap_awards, nmsc_awards=nmsc_awards, generic_awards=generic_awards)

@application.route("/analyze", methods=['GET'])
@login_required
def analyze():
	#ensures user has followed all steps already
    if not (current_user.stats_step and current_user.activity_step and current_user.award_step):
        return redirect(url_for('dashboard'))
    else:
        if 'n' not in request.args:
            tab_num = 0
        else:
            tab_num = int(request.args.get("n"))
            
        #0:overview, last two: extracurriculars and awards
        if tab_num not in range(7):
            tab_num = 0
        if tab_num == 0:
            #overview
            grade = calculateGrade(current_user)
            return render_template("overview_analysis.html", grade = grade)
        
        elif tab_num == 5:
            #activities
            activity_package = {}
        
            if current_user.activity_score < 4:
                activity_package["generic"] = "community college"
                activity_package["tier"] = "tiers 6 and under"
            elif current_user.activity_score < 10:
                activity_package["generic"] = "large public university"
                activity_package["tier"] = "tiers 5 and under"
            elif current_user.activity_score < 17:
                activity_package["generic"] = "good private or public college"
                activity_package["tier"] = "tiers 3 and under"
            else:
                activity_package["tier"] = "tiers 1 and 2"
                activity_package["generic"] = "elite university"
            
            
            #number of activities
            activity_count = len(Activity.query.filter(Activity.user==current_user).all())
            if activity_count == 5:
                activity_package["count"] = "We applaud you for filling up all 5 extracurricular slots. Congratulations on this achievement!"
            else:
                activity_package["count"] = "We noticed that you only entered <b>" + str(activity_count) + "</b> activities from a maximum of 5. The Common Application allows you to enter up to 10, so having at least 5 strong activities is valuable. Of course, the quality of activities matters <i>much</i> more than their quantity, but it is good to have a few for most people."
            
    		#leadership
            activity_leader_count = len(Activity.query.filter(Activity.user==current_user, Activity.leadership).all())
            if activity_leader_count == 0:
                activity_package["leader_count"] = "We noticed that you did not show leadership in any of your extracurricular activities. And sure, it is not easy to be a leader! However, colleges LOVE seeing leadership from applicants. As a personal benefit, being a leader will help you greatly in your future life and career."
            elif activity_leader_count == 1:
                activity_package["leader_count"] = "Based on your activities, you have shown leadership in <b>1</b> activity. This is a good start! Many colleges will notice this and look more favourably on you application. However, this might not be enough. We recommend working harder to be a leader in more activities. Just a reminder, do not do this just for <i>leadership</i>. Become a leader because you truly care about the activity and want to make a difference!"
            else:
                activity_package["leader_count"] = "We noticed that you acted as a leader in <b>" + str(activity_leader_count) + "</b> activities. Great job! Continue putting in consistent effort into those activities and being a great leader! Colleges will reward you for this. If you can, take on more responsibility and become a leader in more activities."
            
    		#impact
            activity_impact_count = len(Activity.query.filter(Activity.user==current_user, Activity.impact).all())
            if activity_impact_count == 0:
                activity_package["impact_count"] = "We noticed that you did not show impact in any of your extracurricular activities. Impact is having an extraordinary effect on the project, cause, or people you work with. Basically, impact is leaving your extracurricular activity better and more successful than you initially found it. We hope that you consider dedicating yourself more to your interests and making great things happen!"
            elif activity_impact_count == 1:
                activity_package["impact_count"] = "Based on your activities, you have had an impact in <b>1</b> activity. This is more than the majority of applicants have! Colleges enjoy seeing impact because it shows dedication, talent, and the desire to constantly improve. We hope that you continue working harder to have an even great impact in more activities. Good luck!"
            else:
                activity_package["impact_count"] = "We noticed that you had a significant impact in <b>" + str(activity_leader_count) + "</b> activities. Great job! Continue putting in consistent effort into those activities and make amazing things happen! Colleges will reward you for this. If you can, take on more responsibility and really dedicate yourself to your interests!"
            
    		#best activity
            best_activity = Activity.query.filter(Activity.user==current_user).order_by(desc(Activity.value)).first()
            activity_package["best"] = "According to our algorithm, your most impressive and valuable extracurricular activity is <b>" + str(best_activity.name) + "</b>. We recommend informing your colleges of this activity and possibly including it in an essay."
            if best_activity.leadership:
                activity_package["best"] += " We saw that you showed leadership in this activity, which is great!"
            if best_activity.impact:
                activity_package["best"] += " We are sure that your impact in this activity is very impressive, and your colleges will love to hear about it."
            
    		#volunteer
            volunteer = Activity.query.filter(Activity.user==current_user, Activity.activity_type==1).all()
            if len(volunteer) == 0:
                activity_package["volunteer"] = "Upon closer inspection, your list of activities did not include any volunteering or community service. Although not strictly mandatory, colleges like to see your willingness to help the causes you feel strongly about. Some options for volunteering include tutoring for free, volunteering at a botanic garden, or helping the homeless."
            else:
                activity_package["volunteer"] = "We want to complement you on doing community service in one or more of your activities, for example in <b>" + str(volunteer[0].name if len(volunteer) == 1 or volunteer[0] != best_activity else volunteer[1].name) + "</b>. Your willingness to work for free and help out different causes is important and will be noticed by college officers."
            
    		#best time
            best_time = Activity.query.filter(Activity.user==current_user).order_by(desc(Activity.time_value)).first()
            activity_package["time"] = "On top of impact and leadership, the time you put into an activity matters; it shows dedication. The number of years, weeks per year, and hours per week are all important. You will be asked to enter these values on Common App. So far, your best activity in terms of the time you spent on it is <b>"+str(best_time.name)+"</b>. Keep up the good work!"
            
            
    		#variety
            activity_types = len(Activity.query.with_entities(Activity.activity_type).filter(Activity.user == current_user).distinct(Activity.activity_type).all())
            if activity_types == 1:
                activity_package["type"] = "We noticed that all of your activities fall under the <b>same category</b>. We recommend trying other types of activities, like music, community service, or academic clubs. This will show colleges the diversity of your interests!"
            elif activity_types == 2:
                activity_package["type"] = "You have <b>2</b> types of extracurricular activities, according to what you have entered. Although this is good, you could try even more categories to show colleges (especially ones focused on a well-rounded education) how diverse your interests are."
            else:
                activity_package["type"] = "Well done! You have extracurriculars in <b>"+str(activity_types)+"</b> different categories. You are showing colleges that you are a dedicated and well-rounded person."
            return render_template("activity_analysis.html", activity_package = activity_package)
            
            
        
        elif tab_num == 6:
            #awards
            award_package = {}
            if current_user.award_score < 4:
                award_package["generic"] = "community college"
                award_package["tier"] = "tiers 6 and under"
            elif current_user.award_score < 10:
                award_package["generic"] = "large public university"
                award_package["tier"] = "tiers 5 and under"
            elif current_user.award_score < 17:
                award_package["generic"] = "good private or public college"
                award_package["tier"] = "tiers 3 and under"
            else:
                award_package["tier"] = "tiers 1 and 2"
                award_package["generic"] = "elite university"
            award_count = len(Award.query.filter(Award.user==current_user).all())
            if award_count == 5:
                award_package["count"] = "We applaud you for filling up all 5 award slots. Congratulations on this achievement!"
            else:
                award_package["count"] = "We noticed that you only entered <b>" + str(award_count) + "</b> award(s) from a maximum of 5. The Common Application allows you to enter up to 5, so it is often a good idea to fill up all the slots. Try to be more active in your extracurriculars, and you will soon have 5 as well!"
              
            award_check_count = len(Award.query.filter(Award.user==current_user, Award.check).all())
            if award_check_count == 0:
                award_package["check"] = "We noticed that none of your awards related to your anticipated major. Although it is good to have well-rounded awards, it is often great to show colleges achievement in your anticipated major. This shows interest and dedication. We recommend trying to get 1-2 such awards through school or extracurricular involvements"
            else:
                award_package["check"] = "We noticed that <b>"+str(award_check_count)+"</b> of your awards relate(s) to your main major. That is great! Keep pursuing your passions, but do not be afraid to branch out. It is good to have a few awards in your anticipated major and a few unrelated ones to show that you have a variety of interests and are a well-rounded person."
                
            award_list = Award.query.filter(Award.user==current_user).all()
            award_dict = {0:0.0, 1:2.0, 2:3.0, 3:4.0, 4:5.0, 5:2.0, 6:4.0, 7:16.0, 8:8.0, 9:4.0, 10:2.0, 11:1.0, 12:1.0}
            max_award_id = 0
            max_award_val = 0
            for a in award_list:
                if award_dict[a.award_type] * (1.5 if a.check else 1.0) > max_award_val:
                    max_award_val = award_dict[a.award_type] * (1.5 if a.check else 1.0)
                    max_award_id = a.award_type
                    
            award_names = {1:"AP Scholar", 2:"AP Scholar With Honor/Distinction", 3:"AP Capstone/WE Service/PLTW", 4:"AP State or National Scholar", 5:"National Merit Commended", 6:"National Merit Semifinalist", 7:"International Award", 8:"National Award", 9:"State Award", 10:"Local Award", 11:"National Honor Society", 12:"School Award"}
            award_package["biggest"] = award_names[max_award_id]
            return render_template("award_analysis.html", award_package = award_package)
                   
        else:
            tier_package = getTierOutput(tab_num)
            return render_template("tier_analysis.html", tier_package = tier_package)
        

def getTierOutput(n):
    global prediction_models
    standards = {
                1: {'act': 35, 'sat':1530, 'gpa':3.95, 'sat2':760, 'essay':9, 'rec':9}, 
                2: {'act': 34, 'sat':1490, 'gpa':3.9, 'sat2':740, 'essay':8.5, 'rec':8.5},
                3: {'act': 34, 'sat':1490, 'gpa':3.85, 'sat2':730, 'essay':8, 'rec':8},
                4: {'act': 33, 'sat':1470, 'gpa':3.85, 'sat2':730, 'essay':8, 'rec':8}
                }
    
    tier_package = {}
    tier_package["tier"] = "Tier " + str(n)
    tier_sigmoid = (current_user.tier1, current_user.tier2, current_user.tier3, current_user.tier4)[n-1]
    if tier_sigmoid >= 0.5:
        tier_package["competitive"] = "very competitive"
        tier_package["otherWords"] = "high chance"
    elif tier_sigmoid >= 0.4:
        tier_package["competitive"] = "somewhat competitive"
        tier_package["otherWords"] = "moderate chance"
    else:
        tier_package["competitive"] = "not competitive"
        tier_package["otherWords"] = "low chance"
        
    #advice
    tier_advice = advice(current_user, standards[n]['act'], standards[n]['gpa'], standards[n]['sat2'], standards[n]['essay'], standards[n]['rec'], prediction_models[n-1][0], prediction_models[n-1][1])
    tier_advice_messages = []
    tier_advice_message_dict = {
		               "round": "Try to apply to your top choices using <b>Early Action</b> or <b>Early Decision</b> rounds, if possible. Both if these show interest and greatly increase your chance of getting in!",
					   "act": "Increase your standardized test score to a <b>"+str(standards[n]['act'])+"+</b> on the ACT or to a <b>"+str(standards[n]['sat'])+"+</b> on the SAT. A large chunk of applicants have these scores, so it would be good for you to have them as well!",
                       "gpa": "Bump up your GPA to about <b>" + str(standards[n]['gpa'])+" or higher</b>. Our neural network believes that this would greatly increase your chances.",
                       "sat2": "Increase your SAT Subject Test average score to <b>"+str(standards[n]['sat2'])+"</b>. These tests are very important in showing mastery of various subjects, and many colleges in this tier <i>strongly</i> recommend them.",
                       "essay": "Put more effort into your essays when writing them or go back and edit existing essays. The algorithm believes that if your essays are a <b>" + str(standards[n]['essay']) + "</b> on a scale from 1 to 10, your chances would improve a lot.", 
                       "recommendation":"Secure better recommendation letters by building relationships with your teachers. This can also help you get other opportunities like internships for the summer! The neural network believes that if your recommendations were a solid <b>" + str(standards[n]['rec']) + "</b> on a scale from 1 to 10, the strength of your application would benefit a lot.",
                       "home":"Apply as a <b>home state student</b>. If one of the 8 colleges in this tier are located in your home state, you have a distinct advantage over out of state applicants, so make sure to apply to the college in your state. Good luck!"}
		
    for adv in tier_advice:
        tier_advice_messages.append(tier_advice_message_dict[adv])
        
    if len(tier_advice) == 0:
        tier_advice_messages.append("The neural network was not able to come up with any suggestions for your profile. This is because it is already incredibly competitive for this tier, so you already have a great chance of success at these institutions!")
    
    if n == 1:
        tier_package["colleges"] = "This tier consists of eight of the best universities in the United States, particularly Harvard, Stanford, MIT, Yale, Princeton, University of Pennsylvania, Columbia, and Caltech. These colleges are characterized by <8% acceptance rates and are extremely difficult to get into."
    elif n == 2:
        tier_package["colleges"] = "This tier consists of some of the best universities in the United States, like Brown, Northwestern, and Duke. These colleges are characterized by <12% acceptance rates and are very challenging to get into."
    elif n == 3:
        tier_package["colleges"] = "Unlike previous tiers, Tier 3 contains some public universities as well. Some well-known colleges from this tier include UC Berkeley, University of Southern California, Rice, and Vanderbilt. Despite this being Tier 3, these colleges are still <i>very</i> hard to get into with acceptance rates generally below 25%."
    elif n == 4:
        tier_package["colleges"] = "This tier has a few more selective colleges which are just slightly last competitive than in the last tier. Some notable examples are UC San Diego, University of Michigan, Boston College, and Georgia Institute of Technology. With acceptance rates generally below 30%, even qualified applicants will face a challenge when applying to these institutions."

    tier_package["advice"] = tier_advice_messages
    return tier_package
		
@application.route("/process_activities", methods=['POST'])
@login_required
def process_activities():
	#calculates total score for activities and saves activities
    if request.method == 'POST':
        try:
            values = request.get_json()
            score = 0
            result = 0
            types = []
			#clears all activities and saves again
            Activity.query.filter(Activity.user==current_user).delete()
            db.session.commit()
            for val in values:
                val = json.loads(val)
                activity_score = activity_value(val.get('weeks'), val.get('hours'), val.get('years'), val.get('leader'), val.get('impact'), val.get('type'))
                score += activity_score
                types.append(val.get("type"))
                activity = Activity(name=val.get("name"), activity_type=int(val.get("type")), leadership=(float(val.get('leader'))==2.0), impact=(float(val.get('impact'))==1.5), years=float(val.get('years')), weeks=float(val.get('weeks')), hours=float(val.get('hours')), value=float(activity_score), time_value = float(activity_time(val.get('weeks'), val.get('hours'), val.get('years'))), user=current_user)
                db.session.add(activity)
            db.session.commit()
            num_types = len(set(types))
            if num_types == 2:
                score *= 1.5
            elif num_types >=3:
                score *= 1.8
            if score < 4:
                result = 0
            elif score < 10:
                result = 1
            elif score < 17:
                result = 2
            else:
                result = 3
            current_user.activity_score = score
            current_user.activity_step = True
            db.session.commit()
            return jsonify({'result': str(result), 'points': str(score)})
            
        except:
            return jsonify({'result': 'error'})
    else:
        return jsonify({'result': 'error'})
  
def activity_value(weeks, hours, years, leader, impact, aType):
	#calculates value for each activity
    return float(activity_time(weeks, hours, years)) * leader * impact * (1.2 if aType == 1 else 1.0)
	
def activity_time(weeks, hours, years):
	#time score for each activity
    return (1.0 + (weeks-20)/52 + hours + years)

def runModel(model, scaler, data):
	#evaluates model
    with graph.as_default():
        p = model.predict(scaler.transform(data))[0][0]
    return p

def advice(c_user, ACT_THRESHOLD, GPA_THRESHOLD, SAT2_THRESHOLD, REC_THRESHOLD, ESSAY_THRESHOLD, md, sc):
	#returns most important improvements
    (gpa, act, sat2, gender, race, essay, recommendation, school, region) = (c_user.gpa, c_user.test, c_user.sat2_avg, c_user.gender, c_user.race, c_user.essay, c_user.recommendation, c_user.school, c_user.region)
    race = 2.0 if race == 3.0 else race #race conversion
    act = converter.convert_test([float(act)])[0]
    baseline = runModel(md, sc, np.array([[gpa, act, sat2, gender, race, essay, recommendation, school, region]]))

    #ACT
    if act < ACT_THRESHOLD:
        act_output = runModel(md, sc, np.array([[gpa, ACT_THRESHOLD, sat2, gender, race, essay, recommendation, school, region]]))
    else:
        act_output = -1
    
    #GPA
    if gpa < GPA_THRESHOLD:
        gpa_output = runModel(md, sc, np.array([[GPA_THRESHOLD, act, sat2, gender, race, essay, recommendation, school, region]]))
    else:
        gpa_output = -1
    
    #SAT2
    if sat2 < SAT2_THRESHOLD:
        sat2_output = runModel(md, sc, np.array([[gpa, act, SAT2_THRESHOLD, gender, race, essay, recommendation, school, region]]))
    else:
        sat2_output = -1
        
    #Essay
    if essay < ESSAY_THRESHOLD:
        essay_output = runModel(md, sc, np.array([[gpa, act, sat2, gender, race, ESSAY_THRESHOLD, recommendation, school, region]]))
    else:
        essay_output = -1
        
    #Recommendation
    if recommendation < REC_THRESHOLD:
        rec_output = runModel(md, sc, np.array([[gpa, act, sat2, gender, race, essay, REC_THRESHOLD, school, region]]))
    else:
        rec_output = -1
        
    #Home State Applicant
    home_output = runModel(md, sc, np.array([[gpa, act, sat2, gender, race, essay, recommendation, school, 4]]))

    
    #changes in output after small alterations
    deltas = {"act": act_output-baseline, "gpa": gpa_output-baseline, "sat2": sat2_output-baseline, "essay": essay_output-baseline, "recommendation": rec_output-baseline, "home": home_output-baseline}
    
    sorted_deltas = sorted(deltas.items(), key=lambda x: x[1], reverse=True)
    advice_list = []
    #always try to apply early
    advice_list.append("round")
	#checks what change made biggest impact on sigmoid output
    for i in range(2):
        if sorted_deltas[i][1] > 0:
            advice_list.append(sorted_deltas[i][0])
    return advice_list

@application.route("/process_awards", methods=['POST'])
@login_required
def process_awards():
	#calculates award scores
    if request.method == 'POST':
        try:
            award_dict = {0:0.0, 1:2.0, 2:3.0, 3:4.0, 4:5.0, 5:2.0, 6:4.0, 7:16.0, 8:8.0, 9:4.0, 10:2.0, 11:1.0, 12:1.0}
            awards = request.form.getlist('award[]')
            mult = request.form.getlist('mult[]')
            score = 0
            result = 0
            Award.query.filter(Award.user==current_user).delete()
            db.session.commit()
            for i in range(len(awards)):
                if(int(awards[i]) != 0):
                    award = Award(award_type=int(awards[i]), user=current_user, check=(float(mult[i])==1.5))
                    db.session.add(award)
                score += award_dict[int(awards[i])] * float(mult[i])
            db.session.commit()
            if score < 4:
                result = 0
            elif score < 11:
                result = 1
            elif score < 18:
                result = 2
            else:
                result = 3
            current_user.award_score = score
            current_user.award_step = True
            db.session.commit()
            return jsonify({'result': str(result), 'points':str(score)})
            
        except:
            return jsonify({'result': 'error'})
    else:
        return jsonify({'result': 'error'})
    
@application.route("/predict_sat2", methods=['POST'])
@login_required
def predict_sat2():
    global model_sat2, scaler_sat2, graph
    if request.method == 'POST':
        try:
            gpa = float(request.form.get('gpa'))
            act = converter.convert_test([float(request.form.get('act'))])[0]
            with graph.as_default():
                sat2 = round(runModel(model_sat2, scaler_sat2, np.array([[gpa, act]])))
            sat2 = 800 if sat2>800 else sat2
            return jsonify({'sat2':str(sat2)})
        except:
            return jsonify({'result': 'error'})
    else:
        return jsonify({'result': 'error'})
    
    
@application.route("/tier", methods = ['POST'])
@login_required
def tier():
    global prediction_models, graph
    if request.method == 'POST':
        try:
            gpa = float(request.form.get('gpa'))
            act = converter.convert_test([float(request.form.get('act'))])[0]
            sat2 = float(request.form.get('sat2'))
            gender = float(request.form.get('gender'))
            race = float(request.form.get('race'))
            essay = float(request.form.get('essay'))
            recommendation = float(request.form.get('recommendation'))
            school = float(request.form.get('school'))
            region = float(request.form.get('region'))
            sat2_list = request.form.getlist('sat2_list[]')
            
            scaled = prediction_models[0][1].transform(np.array([[gpa, act, sat2, gender, 2.0 if race == 3.0 else race, essay, recommendation, school, region]]))
            with graph.as_default():
                prediction = prediction_models[0][0].predict(scaled)[0][0]
            current_user.tier1 = float(prediction)
            #print("1:"+str(prediction))
			
            scaled = prediction_models[1][1].transform(np.array([[gpa, act, sat2, gender, 2.0 if race == 3.0 else race, essay, recommendation, school, region]]))
            with graph.as_default():
                prediction = prediction_models[1][0].predict(scaled)[0][0]
            current_user.tier2 = float(prediction)
            #print("2:"+str(prediction))
			
            scaled = prediction_models[2][1].transform(np.array([[gpa, act, sat2, gender, 2.0 if race == 3.0 else race, essay, recommendation, school, region]]))
            with graph.as_default():
                prediction = prediction_models[2][0].predict(scaled)[0][0]
            current_user.tier3 = float(prediction)
            #print("3:"+str(prediction))
			
            scaled = prediction_models[3][1].transform(np.array([[gpa, act, sat2, gender, 2.0 if race == 3.0 else race, essay, recommendation, school, region]]))
            with graph.as_default():
                prediction = prediction_models[3][0].predict(scaled)[0][0]
            current_user.tier4 = float(prediction)
            #print("4:"+str(prediction))
            
            current_user.gpa=gpa
            current_user.test=int(request.form.get('act'))
            current_user.sat2_avg = int(sat2)
            current_user.gender = int(gender)
            current_user.race = int(race)
            current_user.school = school
            current_user.essay = essay
            current_user.recommendation = recommendation
            current_user.region = int(region)
            current_user.stats_step = True
            #saving sat2 scores
            (current_user.sat1, current_user.sat2, current_user.sat3, current_user.sat4, current_user.sat5) = (sat2_list[0], sat2_list[1] if len(sat2_list)>1 else None, sat2_list[2] if len(sat2_list)>2 else None, sat2_list[3] if len(sat2_list)>3 else None,sat2_list[4] if len(sat2_list)>4 else None)
            db.session.commit()
            response = jsonify({'prediction': str(prediction)})
            return response
        except:
            return jsonify({'error': 'error'})
    else:
        return False
