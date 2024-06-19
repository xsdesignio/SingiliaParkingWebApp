from flask import Blueprint, render_template, request, jsonify, flash, redirect
from auth.controllers.login import login_required
from .models.schedule_model import ScheduleModel
from .entities.schedule import DailySchedule

schedule_bp = Blueprint('schedule', __name__, url_prefix='/schedule', template_folder='./templates')


@schedule_bp.get("/")
@login_required
def edit_schedule_page():
    week_schedule = ScheduleModel.get_week_schedule()

    # Setting keys in spanish to be shown on frontend
    week_schedule_dict = {
        'Lunes': week_schedule.monday,
        'Martes': week_schedule.tuesday,
        'Miercoles': week_schedule.wednesday,
        'Jueves': week_schedule.thursday,
        'Viernes': week_schedule.friday,
        'Sabado': week_schedule.saturday,
        'Domingo': week_schedule.sunday,
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


@schedule_bp.post("/add/<week_day>/")
@login_required
def add_open_span_to_week_day(week_day):
    """Add an open span to the schedule of a certain day.

    The request must have a form with openTime and closeTime time objects
    
    Keyword arguments:
    argument - weekday - Number from 0(monday) to 6(sunday)
    Return: redirect
    """
    
    week_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    

    # Obtains week day from url index
    week_day = int(week_day)
    if week_day < 0 or week_day > 6:
        flash('El día de la semana introducido no es válido.', "error")
        return redirect("/schedule", 301)

    day_key = week_days[week_day]

    # Obtains reqquest data
    data = request.form
    open_time = data.get('openTime', None)
    close_time = data.get('closeTime', None)

    if open_time is None and close_time is None:
        flash('No se ha introducido el horario correctamente. Añade la hora de apertura y hora de cierre', "error")
        return redirect("/schedule", 301)
        
    try:
        # Get current week schedule
        week_schedule: ScheduleWeek = ScheduleModel.get_week_schedule()
        
        daily_schedule_id = getattr(week_schedule, day_key).id if week_schedule and getattr(week_schedule, day_key) else None

        if daily_schedule_id:
            # Update existing daily schedule
            updated_daily_schedule: OpenSpan = ScheduleModel.add_open_span(daily_schedule_id, open_time, close_time)
        else:
            # Insert new daily schedule
            new_daily_schedule: DailySchedule = ScheduleModel.create_daily_schedule()

            updated_daily_schedule = ScheduleModel.update_week_schedule(day_key, new_daily_schedule.id)

            updated_daily_schedule: DailySchedule = ScheduleModel.add_open_span(new_daily_schedule.id, open_time, close_time)
            
            if not updated_daily_schedule:
                raise Exception("El lapso de apertura no se pudo añadir. Comprueba los datos e inténtalo de nuevo.")

    except Exception as e:
        print(f"Error on add_open_span_to_week_day: {e}")
        
        flash('Ha ocurrido un error actualizando el horario.', "error")
        return redirect("/schedule", 301)

    flash(f'El horario ha sido actualizado con éxito', "success")
    return redirect("/schedule", 301)


@schedule_bp.post("/remove/<week_day>/")
@login_required
def remove_open_span_from_week_day(week_day):
    """Remove the last open span from the schedule of a certain day.
    
    Keyword arguments:
    argument - weekday - Number from 0(monday) to 6(sunday)
    Return: redirect
    """
    
    week_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    

    # Obtains week day from url index
    week_day = int(week_day)
    if week_day < 0 or week_day > 6:
        flash('El día de la semana introducido no es válido.', "error")
        return redirect("/schedule", 301)

    # Get current week schedule
    week_schedule: ScheduleWeek = ScheduleModel.get_week_schedule()
    day_key = week_days[week_day]

    daily_schedule_id = getattr(week_schedule, day_key).id if week_schedule and getattr(week_schedule, day_key) else None

    if daily_schedule_id:
        # Update existing daily schedule
        removed_element = ScheduleModel.remove_last_open_span(daily_schedule_id)
        if not removed_element:
            flash('Ha ocurrido un error eliminando el tramo de apertura.', "error")
    else:
        flash('Ha ocurrido un problema reconociendo el día seleccionado', "error")
        
    return redirect("/schedule", 301)
