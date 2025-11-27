import json
import random
import requests
import time
from datetime import datetime, timedelta

def fetch_users(count=10):
    print(f"Fetching {count} users...")
    response = requests.get(f"https://randomuser.me/api/?results={count}")
    if response.status_code == 200:
        users_data = response.json()['results']
        users = []
        for i, u in enumerate(users_data):
            users.append({
                "id": f"u_gen_{i+1}",
                "name": f"{u['name']['first']} {u['name']['last']}",
                "preferences": random.sample(["Italian", "Asian", "Fast Food", "Mexican", "Indian", "Vegetarian"], k=random.randint(1, 3))
            })
        return users
    return []

def fetch_meals(count=10):
    print(f"Fetching {count} meals...")
    meals = []
    ingredients_map = {} # name -> id
    dish_ingredients = []
    
    # We fetch one by one as the random API returns one
    for i in range(count):
        try:
            response = requests.get("https://www.themealdb.com/api/json/v1/1/random.php")
            if response.status_code == 200:
                meal = response.json()['meals'][0]
                dish_id = f"d_gen_{i+1}"
                
                # Extract ingredients
                current_dish_ingredients = []
                for j in range(1, 21):
                    ing_name = meal.get(f"strIngredient{j}")
                    if ing_name and ing_name.strip():
                        ing_name = ing_name.strip()
                        if ing_name not in ingredients_map:
                            ingredients_map[ing_name] = f"i_gen_{len(ingredients_map)+1}"
                        current_dish_ingredients.append(ingredients_map[ing_name])
                
                dish_ingredients.append({
                    "dish_id": dish_id,
                    "ingredient_ids": current_dish_ingredients
                })
                
                meals.append({
                    "id": dish_id,
                    "name": meal['strMeal'],
                    "cuisine": meal['strArea'], # Use Area as Cuisine
                    "category": meal['strCategory'],
                    "price": round(random.uniform(8.0, 25.0), 2),
                    "attributes": [meal['strCategory'], meal['strArea']]
                })
            time.sleep(0.2) # Be nice to the API
        except Exception as e:
            print(f"Error fetching meal: {e}")
            
    return meals, ingredients_map, dish_ingredients

def generate_restaurants(meals, count=5):
    print(f"Generating {count} restaurants...")
    cuisines = list(set(m['cuisine'] for m in meals))
    restaurants = []
    
    prefixes = ["The", "Golden", "Royal", "Tasty", "Spicy", "Urban"]
    suffixes = ["Kitchen", "Place", "Bistro", "Grill", "House", "Garden"]
    
    for i in range(count):
        cuisine = random.choice(cuisines) if cuisines else "International"
        restaurants.append({
            "id": f"r_gen_{i+1}",
            "name": f"{random.choice(prefixes)} {cuisine} {random.choice(suffixes)}",
            "cuisine": cuisine,
            "location": random.choice(["Downtown", "Uptown", "Midtown", "Suburbs", "Waterfront"])
        })
    return restaurants

def assign_dishes_to_restaurants(dishes, restaurants):
    for dish in dishes:
        # Try to match cuisine
        matching_restaurants = [r for r in restaurants if r['cuisine'] == dish['cuisine']]
        if matching_restaurants:
            dish['restaurant_id'] = random.choice(matching_restaurants)['id']
        else:
            dish['restaurant_id'] = random.choice(restaurants)['id']
        
        # Remove internal fields not in schema
        if 'cuisine' in dish: del dish['cuisine']
        if 'category' in dish: del dish['category']
        
    return dishes

def generate_orders(users, dishes, count=20):
    print(f"Generating {count} orders...")
    orders = []
    start_date = datetime.now() - timedelta(days=30)
    
    for i in range(count):
        user = random.choice(users)
        # Pick 1-3 dishes
        order_dishes = random.sample(dishes, k=random.randint(1, 3))
        dish_ids = [d['id'] for d in order_dishes]
        
        # Random time in last 30 days
        random_seconds = random.randint(0, 30 * 24 * 3600)
        timestamp = (start_date + timedelta(seconds=random_seconds)).isoformat()
        
        orders.append({
            "id": f"o_gen_{i+1}",
            "user_id": user['id'],
            "dish_ids": dish_ids,
            "timestamp": timestamp
        })
    return orders

def main():
    # 1. Fetch Users
    users = fetch_users(20)
    
    # 2. Fetch Meals (Dishes) & Ingredients
    meals, ingredients_map, dish_ingredients = fetch_meals(30)
    
    # Format ingredients list
    ingredients = [{"id": v, "name": k} for k, v in ingredients_map.items()]
    
    # 3. Generate Restaurants
    restaurants = generate_restaurants(meals, 10)
    
    # 4. Link Dishes to Restaurants
    dishes = assign_dishes_to_restaurants(meals, restaurants)
    
    # 5. Generate Orders
    orders = generate_orders(users, dishes, 50)
    
    # 6. Construct Final Data
    data = {
        "users": users,
        "restaurants": restaurants,
        "dishes": dishes,
        "ingredients": ingredients,
        "dish_ingredients": dish_ingredients,
        "orders": orders
    }
    
    # 7. Save
    output_path = "data/generated_data.json"
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Successfully generated data to {output_path}")
    print(f"Stats: {len(users)} Users, {len(restaurants)} Restaurants, {len(dishes)} Dishes, {len(ingredients)} Ingredients, {len(orders)} Orders")

if __name__ == "__main__":
    main()
