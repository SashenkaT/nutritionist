import sys
from recipes import RecipeManager

def main():
    if len(sys.argv) < 2:
        return

    # Получаем ингредиенты из команды запуска
    args = " ".join(sys.argv[1:])
    ingredients = [i.strip() for i in args.split(",")]

    # Инициализация (убедись, что названия файлов совпадают с твоими)
    manager = RecipeManager('best_model.joblib', 'epi_r.csv', 'nutrients.csv')

    # Блок 1: Прогноз
    print("I. OUR FORECAST")
    pred = manager.predict_rating(ingredients)
    if "bad" in pred:
        print("You might find it tasty, but in our opinion, it is a bad idea to have a dish with that list of ingredients.")
    elif "so-so" in pred:
        print("It is a so-so idea to have a dish with that list of ingredients.")
    else:
        print("It is an excellent idea to have a dish with that list of ingredients!")

    # Блок 2: Нутриенты
    print("II. NUTRITION FACTS")
    facts = manager.get_nutrition_facts(ingredients)
    for f in facts:
        print(f['ingredient'].capitalize())
        print(f"Protein - {f.get('protein_%', 0)}% of Daily Value")
        print(f"Total Carbohydrate - {f.get('carbs_%', 0)}% of Daily Value")
        print(f"Total Fat - {f.get('fat_%', 0)}% of Daily Value")

    # Блок 3: Похожие рецепты
    print("III. TOP-3 SIMILAR RECIPES:")
    top = manager.find_similar_recipes(ingredients)
    for _, row in top.iterrows():
        title = str(row['title'])
        rating = round(row['rating'], 2)
        link = f"https://www.google.com/search?q={title.replace(' ', '+')}+recipe"
        print(f"- {title}, rating: {rating}, URL:\n{link}")

if __name__ == '__main__':
    main()