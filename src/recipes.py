import pandas as pd
import joblib
from sklearn.metrics.pairwise import cosine_similarity

class RecipeManager:
    def __init__(self, model_path, data_path, nutrients_path):
        self.model = joblib.load(model_path) # грузим модель
        self.df_raw = pd.read_csv(data_path) # база рецептов
        self.nutrients = pd.read_csv(nutrients_path) # нутриенты
        
        self.recipe_titles = self.df_raw['title'].copy() # названия
        
        # оставляем только ингредиенты
        self.df_features = self.df_raw.drop(
            columns=['title', 'calories', 'protein', 'fat', 'sodium', 'rating'], 
            errors='ignore'
        )
        self.all_ingredients = self.df_features.columns.to_list()

    def _prepare_user_features(self, ingredients_list):
        # пустой вектор (нули)
        user_features = pd.DataFrame(0, index=[0], columns=self.all_ingredients)
        
        # ставим 1 при совпадении
        for item in ingredients_list:
            item = item.strip().lower()
            if item in self.all_ingredients:
                user_features[item] = 1.0
                
        return user_features

    def predict_rating(self, ingredients_list):
        features = self._prepare_user_features(ingredients_list)
        pred = self.model.predict(features)[0] # прогноз
        
        # расшифровка класса
        if pred == 0: return "bad"
        elif pred == 1: return "so-so"
        else: return "excellent"

    def get_nutrition_facts(self, ingredients_list):
        facts = []
        for item in ingredients_list:
            item = item.strip().lower()
            match = self.nutrients[self.nutrients['ingredient'] == item] # ищем бжу
            if not match.empty:
                facts.append(match.iloc[0].to_dict())
        return facts

    def find_similar_recipes(self, ingredients_list, top_n=3):
        user_features = self._prepare_user_features(ingredients_list)
        
        # считаем сходство
        similarities = cosine_similarity(user_features, self.df_features)[0]
        
        recomm = pd.DataFrame({
            'title': self.recipe_titles,
            'rating': self.df_raw['rating'] if 'rating' in self.df_raw else 0,
            'similarity': similarities
        })
        
        # выдаем топ
        return recomm.sort_values(by='similarity', ascending=False).head(top_n)

if __name__ == '__main__':
    pass