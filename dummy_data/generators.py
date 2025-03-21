import json
import random
import os
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

data_store = {}

class DummyDataGenerator:
    """Generate dummy data based on schema definitions"""
    
    def __init__(self, schema_file=None):
        self.schema = None
        if schema_file:
            self.load_schema(schema_file)
    
    def load_schema(self, schema_file):
        """Load schema from a JSON file"""
        try:
            with open(schema_file, 'r') as f:
                self.schema = json.load(f)
            print(f"Successfully loaded schema from {schema_file}")
            return True
        except Exception as e:
            print(f"Error loading schema: {e}")
            return False
    
    def generate_field_value(self, field_type, field_options=None):
        """Generate a single field value based on type and options"""
        field_options = field_options or {}
        
        # Basic data types
        if field_type == "string":
            if field_options.get("format") == "name":
                return fake.name()
            elif field_options.get("format") == "email":
                return fake.email()
            elif field_options.get("format") == "address":      
                return fake.address()
            elif field_options.get("format") == "phone":
                return fake.phone_number()
            elif field_options.get("format") == "job":
                return fake.job()
            elif field_options.get("format") == "company":
                return fake.company()
            elif field_options.get("enum"):
                return random.choice(field_options["enum"])
            elif field_options.get("format") == "uuid":
                return str(fake.uuid4())
            else:
                min_length = field_options.get("min_length", 5)
                max_length = field_options.get("max_length", 20)
            
            if min_length < 5:
                length = random.randint(min_length, min(max_length, 4))
                chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "
                return ''.join(random.choice(chars) for _ in range(length))
            else:
            # Use Faker's text for lengths >= 5
                max_length = max(max_length, min_length)  # Ensure max >= min
                return fake.text(max_nb_chars=random.randint(min_length, max_length))

        
        elif field_type == "integer":
            min_val = field_options.get("minimum", 1)
            max_val = field_options.get("maximum", 1000)
            return random.randint(min_val, max_val)
        
        elif field_type == "number":
            min_val = field_options.get("minimum", 0)
            max_val = field_options.get("maximum", 1000)
            precision = field_options.get("precision", 2)
            return round(random.uniform(min_val, max_val), precision)
        
        elif field_type == "boolean":
            return random.choice([True, False])
        
        elif field_type == "date":
            start_date = datetime.now() - timedelta(days=365)
            end_date = datetime.now() + timedelta(days=365)
            return fake.date_between(start_date=start_date, end_date=end_date).isoformat()
        
        elif field_type == "datetime":
            start_date = datetime.now() - timedelta(days=365)
            end_date = datetime.now() + timedelta(days=365)
            return fake.date_time_between(start_date=start_date, end_date=end_date).isoformat()
        
        elif field_type == "array":
            items_type = field_options.get("items", {}).get("type", "string")
            items_options = field_options.get("items", {}).get("options", {})
            min_items = field_options.get("min_items", 1)
            max_items = field_options.get("max_items", 5)
            count = random.randint(min_items, max_items)
            return [self.generate_field_value(items_type, items_options) for _ in range(count)]
        
        elif field_type == "object":
            properties = field_options.get("properties", {})
            result = {}
            for prop_name, prop_details in properties.items():
                result[prop_name] = self.generate_field_value(
                    prop_details.get("type", "string"),
                    prop_details.get("options", {})
                )
            return result
        
        # Handle relationships
        elif field_type == "relation":
            related_entity = field_options.get("entity")
            if related_entity and related_entity in data_store:
                items = data_store[related_entity]
                if items:
                    if field_options.get("relation_type") == "one_to_many":
                        min_items = field_options.get("min_items", 1)
                        max_items = min(field_options.get("max_items", 3), len(items))
                        count = random.randint(min_items, max_items)
                        return random.sample([item["id"] for item in items], count)
                    else:  # one_to_one relation
                        return random.choice([item["id"] for item in items])
            return None
        
        else:
            return None
    
    def generate_entity_data(self, entity_name, count=10):
        """Generate data for a specific entity based on its schema"""
        if not self.schema or entity_name not in self.schema:
            return []
        
        entity_schema = self.schema[entity_name]
        result = []
        
        for i in range(count):
            item = {"id": i + 1}  # Start with ID
            
            for field_name, field_details in entity_schema.items():
                if field_name != "id":  # Skip ID field as we've already set it
                    field_type = field_details.get("type", "string")
                    field_options = field_details.get("options", {})
                    item[field_name] = self.generate_field_value(field_type, field_options)
            
            result.append(item)
        
        return result
    
    def generate_all_data(self, counts=None):
        """Generate data for all entities in the schema"""
        if not self.schema:
            return {}
        
        counts = counts or {}
        result = {}
        
        # First pass: generate basic data without relations
        for entity_name in self.schema.keys():
            count = counts.get(entity_name, 10)
            entity_data = []
            
            entity_schema = self.schema[entity_name]
            for i in range(count):
                item = {"id": i + 1}
                
                for field_name, field_details in entity_schema.items():
                    if field_name != "id" and field_details.get("type") != "relation":
                        field_type = field_details.get("type", "string")
                        field_options = field_details.get("options", {})
                        item[field_name] = self.generate_field_value(field_type, field_options)
                
                entity_data.append(item)
            
            result[entity_name] = entity_data
        
        # Update global data store
        global data_store
        data_store.update(result)
        
        # Second pass: handle relations
        for entity_name in self.schema.keys():
            entity_schema = self.schema[entity_name]
            
            for i, item in enumerate(result[entity_name]):
                for field_name, field_details in entity_schema.items():
                    if field_name != "id" and field_details.get("type") == "relation":
                        field_options = field_details.get("options", {})
                        item[field_name] = self.generate_field_value("relation", field_options)
        
        return result
    
    def save_to_json(self, data, output_dir="output"):
        """Save generated data to JSON files"""
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            for entity_name, entity_data in data.items():
                output_file = os.path.join(output_dir, f"{entity_name}.json")
                with open(output_file, 'w') as f:
                    json.dump(entity_data, f, indent=2)
                print(f"Generated {len(entity_data)} {entity_name} records -> {output_file}")
            
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False