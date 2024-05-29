from flask import Blueprint, render_template, request, jsonify, flash, redirect
from auth.controllers.login import login_required
from .models.schedule_model import ScheduleModel
from .entities.schedule import ScheduleDay

schedule_bp = Blueprint('schedule', __name__, url_prefix='/schedule', template_folder='./templates')


@schedule_bp.get("/")
@login_required
def edit_schedule_page():
    week_schedule = ScheduleModel.get_week_schedule()

    # Setting keys in spanish to be shown on frontend
    week_schedule_dict = {
        'Lunes': {
            'openTime': week_schedule.monday.openTime, 
            'closeTime': week_schedule.monday.closeTime
            } if week_schedule.monday else None,
        'Martes': {
            'openTime': week_schedule.tuesday.openTime, 
            'closeTime': week_schedule.tuesday.closeTime
            } if week_schedule.tuesday else None,
        'Miercoles': {
            'openTime': week_schedule.wednesday.openTime, 
            'closeTime': week_schedule.wednesday.closeTime
            } if week_schedule.wednesday else None,
        'Jueves': {
            'openTime': week_schedule.thursday.openTime, 
            'closeTime': week_schedule.thursday.closeTime
            } if week_schedule.thursday else None,
        'Viernes': {
            'openTime': week_schedule.friday.openTime, 
            'closeTime': week_schedule.friday.closeTime
            } if week_schedule.friday else None,
        'Sabado': {
            'openTime': week_schedule.saturday.openTime, 
            'closeTime': week_schedule.saturday.closeTime
            } if week_schedule.saturday else None,
        'Domingo': {
            'openTime': week_schedule.sunday.openTime, 
            'closeTime': week_schedule.sunday.closeTime
            } if week_schedule.sunday else None,
    }

    return render_template('schedule.html', schedule=week_schedule_dict)
    

@schedule_bp.get("/obtain/")
@login_required
def get_schedule():
    try:
        week_schedule = ScheduleModel.get_week_schedule()
        return jsonify(week_schedule.to_dict()), 200
    except Exception as e:
        print(f"Error getting schedule: {e}")
        return {'message': 'An error occurred while fetching the schedule.'}, 500


@schedule_bp.post("/set/<week_day>/")
@login_required
def set_schedule_for_day(week_day):
    """Set an schedule for a certain day.

    The request must have a form with openTime and closeTime time objects
    
    Keyword arguments:
    argument - weekday - Number from 0(monday) to 6(sunday)
    Return: redirect
    """
    
    week_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    
    
    week_day = int(week_day)
    if week_day < 0 or week_day > 6:
        return {'message': 'Invalid day of the week.'}, 400

    data = request.form
    open_time = data.get('openTime', None)
    close_time = data.get('closeTime', None)

    day_key = week_days[week_day]


    try:
        # Get current week schedule
        week_schedule = ScheduleModel.get_week_schedule()
        
        daily_schedule_id = getattr(week_schedule, day_key).id if week_schedule and getattr(week_schedule, day_key) else None

        if open_time is None and close_time is None:
                # Set day as closed
            if daily_schedule_id:
                # Delete existing daily schedule
                ScheduleModel.update_week_schedule(day_key, None)
                ScheduleModel.delete_element('dailySchedule', daily_schedule_id)

                flash(f'Se ha cerrado correctamente', "success")
                return redirect("/schedule", 301)
                
        else:
            if daily_schedule_id:
                    # Update existing daily schedule
                ScheduleModel.update_daily_schedule(daily_schedule_id, open_time, close_time)
            else:
                # Insert new daily schedule
                new_daily_schedule_id = ScheduleModel.create_daily_schedule(open_time, close_time)
                ScheduleModel.update_week_schedule(day_key, new_daily_schedule_id)

    except Exception as e:
        flash('Ha ocurrido un error actualizando el horario.', "error")
        return redirect("/schedule", 301)

    flash(f'El horario ha sido actualizado con éxito', "success")
    return redirect("/schedule", 301)
    
    

