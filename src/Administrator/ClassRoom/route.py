"""
ClassRoom Routes
Defines Flask routes for classroom management using Flask-SQLAlchemy
Enhanced with class-based handler for better organization
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import json
from datetime import datetime

from src.db import db, DatabaseConfig
from src.Models.ClassRoom import ClassRoom
from .form import ClassRoomForm

# Create blueprint for classroom routes
classroom_bp = Blueprint('classroom_bp', __name__, url_prefix='/classrooms')


class ClassRoomRouteHandler:
    """
    Class-based handler for classroom routes
    Provides better organization and reusability of route logic
    """
    
    def __init__(self, db_instance=None):
        """Initialize the route handler with database instance"""
        self.db = db_instance or db
        # self.service = ClassRoomService(self.db)
    
    def get_classroom_list(self, request_args):
        """
        Handle classroom list logic
        Returns: dict with classrooms data and metadata
        """
        try:
            # Get search parameters
            search_query = request_args.get('search', '')
            room_type = request_args.get('room_type', 'all')
            availability_filter = request_args.get('availability_filter', 'all')
            building = request_args.get('building', 'all')
            department = request_args.get('department', 'all')
            page = request_args.get('page', 1, type=int)
            per_page = request_args.get('per_page', 10, type=int)
            min_capacity = request_args.get('min_capacity', type=int)
            
            # Debug query
            query_data = self.db.session.query(ClassRoom).all()
            current_app.logger.info(f"Total classrooms in database: {len(query_data)}")
            
            # Get classrooms using service
            result = self.service.get_all_classrooms(
                page=page,
                per_page=per_page,
                search=search_query if search_query else None,
                room_type=room_type if room_type != 'all' else None,
                availability_filter=availability_filter if availability_filter != 'all' else None,
                building=building if building != 'all' else None,
                department=department if department != 'all' else None
            )
            
            # Filter by capacity if specified
            if min_capacity:
                result['classrooms'] = [
                    classroom for classroom in result['classrooms'] 
                    if classroom.capacity >= min_capacity
                ]
                result['total'] = len(result['classrooms'])
            
            current_app.logger.info(f"Classrooms found: {len(result['classrooms'])}")
            
            return {
                'success': True,
                'data': result,
                'search_query': search_query,
                'room_type': room_type,
                'availability_filter': availability_filter,
                'building': building,
                'department': department,
                'min_capacity': min_capacity
            }
            
        except Exception as e:
            current_app.logger.error(f'Error in get_classroom_list: {str(e)}')
            return {
                'success': False,
                'error': str(e),
                'data': {'classrooms': [], 'total': 0, 'page': 1, 'pages': 0},
                'search_query': '',
                'room_type': 'all',
                'availability_filter': 'all',
                'building': 'all',
                'department': 'all',
                'min_capacity': None
            }
    
    def create_classroom(self, form):
        """
        Handle classroom creation logic
        Returns: dict with success status and classroom data or error
        """
        try:
            if form.validate_on_submit():
                # Prepare classroom data
                classroom_data = self._prepare_classroom_data(form)
                
                # Create classroom using service
                classroom = self.service.create_classroom(classroom_data)
                
                # Log successful creation
                current_app.logger.info(f'Classroom created: {classroom.room_number} (ID: {classroom.id})')
                
                return {
                    'success': True,
                    'classroom': classroom,
                    'message': f'✅ Success! Classroom "{classroom.full_name}" has been created successfully.'
                }
            else:
                return {
                    'success': False,
                    'errors': form.errors,
                    'message': 'Please correct the form errors and try again.'
                }
                
        except ValueError as e:
            current_app.logger.warning(f'Validation error creating classroom: {str(e)}')
            return {
                'success': False,
                'error': str(e),
                'message': f'❌ Validation Error: {str(e)}'
            }
        except IntegrityError as e:
            current_app.logger.error(f'Database integrity error: {str(e)}')
            self.db.session.rollback()
            return {
                'success': False,
                'error': 'integrity_error',
                'message': '❌ Error: A classroom with this room number already exists.'
            }
        except Exception as e:
            current_app.logger.error(f'Unexpected error creating classroom: {str(e)}')
            self.db.session.rollback()
            return {
                'success': False,
                'error': str(e),
                'message': f'❌ Unexpected Error: {str(e)}'
            }
    
    def get_classroom(self, classroom_id):
        """
        Handle getting a single classroom
        Returns: dict with success status and classroom data or error
        """
        try:
            classroom = self.service.get_classroom_by_id(classroom_id)
            
            if not classroom:
                return {
                    'success': False,
                    'error': 'not_found',
                    'message': 'Classroom not found'
                }
            
            return {
                'success': True,
                'classroom': classroom
            }
            
        except Exception as e:
            current_app.logger.error(f'Error getting classroom {classroom_id}: {str(e)}')
            return {
                'success': False,
                'error': str(e),
                'message': f'Error loading classroom: {str(e)}'
            }
    
    def update_classroom(self, classroom_id, form):
        """
        Handle classroom update logic
        Returns: dict with success status and updated classroom data or error
        """
        try:
            classroom = self.service.get_classroom_by_id(classroom_id)
            
            if not classroom:
                return {
                    'success': False,
                    'error': 'not_found',
                    'message': 'Classroom not found'
                }
            
            if form.validate_on_submit():
                # Prepare update data
                update_data = self._prepare_classroom_data(form)
                
                # Update classroom using service
                updated_classroom = self.service.update_classroom(classroom_id, update_data)
                
                # Log successful update
                self._log_classroom_action('updated', classroom_id=classroom_id, room_number=updated_classroom.room_number)
                
                return {
                    'success': True,
                    'classroom': updated_classroom,
                    'message': f'✅ Success! Classroom "{updated_classroom.full_name}" has been updated successfully.'
                }
            else:
                return {
                    'success': False,
                    'errors': form.errors,
                    'classroom': classroom,
                    'message': 'Please correct the form errors and try again.'
                }
                
        except ValueError as e:
            current_app.logger.warning(f'Validation error updating classroom {classroom_id}: {str(e)}')
            return {
                'success': False,
                'error': str(e),
                'message': f'❌ Validation Error: {str(e)}'
            }
        except IntegrityError as e:
            current_app.logger.error(f'Database integrity error updating classroom {classroom_id}: {str(e)}')
            self.db.session.rollback()
            return {
                'success': False,
                'error': 'integrity_error',
                'message': '❌ Error: Room number is already in use by another classroom.'
            }
        except Exception as e:
            current_app.logger.error(f'Unexpected error updating classroom {classroom_id}: {str(e)}')
            self.db.session.rollback()
            return {
                'success': False,
                'error': str(e),
                'message': f'❌ Unexpected Error: {str(e)}'
            }
    
    def delete_classroom(self, classroom_id):
        """
        Handle classroom deletion logic
        Returns: dict with success status and message or error
        """
        try:
            classroom = self.service.get_classroom_by_id(classroom_id)
            
            if not classroom:
                return {
                    'success': False,
                    'error': 'not_found',
                    'message': 'Classroom not found'
                }
            
            # Store classroom info for logging before deletion
            classroom_name = classroom.full_name
            room_number = classroom.room_number
            
            # Delete classroom
            self.service.delete_classroom(classroom_id)
            
            # Log the action
            self._log_classroom_action('deleted', classroom_id=classroom_id, room_number=room_number)
            
            return {
                'success': True,
                'message': f'✅ Classroom "{classroom_name}" has been deleted successfully.'
            }
            
        except Exception as e:
            current_app.logger.error(f'Error deleting classroom {classroom_id}: {str(e)}')
            return {
                'success': False,
                'error': str(e),
                'message': f'❌ Error deleting classroom: {str(e)}'
            }
    
    def reserve_classroom(self, classroom_id, occupancy_count=None):
        """
        Handle classroom reservation logic
        Returns: dict with success status and message or error
        """
        try:
            classroom = self.service.reserve_classroom(classroom_id, occupancy_count)
            
            self._log_classroom_action('reserved', classroom_id=classroom_id, room_number=classroom.room_number)
            
            return {
                'success': True,
                'classroom': classroom,
                'message': f'✅ Classroom "{classroom.full_name}" has been reserved successfully.'
            }
            
        except ValueError as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'❌ {str(e)}'
            }
        except Exception as e:
            current_app.logger.error(f'Error reserving classroom {classroom_id}: {str(e)}')
            return {
                'success': False,
                'error': str(e),
                'message': f'❌ Error reserving classroom: {str(e)}'
            }
    
    def release_classroom(self, classroom_id):
        """
        Handle classroom release logic
        Returns: dict with success status and message or error
        """
        try:
            classroom = self.service.release_classroom(classroom_id)
            
            self._log_classroom_action('released', classroom_id=classroom_id, room_number=classroom.room_number)
            
            return {
                'success': True,
                'classroom': classroom,
                'message': f'✅ Classroom "{classroom.full_name}" has been released successfully.'
            }
            
        except ValueError as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'❌ {str(e)}'
            }
        except Exception as e:
            current_app.logger.error(f'Error releasing classroom {classroom_id}: {str(e)}')
            return {
                'success': False,
                'error': str(e),
                'message': f'❌ Error releasing classroom: {str(e)}'
            }
    
    def get_classroom_stats(self):
        """
        Get classroom statistics
        Returns: dict with classroom statistics
        """
        try:
            stats = self.service.get_classroom_stats()
            return {
                'success': True,
                'stats': stats
            }
        except Exception as e:
            current_app.logger.error(f'Error getting classroom stats: {str(e)}')
            return {
                'success': False,
                'error': str(e),
                'stats': {}
            }
    
    def get_available_classrooms(self, capacity_needed=None, room_type=None, building=None):
        """
        Get available classrooms with filters
        Returns: dict with available classrooms
        """
        try:
            classrooms = self.service.get_available_classrooms(capacity_needed, room_type, building)
            return {
                'success': True,
                'classrooms': classrooms,
                'count': len(classrooms)
            }
        except Exception as e:
            current_app.logger.error(f'Error getting available classrooms: {str(e)}')
            return {
                'success': False,
                'error': str(e),
                'classrooms': [],
                'count': 0
            }
    
    def _prepare_classroom_data(self, form):
        """
        Prepare classroom data from form with proper validation and defaults
        """
        return {
            'name': form.name.data.strip(),
            'room_number': form.room_number.data.strip().upper(),
            'building': form.building.data.strip() if form.building.data else None,
            'floor': form.floor.data if form.floor.data is not None else None,
            'capacity': form.capacity.data,
            'current_occupancy': form.current_occupancy.data if form.current_occupancy.data is not None else 0,
            'has_projector': form.has_projector.data if hasattr(form, 'has_projector') else False,
            'has_whiteboard': form.has_whiteboard.data if hasattr(form, 'has_whiteboard') else True,
            'has_computer': form.has_computer.data if hasattr(form, 'has_computer') else False,
            'has_air_conditioning': form.has_air_conditioning.data if hasattr(form, 'has_air_conditioning') else True,
            'has_audio_system': form.has_audio_system.data if hasattr(form, 'has_audio_system') else False,
            'is_active': form.is_active.data if hasattr(form, 'is_active') else True,
            'is_available': form.is_available.data if hasattr(form, 'is_available') else True,
            'maintenance_status': form.maintenance_status.data if hasattr(form, 'maintenance_status') else 'good',
            'room_type': form.room_type.data if hasattr(form, 'room_type') else 'lecture',
            'department': form.department.data.strip() if hasattr(form, 'department') and form.department.data else None,
            'description': form.description.data.strip() if hasattr(form, 'description') and form.description.data else None,
            'special_features': form.special_features.data.strip() if hasattr(form, 'special_features') and form.special_features.data else None,
            'access_requirements': form.access_requirements.data.strip() if hasattr(form, 'access_requirements') and form.access_requirements.data else None
        }
    
    def _log_classroom_action(self, action, classroom_id=None, room_number=None, details=None):
        """
        Log classroom-related actions for auditing
        """
        log_message = f'Classroom {action}'
        if classroom_id:
            log_message += f' (ID: {classroom_id})'
        if room_number:
            log_message += f' (Room: {room_number})'
        if details:
            log_message += f' - {details}'
        
        current_app.logger.info(log_message)


# Global instance of the route handler
classroom_handler = ClassRoomRouteHandler()


# Routes using the class-based handler
@classroom_bp.route('/')
@classroom_bp.route('/list')
def classroom_list():
    """Classroom list page using class-based handler"""
    try:
        # Use the class-based handler
        result = classroom_handler.get_classroom_list(request.args)
        
        search_form = ClassRoomSearchForm()
        # Populate dynamic choices
        from .form import populate_building_choices, populate_department_choices
        populate_building_choices(search_form)
        populate_department_choices(search_form)
        
        if result['success']:
            return render_template('classrooms/index.html', 
                                 classrooms=result['data'], 
                                 search_form=search_form,
                                 filters=result)
        else:
            flash(result.get('message', f'Error loading classrooms: {result.get("error", "Unknown error")}'), 'error')
            return render_template('classrooms/index.html', 
                                 classrooms=result['data'], 
                                 search_form=search_form,
                                 filters=result)
                                 
    except Exception as e:
        current_app.logger.error(f'Unexpected error in classroom_list: {str(e)}')
        flash(f'Unexpected error: {str(e)}', 'error')
        return render_template('classrooms/index.html', 
                             classrooms={'classrooms': [], 'total': 0, 'page': 1, 'pages': 0}, 
                             search_form=ClassRoomSearchForm(),
                             filters={})


@classroom_bp.route('/create', methods=['GET', 'POST'])
def create():
    """Create new classroom using class-based handler"""
    form = ClassRoomForm()
    
    if request.method == 'POST':
        result = classroom_handler.create_classroom(form)
        
        if result['success']:
            flash(result['message'], 'success')
            return redirect(url_for('classroom_bp.view', classroom_id=result['classroom'].id))
        else:
            flash(result['message'], 'error')
            if 'errors' in result:
                for field_name, errors in result['errors'].items():
                    for error in errors:
                        field_label = getattr(form[field_name], 'label', field_name).text if hasattr(form[field_name], 'label') else field_name.replace('_', ' ').title()
                        flash(f'❌ {field_label}: {error}', 'error')
    
    return render_template('classrooms/create.html', form=form, title='Create New Classroom')


@classroom_bp.route('/<int:classroom_id>')
def view(classroom_id):
    """View classroom details using class-based handler"""
    result = classroom_handler.get_classroom(classroom_id)
    
    if result['success']:
        return render_template('classrooms/view.html', classroom=result['classroom'])
    else:
        flash(result['message'], 'error')
        return redirect(url_for('classroom_bp.classroom_list'))


@classroom_bp.route('/<int:classroom_id>/edit', methods=['GET', 'POST'])
def edit(classroom_id):
    """Edit classroom using class-based handler"""
    # First get the classroom
    classroom_result = classroom_handler.get_classroom(classroom_id)
    
    if not classroom_result['success']:
        flash(classroom_result['message'], 'error')
        return redirect(url_for('classroom_bp.classroom_list'))
    
    classroom = classroom_result['classroom']
    form = ClassRoomForm(obj=classroom)
    
    if request.method == 'POST':
        result = classroom_handler.update_classroom(classroom_id, form)
        
        if result['success']:
            flash(result['message'], 'success')
            return redirect(url_for('classroom_bp.view', classroom_id=classroom_id))
        else:
            flash(result['message'], 'error')
            if 'errors' in result:
                for field_name, errors in result['errors'].items():
                    for error in errors:
                        field_label = getattr(form[field_name], 'label', field_name).text if hasattr(form[field_name], 'label') else field_name.replace('_', ' ').title()
                        flash(f'❌ {field_label}: {error}', 'error')
    
    return render_template('classrooms/edit.html', form=form, classroom=classroom, title=f'Edit Classroom: {classroom.full_name}')


@classroom_bp.route('/<int:classroom_id>/delete', methods=['POST'])
def delete(classroom_id):
    """Delete classroom using class-based handler"""
    result = classroom_handler.delete_classroom(classroom_id)
    
    if result['success']:
        flash(result['message'], 'success')
    else:
        flash(result['message'], 'error')
    
    return redirect(url_for('classroom_bp.classroom_list'))


@classroom_bp.route('/<int:classroom_id>/reserve', methods=['POST'])
def reserve(classroom_id):
    """Reserve classroom using class-based handler"""
    occupancy_count = request.form.get('occupancy_count', type=int)
    
    result = classroom_handler.reserve_classroom(classroom_id, occupancy_count)
    
    if request.is_json or request.args.get('format') == 'json':
        return jsonify(result)
    
    if result['success']:
        flash(result['message'], 'success')
    else:
        flash(result['message'], 'error')
    
    return redirect(url_for('classroom_bp.view', classroom_id=classroom_id))


@classroom_bp.route('/<int:classroom_id>/release', methods=['POST'])
def release(classroom_id):
    """Release classroom using class-based handler"""
    result = classroom_handler.release_classroom(classroom_id)
    
    if request.is_json or request.args.get('format') == 'json':
        return jsonify(result)
    
    if result['success']:
        flash(result['message'], 'success')
    else:
        flash(result['message'], 'error')
    
    return redirect(url_for('classroom_bp.view', classroom_id=classroom_id))


# API Routes
@classroom_bp.route('/api/stats')
def api_stats():
    """Get classroom statistics API"""
    result = classroom_handler.get_classroom_stats()
    
    if result['success']:
        return jsonify({
            'success': True,
            'stats': result['stats']
        })
    else:
        return jsonify({
            'success': False,
            'error': result['error']
        }), 500


@classroom_bp.route('/api/available')
def api_available():
    """Get available classrooms API"""
    capacity_needed = request.args.get('capacity', type=int)
    room_type = request.args.get('room_type')
    building = request.args.get('building')
    
    result = classroom_handler.get_available_classrooms(capacity_needed, room_type, building)
    
    if result['success']:
        classrooms_data = [classroom.to_dict() for classroom in result['classrooms']]
        return jsonify({
            'success': True,
            'classrooms': classrooms_data,
            'count': result['count']
        })
    else:
        return jsonify({
            'success': False,
            'error': result['error'],
            'classrooms': [],
            'count': 0
        }), 500


@classroom_bp.route('/api')
def api_list():
    """Get classrooms list API"""
    result = classroom_handler.get_classroom_list(request.args)
    
    if result['success']:
        classrooms_data = [classroom.to_dict() for classroom in result['data']['classrooms']]
        return jsonify({
            'success': True,
            'classrooms': classrooms_data,
            'pagination': {
                'total': result['data']['total'],
                'page': result['data']['page'],
                'pages': result['data']['pages'],
                'per_page': result['data']['per_page'],
                'has_prev': result['data']['has_prev'],
                'has_next': result['data']['has_next']
            }
        })
    else:
        return jsonify({
            'success': False,
            'error': result['error'],
            'classrooms': []
        }), 500


# Template filters
@classroom_bp.app_template_filter('classroom_status_class')
def classroom_status_class(classroom):
    """Template filter to get CSS class for classroom status"""
    if not classroom.is_active:
        return 'inactive'
    elif not classroom.is_available:
        return 'occupied'
    elif classroom.maintenance_status == 'under_maintenance':
        return 'maintenance'
    elif classroom.maintenance_status == 'needs_repair':
        return 'needs-repair'
    else:
        return 'available'


@classroom_bp.app_template_filter('equipment_icons')
def equipment_icons(classroom):
    """Template filter to get equipment icons"""
    icons = []
    if classroom.has_projector:
        icons.append('🎥')
    if classroom.has_computer:
        icons.append('💻')
    if classroom.has_audio_system:
        icons.append('🔊')
    if classroom.has_air_conditioning:
        icons.append('❄️')
    return ' '.join(icons)
