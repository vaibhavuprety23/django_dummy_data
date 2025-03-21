

import json
import os
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .generators import DummyDataGenerator, data_store

# Global variable to store generated data
data_store = {}




def get_entities(request, entity):
    """Get all entities or filtered ones"""
    if entity not in data_store:
        return JsonResponse({"error": f"Entity '{entity}' not found"}, status=404)
    
    # Implement filtering, pagination, sorting
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 10))
    
    # Handle filters
    filtered_data = data_store[entity]
    for key, value in request.GET.items():
        if key not in ['page', 'per_page', 'sort']:
            filtered_data = [item for item in filtered_data if str(item.get(key, '')) == value]
    
    # Handle sorting
    sort_by = request.GET.get('sort')
    if sort_by:
        reverse = False
        if sort_by.startswith('-'):
            reverse = True
            sort_by = sort_by[1:]
        
        if sort_by in data_store[entity][0] if data_store[entity] else False:
            filtered_data.sort(key=lambda x: x.get(sort_by, ''), reverse=reverse)
    
    # Calculate pagination
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_data = filtered_data[start_idx:end_idx]
    
    return JsonResponse({
        "data": paginated_data,
        "meta": {
            "total": len(filtered_data),
            "page": page,
            "per_page": per_page,
            "total_pages": (len(filtered_data) + per_page - 1) // per_page
        }
    })

def get_entity(request, entity, id):
    """Get a specific entity by ID"""
    if entity not in data_store:
        return JsonResponse({"error": f"Entity '{entity}' not found"}, status=404)
    
    for item in data_store[entity]:
        if item.get('id') == id:
            return JsonResponse(item)
    
    return JsonResponse({"error": f"{entity} with id {id} not found"}, status=404)

def get_schema(request):
    """Get the current schema"""
    generator = DummyDataGenerator()
    return JsonResponse(generator.schema or {})

@csrf_exempt
def regenerate_data(request):
    """Regenerate all data based on the current schema"""
    if request.method != 'POST':
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    try:
        # Get counts from request body
        body = json.loads(request.body.decode('utf-8')) if request.body else {}
        counts = body.get('counts', {})
        
        schema_path = os.path.join(settings.BASE_DIR, 'dummy_data', 'schema.json')
        generator = DummyDataGenerator(schema_path)
        global data_store
        data_store = generator.generate_all_data(counts)
        
        output_dir = os.path.join(settings.BASE_DIR, 'dummy_data', 'output')
        generator.save_to_json(data_store, output_dir)
        
        return JsonResponse({"message": "Data regenerated successfully"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def initialize_data():
    """Initialize data when Django starts"""
    schema_path = os.path.join(settings.BASE_DIR, 'dummy_data', 'schema.json')
    if os.path.exists(schema_path):
        try:
            generator = DummyDataGenerator(schema_path)
            global data_store
            data_store.clear()  # Clear any existing data
            
            # Generate initial data
            generated_data = generator.generate_all_data()
            
            # Save to files
            output_dir = os.path.join(settings.BASE_DIR, 'dummy_data', 'output')
            generator.save_to_json(generated_data, output_dir)
            
            print("✅ Dummy data initialized successfully")
            print(f"Generated entities: {', '.join(generated_data.keys())}")
        except Exception as e:
            print(f"❌ Error initializing dummy data: {e}")